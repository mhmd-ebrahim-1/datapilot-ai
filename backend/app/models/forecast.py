import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, Uuid, func
from app.config.database import Base

class Forecast(Base):
    __tablename__ = 'forecasts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey('datasets.id'), index=True)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey('analyses.id'))
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    dataset_id = Column(Uuid, ForeignKey('datasets.id'), index=True)
    analysis_id = Column(Uuid, ForeignKey('analyses.id'), nullable=True)
    metric = Column(String, nullable=False)
    horizon = Column(Integer, nullable=False)
    model_name = Column(String)
    predictions_json = Column(JSON)
    confidence_intervals_json = Column(JSON)
    metrics_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
