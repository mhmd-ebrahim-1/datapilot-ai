from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

class CreateAnalysisRequest(BaseModel):
    dataset_id: UUID

class AnalysisResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    workspace_id: UUID
    status: str
    summary_json: Optional[Dict[str, Any]] = None
    kpis_json: Optional[List[Dict[str, Any]]] = None
    charts_json: Optional[List[Dict[str, Any]]] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
