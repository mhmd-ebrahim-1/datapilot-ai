import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember
from app.models.subscription import Subscription
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.api.dependencies import get_current_user
from app.services.email.email_service import EmailService

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    normalized_email = request.email.lower().strip()
    if db.query(User).filter(User.email == normalized_email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
        
    user = User(
        id=uuid.uuid4(),
        name=request.name.strip(),
        email=normalized_email,
        password_hash=hash_password(request.password)
    )
    db.add(user)
    db.flush()
    
    workspace = Workspace(
        id=uuid.uuid4(),
        name=f"{user.name}'s Workspace",
        owner_id=user.id,
        brand_color="#4F46E5"
    )
    db.add(workspace)
    db.flush()
    
    member = WorkspaceMember(
        id=uuid.uuid4(),
        workspace_id=workspace.id,
        user_id=user.id,
        role='owner'
    )
    db.add(member)
    
    sub = Subscription(
        id=uuid.uuid4(),
        workspace_id=workspace.id,
        plan='free',
        status='active'
    )
    db.add(sub)
    
    db.commit()
    db.refresh(user)
    
    # Send welcome email
    EmailService.send_welcome_email(user.email, user.name)
    
    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token({"sub": str(user.id)})
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    normalized_email = request.email.lower().strip()
    user = db.query(User).filter(User.email == normalized_email).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token({"sub": str(user.id)})
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(body: dict, db: Session = Depends(get_db)):
    refresh = body.get("refresh_token")
    if not refresh:
        raise HTTPException(status_code=400, detail="refresh_token is required")
        
    payload = decode_token(refresh)
    if not payload or not payload.get("sub"):
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    user_id = payload.get("sub")
    try:
        user_uuid = uuid.UUID(str(user_id)) if isinstance(user_id, str) else user_id
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user ID in token")
        
    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
        
    new_access = create_access_token({"sub": str(user.id)})
    new_refresh = create_refresh_token({"sub": str(user.id)})
    return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Successfully logged out"}

@router.post("/password-reset")
def request_password_reset(body: dict, db: Session = Depends(get_db)):
    email = body.get("email")
    if email:
        user = db.query(User).filter(User.email == email.lower().strip()).first()
        if user:
            reset_token = uuid.uuid4().hex
            EmailService.send_password_reset_email(user.email, reset_token)
    return {"message": "If this email is registered, password reset instructions have been sent."}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_me(body: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if "name" in body and body["name"]:
        current_user.name = body["name"].strip()
    if "avatar_url" in body:
        current_user.avatar_url = body["avatar_url"]
    db.commit()
    db.refresh(current_user)
    return current_user
