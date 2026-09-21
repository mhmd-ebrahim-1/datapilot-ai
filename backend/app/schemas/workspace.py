from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class WorkspaceCreate(BaseModel):
    name: str
    logo_url: Optional[str] = None
    brand_color: Optional[str] = None

class WorkspaceResponse(BaseModel):
    id: UUID
    name: str
    owner_id: UUID
    logo_url: Optional[str] = None
    brand_color: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class WorkspaceMemberResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    user_id: UUID
    role: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class InviteMemberRequest(BaseModel):
    email: str
    role: Optional[str] = "analyst"
