import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional

def detect_anomalies(df: pd.DataFrame, numeric_columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Detect statistical anomalies across numeric columns using IQR and Z-Score methods."""
    anomalies = []
    
    if df.empty:
        return anomalies
        
    if not numeric_columns:
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        
    for col in numeric_columns:
        if col not in df.columns:
            continue
            
        series = pd.to_numeric(df[col], errors='coerce').dropna()
        if len(series) < 5:
            continue
            
        mean_val = float(series.mean())
        std_val = float(series.std()) if len(series) > 1 else 0.0
        
        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        # Outlier mask
        outlier_mask = (series < lower_bound) | (series > upper_bound)
        outliers = series[outlier_mask]
        
        if not outliers.empty:
            distances = np.maximum(0, outliers - upper_bound) + np.maximum(0, lower_bound - outliers)
            sorted_outliers = outliers.loc[distances.sort_values(ascending=False).index]
            
            for idx, val in sorted_outliers.head(10).items():
                z_score = abs(float(val) - mean_val) / (std_val + 1e-6)
                
                # Conservative business-friendly statistical explanation
                if val > upper_bound:
                    explanation = f"Statistical outlier detected: value ({val:,.2f}) significantly exceeds typical upper range ({upper_bound:,.2f})."
                else:
                    explanation = f"Statistical outlier detected: value ({val:,.2f}) is significantly below typical lower range ({lower_bound:,.2f})."
                    
                anomalies.append({
                    "column": col,
                    "column_name": col,
                    "row": str(idx),
                    "row_reference": f"Row #{idx + 1 if isinstance(idx, int) else idx}",
                    "value": str(val),
                    "value_str": str(val),
                    "score": round(float(z_score), 2),
                    "expected_range": f"{lower_bound:,.2f} – {upper_bound:,.2f}",
                    "method": "IQR & Z-Score",
                    "explanation": explanation
                })
                
    return anomalies
