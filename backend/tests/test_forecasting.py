import pytest
import pandas as pd
from app.services.forecasting.forecast_engine import generate_forecast

def test_forecasting_valid_series():
    dates = pd.date_range("2024-01-01", periods=20)
    df = pd.DataFrame({
        "order_date": dates,
        "revenue": [100.0 + i * 5 for i in range(20)]
    })
    
    result = generate_forecast(df, horizon=14)
    assert "error" not in result
    assert "predictions" in result
    assert len(result["predictions"]) == 14
    assert "metrics" in result
    assert "mae" in result["metrics"]
    assert "historical" in result

def test_forecasting_no_date_column():
    df = pd.DataFrame({
        "product": ["A", "B", "C"],
        "price": [10, 20, 30]
    })
    result = generate_forecast(df)
    assert "error" in result
    assert "datetime column" in result["error"]

