import io
import pytest

def test_report_security_and_authenticated_download(client):
    # 1. Register User A
    res_a = client.post("/api/v1/auth/register", json={
        "name": "User Alpha",
        "email": "alpha@tenant-a.com",
        "password": "Password123!"
    })
    assert res_a.status_code == 201
    token_a = res_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Register User B (separate tenant)
    res_b = client.post("/api/v1/auth/register", json={
        "name": "User Beta",
        "email": "beta@tenant-b.com",
        "password": "Password123!"
    })
    assert res_b.status_code == 201
    token_b = res_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Get User A workspace
    ws_res_a = client.get("/api/v1/workspaces", headers=headers_a)
    assert ws_res_a.status_code == 200
    ws_id_a = ws_res_a.json()[0]["id"]

    # Upload dataset for User A
    csv_data = "date,revenue,cost\n2024-01-01,1000,400\n2024-01-02,1500,600\n2024-01-03,2000,800\n"
    up_res = client.post(
        "/api/v1/datasets/upload",
        headers=headers_a,
        data={"workspace_id": ws_id_a},
        files={"file": ("tenant_a_data.csv", io.BytesIO(csv_data.encode("utf-8")), "text/csv")}
    )
    assert up_res.status_code == 201
    dataset_id = up_res.json()["id"]

    # Generate Report for User A
    rep_res = client.post("/api/v1/reports/", headers=headers_a, json={
        "dataset_id": dataset_id,
        "title": "Alpha Q1 Report"
    })
    assert rep_res.status_code == 201
    report = rep_res.json()
    report_id = report["id"]

    # TEST 1: Unauthenticated download attempt MUST return 401 Unauthorized
    unauth_dl = client.get(f"/api/v1/reports/{report_id}/download")
    assert unauth_dl.status_code == 401

    # TEST 2: Cross-workspace User B download attempt MUST return 403 Forbidden
    cross_dl = client.get(f"/api/v1/reports/{report_id}/download", headers=headers_b)
    assert cross_dl.status_code == 403

    # TEST 3: Cross-workspace User B get_report MUST return 403 Forbidden
    cross_get = client.get(f"/api/v1/reports/{report_id}", headers=headers_b)
    assert cross_get.status_code == 403

    # TEST 4: Authorized User A download returns 200 with PDF content
    auth_dl = client.get(f"/api/v1/reports/{report_id}/download", headers=headers_a)
    assert auth_dl.status_code == 200
    assert auth_dl.headers["content-type"] == "application/pdf"
    assert len(auth_dl.content) > 500

    # TEST 5: Authorized User A lists report
    list_res = client.get("/api/v1/reports", headers=headers_a)
    assert list_res.status_code == 200
    assert any(r["id"] == report_id for r in list_res.json())

    # User B listing reports does not include User A report
    list_b = client.get("/api/v1/reports", headers=headers_b)
    assert list_b.status_code == 200
    assert not any(r["id"] == report_id for r in list_b.json())

    # TEST 6: Delete report
    del_res = client.delete(f"/api/v1/reports/{report_id}", headers=headers_a)
    assert del_res.status_code == 200

    # Verify deleted
    get_after_del = client.get(f"/api/v1/reports/{report_id}", headers=headers_a)
    assert get_after_del.status_code == 404

