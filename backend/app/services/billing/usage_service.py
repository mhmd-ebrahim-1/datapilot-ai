import uuid
from datetime import datetime, date, timezone
from sqlalchemy.orm import Session
from app.models.usage import Usage
from app.models.subscription import Subscription
from app.config.settings import PLAN_LIMITS

def get_current_month_date() -> date:
    today = datetime.now(timezone.utc).date()
    return date(today.year, today.month, 1)

def get_or_create_usage(db: Session, workspace_id: uuid.UUID) -> Usage:
    current_month = get_current_month_date()
    usage = db.query(Usage).filter(
        Usage.workspace_id == workspace_id,
        Usage.month == current_month
    ).first()
    
    if not usage:
        usage = Usage(
            id=uuid.uuid4(),
            workspace_id=workspace_id,
            month=current_month,
            analyses_count=0,
            uploads_count=0,
            ai_requests_count=0,
            chat_requests_count=0,
            reports_count=0,
            forecast_requests_count=0,
            storage_used_mb=0
        )
        db.add(usage)
        db.commit()
        db.refresh(usage)
    return usage

def increment_usage(db: Session, workspace_id: uuid.UUID, metric: str, amount: int = 1) -> Usage:
    usage = get_or_create_usage(db, workspace_id)
    field_map = {
        "analysis": "analyses_count",
        "analyses": "analyses_count",
        "upload": "uploads_count",
        "uploads": "uploads_count",
        "ai_request": "ai_requests_count",
        "ai_requests": "ai_requests_count",
        "chat": "chat_requests_count",
        "report": "reports_count",
        "reports": "reports_count",
        "forecast": "forecast_requests_count",
        "storage": "storage_used_mb"
    }
    field_name = field_map.get(metric)
    if field_name and hasattr(usage, field_name):
        current_val = getattr(usage, field_name, 0) or 0
        setattr(usage, field_name, current_val + amount)
        db.commit()
        db.refresh(usage)
    return usage

def check_usage_allowed(db: Session, workspace_id: uuid.UUID, metric: str, amount: int = 1) -> bool:
    sub = db.query(Subscription).filter(Subscription.workspace_id == workspace_id).first()
    plan_name = sub.plan if sub else "free"
    limits = PLAN_LIMITS.get(plan_name, PLAN_LIMITS["free"])
    
    usage = get_or_create_usage(db, workspace_id)
    
    limit_mapping = {
        "analysis": ("analyses_count", "max_analyses_per_month"),
        "upload": ("uploads_count", "max_datasets"),
        "ai_request": ("ai_requests_count", "max_ai_requests_per_month"),
        "chat": ("chat_requests_count", "max_chat_messages_per_month"),
        "report": ("reports_count", "max_reports_per_month"),
        "forecast": ("forecast_requests_count", "max_forecast_requests_per_month"),
        "storage": ("storage_used_mb", "max_storage_mb")
    }
    
    if metric in limit_mapping:
        usage_col, limit_key = limit_mapping[metric]
        current_used = getattr(usage, usage_col, 0) or 0
        max_allowed = limits.get(limit_key, 999999)
        return (current_used + amount) <= max_allowed
    return True

