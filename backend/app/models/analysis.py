import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Uuid, func
from app.config.database import Base

class Analysis(Base):
    __tablename__ = 'analyses'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey('datasets.id'), index=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(Uuid, ForeignKey('datasets.id'), index=True)
    workspace_id = Column(Uuid, ForeignKey('workspaces.id'), index=True)
    created_by = Column(Uuid, ForeignKey('users.id'))
    status = Column(String)
    summary_json = Column(JSON)
    kpis_json = Column(JSON)
    charts_json = Column(JSON)
    metadata_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
