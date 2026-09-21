import pytest
import pandas as pd
import numpy as np
from app.services.profiling.profiler import profile_dataframe
from app.services.profiling.type_detector import detect_dataset_type

def test_profile_dataframe_computes_exact_statistics():
    df = pd.DataFrame({
        "revenue": [100.0, 200.0, 300.0, 400.0, 500.0],
        "quantity": [1, 2, 3, 4, 5],
        "category": ["A", "B", "A", "B", "C"],
        "order_date": pd.date_range("2024-01-01", periods=5)
    })
    
    profile = profile_dataframe(df)
    assert profile["overall"]["row_count"] == 5
    assert profile["overall"]["column_count"] == 4
    
    # Check numeric stats
    rev_stats = profile["columns"]["revenue"]
    assert rev_stats["min"] == 100.0
    assert rev_stats["max"] == 500.0
    assert rev_stats["mean"] == 300.0
    assert rev_stats["median"] == 300.0

def test_detect_dataset_type_sales():
    df = pd.DataFrame({
        "order_id": [1, 2, 3],
        "product_name": ["Widget", "Gadget", "Gizmo"],
        "unit_price": [10.5, 20.0, 15.0],
        "quantity": [2, 1, 4],
        "revenue": [21.0, 20.0, 60.0]
    })
    res = detect_dataset_type(df)
    assert res["dataset_type"] == "Sales"
    assert res["confidence"] > 0.5

def test_detect_dataset_type_marketing():
    df = pd.DataFrame({
        "campaign_name": ["Summer Launch", "Retargeting"],
        "impressions": [10000, 25000],
        "clicks": [450, 1200],
        "spend": [350.0, 800.0],
        "conversions": [25, 70]
    })
    res = detect_dataset_type(df)
    assert res["dataset_type"] == "Marketing"

