import os
import uuid
import json
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.dataset import Dataset
from app.models.analysis import Analysis
from app.models.insight import Insight
from app.models.report import Report
from app.services.reporting.report_generator import create_report_for_dataset
from app.services.ingestion.storage import get_file_path

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_report(body: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    dataset_id_raw = body.get("dataset_id")
    title = body.get("title", "Executive Analytics Report").strip()
    
    if not dataset_id_raw:
        raise HTTPException(status_code=400, detail="dataset_id is required")
        
    try:
        dataset_uuid = uuid.UUID(str(dataset_id_raw)) if isinstance(dataset_id_raw, str) else dataset_id_raw
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid dataset_id format")
        
    try:
        report = create_report_for_dataset(
            db=db,
            dataset_id=dataset_uuid,
            user_id=current_user.id,
            title=title
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report PDF: {str(e)}")
        
    return {
        "id": str(report.id),
        "title": report.title,
        "format": report.format,
        "dataset_id": str(report.dataset_id),
        "created_at": str(report.created_at)
    }

@router.get("", response_model=list)
@router.get("/", response_model=list, include_in_schema=False)
async def list_reports(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reports = db.query(Report).filter(Report.created_by == current_user.id).order_by(Report.created_at.desc()).all()
    results = []
    for r in reports:
        d = db.query(Dataset).filter(Dataset.id == r.dataset_id).first()
        results.append({
            "id": str(r.id),
            "title": r.title,
            "format": r.format,
            "dataset_id": str(r.dataset_id),
            "dataset_name": d.name if d else "Dataset",
            "created_at": str(r.created_at)
        })
    return results

@router.get("/{report_id}", response_model=dict)
async def get_report(report_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    d = db.query(Dataset).filter(Dataset.id == report.dataset_id).first()
    return {
        "id": str(report.id),
        "title": report.title,
        "format": report.format,
        "dataset_id": str(report.dataset_id),
        "dataset_name": d.name if d else "Dataset",
        "created_at": str(report.created_at)
    }

@router.get("/{report_id}/download")
async def download_report(report_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    abs_path = get_file_path(report.storage_path)
    if not os.path.exists(abs_path):
        raise HTTPException(status_code=404, detail="Report PDF file not found on disk")
        
    safe_filename = f"{report.title.replace(' ', '_')}.pdf"
    return FileResponse(
        abs_path,
        media_type="application/pdf",
        filename=safe_filename,
        headers={"Content-Disposition": f'attachment; filename="{safe_filename}"'}
    )

@router.delete("/{report_id}", response_model=dict)
async def delete_report(report_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    if report.storage_path:
        abs_path = get_file_path(report.storage_path)
        if os.path.exists(abs_path):
            try:
                os.remove(abs_path)
            except Exception:
                pass
                
    db.delete(report)
    db.commit()
    return {"message": "Report deleted successfully", "id": str(report_id)}
