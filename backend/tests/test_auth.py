import pytest
from app.services.auth_service import hash_password, verify_password, create_access_token, decode_token

def test_password_hashing():
    pwd = "SecurePassword123!"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_generation_and_decoding():
    user_id = "12345678-1234-5678-1234-567812345678"
    token = create_access_token({"sub": user_id, "role": "admin"})
    assert isinstance(token, str)
    
    payload = decode_token(token)
    assert payload is not None
    assert payload.get("sub") == user_id
    assert payload.get("role") == "admin"
    assert payload.get("type") == "access"

def test_auth_api_register_and_login(client):
    email = "testuser@datapilot.ai"
    reg_res = client.post("/api/v1/auth/register", json={
        "name": "Test User",
        "email": email,
        "password": "Password123!"
    })
    assert reg_res.status_code == 201
    data = reg_res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    
    # Login with the created credentials
    login_res = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "Password123!"
    })
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert "access_token" in login_data
    
    # Get current user profile
    token = login_data["access_token"]
    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["email"] == email
    assert me_data["name"] == "Test User"

