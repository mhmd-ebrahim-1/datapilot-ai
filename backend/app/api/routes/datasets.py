import os
import uuid
import logging
import traceback
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, Request, status
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
from app.services.ingestion.storage import (
    save_file,
    get_file_path,
    delete_file,
    get_storage_service
)
from app.services.ingestion.file_validator import validate_file, validate_upload_metadata
from app.services.ingestion.parser import parse_file
from app.services.cleaning.cleaner import clean_dataset
from app.services.profiling.profiler import profile_dataframe
from app.services.profiling.quality_scorer import calculate_quality_score
from app.services.profiling.type_detector import detect_dataset_type
from app.services.billing.usage_service import increment_usage, check_usage_allowed
from app.schemas.dataset import (
    PresignedUploadRequest,
    PresignedUploadResponse,
    ProcessDatasetRequest,
    DatasetResponse
)

logger = logging.getLogger("datapilot.datasets")
router = APIRouter(prefix="/api/v1/datasets", tags=["Datasets"])

def check_workspace_access(user: User, workspace_id: uuid.UUID, db: Session) -> Workspace:
    """Ensure user is a member or owner of the workspace."""
    if user.role in ["admin", "superadmin"]:
        ws = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        if ws:
            return ws
            
    membership = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == user.id
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="You do not have access to this workspace.")
        
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    return workspace

def check_dataset_access(user: User, dataset: Dataset, db: Session):
    """Ensure user has permission to access or operate on this dataset."""
    if user.role in ["admin", "superadmin"] or dataset.uploaded_by == user.id:
        return True
        
    if dataset.workspace_id:
        membership = db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == dataset.workspace_id,
            WorkspaceMember.user_id == user.id
        ).first()
        if membership:
            return True
            
    raise HTTPException(status_code=403, detail="You do not have permission to access this dataset.")

def process_dataset_synchronously(dataset: Dataset, db: Session):
    """Perform dataset parsing, cleaning, profiling, type detection and scoring with complete error capture."""
    try:
        dataset.status = "processing"
        dataset.error_message = None
        db.commit()
        
        storage_service = get_storage_service()
        if not storage_service.check_file_exists(dataset.storage_path):
            raise FileNotFoundError(f"Dataset file does not exist in storage: {dataset.storage_path}")
            
        file_path = get_file_path(dataset.storage_path)
        logger.info(f"Starting synchronous ingestion for dataset {dataset.id} ({dataset.original_filename}) from {file_path}")
        
        # 1. Parse file
        df = parse_file(file_path, dataset.file_type or "text/csv")
        if df is None or df.empty:
            raise ValueError("Parsed dataset contains 0 rows or empty data.")
            
        # 2. Clean dataset
        clean_result = clean_dataset(df)
        cleaned_df = clean_result["cleaned_df"]
        if cleaned_df.empty or len(cleaned_df.columns) == 0:
            raise ValueError("Dataset has no valid columns or rows after cleaning.")
            
        # 3. Profile & Quality scoring
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
        dataset.error_message = None
        
        db.commit()
        db.refresh(dataset)
        logger.info(f"Dataset {dataset.id} successfully processed: {dataset.row_count} rows, {dataset.column_count} cols, score={dataset.quality_score}")
    except Exception as e:
        error_detail = str(e.detail) if hasattr(e, 'detail') else str(e)
        logger.error(f"Failed to process dataset {dataset.id}: {error_detail}\n{traceback.format_exc()}")
        
        dataset.status = "failed"
        dataset.error_message = error_detail
        dataset.row_count = None
        dataset.column_count = None
        dataset.quality_score = None
        db.commit()
        db.refresh(dataset)

