import json
import uuid
import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.dataset import Dataset
from app.models.analysis import Analysis
from app.models.insight import Insight
from app.models.report import Report
from app.services.reporting.pdf_generator import generate_pdf_report

logger = logging.getLogger("datapilot.reports")

def create_report_for_dataset(
    db: Session,
    dataset_id: uuid.UUID,
    user_id: uuid.UUID,
    title: str = "Executive Dataset Report"
) -> Report:
    """Orchestrate verified report metrics gathering and render executive PDF."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise ValueError("Dataset not found")
        
    if dataset.status == "failed":
        raise ValueError(f"Cannot generate report for a failed dataset: {dataset.error_message or 'Processing error'}")
        
    analysis = db.query(Analysis).filter(Analysis.dataset_id == dataset.id).order_by(Analysis.created_at.desc()).first()
    
    analysis_data = {}
    insights_data = []
    
    if analysis:
        kpis = json.loads(analysis.kpis_json) if isinstance(analysis.kpis_json, str) else (analysis.kpis_json or [])
        summary = json.loads(analysis.summary_json) if isinstance(analysis.summary_json, str) else (analysis.summary_json or {})
        charts = json.loads(analysis.charts_json) if isinstance(analysis.charts_json, str) else (analysis.charts_json or [])
        
        analysis_data = {
            "kpis": kpis,
            "summary": summary,
            "charts": charts
        }
        db_insights = db.query(Insight).filter(Insight.analysis_id == analysis.id).all()
        insights_data = [{
            "title": ins.title,
            "category": ins.category,
            "severity": ins.severity,
            "description": ins.description,
            "recommendation": ins.recommendation
        } for ins in db_insights]
        
    report_payload = {
        "title": title,
        "dataset_name": dataset.original_filename or dataset.name,
        "row_count": dataset.row_count or 0,
        "column_count": dataset.column_count or 0,
        "analysis": analysis_data,
        "insights": insights_data,
        "cleaning_summary": dataset.cleaning_summary_json or [],
        "dataset_type": dataset.dataset_type or "General Analytics",
        "quality_score": dataset.quality_score if dataset.quality_score is not None else 90.0
    }
    
    storage_path = generate_pdf_report(report_payload, str(dataset.workspace_id))
    
    report = Report(
        id=uuid.uuid4(),
        workspace_id=dataset.workspace_id,
        dataset_id=dataset.id,
        analysis_id=analysis.id if analysis else None,
        created_by=user_id,
        title=title,
        format="pdf",
        storage_path=storage_path
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    logger.info(f"Executive Report '{title}' (ID: {report.id}) generated successfully at {storage_path}")
    return report
