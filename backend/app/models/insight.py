import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Uuid, func
from app.config.database import Base

class Insight(Base):
    __tablename__ = 'insights'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey('analyses.id'), index=True)
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    analysis_id = Column(Uuid, ForeignKey('analyses.id'), index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    description = Column(String)
    recommendation = Column(String)
    supporting_metrics_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
