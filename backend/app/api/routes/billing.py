from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.api.dependencies import get_current_user, get_user_default_workspace
from app.models.user import User
from app.models.subscription import Subscription
from app.models.usage import Usage
from app.models.workspace import WorkspaceMember
from app.config.settings import PLAN_LIMITS
from datetime import datetime, timezone
from app.services.billing.billing_service import BillingService
from app.services.billing.usage_service import get_or_create_usage, get_current_month_date

router = APIRouter(prefix="/api/v1/billing", tags=["Billing"])

@router.get("/subscription", response_model=dict)
async def get_subscription(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    membership = db.query(WorkspaceMember).filter(WorkspaceMember.user_id == current_user.id).first()
    if not membership:
        ws = get_user_default_workspace(current_user, db)
        sub = db.query(Subscription).filter(Subscription.workspace_id == ws.id).first()
    else:
        sub = db.query(Subscription).filter(Subscription.workspace_id == membership.workspace_id).first()
        
    if not sub:
        return {"plan": "free", "status": "active", "limits": PLAN_LIMITS["free"]}
        
    return {
        "plan": sub.plan,
        "status": sub.status,
        "limits": PLAN_LIMITS.get(sub.plan, PLAN_LIMITS["free"]),
        "current_period_start": str(sub.current_period_start) if sub.current_period_start else None,
        "current_period_end": str(sub.current_period_end) if sub.current_period_end else None
    }

@router.get("/usage", response_model=dict)
async def get_usage(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    membership = db.query(WorkspaceMember).filter(WorkspaceMember.user_id == current_user.id).first()
    if not membership:
        ws = get_user_default_workspace(current_user, db)
        workspace_id = ws.id
    else:
        workspace_id = membership.workspace_id
        
    usage = get_or_create_usage(db, workspace_id)
    sub = db.query(Subscription).filter(Subscription.workspace_id == workspace_id).first()
    plan = sub.plan if sub else "free"
    limits = PLAN_LIMITS.get(plan, PLAN_LIMITS["free"])
    
    return {
        "plan": plan,
        "analyses": {"used": usage.analyses_count, "limit": limits["max_analyses_per_month"]},
        "ai_requests": {"used": usage.ai_requests_count, "limit": limits["max_ai_requests_per_month"]},
        "uploads": {"used": usage.uploads_count, "limit": limits["max_datasets"]},
        "chat_requests": {"used": usage.chat_requests_count, "limit": limits.get("max_chat_messages_per_month", 50)},
        "reports": {"used": usage.reports_count, "limit": limits.get("max_reports_per_month", 5)},
        "storage_mb": {"used": usage.storage_used_mb, "limit": limits["max_storage_mb"]}
    }

@router.get("/plans", response_model=list)
async def get_plans():
    return [{"name": name, "limits": limits} for name, limits in PLAN_LIMITS.items()]

@router.post("/checkout", response_model=dict)
async def create_checkout(body: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan = body.get("plan", "pro").lower()
    if plan not in PLAN_LIMITS:
        raise HTTPException(status_code=400, detail="Invalid plan selected")
        
    membership = db.query(WorkspaceMember).filter(WorkspaceMember.user_id == current_user.id).first()
    if not membership:
        ws = get_user_default_workspace(current_user, db)
        workspace_id = ws.id
    else:
        workspace_id = membership.workspace_id
        
    checkout = BillingService.create_checkout_session(workspace_id, plan)
    return checkout

@router.post("/upgrade", response_model=dict)
async def upgrade_plan(body: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan = body.get("plan", "pro").lower()
    if plan not in PLAN_LIMITS:
        raise HTTPException(status_code=400, detail="Invalid plan selected")
        
    membership = db.query(WorkspaceMember).filter(WorkspaceMember.user_id == current_user.id).first()
    if not membership:
        ws = get_user_default_workspace(current_user, db)
        workspace_id = ws.id
    else:
        workspace_id = membership.workspace_id
        
    sub = BillingService.upgrade_subscription(db, workspace_id, plan)
    return {
        "message": f"Successfully upgraded workspace to {plan.upper()} plan!",
        "plan": sub.plan,
        "status": sub.status
    }
