from fastapi.testclient import TestClient
from dataclasses import dataclass
from main import app
import json

client = TestClient(app)


@dataclass
class Tests:
    Token: str


def test_register():
    response = client.post(
        "/register",
        params={
            'username': 'vlad',
            'phone': '890',
            'password': 'vlad'
        },
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Register successfully"


def test_register_user_exists():
    response = client.post(
        "/register",
        params={
            'username': 'vlad',
            'phone': '891',
            'password': 'vlad'
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"
    response = client.post(
        "/register",
        params={
            'username': 'vladik',
            'phone': '890',
            'password': 'vladik'
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"


def test_login_invalid_username():
    response = client.post(
        "/token",
        data={
            'username': 'JohnDoe',
            'password': 'vlad',
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_login_invalid_password():
    response = client.post(
        "/token",
        data={
            'username': 'vlad',
            'password': 'JohnDoe',
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect password"


def test_success_login():
    response = client.post(
        "/token",
        data={
            'username': '890',
            'password': 'vlad',
        }
    )
    assert response.status_code == 200
    Tests.Token = response.json()["access_token"]


def test_edit_profile():
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {Tests.Token}',
    }
    params = {
        'username': 'VLAD',
        'password_hash': 'VLAD',
        'userinfo': 'NEW INFO ABOUT ME',
    }
    response = client.put(
        "/edit",
        params=params,
        headers=headers
    )
    assert response.status_code == 200
    assert ["username", "password_hash", "userinfo"] == list(response.json().keys())
