import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, ForeignKey, Uuid, func
from app.config.database import Base

class Report(Base):
    __tablename__ = 'reports'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey('datasets.id'))
    analysis_id = Column(UUID(as_uuid=True), ForeignKey('analyses.id'))
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(Uuid, ForeignKey('workspaces.id'), index=True)
    dataset_id = Column(Uuid, ForeignKey('datasets.id'))
    analysis_id = Column(Uuid, ForeignKey('analyses.id'), nullable=True)
    created_by = Column(Uuid, ForeignKey('users.id'))
    title = Column(String, nullable=False)
    format = Column(String, default='pdf')
    storage_path = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
