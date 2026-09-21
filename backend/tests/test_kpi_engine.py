import pytest
import pandas as pd
from app.services.analytics.kpi_engine import compute_kpis

def test_kpi_sales_calculation():
    df = pd.DataFrame({
        "order_id": [1, 2, 3],
        "revenue": [100.0, 200.0, 300.0],
        "cost": [60.0, 100.0, 140.0],
        "quantity": [2, 5, 3]
    })
    kpis = compute_kpis(df, "Sales")
    kpi_dict = {k["name"]: k["value"] for k in kpis}
    
    assert kpi_dict["Total Revenue"] == 600.0
    assert kpi_dict["Total Profit"] == 300.0
    assert kpi_dict["Profit Margin"] == 50.0
    assert kpi_dict["Units Sold"] == 10
    assert kpi_dict["Total Orders"] == 3

def test_kpi_marketing_calculation():
    df = pd.DataFrame({
        "spend": [500.0, 1500.0],
        "conversions": [20, 80],
        "clicks": [200, 800],
        "impressions": [5000, 20000]
    })
    kpis = compute_kpis(df, "Marketing")
    kpi_dict = {k["name"]: k["value"] for k in kpis}
    
    assert kpi_dict["Total Ad Spend"] == 2000.0
    assert kpi_dict["Total Conversions"] == 100.0
    assert kpi_dict["Click-Through Rate"] == 4.0

