import pandas as pd
import numpy as np
from typing import Any

def clean_dataset(df: pd.DataFrame) -> dict[str, Any]:
    changes_log = []
    cleaned = df.copy()
    
    # 1. Normalize column names
    original_cols = list(cleaned.columns)
    cleaned.columns = [str(c).strip().lower().replace(' ', '_').replace('-', '_') for c in cleaned.columns]
    renamed = sum(1 for o, n in zip(original_cols, cleaned.columns) if o != n)
    if renamed > 0:
        changes_log.append({"action": "normalize_columns", "details": f"Normalized {renamed} column names", "affected_count": renamed})
    
    # 2. Trim whitespace
    str_cols = cleaned.select_dtypes(include=['object']).columns
    trimmed = 0
    for col in str_cols:
        mask = cleaned[col].astype(str).str.strip() != cleaned[col].astype(str)
        trimmed += mask.sum()
        cleaned[col] = cleaned[col].astype(str).str.strip()
    if trimmed > 0:
        changes_log.append({"action": "trim_whitespace", "details": f"Trimmed whitespace in {trimmed} cells", "affected_count": int(trimmed)})
    
    # 3. Standardize null representations
    null_values = ['', 'NA', 'N/A', 'n/a', 'null', 'none', 'None', 'NULL', 'nan', 'NaN', '-', '--']
    null_count = 0
    for col in str_cols:
        mask = cleaned[col].isin(null_values)
        null_count += mask.sum()
        cleaned.loc[mask, col] = np.nan
    if null_count > 0:
        changes_log.append({"action": "standardize_nulls", "details": f"Standardized {null_count} null representations", "affected_count": int(null_count)})
    
    # 4. Remove exact duplicates
    dup_count = cleaned.duplicated().sum()
    if dup_count > 0:
        cleaned = cleaned.drop_duplicates()
        changes_log.append({"action": "remove_duplicates", "details": f"Removed {dup_count} duplicate rows", "affected_count": int(dup_count)})
    
    # 5. Convert numeric strings
    converted = 0
    for col in cleaned.select_dtypes(include=['object']).columns:
        try:
            numeric_vals = pd.to_numeric(cleaned[col], errors='coerce')
            valid_ratio = numeric_vals.notna().sum() / max(cleaned[col].notna().sum(), 1)
            if valid_ratio > 0.8:
                cleaned[col] = numeric_vals
                converted += 1
        except Exception:
            pass
    if converted > 0:
        changes_log.append({"action": "convert_numeric", "details": f"Converted {converted} columns to numeric", "affected_count": converted})
    
    # 6. Parse dates
    date_converted = 0
    for col in cleaned.select_dtypes(include=['object']).columns:
        try:
            parsed = pd.to_datetime(cleaned[col], errors='coerce')
            valid_ratio = parsed.notna().sum() / max(cleaned[col].notna().sum(), 1)
            if valid_ratio > 0.8:
                cleaned[col] = parsed
                date_converted += 1
        except Exception:
            pass
    if date_converted > 0:
        changes_log.append({"action": "parse_dates", "details": f"Parsed {date_converted} date columns", "affected_count": date_converted})
    
    return {"cleaned_df": cleaned, "changes_log": changes_log, "rows_before": len(df), "rows_after": len(cleaned)}
