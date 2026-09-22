import os
import io
import shutil
import logging
from typing import Optional, BinaryIO
from typing import Optional, BinaryIO, Dict, Any
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
        if (self.provider == "s3" or settings.STORAGE_BUCKET) and settings.STORAGE_ACCESS_KEY and settings.STORAGE_SECRET_KEY:
            try:
                import boto3
                from botocore.config import Config
                s3_kwargs = {
                    "aws_access_key_id": settings.STORAGE_ACCESS_KEY,
                    "aws_secret_access_key": settings.STORAGE_SECRET_KEY,
                    "region_name": settings.STORAGE_REGION or "us-east-1"
                    "region_name": settings.STORAGE_REGION or "us-east-1",
                    "config": Config(signature_version='s3v4')
                }
                if settings.STORAGE_ENDPOINT:
                    s3_kwargs["endpoint_url"] = settings.STORAGE_ENDPOINT
                self.s3_client = boto3.client("s3", **s3_kwargs)
                logger.info("Initialized S3/Object Storage client successfully.")
                logger.info(f"Initialized S3/Supabase Storage client successfully (Bucket: {settings.STORAGE_BUCKET}).")
            except Exception as e:
                logger.warning(f"Could not initialize S3 client: {e}. Falling back to persistent local storage.")
                self.s3_client = None

    def generate_presigned_upload_url(
        self,
        storage_path: str,
        content_type: str = "application/octet-stream",
        expires_in: int = 600
    ) -> Dict[str, Any]:
        """
        Generate a short-lived presigned PUT URL for direct browser-to-storage upload.
        Bypasses Vercel Serverless 4.5MB request limit completely.
        """
        if self.s3_client and settings.STORAGE_BUCKET:
            try:
                url = self.s3_client.generate_presigned_url(
                    ClientMethod='put_object',
                    Params={
                        'Bucket': settings.STORAGE_BUCKET,
                        'Key': storage_path,
                        'ContentType': content_type
                    },
                    ExpiresIn=expires_in
                )
                return {
                    "upload_url": url,
                    "method": "PUT",
                    "storage_path": storage_path,
                    "headers": {
                        "Content-Type": content_type
                    },
                    "expires_in": expires_in,
                    "is_direct_s3": True
                }
            except Exception as e:
                logger.error(f"Failed to generate S3 presigned upload URL: {e}")
                
        # Fallback for local development / testing without live S3 credentials
        local_endpoint = f"/api/v1/datasets/local-direct-upload?storage_path={storage_path}"
        return {
            "upload_url": local_endpoint,
            "method": "PUT",
            "storage_path": storage_path,
            "headers": {
                "Content-Type": content_type
            },
            "expires_in": expires_in,
            "is_direct_s3": False
        }

    def generate_presigned_download_url(
        self,
        storage_path: str,
        expires_in: int = 600,
        filename: Optional[str] = None
    ) -> Optional[str]:
        """Generate a short-lived presigned GET URL for authenticated downloads."""
        if self.s3_client and settings.STORAGE_BUCKET:
            try:
                params = {
                    'Bucket': settings.STORAGE_BUCKET,
                    'Key': storage_path
                }
                if filename:
                    safe_fname = filename.replace('"', '_')
                    params['ResponseContentDisposition'] = f'attachment; filename="{safe_fname}"'
                url = self.s3_client.generate_presigned_url(
                    ClientMethod='get_object',
                    Params=params,
                    ExpiresIn=expires_in
                )
                return url
            except Exception as e:
                logger.error(f"Failed to generate S3 presigned download URL: {e}")
        return None

    def save_file_bytes(self, data_bytes: bytes, storage_path: str, content_type: str = "application/octet-stream") -> str:
        """Save raw bytes to local cache and S3 bucket."""
        local_file_path = os.path.join(self.local_base_path, storage_path)
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        with open(local_file_path, "wb") as f:
            f.write(data_bytes)
            
        if self.s3_client and settings.STORAGE_BUCKET:
            try:
                self.s3_client.put_object(
                    Bucket=settings.STORAGE_BUCKET,
                    Key=storage_path,
                    Body=data_bytes,
                    ContentType=content_type
                )
            except Exception as e:
                logger.error(f"Failed to sync bytes to S3: {e}")
        return storage_path

    def upload_file_from_path(self, local_path: str, storage_path: str, content_type: str = "application/octet-stream"):
        """Sync an existing local file to S3 bucket."""
        if self.s3_client and settings.STORAGE_BUCKET and os.path.exists(local_path):
            try:
                with open(local_path, "rb") as f:
                    self.s3_client.upload_fileobj(
                        f,
                        settings.STORAGE_BUCKET,
                        storage_path,
                        ExtraArgs={"ContentType": content_type}
                    )
            except Exception as e:
                logger.error(f"Failed to upload local file {local_path} to S3 {storage_path}: {e}")

    def check_file_exists(self, storage_path: str) -> bool:
        """Check if file exists on local disk or S3 bucket."""
        local_path = os.path.join(self.local_base_path, storage_path)
        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            return True
            
        if self.s3_client and settings.STORAGE_BUCKET:
            try:
                self.s3_client.head_object(Bucket=settings.STORAGE_BUCKET, Key=storage_path)
                return True
            except Exception:
                return False
        return False

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

def get_storage_service() -> StorageService:
    return _storage

def save_file(file: UploadFile, workspace_id: uuid.UUID) -> str:
    return _storage.save_file(file, workspace_id)

def get_file_path(storage_path: str) -> str:
    return _storage.get_file_path(storage_path)

def delete_file(storage_path: str):
    return _storage.delete_file(storage_path)
