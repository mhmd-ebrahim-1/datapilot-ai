import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.user import User
from app.models.dataset import Dataset
from app.models.workspace import Workspace, WorkspaceMember
from app.models.analysis import Analysis
from app.models.insight import Insight
from app.models.report import Report
from app.models.chat import ChatSession, ChatMessage
from app.models.forecast import Forecast
from app.models.anomaly import Anomaly
from app.api.dependencies import get_current_user, get_user_default_workspace
from app.services.ingestion.storage import save_file, get_file_path, delete_file
from app.services.ingestion.file_validator import validate_file
from app.services.ingestion.parser import parse_file
from app.services.cleaning.cleaner import clean_dataset
from app.services.profiling.profiler import profile_dataframe
from app.services.profiling.quality_scorer import calculate_quality_score
from app.services.profiling.type_detector import detect_dataset_type
from app.services.billing.usage_service import increment_usage, check_usage_allowed

router = APIRouter(prefix="/api/v1/datasets", tags=["Datasets"])

def process_dataset_synchronously(dataset: Dataset, db: Session):
    """Perform dataset parsing, cleaning, profiling, type detection and scoring."""
    try:
        dataset.status = "processing"
        db.commit()
        
        file_path = get_file_path(dataset.storage_path)
        df = parse_file(file_path, dataset.file_type or "text/csv")
        
        clean_result = clean_dataset(df)
        cleaned_df = clean_result["cleaned_df"]
        
        profile = profile_dataframe(cleaned_df)
        quality = calculate_quality_score(cleaned_df, profile)
        type_info = detect_dataset_type(cleaned_df)
        
        dataset.dataset_type = type_info.get("dataset_type", "General")
        dataset.row_count = len(cleaned_df)
        dataset.column_count = len(cleaned_df.columns)
        dataset.quality_score = float(quality.get("overall", 90.0))
        dataset.profile_json = profile
        dataset.cleaning_summary_json = clean_result.get("changes_log", [])
        dataset.status = "ready"
        db.commit()
        db.refresh(dataset)
    except Exception as e:
        dataset.status = "failed"
        db.commit()
        db.refresh(dataset)

