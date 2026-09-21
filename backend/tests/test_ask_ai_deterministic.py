import io
import pytest
import pandas as pd
from app.services.ai.semantic_resolver import SemanticResolver
from app.services.ai.intent_engine import IntentEngine
from app.services.ai.query_engine import QueryExecutionEngine
from app.services.ai.deterministic_explainer import DeterministicExplainer
from app.services.ai.chat_engine import ChatEngine

@pytest.fixture
def sample_superstore_df():
    # Synthetic micro-dataset matching Superstore schema
    data = {
        "Row ID": [1, 2, 3, 4, 5, 6],
        "Order ID": ["CA-1", "CA-1", "CA-2", "CA-3", "CA-4", "CA-5"],
        "Order Date": pd.to_datetime(["2024-01-10", "2024-01-10", "2024-02-15", "2024-03-20", "2024-04-05", "2024-05-12"]),
        "Customer ID": ["C-101", "C-101", "C-102", "C-103", "C-101", "C-104"],
        "Customer Name": ["Alice Smith", "Alice Smith", "Bob Jones", "Charlie Brown", "Alice Smith", "Diana Ross"],
        "Postal Code": [90001, 90001, 10001, 60601, 90001, 30301],
        "Region": ["West", "West", "East", "Central", "West", "South"],
        "Category": ["Technology", "Furniture", "Technology", "Office Supplies", "Technology", "Furniture"],
        "Product Name": ["Canon Copier", "Office Chair", "Cisco Router", "Paper Box", "Canon Copier", "Desk Table"],
        "Sales": [5000.0, 300.0, 2000.0, 100.0, 3000.0, 1200.0],
        "Profit": [2000.0, 50.0, 800.0, 20.0, 1200.0, 300.0],
        "Discount": [0.0, 0.1, 0.0, 0.05, 0.0, 0.2],
        "Quantity": [2, 1, 1, 5, 1, 2]
    }
    return pd.DataFrame(data)

def test_semantic_resolver_identifies_and_excludes_identifiers(sample_superstore_df):
    resolver = SemanticResolver(sample_superstore_df)
    
    assert "Row ID" in resolver.identifiers
    assert "Postal Code" in resolver.identifiers
    assert "Customer ID" in resolver.identifiers
    
    assert "Sales" in resolver.metrics
    assert "Profit" in resolver.metrics
    assert "Discount" in resolver.metrics
    assert "Quantity" in resolver.metrics
    
    assert "Row ID" not in resolver.metrics
    assert "Postal Code" not in resolver.metrics

def test_top_n_products_deterministic_calculation(sample_superstore_df):
    resolver = SemanticResolver(sample_superstore_df)
    intent_engine = IntentEngine(resolver)
    plan = intent_engine.parse_intent("What are the top 5 products by sales?")
    
    assert plan.intent == "TOP_N"
    assert plan.metric == "Sales"
    assert plan.dimension == "Product Name"
    assert plan.limit == 5
    
    query_engine = QueryExecutionEngine(sample_superstore_df)
    result = query_engine.execute(plan)
    
    # Canon Copier: 5000 + 3000 = 8000
    # Cisco Router: 2000
    # Desk Table: 1200
    assert result["results"][0]["label"] == "Canon Copier"
    assert result["results"][0]["value"] == 8000.0
    assert result["results"][1]["label"] == "Cisco Router"
    assert result["results"][1]["value"] == 2000.0
    assert result["chart"]["type"] == "bar"

def test_highest_sales_region(sample_superstore_df):
    resolver = SemanticResolver(sample_superstore_df)
    intent_engine = IntentEngine(resolver)
    plan = intent_engine.parse_intent("Which region generated the highest sales?")
    
    assert plan.intent == "MAX"
    assert plan.dimension == "Region"
    assert plan.metric == "Sales"
    
    query_engine = QueryExecutionEngine(sample_superstore_df)
    result = query_engine.execute(plan)
    
    # West: 5000 + 300 + 3000 = 8300
    assert result["winner_label"] == "West"
    assert result["winner_value"] == 8300.0

