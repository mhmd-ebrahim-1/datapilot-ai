import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Uuid, func
from app.config.database import Base

class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), index=True)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey('datasets.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(Uuid, ForeignKey('workspaces.id'), index=True)
    dataset_id = Column(Uuid, ForeignKey('datasets.id'))
    user_id = Column(Uuid, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey('chat_sessions.id'), index=True)
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    session_id = Column(Uuid, ForeignKey('chat_sessions.id'), index=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    metadata_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
