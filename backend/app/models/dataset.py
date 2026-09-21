import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float, JSON, Uuid, func
from app.config.database import Base

class Dataset(Base):
    __tablename__ = 'datasets'
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(Uuid, ForeignKey('workspaces.id'), index=True)
    uploaded_by = Column(Uuid, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    original_filename = Column(String)
    file_type = Column(String)
    file_size = Column(Integer)
    storage_path = Column(String)
    row_count = Column(Integer, nullable=True)
    column_count = Column(Integer, nullable=True)
    dataset_type = Column(String, nullable=True)
    quality_score = Column(Float, nullable=True)
    status = Column(String, default="uploaded")
    error_message = Column(String, nullable=True)
    profile_json = Column(JSON, nullable=True)
    cleaning_summary_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
