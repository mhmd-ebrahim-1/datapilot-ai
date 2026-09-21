import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.config.settings import settings

class BillingService:
    @staticmethod
    def create_checkout_session(workspace_id: uuid.UUID, plan: str) -> Dict[str, Any]:
        """Create checkout session (mock or Stripe integration ready)."""
        session_id = f"cs_{uuid.uuid4().hex[:16]}"
        return {
            "session_id": session_id,
            "url": f"{settings.FRONTEND_URL}/settings?session_id={session_id}&plan={plan}&status=success",
            "plan": plan,
            "workspace_id": str(workspace_id)
        }

    @staticmethod
    def upgrade_subscription(db: Session, workspace_id: uuid.UUID, plan: str) -> Subscription:
        sub = db.query(Subscription).filter(Subscription.workspace_id == workspace_id).first()
        now = datetime.now(timezone.utc)
        if not sub:
            sub = Subscription(
                id=uuid.uuid4(),
                workspace_id=workspace_id,
                plan=plan,
                status="active",
                provider=settings.PAYMENT_PROVIDER,
                current_period_start=now,
                current_period_end=now + timedelta(days=30)
            )
            db.add(sub)
        else:
            sub.plan = plan
            sub.status = "active"
            sub.current_period_start = now
            sub.current_period_end = now + timedelta(days=30)
        db.commit()
        db.refresh(sub)
        return sub

    @staticmethod
    def cancel_subscription(db: Session, workspace_id: uuid.UUID) -> Subscription:
        sub = db.query(Subscription).filter(Subscription.workspace_id == workspace_id).first()
        if sub:
            sub.status = "canceled"
            sub.plan = "free"
            db.commit()
            db.refresh(sub)
        return sub

