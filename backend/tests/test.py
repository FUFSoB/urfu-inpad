import os
import httpx
import pytest

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


@pytest.fixture
def wrong_credentials():
    return {"email": "wrong@mail.lsadhf", "password": "wrong_password"}


def test_get_access_token_invalid_credentials(wrong_credentials):
    response = httpx.post(f"{BASE_URL}/login", json=wrong_credentials)
    assert response.status_code == 401
    assert response.json().get("detail") == "Invalid credentials"


def test_protected_endpoint_no_token():
    response = httpx.get(f"{BASE_URL}/current_user")
    assert response.status_code == 401


def test_refresh_token_invalid():
    response = httpx.post(
        f"{BASE_URL}/refresh", json={"refresh_token": "invalid_token"}
    )
    assert response.status_code == 401


def test_register_and_delete_user():
    user_register = {
        "email": "asdfg@gfdsa.test",
        "password": "password",
        "name": "Name",
        "surname": "Surname",
        "middle_name": "Middle Name",
    }
    response = httpx.post(f"{BASE_URL}/register", json=user_register)
    assert response.status_code == 200
    data = response.json()
    token_data = data["token"]
    user_data = data["user"]

    access_token = token_data["access_token"]
    response = httpx.get(
        f"{BASE_URL}/current_user", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json() == user_data

    response = httpx.post(
        f"{BASE_URL}/refresh", json={"refresh_token": token_data["refresh_token"]}
    )
    assert response.status_code == 200

    response = httpx.post(
        f"{BASE_URL}/login",
        json={
            "email": user_register["email"],
            "password": user_register["password"],
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

    response = httpx.delete(
        f"{BASE_URL}/current_user", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
