import uuid
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember
from app.services.auth_service import decode_token
from app.config.settings import settings

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    
    try:
        user_uuid = uuid.UUID(str(user_id_str)) if isinstance(user_id_str, str) else user_id_str
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID format")
        
    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
        
    return user

def get_current_workspace(workspace_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Workspace:
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
        
    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()
    
    if not member and current_user.role not in ['admin', 'superadmin']:
        raise HTTPException(status_code=403, detail="Not a member of this workspace")
        
    return workspace

def get_user_default_workspace(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Workspace:
    membership = db.query(WorkspaceMember).filter(WorkspaceMember.user_id == current_user.id).first()
    if membership:
        workspace = db.query(Workspace).filter(Workspace.id == membership.workspace_id).first()
        if workspace:
            return workspace
    # If no workspace yet, create a default one
    workspace = Workspace(
        id=uuid.uuid4(),
        name=f"{current_user.name}'s Workspace",
        owner_id=current_user.id
    )
    db.add(workspace)
    db.flush()
    member = WorkspaceMember(
        id=uuid.uuid4(),
        workspace_id=workspace.id,
        user_id=current_user.id,
        role="owner"
    )
    db.add(member)
    db.commit()
    db.refresh(workspace)
    return workspace

def check_permission(required_role: str):
    def _check_permission(workspace_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        if current_user.role in ['admin', 'superadmin']:
            return True
            
        member = db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == current_user.id
        ).first()
        
        if not member:
            raise HTTPException(status_code=403, detail="Not a member of this workspace")
        
        role_str = getattr(member.role, 'value', member.role) if member else "viewer"
        roles_hierarchy = {"viewer": 0, "analyst": 1, "admin": 2, "owner": 3}
        if roles_hierarchy.get(role_str, -1) < roles_hierarchy.get(required_role, -1):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
            
        return True
    return _check_permission
