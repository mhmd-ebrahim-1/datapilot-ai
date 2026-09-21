import uuid
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.dataset import Dataset
from app.models.anomaly import Anomaly
from app.services.ingestion.parser import parse_file
from app.services.ingestion.storage import get_file_path
from app.services.anomaly_detection.detector import detect_anomalies

router = APIRouter(prefix="/api/v1/anomalies", tags=["Anomalies"])

@router.post("/detect", response_model=list)
async def detect(body: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    dataset_id_raw = body.get("dataset_id")
    if not dataset_id_raw:
        raise HTTPException(status_code=400, detail="dataset_id is required")
        
    try:
        dataset_uuid = uuid.UUID(str(dataset_id_raw)) if isinstance(dataset_id_raw, str) else dataset_id_raw
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid dataset_id format")
        
    dataset = db.query(Dataset).filter(Dataset.id == dataset_uuid).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    file_path = get_file_path(dataset.storage_path)
    df = parse_file(file_path, dataset.file_type)
    anomalies_list = detect_anomalies(df)
    
    saved = []
    for a in anomalies_list[:50]:
        anomaly = Anomaly(
            id=uuid.uuid4(),
            dataset_id=dataset.id,
            analysis_id=None,
            column_name=a.get("column_name", a.get("column", "")),
            row_reference=str(a.get("row_reference", a.get("row", ""))),
            value_str=str(a.get("value_str", a.get("value", ""))),
            score=float(a.get("score", 0.0)),
            explanation=a.get("explanation", "")
        )
        db.add(anomaly)
        saved.append({
            "id": str(anomaly.id),
            "column": anomaly.column_name,
            "row_reference": anomaly.row_reference,
            "value": anomaly.value_str,
            "score": anomaly.score,
            "explanation": anomaly.explanation,
            "expected_range": a.get("expected_range", "")
        })
    db.commit()
    return saved

@router.get("/{analysis_id}", response_model=list)
async def get_anomalies(analysis_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    anomalies = db.query(Anomaly).filter(Anomaly.analysis_id == analysis_id).all()
    return [{
        "id": str(a.id),
        "column": a.column_name,
        "row_reference": a.row_reference,
        "value": a.value_str,
        "score": a.score,
        "explanation": a.explanation
    } for a in anomalies]

@router.get("/dataset/{dataset_id}", response_model=list)
async def get_dataset_anomalies(dataset_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    anomalies = db.query(Anomaly).filter(Anomaly.dataset_id == dataset_id).order_by(Anomaly.created_at.desc()).all()
    return [{
        "id": str(a.id),
        "column": a.column_name,
        "row_reference": a.row_reference,
        "value": a.value_str,
        "score": a.score,
        "explanation": a.explanation
    } for a in anomalies]
