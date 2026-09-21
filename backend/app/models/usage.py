import uuid
from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, UniqueConstraint, Uuid, func
from app.config.database import Base

class Usage(Base):
    __tablename__ = 'usage'
    __table_args__ = (UniqueConstraint('workspace_id', 'month', name='uq_workspace_month'),)
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), index=True)
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(Uuid, ForeignKey('workspaces.id'), index=True)
    month = Column(Date, nullable=False)
    analyses_count = Column(Integer, default=0)
    uploads_count = Column(Integer, default=0)
    ai_requests_count = Column(Integer, default=0)
    chat_requests_count = Column(Integer, default=0)
    reports_count = Column(Integer, default=0)
    forecast_requests_count = Column(Integer, default=0)
    storage_used_mb = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
