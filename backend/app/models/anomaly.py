import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Uuid, func
from app.config.database import Base

class Anomaly(Base):
    __tablename__ = 'anomalies'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey('datasets.id'), index=True)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey('analyses.id'))
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(Uuid, ForeignKey('datasets.id'), index=True)
    analysis_id = Column(Uuid, ForeignKey('analyses.id'), nullable=True)
    column_name = Column(String, nullable=False)
    row_reference = Column(String)
    value_str = Column(String)
    score = Column(Float)
    explanation = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
