import json
import uuid
from uuid import UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.dataset import Dataset
from app.models.analysis import Analysis
from app.models.insight import Insight
from app.schemas.analysis import AnalysisResponse, CreateAnalysisRequest
from app.services.ingestion.parser import parse_file
from app.services.ingestion.storage import get_file_path
from app.services.profiling.profiler import profile_dataframe
from app.services.cleaning.cleaner import clean_dataset
from app.services.analytics.kpi_engine import compute_kpis as calculate_kpis
from app.services.analytics.chart_recommender import recommend_charts
from app.services.profiling.type_detector import detect_type as detect_dataset_type
from app.services.ai.mock_provider import MockAIProvider

router = APIRouter(prefix="/api/v1/analyses", tags=["Analyses"])

@router.post("", response_model=dict)
@router.post("/", response_model=dict, include_in_schema=False)
async def create_analysis(request: CreateAnalysisRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    dataset_uuid = uuid.UUID(str(request.dataset_id)) if isinstance(request.dataset_id, str) else request.dataset_id
    dataset = db.query(Dataset).filter(Dataset.id == dataset_uuid).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    file_path = get_file_path(dataset.storage_path)
    df = parse_file(file_path, dataset.file_type)
    
    clean_result = clean_dataset(df)
    cleaned_df = clean_result["cleaned_df"]
    
    profile = profile_dataframe(cleaned_df)
    type_result = detect_dataset_type(cleaned_df.columns.tolist())
    dataset_type = type_result.get("dataset_type", dataset.dataset_type or "General")
    
    kpis = calculate_kpis(cleaned_df, dataset_type)
    charts = recommend_charts(cleaned_df, profile)
    
    analysis = Analysis(
        id=uuid.uuid4(),
        dataset_id=dataset.id,
        workspace_id=dataset.workspace_id,
        created_by=current_user.id,
        status="completed",
        summary_json={"rows": len(cleaned_df), "columns": len(cleaned_df.columns), "dataset_type": dataset_type},
        kpis_json=kpis,
        charts_json=charts,
        metadata_json={"profile": profile, "cleaning": clean_result.get("changes_log", [])},
    )
    db.add(analysis)
    
    try:
        provider = MockAIProvider()
        ai_insights = await provider.generate_insights(
            {"kpis": kpis, "profile_summary": {"rows": len(cleaned_df), "columns": len(cleaned_df.columns)}},
            {"name": dataset.name, "dataset_type": dataset_type}
        )
        for insight_data in ai_insights:
            insight = Insight(
                id=uuid.uuid4(),
                analysis_id=analysis.id,
                title=insight_data.get("title", ""),
                category=insight_data.get("category", "performance"),
                severity=insight_data.get("severity", "info"),
                description=insight_data.get("description", ""),
                recommendation=insight_data.get("recommendation", ""),
                supporting_metrics_json=insight_data.get("supporting_metrics_json", {}),
            )
            db.add(insight)
    except Exception:
        pass  
    
    db.commit()
    db.refresh(analysis)
    
    return {"id": str(analysis.id), "status": "completed", "kpis": kpis, "charts": charts, "dataset_type": dataset_type}

@router.get("", response_model=list)
@router.get("/", response_model=list, include_in_schema=False)
async def list_analyses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    analyses = db.query(Analysis).filter(Analysis.created_by == current_user.id).order_by(Analysis.created_at.desc()).all()
    return [{"id": str(a.id), "dataset_id": str(a.dataset_id), "status": a.status, "created_at": str(a.created_at)} for a in analyses]

@router.get("/{analysis_id}", response_model=dict)
async def get_analysis(analysis_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {
        "id": str(analysis.id),
        "dataset_id": str(analysis.dataset_id),
        "status": analysis.status,
        "kpis": analysis.kpis_json or [],
        "charts": analysis.charts_json or [],
        "summary": analysis.summary_json or {},
        "metadata": analysis.metadata_json or {},
        "created_at": str(analysis.created_at)
    }
