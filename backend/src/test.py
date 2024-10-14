import httpx
import pytest

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture
def user_credentials():
    return {"username": "user", "password": "password"}

@pytest.fixture
def wrong_credentials():
    return {"username": "wrong_user", "password": "wrong_password"}

def test_get_access_token(user_credentials):
    response = httpx.post(f"{BASE_URL}/login", json=user_credentials)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_get_access_token_invalid_credentials(wrong_credentials):
    response = httpx.post(f"{BASE_URL}/login", json=wrong_credentials)
    assert response.status_code == 401
    assert response.json().get("detail") == "Invalid credentials"

def test_protected_endpoint(user_credentials):
    token_response = httpx.post(f"{BASE_URL}/login", json=user_credentials)
    access_token = token_response.json().get("access_token")

    headers = {"Authorization": f"Bearer {access_token}"}
    response = httpx.get(f"{BASE_URL}/protected", headers=headers)
    assert response.status_code == 200
    assert "Hello, user!" in response.json().get("message")

def test_protected_endpoint_no_token():
    response = httpx.get(f"{BASE_URL}/protected")
    assert response.status_code == 401

def test_refresh_token(user_credentials):
    token_response = httpx.post(f"{BASE_URL}/login", json=user_credentials)
    refresh_token = token_response.json().get("refresh_token")

    response = httpx.post(f"{BASE_URL}/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_refresh_token_invalid():
    response = httpx.post(f"{BASE_URL}/refresh", json={"refresh_token": "invalid_token"})
    assert response.status_code == 401

def test_register_user():
    user = {
        "username": "new_user",
        "password": "password",
        "email": "asdfg@gfdsa.test",
        "name": "Name",
        "surname": "Surname",
        "middle_name": "Middle Name",
    }
    response = httpx.post(f"{BASE_URL}/register", json=user)
    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    access_token = data["access_token"]
    response = httpx.get(f"{BASE_URL}/protected", headers = {"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200

    assert "refresh_token" in data
    response = httpx.post(f"{BASE_URL}/refresh", json={"refresh_token": data["refresh_token"]})
    assert response.status_code == 200

    response = httpx.post(f"{BASE_URL}/login", json={"username": user["username"], "password": user["password"]})
    assert response.status_code == 200
    assert "access_token" in response.json()
