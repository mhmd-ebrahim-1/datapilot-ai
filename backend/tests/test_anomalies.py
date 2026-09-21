import pytest
import pandas as pd
from app.services.anomaly_detection.detector import detect_anomalies

def test_anomaly_detection_with_outlier():
    # Normal data with one extreme outlier
    values = [10.0, 11.0, 10.5, 9.8, 10.2, 10.8, 11.2, 10.1, 9.9, 500.0]
    df = pd.DataFrame({"revenue": values})
    
    anomalies = detect_anomalies(df)
    assert len(anomalies) > 0
    outlier = anomalies[0]
    assert outlier["column"] == "revenue"
    assert "500" in str(outlier["value"])
    assert outlier["score"] > 2.0
    assert "explanation" in outlier

