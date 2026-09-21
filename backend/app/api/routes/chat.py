import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.config.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.dataset import Dataset
from app.models.chat import ChatSession, ChatMessage
from app.services.ingestion.parser import parse_file
from app.services.ingestion.storage import get_file_path
from app.services.ai.chat_engine import ChatEngine
from app.services.ai.mock_provider import MockAIProvider
from app.services.ai.gemini_provider import GeminiProvider
from app.config.settings import settings

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])

@router.post("", response_model=dict)
@router.post("/", response_model=dict, include_in_schema=False)
async def send_message(body: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    dataset_id_raw = body.get("dataset_id")
    message = body.get("message", "").strip()
    session_id_raw = body.get("session_id")
    
    if not dataset_id_raw or not message:
        raise HTTPException(status_code=400, detail="dataset_id and message are required")
        
    try:
        dataset_uuid = uuid.UUID(str(dataset_id_raw)) if isinstance(dataset_id_raw, str) else dataset_id_raw
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid dataset_id format")
        
    dataset = db.query(Dataset).filter(Dataset.id == dataset_uuid).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    if not session_id_raw:
        session = ChatSession(
            id=uuid.uuid4(),
            workspace_id=dataset.workspace_id,
            dataset_id=dataset.id,
            user_id=current_user.id
        )
        db.add(session)
        db.flush()
        session_id = session.id
    else:
        try:
            session_uuid = uuid.UUID(str(session_id_raw)) if isinstance(session_id_raw, str) else session_id_raw
        except ValueError:
            session_uuid = uuid.uuid4()
            
        session = db.query(ChatSession).filter(ChatSession.id == session_uuid).first()
        if not session:
            session = ChatSession(
                id=session_uuid,
                workspace_id=dataset.workspace_id,
                dataset_id=dataset.id,
                user_id=current_user.id
            )
            db.add(session)
            db.flush()
        session_id = session.id
        
    user_msg = ChatMessage(
        id=uuid.uuid4(),
        session_id=session_id,
        role="user",
        content=message
    )
    db.add(user_msg)
    
    # 1. Deterministic calculation using Pandas & ChatEngine
    try:
        file_path = get_file_path(dataset.storage_path)
        df = parse_file(file_path, dataset.file_type)
        provider = MockAIProvider()
        
        # Select AI Provider
        if settings.AI_PROVIDER.lower() == "gemini" and settings.AI_API_KEY:
            try:
                provider = GeminiProvider()
            except Exception:
                provider = MockAIProvider()
        else:
            provider = MockAIProvider()
            
        engine = ChatEngine(provider)
        result = await engine.answer(
            message,
            df,
            {"name": dataset.name, "dataset_type": dataset.dataset_type or "General"}
        )
        answer = result.get("answer", "I computed the metrics for this dataset based on your request.")
        context = result.get("context", {})
    except Exception as e:
        answer = "The uploaded dataset does not contain sufficient column metadata to compute an answer for this question."
        context = {}
        
    assistant_msg = ChatMessage(
        id=uuid.uuid4(),
        session_id=session_id,
        role="assistant",
        content=answer,
        metadata_json=context
    )
    db.add(assistant_msg)
    db.commit()
    
    return {
        "message": answer,
        "session_id": str(session_id),
        "context": context
    }

@router.get("/sessions", response_model=list)
async def list_sessions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sessions = db.query(ChatSession).filter(ChatSession.user_id == current_user.id).order_by(ChatSession.created_at.desc()).all()
    return [{"id": str(s.id), "dataset_id": str(s.dataset_id), "created_at": str(s.created_at)} for s in sessions]

@router.get("/sessions/{session_id}", response_model=list)
async def get_session(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).all()
    return [{"id": str(m.id), "role": m.role, "content": m.content, "metadata": m.metadata_json, "created_at": str(m.created_at)} for m in messages]
