import pandas as pd
from typing import Dict, Any

def calculate_quality_score(df: pd.DataFrame, profile: Dict[str, Any]) -> Dict[str, Any]:
    if df.empty:
        return {"overall": 0, "completeness": 0, "uniqueness": 0, "validity": 0, "consistency": 0}
        
    total_rows = len(df)
    
    # 1. Completeness (30%)
    missing_pcts = [col["missing_pct"] for col in profile.get("columns", {}).values()]
    avg_missing = sum(missing_pcts) / len(missing_pcts) if missing_pcts else 0
    completeness = max(0, 100 - avg_missing)
    
    # 2. Uniqueness (20%)
    dup_ratio = profile["overall"]["duplicate_count"] / total_rows if total_rows else 0
    uniqueness = max(0, (1 - dup_ratio) * 100)
    
    # 3. Validity (25%) - simplified approximation based on missing values after coercion
    validity = 90.0 # Placeholder for detailed type coercion tracking
    
    # 4. Consistency (25%) - check outliers in numeric columns
    outlier_score = 100.0
    numeric_cols = [c for c, p in profile.get("columns", {}).items() if p.get("type") == "numeric"]
    if numeric_cols:
        total_outliers = 0
        for col in numeric_cols:
            q25 = profile["columns"][col].get("q25", 0)
            q75 = profile["columns"][col].get("q75", 0)
            iqr = q75 - q25
            if iqr > 0:
                outliers = ((df[col] < (q25 - 1.5 * iqr)) | (df[col] > (q75 + 1.5 * iqr))).sum()
                total_outliers += int(outliers)
        outlier_ratio = total_outliers / (total_rows * len(numeric_cols))
        outlier_score = max(0, (1 - outlier_ratio) * 100)
    consistency = outlier_score
    
    overall = (completeness * 0.3) + (uniqueness * 0.2) + (validity * 0.25) + (consistency * 0.25)
    
    return {
        "overall": round(overall, 2),
        "completeness": round(completeness, 2),
        "uniqueness": round(uniqueness, 2),
        "validity": round(validity, 2),
        "consistency": round(consistency, 2)
    }
