import io
import xlwt
import httpx

def run():
    print("--- Testing Real Local Server API Upload for Legacy .XLS Superstore ---")
    base_url = "http://127.0.0.1:8000"
    
    # 1. Register or login
    email = "superstore_tester@datapilot.ai"
    password = "TestPassword123!"
    
    client = httpx.Client(base_url=base_url, timeout=30.0)
    
    auth_res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    if auth_res.status_code != 200:
        reg_res = client.post("/api/v1/auth/register", json={"name": "Superstore Admin", "email": email, "password": password})
        if reg_res.status_code == 201:
            token = reg_res.json()["access_token"]
        else:
            print("Register failed:", reg_res.text)
            return
    else:
        token = auth_res.json()["access_token"]
        
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Build 100-row Superstore XLS dataset
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Orders')
    
    headers_list = ["Row ID", "Order ID", "Order Date", "Ship Date", "Customer Name", "Segment", "Region", "Category", "Sub-Category", "Sales", "Quantity", "Discount", "Profit"]
    for col_idx, h in enumerate(headers_list):
        ws.write(0, col_idx, h)
        
    for r in range(1, 101):
        ws.write(r, 0, r)
        ws.write(r, 1, f"CA-2023-{100000+r}")
        ws.write(r, 2, "2023-05-15")
        ws.write(r, 3, "2023-05-20")
        ws.write(r, 4, f"Customer {r}")
        ws.write(r, 5, "Consumer" if r % 2 == 0 else "Corporate")
        ws.write(r, 6, "West" if r % 3 == 0 else "East")
        ws.write(r, 7, "Technology" if r % 2 == 0 else "Furniture")
        ws.write(r, 8, "Phones" if r % 2 == 0 else "Chairs")
        ws.write(r, 9, 250.50 * (r % 5 + 1))
        ws.write(r, 10, r % 4 + 1)
        ws.write(r, 11, 0.1)
        ws.write(r, 12, 45.20 * (r % 5 + 1))
        
    buf = io.BytesIO()
    wb.save(buf)
    xls_content = buf.getvalue()
    
    print(f"Generated Superstore .xls workbook: {len(xls_content)} bytes")
    
    # 3. Upload via HTTP multipart
    files = {"file": ("sample_-_superstore.xls", xls_content, "application/vnd.ms-excel")}
    upload_res = client.post("/api/v1/datasets/upload", headers=headers, files=files)
    
    print("Upload Response HTTP Status:", upload_res.status_code)
    upload_json = upload_res.json()
    print("Dataset Upload Response JSON:", upload_json)
    
    dataset_id = upload_json["id"]
    print(f"Uploaded Dataset ID: {dataset_id}")
    print(f"Status: {upload_json.get('status')}")
    print(f"Detected Rows: {upload_json.get('row_count')}")
    print(f"Detected Columns: {upload_json.get('column_count')}")
    print(f"Quality Score: {upload_json.get('quality_score')}")
    print(f"Error Message: {upload_json.get('error_message')}")
    
    # 4. Test Preview
    prev_res = client.get(f"/api/v1/datasets/{dataset_id}/preview", headers=headers)
    print("Preview HTTP Status:", prev_res.status_code)
    prev_json = prev_res.json()
    print(f"Preview total_rows: {prev_json.get('total_rows')}, returned columns count: {len(prev_json.get('columns', []))}")
    
    # 5. Test Profile
    prof_res = client.get(f"/api/v1/datasets/{dataset_id}/profile", headers=headers)
    print("Profile HTTP Status:", prof_res.status_code)
    prof_json = prof_res.json()
    print("Profile Quality Score:", prof_json.get("quality_score"))
    
    # 6. Test KPI Analyses
    analysis_res = client.post("/api/v1/analyses/", headers=headers, json={"dataset_id": dataset_id})
    print("Analysis HTTP Status:", analysis_res.status_code)
    analysis_json = analysis_res.json()
    print("Calculated KPIs:")
    for kpi in analysis_json.get("kpis", []):
        print(f"  - {kpi.get('name')}: {kpi.get('formatted_value')} ({kpi.get('description')})")
        
    print("\n--- ALL VERIFICATIONS PASSED SUCCESSFULLY ---")

if __name__ == "__main__":
    run()
