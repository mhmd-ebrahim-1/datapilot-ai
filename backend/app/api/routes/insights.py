from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.config.database import get_db
from app.models.insight import Insight

router = APIRouter(prefix="/api/v1/insights", tags=["Insights"])

@router.get("/{analysis_id}")
async def get_insights(analysis_id: UUID, db: Session = Depends(get_db)):
    insights = db.query(Insight).filter(Insight.analysis_id == analysis_id).all()
    return [{
        "id": str(i.id),
        "title": i.title,
        "category": i.category,
        "severity": i.severity,
        "description": i.description,
        "recommendation": i.recommendation,
        "supporting_metrics": i.supporting_metrics_json
    } for i in insights]
