from fastapi.testclient import TestClient
from main import app
from core.security import create_access_token
import pytest

client = TestClient(app)

@pytest.mark.asyncio
async def test_register_user(client,setup_database):
    response = await client.post(
        "/users",
        json={
            "name": "Alex",
            "email": "alex@example.com",
            "password": "mypassword123"
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "alex@example.com"


@pytest.mark.asyncio
async def test_register_with_existing_user(client,setup_database):
    response = await client.post(
        "/users",
        json={
            "name": "Alex",
            "email": "alex@example.com",
            "password": "mypassword123"
        }
    )
    assert response.status_code == 200

    response = await client.post(
        "/users",
        json={
            "name": "test",
            "email": "alex@example.com",
            "password": "mypassword123"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail" : "User already exists"}


@pytest.mark.asyncio
async def test_login(client,setup_database):
    response = await client.post(
        "/users",
        json={
            "name": "Alex",
            "email": "alex@example.com",
            "password": "mypassword123"
        }
    )
    assert response.status_code == 200

    response = await client.post(
        "/login",
        json={
            "email": "alex@example.com",
            "password": "mypassword123"
        }
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_incorrect_info(client,setup_database):
    response = await client.post(
        "/users",
        json={
            "name": "Alex",
            "email": "alex@example.com",
            "password": "mypassword123"
        }
    )
    assert response.status_code == 200
    response = await client.post(
        "/login",
        json={
            "email": "alex@example.com",
            "password": "test1234"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail" : "Incorrect email or password"}