import io
import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def setup_users(client):
    u1 = uuid.uuid4().hex[:8]
    email1 = f"direct_{u1}@example.com"
    reg1 = client.post("/api/v1/auth/register", json={
        "name": "Direct User One",
        "email": email1,
        "password": "Password123!"
    })
    assert reg1.status_code == 201, f"Register failed: {reg1.text}"
    token1 = reg1.json()["access_token"]
    
    # Get user 1 workspace
    ws_list1 = client.get("/api/v1/workspaces", headers={"Authorization": f"Bearer {token1}"}).json()
    ws1_id = ws_list1[0]["id"]
    
    # Register user 2 (cross-tenant)
    u2 = uuid.uuid4().hex[:8]
    email2 = f"direct_{u2}@example.com"
    reg2 = client.post("/api/v1/auth/register", json={
        "name": "Direct User Two",
        "email": email2,
        "password": "Password123!"
    })
    assert reg2.status_code == 201, f"Register 2 failed: {reg2.text}"
    token2 = reg2.json()["access_token"]
    ws_list2 = client.get("/api/v1/workspaces", headers={"Authorization": f"Bearer {token2}"}).json()
    ws2_id = ws_list2[0]["id"]
    
    return {
        "token1": token1,
        "ws1_id": ws1_id,
        "token2": token2,
        "ws2_id": ws2_id
    }

