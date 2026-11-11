from fastapi.testclient import TestClient
from main import app
from core.security import create_access_token
import pytest

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_project(client,setup_database,test_user):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    data = response.json()
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = await client.post(
        "/projects",headers =headers,
        json={
            "name": "test",
            "description": "test",

        }
    )
    assert response.status_code == 200
    project = response.json()
    assert project["name"] == "test"
    assert project["description"] == "test"
    assert project["owner_id"] == test_user.id