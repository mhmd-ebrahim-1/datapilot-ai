from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class ReportCreate(BaseModel):
    dataset_id: UUID
    analysis_id: Optional[UUID] = None
    title: Optional[str] = "Executive Dataset Report"

class ReportResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    dataset_id: UUID
    analysis_id: Optional[UUID] = None
    title: str
    format: str = "pdf"
    storage_path: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
