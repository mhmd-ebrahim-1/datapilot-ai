from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class AnomalyResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    column_name: str
    row_reference: Optional[str] = None
    value_str: Optional[str] = None
    score: Optional[float] = None
    explanation: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
