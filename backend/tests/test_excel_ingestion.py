import io
import uuid
import pytest
import pandas as pd
import openpyxl
import xlwt
from app.services.ingestion.parser import parse_excel, parse_file
from app.services.analytics.kpi_engine import compute_kpis
from app.services.profiling.profiler import profile_dataframe

def create_sample_xls_bytes() -> bytes:
    """Create a real legacy BI Superstore Excel .xls binary using xlwt."""
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Orders')
    
    headers = ["Row ID", "Order ID", "Order Date", "Ship Date", "Customer Name", "Segment", "Region", "Category", "Sub-Category", "Sales", "Quantity", "Discount", "Profit"]
    for col_idx, header in enumerate(headers):
        ws.write(0, col_idx, header)
        
    rows = [
        [1, "CA-2023-152156", "2023-11-08", "2023-11-11", "Claire Gute", "Consumer", "South", "Furniture", "Bookcases", 261.96, 2, 0.0, 41.91],
        [2, "CA-2023-152156", "2023-11-08", "2023-11-11", "Claire Gute", "Consumer", "South", "Furniture", "Chairs", 731.94, 3, 0.0, 219.58],
        [3, "CA-2023-138688", "2023-06-12", "2023-06-16", "Darrin Van Huff", "Corporate", "West", "Office Supplies", "Labels", 14.62, 2, 0.0, 6.87],
        [4, "US-2023-108966", "2023-10-11", "2023-10-18", "Sean O'Donnell", "Consumer", "South", "Furniture", "Tables", 957.57, 5, 0.45, -383.03],
        [5, "US-2023-108966", "2023-10-11", "2023-10-18", "Sean O'Donnell", "Consumer", "South", "Office Supplies", "Storage", 22.36, 2, 0.2, 2.51],
        [6, "CA-2023-115812", "2023-06-09", "2023-06-14", "Brosina Hoffman", "Consumer", "West", "Furniture", "Furnishings", 48.86, 7, 0.0, 14.17],
        [7, "CA-2023-115812", "2023-06-09", "2023-06-14", "Brosina Hoffman", "Consumer", "West", "Technology", "Phones", 907.15, 4, 0.2, 90.71],
        [8, "CA-2023-115812", "2023-06-09", "2023-06-14", "Brosina Hoffman", "Consumer", "West", "Office Supplies", "Art", 18.50, 3, 0.0, 4.81],
        [9, "CA-2023-115812", "2023-06-09", "2023-06-14", "Brosina Hoffman", "Consumer", "West", "Technology", "Phones", 114.90, 5, 0.2, 34.47],
        [10, "CA-2023-115812", "2023-06-09", "2023-06-14", "Brosina Hoffman", "Consumer", "West", "Office Supplies", "Binders", 1.79, 1, 0.8, -1.34],
    ]
    
    for row_idx, row in enumerate(rows, start=1):
        for col_idx, val in enumerate(row):
            ws.write(row_idx, col_idx, val)
            
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()

def create_sample_xlsx_bytes() -> bytes:
    """Create a modern Excel .xlsx binary using openpyxl."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "SalesData"
    
    headers = ["date", "category", "sales", "cost", "quantity"]
    ws.append(headers)
    
    for i in range(1, 15):
        ws.append([f"2024-01-{i:02d}", "Electronics", 150.0 * i, 75.0 * i, i])
        
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()

def test_xls_parser_direct(tmp_path):
    """Verify legacy .xls parsing via xlrd directly."""
    xls_data = create_sample_xls_bytes()
    xls_file = tmp_path / "superstore.xls"
    xls_file.write_bytes(xls_data)
    
    df = parse_file(str(xls_file), file_type="application/vnd.ms-excel")
    assert not df.empty
    assert len(df) == 10
    assert len(df.columns) == 13
    assert "Sales" in df.columns
    assert "Profit" in df.columns
    assert df["Sales"].sum() > 0

def test_xlsx_parser_direct(tmp_path):
    """Verify modern .xlsx parsing via openpyxl directly."""
    xlsx_data = create_sample_xlsx_bytes()
    xlsx_file = tmp_path / "sales.xlsx"
    xlsx_file.write_bytes(xlsx_data)
    
    df = parse_file(str(xlsx_file), file_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    assert not df.empty
    assert len(df) == 14
    assert len(df.columns) == 5
    assert "sales" in df.columns

def test_invalid_excel_raises_http_exception(tmp_path):
    """Verify corrupted excel files fail cleanly with informative HTTP error."""
    corrupted_file = tmp_path / "corrupted.xls"
    corrupted_file.write_bytes(b"NOT_A_REAL_EXCEL_STREAM_BINARY_HEADER_DATA_12345")
    
    with pytest.raises(Exception) as exc_info:
        parse_file(str(corrupted_file), file_type="application/vnd.ms-excel")
    assert exc_info.value.status_code == 400

def test_api_xls_upload_and_analysis_lifecycle(client):
    """Verify end-to-end API upload of .xls file, preview, profile, and KPI calculation."""
    # 1. Register & get token
    reg_res = client.post("/api/v1/auth/register", json={
        "name": "Superstore Analyst",
        "email": "analyst@superstore.com",
        "password": "Password123!"
    })
    assert reg_res.status_code == 201
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Upload .xls Superstore dataset
    xls_bytes = create_sample_xls_bytes()
    upload_res = client.post(
        "/api/v1/datasets/upload",
        headers=headers,
        files={"file": ("sample_-_superstore.xls", io.BytesIO(xls_bytes), "application/vnd.ms-excel")}
    )
    assert upload_res.status_code == 201
    dataset = upload_res.json()
    
    assert dataset["status"] == "ready"
    assert dataset["row_count"] == 10
    assert dataset["column_count"] == 13
    assert dataset["quality_score"] is not None
    assert dataset["quality_score"] > 80.0
    assert dataset["error_message"] is None
    dataset_id = dataset["id"]
    
    # 3. Verify Preview endpoint
    prev_res = client.get(f"/api/v1/datasets/{dataset_id}/preview", headers=headers)
    assert prev_res.status_code == 200
    prev_data = prev_res.json()
    assert prev_data["total_rows"] == 10
    assert len(prev_data["columns"]) == 13
    assert len(prev_data["rows"]) == 10
    
    # 4. Verify Profile endpoint
    prof_res = client.get(f"/api/v1/datasets/{dataset_id}/profile", headers=headers)
    assert prof_res.status_code == 200
    prof_data = prof_res.json()
    assert "profile" in prof_data
    assert prof_data["profile"]["overall"]["row_count"] == 10
    
    # 5. Verify KPI calculations on Superstore data
    analysis_res = client.post("/api/v1/analyses/", headers=headers, json={"dataset_id": dataset_id})
    assert analysis_res.status_code in [200, 201]
    analysis = analysis_res.json()
    assert len(analysis["kpis"]) > 0
    kpi_names = [k["name"] for k in analysis["kpis"]]
    assert "Total Revenue" in kpi_names or "Total Profit" in kpi_names or "Total Records" in kpi_names
