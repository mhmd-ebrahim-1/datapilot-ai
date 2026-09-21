import pandas as pd
import numpy as np
from typing import Dict, Any

def profile_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    profile = {
        "overall": {
            "row_count": len(df),
            "column_count": len(df.columns),
            "duplicate_count": int(df.duplicated().sum()),
            "memory_usage_mb": float(df.memory_usage(deep=True).sum() / (1024 * 1024))
        },
        "columns": {},
        "correlations": {}
    }
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr().to_dict()
        profile["correlations"] = {k: {k2: float(v2) if not pd.isna(v2) else 0.0 for k2, v2 in v.items()} for k, v in corr_matrix.items()}
        
    for col in df.columns:
        series = df[col]
        null_count = int(series.isnull().sum())
        total = len(series)
        unique_count = int(series.nunique(dropna=True))
        
        col_prof = {
            "missing_count": null_count,
            "missing_pct": round(null_count / total * 100, 2) if total else 0,
            "unique_count": unique_count,
            "unique_pct": round(unique_count / total * 100, 2) if total else 0,
        }
        
        if pd.api.types.is_numeric_dtype(series):
            col_prof["type"] = "numeric"
            s_clean = series.dropna()
            if len(s_clean):
                col_prof.update({
                    "min": float(s_clean.min()),
                    "max": float(s_clean.max()),
                    "mean": float(s_clean.mean()),
                    "median": float(s_clean.median()),
                    "std": float(s_clean.std()),
                    "q25": float(s_clean.quantile(0.25)),
                    "q75": float(s_clean.quantile(0.75)),
                    "skew": float(s_clean.skew())
                })
        elif pd.api.types.is_datetime64_any_dtype(series):
            col_prof["type"] = "datetime"
            s_clean = series.dropna()
            if len(s_clean):
                col_prof.update({
                    "min_date": s_clean.min().isoformat(),
                    "max_date": s_clean.max().isoformat(),
                    "range_days": (s_clean.max() - s_clean.min()).days
                })
        else:
            col_prof["type"] = "categorical"
            s_clean = series.dropna()
            if len(s_clean):
                top_vals = s_clean.value_counts().head(10)
                col_prof["top_values"] = top_vals.to_dict()
                col_prof["cardinality"] = "high" if unique_count > 50 else "low"
                
        profile["columns"][str(col)] = col_prof
        
    return profile
