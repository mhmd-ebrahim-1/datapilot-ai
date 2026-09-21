from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class ReportCreate(BaseModel):
    dataset_id: UUID
    title: Optional[str] = "Executive Dataset Report"

class ReportResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    dataset_id: UUID
    title: str
    format: str = "pdf"
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
