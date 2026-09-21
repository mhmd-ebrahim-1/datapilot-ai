from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class InsightResponse(BaseModel):
    id: UUID
    analysis_id: UUID
    title: str
    category: str
    severity: str
    description: str
    recommendation: Optional[str] = None
    supporting_metrics_json: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
