import io
import pytest

def test_full_saas_lifecycle_e2e(client):
    # 1. Register new user
    reg_res = client.post("/api/v1/auth/register", json={
        "name": "Sarah Connor",
        "email": "sarah@cyberdyne.com",
        "password": "Resistance2024!"
    })
    assert reg_res.status_code == 201
    auth_data = reg_res.json()
    token = auth_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Get User Profile & Default Workspace
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    
    ws_res = client.get("/api/v1/workspaces", headers=headers)
    assert ws_res.status_code == 200
    workspaces = ws_res.json()
    assert len(workspaces) > 0
    workspace_id = workspaces[0]["id"]
    
    # 3. Upload CSV Dataset
    csv_content = (
        "date,product,category,revenue,cost,quantity\n"
        "2024-01-01,Laptop Pro,Electronics,1200.0,600.0,1\n"
        "2024-01-02,Mouse,Accessories,50.0,20.0,2\n"
        "2024-01-03,Laptop Pro,Electronics,2400.0,1200.0,2\n"
        "2024-01-04,Keyboard,Peripherals,150.0,75.0,1\n"
        "2024-01-05,Laptop Pro,Electronics,1200.0,600.0,1\n"
        "2024-01-06,Mouse,Accessories,25.0,10.0,1\n"
        "2024-01-07,Monitor,Electronics,800.0,400.0,2\n"
        "2024-01-08,Laptop Pro,Electronics,3600.0,1800.0,3\n"
        "2024-01-09,Headset,Accessories,200.0,90.0,2\n"
        "2024-01-10,Webcam,Peripherals,300.0,140.0,3\n"
    )
    
    upload_res = client.post(
        "/api/v1/datasets/upload",
        headers=headers,
        data={"workspace_id": workspace_id},
        files={"file": ("sales_jan2024.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    )
    assert upload_res.status_code == 201
    dataset = upload_res.json()
    dataset_id = dataset["id"]
    assert dataset["status"] == "ready"
    assert dataset["dataset_type"] == "Sales"
    assert dataset["quality_score"] > 80.0
    
    # 4. Preview Dataset
    prev_res = client.get(f"/api/v1/datasets/{dataset_id}/preview", headers=headers)
    assert prev_res.status_code == 200
    prev_data = prev_res.json()
    assert prev_data["total_rows"] == 10
    assert len(prev_data["columns"]) == 6
    
    # 5. Run Automated Analysis (KPIs, Charts, AI Insights)
    analysis_res = client.post("/api/v1/analyses/", headers=headers, json={"dataset_id": dataset_id})
    assert analysis_res.status_code in [200, 201]
    analysis_data = analysis_res.json()
    assert analysis_data["status"] == "completed"
    assert len(analysis_data["kpis"]) > 0
    analysis_id = analysis_data["id"]
    
    # 6. Ask AI Data Chat Question (Deterministic analytics + explanation)
    chat_res = client.post("/api/v1/chat/", headers=headers, json={
        "dataset_id": dataset_id,
        "message": "What was our total revenue?"
    })
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert "message" in chat_data
    assert "session_id" in chat_data
    
    # 7. Generate Forecast
    forecast_res = client.post("/api/v1/forecasts/", headers=headers, json={
        "dataset_id": dataset_id,
        "horizon": 14
    })
    assert forecast_res.status_code == 200
    f_data = forecast_res.json()
    assert len(f_data["predictions"]) == 14
    
    # 8. Detect Anomalies
    anom_res = client.post("/api/v1/anomalies/detect", headers=headers, json={
        "dataset_id": dataset_id
    })
    assert anom_res.status_code == 200
    
    # 9. Generate PDF Report
    report_res = client.post("/api/v1/reports/", headers=headers, json={
        "dataset_id": dataset_id,
        "title": "January Executive Review"
    })
    assert report_res.status_code == 201
    report_data = report_res.json()
    report_id = report_data["id"]
    
    # 10. Download PDF Report
    dl_res = client.get(f"/api/v1/reports/{report_id}/download", headers=headers)
    assert dl_res.status_code == 200
    assert dl_res.headers["content-type"] == "application/pdf"
    assert len(dl_res.content) > 1000 # Actual binary PDF bytes
    
    # 11. Check Usage Tracking
    usage_res = client.get("/api/v1/billing/usage", headers=headers)
    assert usage_res.status_code == 200
    usage_data = usage_res.json()
    assert usage_data["uploads"]["used"] >= 1
    
    # 12. Delete Dataset and ensure safe cascade
    del_res = client.delete(f"/api/v1/datasets/{dataset_id}", headers=headers)
    assert del_res.status_code == 200
    
    # Verify dataset is no longer accessible
    get_del = client.get(f"/api/v1/datasets/{dataset_id}", headers=headers)
    assert get_del.status_code == 404