def test_presigned_upload_url_endpoint(client, setup_users):
    headers = {"Authorization": f"Bearer {setup_users['token1']}"}
    payload = {
        "filename": "superstore_sales.csv",
        "file_size": 1024 * 50, # 50 KB
        "content_type": "text/csv"
    }
    response = client.post("/api/v1/datasets/presigned-upload", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert "dataset_id" in data
    assert "upload_url" in data
    assert data["method"] == "PUT"
    assert "storage_path" in data
    assert "headers" in data

def test_unauthenticated_request_rejected(client):
    payload = {
        "filename": "test.csv",
        "file_size": 1000,
        "content_type": "text/csv"
    }
    response = client.post("/api/v1/datasets/presigned-upload", json=payload)
    assert response.status_code == 401

def test_cross_tenant_workspace_access_rejected(client, setup_users):
    # User 1 tries to request upload into User 2's workspace
    headers = {"Authorization": f"Bearer {setup_users['token1']}"}
    payload = {
        "filename": "hack.csv",
        "file_size": 1000,
        "content_type": "text/csv",
        "workspace_id": setup_users["ws2_id"]
    }
    response = client.post("/api/v1/datasets/presigned-upload", json=payload, headers=headers)
    assert response.status_code == 403
    assert "You do not have access" in response.json()["detail"]

def test_invalid_extension_rejected(client, setup_users):
    headers = {"Authorization": f"Bearer {setup_users['token1']}"}
    for bad_file in ["malicious.exe", "script.py", "document.pdf"]:
        payload = {
            "filename": bad_file,
            "file_size": 5000,
            "content_type": "application/octet-stream"
        }
        response = client.post("/api/v1/datasets/presigned-upload", json=payload, headers=headers)
        assert response.status_code == 400
        assert "Invalid file extension" in response.json()["detail"]

def test_file_too_large_rejected(client, setup_users):
    headers = {"Authorization": f"Bearer {setup_users['token1']}"}
    payload = {
        "filename": "huge_file.csv",
        "file_size": 55 * 1024 * 1024, # 55 MB (> 50 MB limit)
        "content_type": "text/csv"
    }
    response = client.post("/api/v1/datasets/presigned-upload", json=payload, headers=headers)
    assert response.status_code == 400
    assert "exceeds maximum allowed limit" in response.json()["detail"]

def test_successful_direct_upload_and_process_lifecycle(client, setup_users):
    headers = {"Authorization": f"Bearer {setup_users['token1']}"}
    
    # 1. Request presigned upload URL
    req_payload = {
        "filename": "monthly_revenue.csv",
        "file_size": 1500,
        "content_type": "text/csv"
    }
    init_res = client.post("/api/v1/datasets/presigned-upload", json=req_payload, headers=headers)
    assert init_res.status_code == 201
    presigned = init_res.json()
    dataset_id = presigned["dataset_id"]
    upload_url = presigned["upload_url"]
    
    # 2. Upload file directly to the upload URL (PUT)
    csv_content = (
        "Date,Product,Category,Region,Revenue,Cost,Units\n"
        "2024-01-01,Laptop,Electronics,North,2400,1200,2\n"
        "2024-01-02,Mouse,Electronics,North,80,30,4\n"
        "2024-01-03,Chair,Furniture,South,450,200,1\n"
        "2024-01-04,Desk,Furniture,South,900,450,1\n"
        "2024-01-05,Monitor,Electronics,East,600,300,2\n"
    )
    
    put_res = client.put(
        upload_url,
        content=csv_content.encode("utf-8"),
        headers={"Content-Type": "text/csv"}
    )
    assert put_res.status_code == 200
    
    # 3. Trigger processing with tiny JSON payload
    proc_res = client.post(f"/api/v1/datasets/{dataset_id}/process", headers=headers)
    assert proc_res.status_code == 200
    dataset_data = proc_res.json()
    
    assert dataset_data["status"] == "ready"
    assert dataset_data["row_count"] == 5
    assert dataset_data["column_count"] == 7
    assert dataset_data["dataset_type"] == "Sales"
    assert dataset_data["quality_score"] > 80.0

def test_missing_storage_object_handling(client, setup_users):
    headers = {"Authorization": f"Bearer {setup_users['token1']}"}
    
    # Request presigned upload URL but DO NOT upload any content
    req_payload = {
        "filename": "unuploaded.csv",
        "file_size": 500,
        "content_type": "text/csv"
    }
    init_res = client.post("/api/v1/datasets/presigned-upload", json=req_payload, headers=headers)
    dataset_id = init_res.json()["dataset_id"]
    
    # Trigger processing immediately
    proc_res = client.post(f"/api/v1/datasets/{dataset_id}/process", headers=headers)
    assert proc_res.status_code == 400
    assert "File was not uploaded or does not exist" in proc_res.json()["detail"]

def test_cross_tenant_dataset_processing_rejected(client, setup_users):
    headers1 = {"Authorization": f"Bearer {setup_users['token1']}"}
    headers2 = {"Authorization": f"Bearer {setup_users['token2']}"}
    
    # User 1 creates dataset
    init_res = client.post("/api/v1/datasets/presigned-upload", json={"filename": "secret.csv", "file_size": 100}, headers=headers1)
    dataset_id = init_res.json()["dataset_id"]
    
    # User 2 tries to trigger processing or access dataset
    proc_res = client.post(f"/api/v1/datasets/{dataset_id}/process", headers=headers2)
    assert proc_res.status_code == 403
    
    get_res = client.get(f"/api/v1/datasets/{dataset_id}", headers=headers2)
    assert get_res.status_code == 403

def test_pdf_report_generation_and_download_flow(client, setup_users):
    headers = {"Authorization": f"Bearer {setup_users['token1']}"}
    
    # Create and process dataset
    init_res = client.post("/api/v1/datasets/presigned-upload", json={"filename": "report_test.csv", "file_size": 200}, headers=headers)
    dataset_id = init_res.json()["dataset_id"]
    upload_url = init_res.json()["upload_url"]
    
    client.put(upload_url, content=b"A,B,Revenue\n1,2,100\n3,4,200\n", headers={"Content-Type": "text/csv"})
    client.post(f"/api/v1/datasets/{dataset_id}/process", headers=headers)
    
    # Generate Report
    rep_res = client.post("/api/v1/reports", json={"dataset_id": dataset_id, "title": "Executive Direct Report"}, headers=headers)
    assert rep_res.status_code == 201
    report_id = rep_res.json()["id"]
    
    # Download Report
    down_res = client.get(f"/api/v1/reports/{report_id}/download", headers=headers, follow_redirects=False)
    assert down_res.status_code in [200, 307]
    if down_res.status_code == 200:
        assert down_res.headers["content-type"] == "application/pdf"
        assert len(down_res.content) > 1000