@router.post("/upload", response_model=dict, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    workspace_id: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Determine target workspace
    if workspace_id:
        try:
            ws_uuid = uuid.UUID(str(workspace_id))
            workspace = db.query(Workspace).filter(Workspace.id == ws_uuid).first()
            if not workspace:
                workspace = get_user_default_workspace(current_user, db)
        except ValueError:
            workspace = get_user_default_workspace(current_user, db)
    else:
        workspace = get_user_default_workspace(current_user, db)
        
    # Check plan limit
    if not check_usage_allowed(db, workspace.id, "upload"):
        raise HTTPException(status_code=402, detail="Upload limit reached for your current plan. Please upgrade to continue.")
        
    # Validate file
    validation = validate_file(file)
    if not validation.get("valid"):
        raise HTTPException(status_code=400, detail=validation.get("error", "Invalid file format or size"))
        
    # Save file to storage
    storage_path = save_file(file, workspace.id)
    file_size = validation.get("size", 0)
    
    dataset = Dataset(
        id=uuid.uuid4(),
        workspace_id=workspace.id,
        uploaded_by=current_user.id,
        name=file.filename or "Unnamed Dataset",
        original_filename=file.filename or "unnamed.csv",
        file_type=validation.get("mime_type", "text/csv"),
        file_size=file_size,
        storage_path=storage_path,
        status="uploaded"
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    
    # Increment usage counter
    increment_usage(db, workspace.id, "upload")
    
    # Process dataset (synchronously or fallback)
    try:
        process_dataset_synchronously(dataset, db)
    except Exception:
        try:
            from app.tasks.analysis_tasks import process_dataset_task
            process_dataset_task.delay(str(dataset.id))
        except Exception:
            pass

    return {
        "id": str(dataset.id),
        "name": dataset.name,
        "original_filename": dataset.original_filename,
        "file_type": dataset.file_type,
        "file_size": dataset.file_size,
        "row_count": dataset.row_count,
        "column_count": dataset.column_count,
        "dataset_type": dataset.dataset_type,
        "quality_score": dataset.quality_score,
        "status": dataset.status,
        "created_at": str(dataset.created_at)
    }

@router.get("", response_model=List[dict])
@router.get("/", response_model=List[dict], include_in_schema=False)
def list_datasets(
    workspace_id: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if workspace_id:
        try:
            ws_uuid = uuid.UUID(str(workspace_id))
            query = db.query(Dataset).filter(Dataset.workspace_id == ws_uuid)
        except ValueError:
            query = db.query(Dataset).filter(Dataset.uploaded_by == current_user.id)
    else:
        memberships = db.query(WorkspaceMember).filter(WorkspaceMember.user_id == current_user.id).all()
        ws_ids = [m.workspace_id for m in memberships]
        query = db.query(Dataset).filter(Dataset.workspace_id.in_(ws_ids))
        
    datasets = query.filter(Dataset.status != "deleted").order_by(Dataset.created_at.desc()).all()
    
    return [
        {
            "id": str(d.id),
            "workspace_id": str(d.workspace_id),
            "name": d.name,
            "original_filename": d.original_filename,
            "file_type": d.file_type,
            "file_size": d.file_size,
            "row_count": d.row_count,
            "column_count": d.column_count,
            "dataset_type": d.dataset_type,
            "quality_score": d.quality_score,
            "status": d.status,
            "created_at": str(d.created_at)
        }
        for d in datasets
    ]

@router.get("/{dataset_id}", response_model=dict)
def get_dataset(dataset_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.status != "deleted").first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    return {
        "id": str(dataset.id),
        "workspace_id": str(dataset.workspace_id),
        "name": dataset.name,
        "original_filename": dataset.original_filename,
        "file_type": dataset.file_type,
        "file_size": dataset.file_size,
        "row_count": dataset.row_count,
        "column_count": dataset.column_count,
        "dataset_type": dataset.dataset_type,
        "quality_score": dataset.quality_score,
        "status": dataset.status,
        "profile": dataset.profile_json,
        "cleaning_summary": dataset.cleaning_summary_json,
        "created_at": str(dataset.created_at)
    }

@router.get("/{dataset_id}/preview", response_model=dict)
def preview_dataset(
    dataset_id: uuid.UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    search: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.status != "deleted").first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    file_path = get_file_path(dataset.storage_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dataset source file not found")
        
    df = parse_file(file_path, dataset.file_type or "text/csv")
    
    if search:
        search_lower = search.lower()
        mask = df.astype(str).apply(lambda row: row.str.lower().str.contains(search_lower).any(), axis=1)
        df = df[mask]
        
    total_rows = len(df)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paged_df = df.iloc[start_idx:end_idx]
    
    rows = paged_df.replace({float('nan'): None}).to_dict(orient="records")
    columns = [{"key": col, "label": col, "type": str(df[col].dtype)} for col in df.columns]
    
    return {
        "columns": columns,
        "rows": rows,
        "total_rows": total_rows,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, (total_rows + page_size - 1) // page_size)
    }

@router.get("/{dataset_id}/profile", response_model=dict)
def get_dataset_profile(dataset_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.status != "deleted").first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    if not dataset.profile_json:
        file_path = get_file_path(dataset.storage_path)
        df = parse_file(file_path, dataset.file_type or "text/csv")
        profile = profile_dataframe(df)
        dataset.profile_json = profile
        db.commit()
        
    return {
        "profile": dataset.profile_json,
        "quality_score": dataset.quality_score,
        "cleaning_summary": dataset.cleaning_summary_json,
        "dataset_type": dataset.dataset_type
    }

@router.delete("/{dataset_id}", response_model=dict)
def delete_dataset(dataset_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    db.query(Insight).filter(Insight.analysis_id.in_(
        db.query(Analysis.id).filter(Analysis.dataset_id == dataset.id)
    )).delete(synchronize_session=False)
    
    db.query(Analysis).filter(Analysis.dataset_id == dataset.id).delete(synchronize_session=False)
    db.query(Forecast).filter(Forecast.dataset_id == dataset.id).delete(synchronize_session=False)
    db.query(Anomaly).filter(Anomaly.dataset_id == dataset.id).delete(synchronize_session=False)
    db.query(ChatMessage).filter(ChatMessage.session_id.in_(
        db.query(ChatSession.id).filter(ChatSession.dataset_id == dataset.id)
    )).delete(synchronize_session=False)
    db.query(ChatSession).filter(ChatSession.dataset_id == dataset.id).delete(synchronize_session=False)
    db.query(Report).filter(Report.dataset_id == dataset.id).delete(synchronize_session=False)
    
    if dataset.storage_path:
        delete_file(dataset.storage_path)
        
    db.delete(dataset)
    db.commit()
    
    return {"message": "Dataset and all associated analyses deleted successfully", "id": str(dataset_id)}
