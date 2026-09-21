import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Uuid, func
from app.config.database import Base

class Report(Base):
    __tablename__ = 'reports'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(Uuid, ForeignKey('workspaces.id'), index=True, nullable=True)
    dataset_id = Column(Uuid, ForeignKey('datasets.id'))
    analysis_id = Column(Uuid, ForeignKey('analyses.id'), nullable=True)
    created_by = Column(Uuid, ForeignKey('users.id'))
    title = Column(String, nullable=False)
    format = Column(String, default='pdf')
    storage_path = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
