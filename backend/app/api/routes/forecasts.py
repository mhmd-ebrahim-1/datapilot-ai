import uuid
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.dataset import Dataset
from app.models.forecast import Forecast
from app.services.ingestion.parser import parse_file
from app.services.ingestion.storage import get_file_path
from app.services.forecasting.forecast_engine import generate_forecast

router = APIRouter(prefix="/api/v1/forecasts", tags=["Forecasts"])

@router.post("", response_model=dict)
@router.post("/", response_model=dict, include_in_schema=False)
async def create_forecast(body: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    dataset_id_raw = body.get("dataset_id")
    metric = body.get("metric")
    date_col = body.get("date_col")
    horizon = int(body.get("horizon", 30))
    
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
    
    result = generate_forecast(df, date_col=date_col, target_col=metric, horizon=horizon)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    forecast = Forecast(
        id=uuid.uuid4(),
        dataset_id=dataset.id,
        analysis_id=None,
        metric=result.get("metric", "auto"),
        horizon=horizon,
        model_name=result.get("model", "Moving Average"),
        predictions_json=result.get("predictions", []),
        confidence_intervals_json=result.get("confidence_intervals", []),
        metrics_json=result.get("metrics", {})
    )
    db.add(forecast)
    db.commit()
    db.refresh(forecast)
    
    return {
        "id": str(forecast.id),
        **result
    }

@router.get("/{forecast_id}", response_model=dict)
async def get_forecast(forecast_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    f = db.query(Forecast).filter(Forecast.id == forecast_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Forecast not found")
        
    return {
        "id": str(f.id),
        "metric": f.metric,
        "horizon": f.horizon,
        "model": f.model_name,
        "predictions": f.predictions_json or [],
        "confidence_intervals": f.confidence_intervals_json or [],
        "metrics": f.metrics_json or {},
        "created_at": str(f.created_at)
    }

@router.get("/dataset/{dataset_id}", response_model=list)
async def list_forecasts(dataset_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    forecasts = db.query(Forecast).filter(Forecast.dataset_id == dataset_id).order_by(Forecast.created_at.desc()).all()
    return [{
        "id": str(f.id),
        "metric": f.metric,
        "model": f.model_name,
        "horizon": f.horizon,
        "predictions": f.predictions_json or [],
        "metrics": f.metrics_json or {},
        "created_at": str(f.created_at)
    } for f in forecasts]
