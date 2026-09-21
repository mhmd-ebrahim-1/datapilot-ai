import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float, JSON, Uuid, func
from app.config.database import Base

class Dataset(Base):
    __tablename__ = 'datasets'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), index=True)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(Uuid, ForeignKey('workspaces.id'), index=True)
    uploaded_by = Column(Uuid, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    original_filename = Column(String)
    file_type = Column(String)
    file_size = Column(Integer)
    storage_path = Column(String)
    row_count = Column(Integer)
    column_count = Column(Integer)
    dataset_type = Column(String)
    quality_score = Column(Float)
    status = Column(String, default="uploaded")
    profile_json = Column(JSON)
    cleaning_summary_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