def test_count_distinct_customers_and_orders(sample_superstore_df):
    resolver = SemanticResolver(sample_superstore_df)
    intent_engine = IntentEngine(resolver)
    
    plan_cust = intent_engine.parse_intent("How many unique customers are there?")
    assert plan_cust.intent == "COUNT_DISTINCT"
    query_engine = QueryExecutionEngine(sample_superstore_df)
    res_cust = query_engine.execute(plan_cust)
    assert res_cust["distinct_count"] == 4 # C-101, C-102, C-103, C-104

    plan_ord = intent_engine.parse_intent("How many orders are there?")
    res_ord = query_engine.execute(plan_ord)
    assert res_ord["distinct_count"] == 5 # CA-1, CA-2, CA-3, CA-4, CA-5

def test_average_metric_calculation(sample_superstore_df):
    resolver = SemanticResolver(sample_superstore_df)
    intent_engine = IntentEngine(resolver)
    
    plan = intent_engine.parse_intent("What is the average sales value?")
    assert plan.intent == "AVERAGE"
    assert plan.metric == "Sales"
    
    query_engine = QueryExecutionEngine(sample_superstore_df)
    res = query_engine.execute(plan)
    # Total sales: 11,600 / 6 = 1933.333
    assert round(res["average"], 2) == 1933.33

def test_trend_and_growth_calculation(sample_superstore_df):
    resolver = SemanticResolver(sample_superstore_df)
    intent_engine = IntentEngine(resolver)
    
    plan = intent_engine.parse_intent("How did sales change over time?")
    assert plan.intent == "TREND"
    assert plan.metric == "Sales"
    
    query_engine = QueryExecutionEngine(sample_superstore_df)
    res = query_engine.execute(plan)
    assert res["intent"] == "trend"
    assert res["total"] == 11600.0
    assert "highest_period" in res
    assert "growth_pct" in res
    assert res["chart"]["type"] == "line"

def test_chat_engine_follow_up_context(sample_superstore_df):
    import asyncio
    async def _run():
        engine = ChatEngine(ai_provider=None)
        
        # First turn
        r1 = await engine.answer("What are the top 3 products by sales?", sample_superstore_df, {"name": "Test Data"}, session_id="sess_abc")
        assert r1["analysis"]["intent"] == "top_n"
        assert r1["analysis"]["metric"] == "Sales"
        assert r1["analysis"]["results"][0]["label"] == "Canon Copier"
        
        # Follow-up turn
        r2 = await engine.answer("What about profit?", sample_superstore_df, {"name": "Test Data"}, session_id="sess_abc")
        assert r2["analysis"]["intent"] == "top_n"
        assert r2["analysis"]["metric"] == "Profit"
        assert r2["analysis"]["results"][0]["label"] == "Canon Copier"
        assert r2["analysis"]["results"][0]["value"] == 3200.0 # 2000 + 1200
    asyncio.run(_run())

def test_no_mock_prefix_in_production(sample_superstore_df):
    import asyncio
    async def _run():
        engine = ChatEngine(ai_provider=None)
        res = await engine.answer("What is the total sales?", sample_superstore_df, {"name": "Test Store"})
        
        assert "[Mock Generated]" not in res["answer"]
        assert "$11,600.00" in res["answer"]
        assert "Verification Details:" in res["answer"]
    asyncio.run(_run())

def test_api_chat_workspace_security_rejection(client):
    # Register User A
    res_a = client.post("/api/v1/auth/register", json={
        "name": "Owner A",
        "email": "owner_a@datapilot.ai",
        "password": "Password123!"
    })
    token_a = res_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Register User B
    res_b = client.post("/api/v1/auth/register", json={
        "name": "Attacker B",
        "email": "attacker_b@datapilot.ai",
        "password": "Password123!"
    })
    token_b = res_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User A uploads dataset
    ws_id = client.get("/api/v1/workspaces", headers=headers_a).json()[0]["id"]
    csv_bytes = "date,product,sales\n2024-01-01,Widget,100\n".encode("utf-8")
    up_res = client.post(
        "/api/v1/datasets/upload",
        headers=headers_a,
        data={"workspace_id": ws_id},
        files={"file": ("data.csv", io.BytesIO(csv_bytes), "text/csv")}
    )
    dataset_id = up_res.json()["id"]

    # User B tries to query User A's dataset
    cross_res = client.post("/api/v1/chat/", headers=headers_b, json={
        "dataset_id": dataset_id,
        "message": "What is the total sales?"
    })
    assert cross_res.status_code == 403
