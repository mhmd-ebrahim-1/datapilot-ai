from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime

class DatasetResponse(BaseModel):
    id: UUID
    name: str
    original_filename: str
    file_type: str
    file_size: int
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    dataset_type: Optional[str] = None
    quality_score: Optional[float] = None
    status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class DatasetPreviewResponse(BaseModel):
    columns: List[Any]
    rows: List[Dict[str, Any]]
    total_rows: int
    page: int
    page_size: int

class DatasetProfileResponse(BaseModel):
    profile: Dict[str, Any]
    quality_metrics: Optional[Dict[str, Any]] = None
    quality_score: Optional[float] = None
    cleaning_summary: Optional[List[Dict[str, Any]]] = None
    dataset_type: Optional[str] = None
