import os
import logging
from pathlib import Path
from typing import Optional
import pandas as pd
from fastapi import HTTPException

logger = logging.getLogger("datapilot.parser")

def parse_excel(file_path: str, ext: Optional[str] = None) -> pd.DataFrame:
    """Parse legacy .xls and modern .xlsx Excel workbooks with engine fallbacks and clear error reporting."""
    path = Path(file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Excel file not found at path: {file_path}")
        
    if os.path.getsize(path) == 0:
        raise HTTPException(status_code=400, detail="Uploaded Excel file is empty (0 bytes).")
        
    extension = (ext or path.suffix).lower()
    
    # Priority engine based on extension
    engines = ['xlrd', 'openpyxl'] if extension == '.xls' else ['openpyxl', 'xlrd']
    
    last_error = None
    for engine in engines:
        try:
            df = pd.read_excel(path, engine=engine, sheet_name=0)
            if df is not None and not df.empty and len(df.columns) > 0:
                logger.info(f"Successfully parsed Excel file '{path.name}' using engine '{engine}'. Rows: {len(df)}, Cols: {len(df.columns)}")
                return df
        except Exception as err:
            last_error = err
            logger.warning(f"Engine '{engine}' failed to read '{path.name}': {str(err)}. Trying fallback...")
            
    # Check if this is an HTML or CSV table incorrectly saved with an .xls extension
    try:
        tables = pd.read_html(path)
        if tables and len(tables) > 0 and not tables[0].empty:
            logger.info(f"Successfully parsed HTML-formatted spreadsheet '{path.name}'.")
            return tables[0]
    except Exception:
        pass

    try:
        df_csv = pd.read_csv(path, sep=None, engine='python', on_bad_lines='skip')
        if not df_csv.empty and len(df_csv.columns) > 1:
            logger.info(f"Successfully recovered text-delimited data from spreadsheet '{path.name}'.")
            return df_csv
    except Exception:
        pass

    error_msg = str(last_error) if last_error else "Unsupported or corrupted Excel format."
    logger.error(f"Failed to parse Excel file '{path.name}': {error_msg}")
    raise HTTPException(
        status_code=400,
        detail=f"Failed to parse Excel file '{path.name}': {error_msg}. Please verify the file is a valid .xls or .xlsx spreadsheet."
    )

def parse_csv(file_path: str) -> pd.DataFrame:
    """Parse CSV text file with multi-encoding and delimiter auto-detection."""
    path = Path(file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"CSV file not found at path: {file_path}")
        
    if os.path.getsize(path) == 0:
        raise HTTPException(status_code=400, detail="Uploaded CSV file is empty (0 bytes).")
        
    encodings_to_try = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252', 'iso-8859-1']
    
    for enc in encodings_to_try:
        try:
            df = pd.read_csv(path, encoding=enc, on_bad_lines='skip')
            if not df.empty and len(df.columns) > 0:
                return df
        except UnicodeDecodeError:
            continue
        except Exception:
            # Try python engine with automatic separator detection
            try:
                df = pd.read_csv(path, encoding=enc, sep=None, engine='python', on_bad_lines='skip')
                if not df.empty and len(df.columns) > 0:
                    return df
            except Exception:
                pass
                
    raise HTTPException(
        status_code=400,
        detail="Could not parse CSV file. Please ensure it contains valid tabular data."
    )

def parse_file(file_path: str, file_type: str = "text/csv") -> pd.DataFrame:
    """Universal parser routing to appropriate engine based on file format."""
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if ext in ['.xls', '.xlsx', '.xlsm', '.xlsb'] or any(k in (file_type or "").lower() for k in ['excel', 'spreadsheet', 'vnd.ms-excel', 'openxmlformats']):
        return parse_excel(file_path, ext=ext)
    else:
        try:
            return parse_csv(file_path)
        except Exception as csv_err:
            # In case an Excel file was uploaded with generic MIME text/csv or wrong extension
            try:
                return parse_excel(file_path)
            except Exception:
                raise csv_err
