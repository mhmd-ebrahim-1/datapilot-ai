from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.workspace import Workspace
from app.models.dataset import Dataset
from app.models.subscription import Subscription

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(403, "Admin access required")
    return current_user

@router.get("/users")
async def list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [{"id": str(u.id), "name": u.name, "email": u.email, "role": u.role, "is_active": u.is_active, "created_at": str(u.created_at)} for u in users]

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return {"total_users": db.query(User).count(), "total_workspaces": db.query(Workspace).count(), "total_datasets": db.query(Dataset).count(), "active_subscriptions": db.query(Subscription).filter(Subscription.status == "active").count()}
