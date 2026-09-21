import os
import shutil
from fastapi import UploadFile
from app.config.settings import settings
import uuid

def save_file(file: UploadFile, workspace_id: uuid.UUID) -> str:
    workspace_dir = os.path.join(settings.STORAGE_PATH, str(workspace_id))
    os.makedirs(workspace_dir, exist_ok=True)
    
    from app.services.ingestion.file_validator import validate_file
    meta = validate_file(file)
    safe_filename = meta["safe_filename"]
    
    file_path = os.path.join(workspace_dir, safe_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return f"{workspace_id}/{safe_filename}"

def get_file_path(storage_path: str) -> str:
    return os.path.join(settings.STORAGE_PATH, storage_path)

def delete_file(storage_path: str):
    full_path = get_file_path(storage_path)
    if os.path.exists(full_path):
        os.remove(full_path)
