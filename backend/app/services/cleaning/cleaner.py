import re
import pandas as pd
import numpy as np
from typing import Any, Dict, List

def clean_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """Execute rigorous multi-stage cleaning pipeline preserving original semantics."""
    changes_log: List[Dict[str, Any]] = []
    cleaned = df.copy()
    rows_before = len(cleaned)
    
    # 1. Normalize column names (lowercase, alphanumeric + underscore)
    original_cols = list(cleaned.columns)
    cleaned.columns = [
        re.sub(r'[^a-zA-Z0-9_]', '_', str(c).strip().lower()).strip('_') 
        for c in cleaned.columns
    ]
    renamed = sum(1 for o, n in zip(original_cols, cleaned.columns) if str(o) != str(n))
    if renamed > 0:
        changes_log.append({
            "action": "normalize_columns",
            "details": f"Normalized {renamed} column names for consistent indexing",
            "affected_count": renamed
        })
    
    # 2. Trim whitespace on text columns
    str_cols = cleaned.select_dtypes(include=['object']).columns.tolist()
    trimmed_count = 0
    for col in str_cols:
        try:
            s_str = cleaned[col].astype(str)
            s_trimmed = s_str.str.strip()
            diff_count = int((s_str != s_trimmed).sum())
            if diff_count > 0:
                trimmed_count += diff_count
                cleaned[col] = s_trimmed
        except Exception:
            pass
            
    if trimmed_count > 0:
        changes_log.append({
            "action": "trim_whitespace",
            "details": f"Trimmed whitespace in {trimmed_count} text cells",
            "affected_count": trimmed_count
        })
    
    # 3. Standardize missing/null representations
    null_literals = {
        '', ' ', 'na', 'n/a', 'n.a.', 'null', 'none', 'nil', 
        'nan', 'nan%', '-', '--', '---', '?', '.', 'undefined', '#n/a', '#value!'
    }
    repaired_nulls = 0
    for col in cleaned.select_dtypes(include=['object']).columns:
        try:
            mask = cleaned[col].astype(str).str.strip().str.lower().isin(null_literals)
            count = int(mask.sum())
            if count > 0:
                repaired_nulls += count
                cleaned.loc[mask, col] = np.nan
        except Exception:
            pass
            
    if repaired_nulls > 0:
        changes_log.append({
            "action": "standardize_nulls",
            "details": f"Standardized {repaired_nulls} missing/null placeholders to standard NaN",
            "affected_count": repaired_nulls
        })
    
    # 4. Remove exact duplicate rows
    dup_count = int(cleaned.duplicated().sum())
    if dup_count > 0:
        cleaned = cleaned.drop_duplicates().reset_index(drop=True)
        changes_log.append({
            "action": "remove_duplicates",
            "details": f"Removed {dup_count} exact duplicate rows",
            "affected_count": dup_count
        })
    
    # 5. Currency & Percentage numeric clean-up
    currency_converted = 0
    for col in cleaned.select_dtypes(include=['object']).columns:
        try:
            sample = cleaned[col].dropna().astype(str)
            if sample.empty:
                continue
            # Detect currency symbols or % in sample
            if sample.str.contains(r'[$€£¥%]', regex=True).any() or sample.str.contains(r'^\(.*\)$', regex=True).any():
                cleaned_num_str = (
                    sample.str.replace('$', '', regex=False)
                          .str.replace('€', '', regex=False)
                          .str.replace('£', '', regex=False)
                          .str.replace('¥', '', regex=False)
                          .str.replace('%', '', regex=False)
                          .str.replace(',', '', regex=False)
                          .str.strip()
                )
                # Handle accounting negative (123.45) -> -123.45
                paren_mask = cleaned_num_str.str.startswith('(') & cleaned_num_str.str.endswith(')')
                cleaned_num_str = cleaned_num_str.str.replace('(', '-', regex=False).str.replace(')', '', regex=False)
                
                parsed_num = pd.to_numeric(cleaned_num_str, errors='coerce')
                if parsed_num.notna().sum() / len(sample) > 0.7:
                    cleaned[col] = parsed_num
                    currency_converted += 1
        except Exception:
            pass
            
    if currency_converted > 0:
        changes_log.append({
            "action": "parse_currency_percentage",
            "details": f"Parsed {currency_converted} formatted currency/percentage columns into numeric floats",
            "affected_count": currency_converted
        })
    
    # 6. General numeric string conversion
    num_converted = 0
    for col in cleaned.select_dtypes(include=['object']).columns:
        try:
            cleaned_str = cleaned[col].dropna().astype(str).str.replace(',', '', regex=False)
            numeric_vals = pd.to_numeric(cleaned_str, errors='coerce')
            valid_ratio = numeric_vals.notna().sum() / max(cleaned[col].notna().sum(), 1)
            if valid_ratio > 0.85:
                cleaned[col] = numeric_vals
                num_converted += 1
        except Exception:
            pass
            
    if num_converted > 0:
        changes_log.append({
            "action": "convert_numeric",
            "details": f"Converted {num_converted} text columns into numeric types",
            "affected_count": num_converted
        })
    
    # 7. Date parsing
    date_converted = 0
    for col in cleaned.select_dtypes(include=['object']).columns:
        try:
            s_clean = cleaned[col].dropna().astype(str)
            if s_clean.empty:
                continue
            # Fast check if likely a date column (contains dashes or slashes or date keywords)
            if any(k in col.lower() for k in ['date', 'time', 'day', 'month', 'year', 'period']) or s_clean.str.contains(r'[-/]', regex=True).mean() > 0.6:
                parsed = pd.to_datetime(cleaned[col], errors='coerce')
                valid_ratio = parsed.notna().sum() / max(cleaned[col].notna().sum(), 1)
                if valid_ratio > 0.8:
                    cleaned[col] = parsed
                    date_converted += 1
        except Exception:
            pass
            
    if date_converted > 0:
        changes_log.append({
            "action": "parse_dates",
            "details": f"Parsed {date_converted} date columns into ISO temporal timestamps",
            "affected_count": date_converted
        })
    
    rows_after = len(cleaned)
    
    cleaning_metrics = {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "rows_removed": rows_before - rows_after,
        "missing_values_repaired": repaired_nulls,
        "duplicates_removed": dup_count,
        "numeric_conversions": num_converted + currency_converted,
        "date_conversions": date_converted,
        "columns_normalized": renamed
    }
    
    return {
        "cleaned_df": cleaned,
        "changes_log": changes_log,
        "cleaning_metrics": cleaning_metrics,
        "rows_before": rows_before,
        "rows_after": rows_after
    }
