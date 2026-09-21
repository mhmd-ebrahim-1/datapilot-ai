import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.api.dependencies import get_current_user, get_current_workspace, check_permission
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember
from app.models.subscription import Subscription
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse, WorkspaceMemberResponse, InviteMemberRequest

router = APIRouter(prefix="/api/v1/workspaces", tags=["Workspaces"])

@router.get("", response_model=List[dict])
@router.get("/", response_model=List[dict], include_in_schema=False)
def list_workspaces(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    memberships = db.query(WorkspaceMember).filter(WorkspaceMember.user_id == current_user.id).all()
    workspace_ids = [m.workspace_id for m in memberships]
    workspaces = db.query(Workspace).filter(Workspace.id.in_(workspace_ids)).all()
    
    role_map = {m.workspace_id: getattr(m.role, 'value', m.role) for m in memberships}
    
    return [
        {
            "id": str(w.id),
            "name": w.name,
            "owner_id": str(w.owner_id),
            "logo_url": w.logo_url,
            "brand_color": w.brand_color,
            "role": role_map.get(w.id, "viewer"),
            "created_at": str(w.created_at)
        }
        for w in workspaces
    ]

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_workspace(body: WorkspaceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workspace = Workspace(
        id=uuid.uuid4(),
        name=body.name,
        owner_id=current_user.id,
        brand_color="#4F46E5"
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
    
    subscription = Subscription(
        id=uuid.uuid4(),
        workspace_id=workspace.id,
        plan="free",
        status="active"
    )
    db.add(subscription)
    
    db.commit()
    db.refresh(workspace)
    
    return {
        "id": str(workspace.id),
        "name": workspace.name,
        "owner_id": str(workspace.owner_id),
        "role": "owner",
        "created_at": str(workspace.created_at)
    }

@router.get("/{workspace_id}", response_model=dict)
def get_workspace(workspace_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workspace = get_current_workspace(workspace_id, current_user, db)
    return {
        "id": str(workspace.id),
        "name": workspace.name,
        "owner_id": str(workspace.owner_id),
        "logo_url": workspace.logo_url,
        "brand_color": workspace.brand_color,
        "created_at": str(workspace.created_at)
    }

@router.put("/{workspace_id}", response_model=dict)
def update_workspace(workspace_id: uuid.UUID, body: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workspace = get_current_workspace(workspace_id, current_user, db)
    check_permission("admin")(workspace_id, current_user, db)
    
    if "name" in body:
        workspace.name = body["name"]
    if "brand_color" in body:
        workspace.brand_color = body["brand_color"]
    if "logo_url" in body:
        workspace.logo_url = body["logo_url"]
        
    db.commit()
    db.refresh(workspace)
    return {
        "id": str(workspace.id),
        "name": workspace.name,
        "brand_color": workspace.brand_color,
        "logo_url": workspace.logo_url
    }

@router.get("/{workspace_id}/members", response_model=List[dict])
def list_workspace_members(workspace_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_current_workspace(workspace_id, current_user, db)
    members = db.query(WorkspaceMember).filter(WorkspaceMember.workspace_id == workspace_id).all()
    results = []
    for m in members:
        u = db.query(User).filter(User.id == m.user_id).first()
        results.append({
            "id": str(m.id),
            "user_id": str(m.user_id),
            "name": u.name if u else "Unknown",
            "email": u.email if u else "Unknown",
            "role": getattr(m.role, 'value', m.role),
            "created_at": str(m.created_at)
        })
    return results

@router.post("/{workspace_id}/members", response_model=dict)
def invite_member(workspace_id: uuid.UUID, body: InviteMemberRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_current_workspace(workspace_id, current_user, db)
    check_permission("admin")(workspace_id, current_user, db)
    
    invited_user = db.query(User).filter(User.email == body.email).first()
    if not invited_user:
        invited_user = User(
            id=uuid.uuid4(),
            name=body.email.split("@")[0],
            email=body.email,
            password_hash="invited_pending_activation",
            role="user"
        )
        db.add(invited_user)
        db.flush()
        
    existing_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == invited_user.id
    ).first()
    if existing_member:
        raise HTTPException(status_code=400, detail="User is already a member of this workspace")
        
    member = WorkspaceMember(
        id=uuid.uuid4(),
        workspace_id=workspace_id,
        user_id=invited_user.id,
        role=body.role or "analyst"
    )
    db.add(member)
    db.commit()
    return {"message": f"Successfully added {body.email} to workspace", "member_id": str(member.id)}

@router.delete("/{workspace_id}/members/{member_id}")
def remove_member(workspace_id: uuid.UUID, member_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_current_workspace(workspace_id, current_user, db)
    check_permission("admin")(workspace_id, current_user, db)
    
    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.id == member_id,
        WorkspaceMember.workspace_id == workspace_id
    ).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
        
    role_str = getattr(member.role, 'value', member.role)
    if role_str == "owner":
        raise HTTPException(status_code=400, detail="Cannot remove workspace owner")
        
    db.delete(member)
    db.commit()
    return {"message": "Member removed"}
