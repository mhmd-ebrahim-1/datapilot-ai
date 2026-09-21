import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Uuid, func
from sqlalchemy.orm import relationship
from app.config.database import Base

class RoleEnum(str, enum.Enum):
    owner = "owner"
    admin = "admin"
    analyst = "analyst"
    viewer = "viewer"

class Workspace(Base):
    __tablename__ = 'workspaces'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Uuid, ForeignKey('users.id'), index=True)
    logo_url = Column(String, nullable=True)
    brand_color = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WorkspaceMember(Base):
    __tablename__ = 'workspace_members'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(Uuid, ForeignKey('workspaces.id'), index=True)
    user_id = Column(Uuid, ForeignKey('users.id'), index=True)
    role = Column(String, default="owner")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

