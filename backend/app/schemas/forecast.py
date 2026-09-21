from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime

class ForecastRequest(BaseModel):
    dataset_id: UUID
    metric: Optional[str] = None
    date_col: Optional[str] = None
    horizon: int = 30

class ForecastResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    metric: str
    horizon: int
    model_name: Optional[str] = None
    predictions_json: Optional[List[Dict[str, Any]]] = None
    confidence_intervals_json: Optional[List[Dict[str, Any]]] = None
    metrics_json: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
