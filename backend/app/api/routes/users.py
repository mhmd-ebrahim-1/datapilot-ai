from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.get("/onboarding")
async def get_onboarding(current_user: User = Depends(get_current_user)):
    return {"completed": current_user.role != "user", "user_type": current_user.role}

@router.post("/onboarding")
async def save_onboarding(body: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if body.get("user_type"):
        current_user.role = body["user_type"]
    db.commit()
    return {"status": "ok"}
