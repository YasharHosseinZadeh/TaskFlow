from wsgiref import headers

from fastapi.testclient import TestClient
from main import app
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


@pytest.mark.asyncio
async def test_get_projects(client,setup_database,test_user):
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

    response = await client.post(
        "/projects",headers =headers,
        json={
            "name": "test2",
            "description": "test2",

        }
    )
    assert response.status_code == 200

    response = await client.get(
        "/projects",headers =headers
    )
    projects = response.json()
    assert response.status_code == 200
    assert len(projects) == 2
    assert projects[0]["name"] == "test"
    assert projects[1]["name"] == "test2"


@pytest.mark.asyncio
async def test_get_project(client,setup_database,test_user):
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
    project_id = response.json()["id"]
    response = await client.get(
        f"/projects/{project_id}",headers =headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "test"
    assert response.json()["description"] == "test"
    assert response.json()["owner_id"] == test_user.id
    assert response.json()["id"] == project_id


@pytest.mark.asyncio
async def test_get_other_user_project(client,setup_database,test_user,test_user2):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    data = response.json()["access_token"]

    response = await client.post(
        "/login",
        json={
            "email": test_user2.email,
            "password": "test12345"
        }
    )
    assert response.status_code == 200
    data2 = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {data}"}
    response = await client.post(
        "/projects",headers =headers,
        json={
            "name": "test",
            "description": "test"
        }
    )
    headers2={"Authorization": f"Bearer {data2}"}
    assert response.status_code == 200
    project_id = response.json()["id"]
    response = await client.get(
        f"/projects/{project_id}",headers =headers2
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Project id is wrong"


@pytest.mark.asyncio
async def test_update_project(client,setup_database,test_user):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    data = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {data}"}
    response = await client.post(
        "/projects",headers =headers,
        json={
            "name": "test",
            "description": "test"
        }
    )
    assert response.status_code == 200
    project_id = response.json()["id"]

    response = await client.patch(
        f"/projects/{project_id}",headers =headers,
        json={
            "name" : "updated name",
            "description": "updated description"
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == "updated name"
    assert response.json()["description"] == "updated description"


@pytest.mark.asyncio
async def test_delete_project(client,setup_database,test_user):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    data = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {data}"}
    response = await client.post(
        "/projects",headers =headers,
        json={
            "name": "test",
            "description": "test"
        }
    )
    assert response.status_code == 200
    project_id = response.json()["id"]
    response = await client.delete(
        f"/projects/{project_id}",headers =headers
    )
    assert response.status_code == 200
    response = await client.get(
        f"/projects/{project_id}",headers =headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Project id is wrong"

# Error handling
@pytest.mark.asyncio
async def test_get_projects_without_auth(client,setup_database):
    response = await client.get(
        "/projects"
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_create_project_invalid_data(client, setup_database, test_user):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    data = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {data}"}
    response = await client.post(
        "/projects",headers =headers,
        json={
            "name": "",
            "description": "test"
        }
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_project_long_name(client,setup_database,test_user):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    data = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {data}"}
    response = await client.post(
        "/projects",headers =headers,
        json={
            "name": "A"* 101,
            "description": "test"
        }
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_nonexistent_project(client,setup_database,test_user):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    data = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {data}"}
    response = await client.get(
        f"/projects/999",headers =headers
    )
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_other_user_project(client,setup_database,test_user,test_user2):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    data = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {data}"}
    response = await client.post(
        "/projects",headers =headers,
        json={
            "name": "test",
            "description": "test"
        }
    )
    assert response.status_code == 200
    project_id = response.json()["id"]
    response = await client.post(
        "/login"
        ,headers =headers
        ,json={
            "email": test_user2.email,
            "password": "test12345"
        }
    )
    assert response.status_code == 200
    data = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {data}"}
    response = await client.patch(
        f"/projects/{project_id}",headers =headers,
        json={
            "name": "hacked project"
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Project id is wrong"


@pytest.mark.asyncio
async def test_delete_other_user_project(client,setup_database,test_user,test_user2):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    data = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {data}"}
    response = await client.post(
        "/projects",headers =headers,
        json={
            "name": "test",
            "description": "test"
        }
    )
    assert response.status_code == 200
    project_id = response.json()["id"]
    response = await client.post(
        "/login"
        ,json={
            "email": test_user2.email,
            "password": "test12345"
        }
    )
    assert response.status_code == 200
    data = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {data}"}
    response = await client.delete(
        f"/projects/{project_id}",headers =headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Project id is wrong"