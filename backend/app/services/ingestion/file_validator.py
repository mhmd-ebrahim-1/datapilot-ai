import os
import uuid
import re
from fastapi import UploadFile, HTTPException
from app.config.settings import settings

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
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension '{ext}'. Only CSV (.csv) and Excel (.xlsx, .xls) files are supported."
        )
        
    content_type = file.content_type or 'text/csv'
    if content_type not in allowed_mimes:
        # If extension is valid csv/xlsx, allow it anyway
        if ext.lower() not in allowed_extensions:
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
