import os
import io
import shutil
import logging
from typing import Optional, BinaryIO
from fastapi import UploadFile
from app.config.settings import settings
import uuid

logger = logging.getLogger("datapilot.storage")

class StorageService:
    def __init__(self):
        self.provider = settings.STORAGE_PROVIDER.lower()
        self.local_base_path = os.path.abspath(settings.STORAGE_PATH)
        os.makedirs(self.local_base_path, exist_ok=True)
        
        self.s3_client = None
        if self.provider == "s3" and settings.STORAGE_ACCESS_KEY and settings.STORAGE_SECRET_KEY:
            try:
                import boto3
                s3_kwargs = {
                    "aws_access_key_id": settings.STORAGE_ACCESS_KEY,
                    "aws_secret_access_key": settings.STORAGE_SECRET_KEY,
                    "region_name": settings.STORAGE_REGION or "us-east-1"
                }
                if settings.STORAGE_ENDPOINT:
                    s3_kwargs["endpoint_url"] = settings.STORAGE_ENDPOINT
                self.s3_client = boto3.client("s3", **s3_kwargs)
                logger.info("Initialized S3/Object Storage client successfully.")
            except Exception as e:
                logger.warning(f"Could not initialize S3 client: {e}. Falling back to persistent local storage.")
                self.s3_client = None

    def save_file(self, file: UploadFile, workspace_id: uuid.UUID) -> str:
        from app.services.ingestion.file_validator import validate_file
        meta = validate_file(file)
        safe_filename = meta["safe_filename"]
        relative_path = f"{workspace_id}/{safe_filename}"
        
        # Always write to local storage cache/path
        workspace_dir = os.path.join(self.local_base_path, str(workspace_id))
        os.makedirs(workspace_dir, exist_ok=True)
        local_file_path = os.path.join(workspace_dir, safe_filename)
        
        # Reset stream position and write to disk
        file.file.seek(0)
        with open(local_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # If S3 configured, also upload to S3 bucket
        if self.s3_client and settings.STORAGE_BUCKET:
            try:
                file.file.seek(0)
                self.s3_client.upload_fileobj(
                    file.file,
                    settings.STORAGE_BUCKET,
                    relative_path,
                    ExtraArgs={"ContentType": file.content_type or "application/octet-stream"}
                )
            except Exception as e:
                logger.error(f"S3 upload error: {e}. Preserved local copy.")
                
        return relative_path

    def get_file_path(self, storage_path: str) -> str:
        local_path = os.path.join(self.local_base_path, storage_path)
        
        # If local file does not exist but S3 client is configured, download it to local cache
        if not os.path.exists(local_path) and self.s3_client and settings.STORAGE_BUCKET:
            try:
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                self.s3_client.download_file(settings.STORAGE_BUCKET, storage_path, local_path)
            except Exception as e:
                logger.error(f"Failed to fetch file from S3 {storage_path}: {e}")
                
        return local_path

    def delete_file(self, storage_path: str):
        full_path = os.path.join(self.local_base_path, storage_path)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
            except Exception as e:
                logger.warning(f"Error removing local file {full_path}: {e}")
                
        if self.s3_client and settings.STORAGE_BUCKET:
            try:
                self.s3_client.delete_object(Bucket=settings.STORAGE_BUCKET, Key=storage_path)
            except Exception as e:
                logger.warning(f"Error deleting S3 object {storage_path}: {e}")

_storage = StorageService()

def save_file(file: UploadFile, workspace_id: uuid.UUID) -> str:
    return _storage.save_file(file, workspace_id)

def get_file_path(storage_path: str) -> str:
    return _storage.get_file_path(storage_path)

def delete_file(storage_path: str):
    return _storage.delete_file(storage_path)
