import os
import uuid
import re
from typing import Optional, Dict, Any
from fastapi import UploadFile, HTTPException
from app.config.settings import settings

ALLOWED_EXTENSIONS = ['.csv', '.xlsx', '.xls']
ALLOWED_MIMES = [
    'text/csv',
    'text/plain',
    'application/csv',
    'application/x-csv',
    'text/comma-separated-values',
    'text/x-comma-separated-values',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel',
    'application/octet-stream'
]

def validate_upload_metadata(filename: str, file_size: int, content_type: Optional[str] = None) -> Dict[str, Any]:
    """Validate dataset filename, extension, and declared size before granting presigned upload URL."""
    if not filename or not filename.strip():
        raise HTTPException(
            status_code=400,
            detail="Filename cannot be empty."
        )
        
    filename = filename.strip()
    _, ext = os.path.splitext(filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension '{ext}'. Only CSV (.csv) and Excel (.xlsx, .xls) files are supported."
        )
        
    if file_size is None or file_size <= 0:
        raise HTTPException(
            status_code=400,
            detail="File size must be greater than 0 bytes."
        )
        
    max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File size ({file_size / (1024*1024):.1f}MB) exceeds maximum allowed limit of {settings.MAX_FILE_SIZE_MB}MB."
        )
        
    # Resolve standard content type based on extension if generic
    resolved_mime = content_type or 'application/octet-stream'
    if ext.lower() == '.csv':
        resolved_mime = 'text/csv'
    elif ext.lower() == '.xlsx':
        resolved_mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif ext.lower() == '.xls':
        resolved_mime = 'application/vnd.ms-excel'
        
    safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', filename)
    unique_name = f"{uuid.uuid4().hex[:12]}_{safe_name}"
    
    return {
        "original_filename": filename,
        "safe_filename": unique_name,
        "valid": True,
        "size": file_size,
        "file_size": file_size,
        "mime_type": resolved_mime,
        "content_type": resolved_mime
    }

def validate_file(file: UploadFile) -> dict:
    """Validate uploaded dataset file extension, MIME type, and size."""
    allowed_extensions = ['.csv', '.xlsx', '.xls']
    allowed_mimes = [
        'text/csv',
        'text/plain',
        'application/csv',
        'application/x-csv',
        'text/comma-separated-values',
        'text/x-comma-separated-values',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
        'application/octet-stream'
    ]
    
    filename = file.filename or "uploaded_file.csv"
    _, ext = os.path.splitext(filename)
    if ext.lower() not in allowed_extensions:
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension '{ext}'. Only CSV (.csv) and Excel (.xlsx, .xls) files are supported."
        )
        
    content_type = file.content_type or 'text/csv'
    if content_type not in allowed_mimes:
    if content_type not in ALLOWED_MIMES:
        # If extension is valid csv/xlsx, allow it anyway
        if ext.lower() not in allowed_extensions:
        if ext.lower() not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid MIME type: '{content_type}'. Please upload a standard CSV or Excel file."
            )
        
    try:
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
    except Exception:
        file_size = 0
        
    max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB."
        )
        
    safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', filename)
    unique_name = f"{uuid.uuid4().hex[:12]}_{safe_name}"
    
    return {
        "original_filename": filename,
        "safe_filename": unique_name,
        "valid": True,
        "size": file_size,
        "file_size": file_size,
        "mime_type": content_type,
        "content_type": content_type
    }