@router.post("/presigned-upload", response_model=PresignedUploadResponse, status_code=status.HTTP_201_CREATED)
@router.post("/upload-url", response_model=PresignedUploadResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def request_presigned_upload(
    req: PresignedUploadRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate short-lived presigned upload URL for direct browser-to-storage upload.
    Completely bypasses Vercel 4.5MB request limits and validates file size up to 50MB+.
    """
    # 1. Resolve & verify workspace access
    if req.workspace_id:
        workspace = check_workspace_access(current_user, req.workspace_id, db)
    else:
        workspace = get_user_default_workspace(current_user, db)
        
    # 2. Check plan usage limit
    if not check_usage_allowed(db, workspace.id, "upload"):
        raise HTTPException(
            status_code=402,
            detail="Upload limit reached for your current plan. Please upgrade to continue."
        )
        
    # 3. Validate file metadata and limits
    validated = validate_upload_metadata(
        filename=req.filename,
        file_size=req.file_size,
        content_type=req.content_type
    )
    
    # 4. Generate secure server-side storage path
    safe_filename = validated["safe_filename"]
    storage_path = f"{workspace.id}/datasets/{safe_filename}"
    
    # 5. Create Dataset record in pending_upload state
    dataset_id = uuid.uuid4()
    dataset = Dataset(
        id=dataset_id,
        workspace_id=workspace.id,
        uploaded_by=current_user.id,
        name=validated["original_filename"],
        original_filename=validated["original_filename"],
        file_type=validated["mime_type"],
        file_size=validated["file_size"],
        storage_path=storage_path,
        status="pending_upload"
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    
    # 6. Generate presigned upload URL
    storage_service = get_storage_service()
    presigned = storage_service.generate_presigned_upload_url(
        storage_path=storage_path,
        content_type=validated["mime_type"],
        expires_in=600
    )
    
    return {
        "dataset_id": dataset.id,
        "upload_url": presigned["upload_url"],
        "method": presigned["method"],
        "storage_path": presigned["storage_path"],
        "headers": presigned["headers"],
        "expires_in": presigned["expires_in"],
        "is_direct_s3": presigned["is_direct_s3"]
    }

@router.post("/{dataset_id}/process", response_model=dict)
@router.post("/confirm-upload", response_model=dict, include_in_schema=False)
async def process_dataset(
    dataset_id: Optional[uuid.UUID] = None,
    req: Optional[ProcessDatasetRequest] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Trigger deterministic processing of an uploaded dataset.
    Receives only tiny metadata JSON, completely bypassing serverless limits.
    """
    target_id = dataset_id or (req.dataset_id if req else None)
    if not target_id:
        raise HTTPException(status_code=400, detail="dataset_id is required.")
        
    dataset = db.query(Dataset).filter(Dataset.id == target_id, Dataset.status != "deleted").first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found.")
        
    check_dataset_access(current_user, dataset, db)
    
    storage_service = get_storage_service()
    if not storage_service.check_file_exists(dataset.storage_path):
        raise HTTPException(
            status_code=400,
            detail=f"File was not uploaded or does not exist at storage key: {dataset.storage_path}"
        )
        
    # Increment usage counter upon confirmed processing
    increment_usage(db, dataset.workspace_id, "upload")
    
    # Run deterministic processing pipeline
    process_dataset_synchronously(dataset, db)
    
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
        "error_message": dataset.error_message,
        "created_at": str(dataset.created_at)
    }

@router.put("/local-direct-upload")
async def local_direct_upload(
    request: Request,
    storage_path: str = Query(...)
):
    """
    Local fallback handler for direct PUT uploads during testing or offline environments.
    """
    body = await request.body()
    if not body:
        raise HTTPException(status_code=400, detail="Request body is empty.")
    content_type = request.headers.get("content-type", "application/octet-stream")
    storage_service = get_storage_service()
    storage_service.save_file_bytes(body, storage_path, content_type)
    return {"status": "ok", "bytes_received": len(body), "storage_path": storage_path}

@router.post("/upload", response_model=dict, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
async def upload_dataset_legacy(
    file: UploadFile = File(...),
    workspace_id: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Direct multipart upload endpoint (kept for local/self-hosted compatibility).
    For serverless/Vercel production, use /api/v1/datasets/presigned-upload instead.
    """
    # Determine target workspace
    if workspace_id:
        try:
            ws_uuid = uuid.UUID(str(workspace_id))
            workspace = db.query(Workspace).filter(Workspace.id == ws_uuid).first()
            if not workspace:
                workspace = get_user_default_workspace(current_user, db)
            workspace = check_workspace_access(current_user, ws_uuid, db)
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
    
    # Process dataset synchronously
    process_dataset_synchronously(dataset, db)

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
        "error_message": dataset.error_message,
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
            "error_message": d.error_message,
            "created_at": str(d.created_at)
        }
        for d in datasets
    ]

@router.get("/{dataset_id}", response_model=dict)
def get_dataset(dataset_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.status != "deleted").first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    check_dataset_access(current_user, dataset, db)
        
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
        "error_message": dataset.error_message,
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
        
    check_dataset_access(current_user, dataset, db)
        
    if dataset.status == "failed":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot preview dataset because processing failed: {dataset.error_message or 'Unknown processing error'}"
        )
        
    file_path = get_file_path(dataset.storage_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dataset source file not found on disk")
        raise HTTPException(status_code=404, detail="Dataset source file not found in storage")
        
    df = parse_file(file_path, dataset.file_type or "text/csv")
    
    if search:
        search_lower = search.lower()
        mask = df.astype(str).apply(lambda row: row.str.lower().str.contains(search_lower).any(), axis=1)
        df = df[mask]
        
    total_rows = len(df)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paged_df = df.iloc[start_idx:end_idx]
    
    # Format nulls to None for clean JSON serialization
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
        
    check_dataset_access(current_user, dataset, db)
        
    if dataset.status == "failed":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot profile dataset because processing failed: {dataset.error_message or 'Unknown processing error'}"
        )
        
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
        
    check_dataset_access(current_user, dataset, db)
        
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
