import os
from pathlib import Path
import pandas as pd
from fastapi import HTTPException

def parse_file(file_path: str, file_type: str = "text/csv") -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Dataset file not found on server")
        
    if os.path.getsize(path) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty (0 bytes)")
        
    ext = path.suffix.lower()
    
    # 1. Excel parsing
    if ext in ['.xlsx', '.xls'] or 'excel' in file_type or 'spreadsheet' in file_type:
        try:
            df = pd.read_excel(path)
            if df.empty or len(df.columns) == 0:
                raise HTTPException(status_code=400, detail="The Excel file contains no data or columns.")
            return df
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse Excel file: {str(e)}")

    # 2. CSV parsing with multi-encoding fallback
    encodings_to_try = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252', 'iso-8859-1']
    
    # Try chardet if available
    try:
        import chardet
        with open(path, 'rb') as f:
            sample = f.read(50000)
            detected = chardet.detect(sample)
            if detected and detected.get('encoding'):
                encodings_to_try.insert(0, detected['encoding'])
    except ImportError:
        pass
        
    for enc in encodings_to_try:
        try:
            df = pd.read_csv(path, encoding=enc, on_bad_lines='skip')
            if df.empty and len(df.columns) == 0:
                raise HTTPException(status_code=400, detail="The CSV file contains no tabular data.")
            return df
        except UnicodeDecodeError:
            continue
        except HTTPException:
            raise
        except Exception as e:
            # If standard delimiter failed, try auto-sep
            try:
                df = pd.read_csv(path, encoding=enc, sep=None, engine='python', on_bad_lines='skip')
                if not df.empty:
                    return df
            except Exception:
                pass
                
    raise HTTPException(status_code=400, detail="Could not parse CSV file. Please ensure it is a valid text/CSV format.")
