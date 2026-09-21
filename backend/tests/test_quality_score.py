import pytest
import pandas as pd
import numpy as np
from app.services.profiling.profiler import profile_dataframe
from app.services.profiling.quality_scorer import calculate_quality_score

def test_quality_scorer_clean_data():
    df = pd.DataFrame({
        "a": [1, 2, 3, 4, 5],
        "b": [10.0, 20.0, 30.0, 40.0, 50.0],
        "c": ["X", "Y", "Z", "W", "V"]
    })
    profile = profile_dataframe(df)
    score = calculate_quality_score(df, profile)
    
    assert "overall" in score
    assert score["overall"] >= 90.0
    assert score["completeness"] == 100.0
    assert score["uniqueness"] == 100.0

def test_quality_scorer_messy_data():
    df = pd.DataFrame({
        "a": [1, 2, 2, np.nan, np.nan],
        "b": [10.0, 20.0, 20.0, np.nan, 50000.0] # Has missing and extreme outlier
    })
    profile = profile_dataframe(df)
    score = calculate_quality_score(df, profile)
    
    assert score["completeness"] < 100.0
    assert score["overall"] < 95.0

