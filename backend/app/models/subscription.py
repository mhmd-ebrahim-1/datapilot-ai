import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, ForeignKey, Uuid, func
from app.config.database import Base

class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), unique=True, index=True)
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(Uuid, ForeignKey('workspaces.id'), unique=True, index=True)
    plan = Column(String, default='free')
    status = Column(String, default='active')
    provider = Column(String)
    provider_customer_id = Column(String)
    provider_subscription_id = Column(String)
    current_period_start = Column(DateTime(timezone=True))
    current_period_end = Column(DateTime(timezone=True))
    provider = Column(String, nullable=True)
    provider_customer_id = Column(String, nullable=True)
    provider_subscription_id = Column(String, nullable=True)
    current_period_start = Column(DateTime(timezone=True), nullable=True)
    current_period_end = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
