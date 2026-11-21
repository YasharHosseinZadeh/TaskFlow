from fastapi.testclient import TestClient
from main import app
import pytest


client = TestClient(app)

@pytest.mark.asyncio
async def test_create_task(client,setup_database,test_project,test_user):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post(
        "/tasks",headers=headers,
        json={
            "title": "Test Task",
            "description": "Test Task",
            "status": "pending",
            "priority": "medium",
            "project_id": test_project.id,
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"
    assert response.json()["description"] == "Test Task"
    assert response.json()["status"] == "pending"
    assert response.json()["priority"] == "medium"
    assert response.json()["project_id"] == test_project.id


@pytest.mark.asyncio
async def test_get_project_tasks(client,setup_database,test_project,test_user):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Test Task",
            "description": "Test Task",
            "status": "pending",
            "priority": "medium",
            "project_id": test_project.id
        }
    )
    assert response.status_code == 200
    response = await client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Test Task2",
            "description": "Test Task2",
            "status": "pending",
            "priority": "medium",
            "project_id": test_project.id
        }
    )
    assert response.status_code == 200
    response = await client.get(
        f"/projects/{test_project.id}/tasks",headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Test Task"
    assert data[1]["title"] == "Test Task2"

@pytest.mark.asyncio
async def test_get_task(client,setup_database,test_project,test_user):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post(
        "/tasks",headers=headers,
    json={
        "title": "Test Task",
        "description": "Test Task",
        "status": "pending",
        "priority": "medium",
        "project_id": test_project.id
        }
    )
    assert response.status_code == 200
    task_id = response.json()["id"]
    response = await client.get(
        f"/tasks/{task_id}",headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Task"
    assert data["status"] == "pending"
    assert data["priority"] == "medium"
    assert data["project_id"] == test_project.id


@pytest.mark.asyncio
async def test_get_other_user_task(client,setup_database,test_project,test_user,test_user2):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Test Task",
            "description": "Test Task",
            "status": "pending",
            "priority": "medium",
            "project_id": test_project.id
        }
    )
    assert response.status_code == 200
    task_id = response.json()["id"]
    response = await client.post(
        "/login",
        json={
            "email": test_user2.email,
            "password": "test12345"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get(
        f"/tasks/{task_id}",headers=headers
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


@pytest.mark.asyncio
async def test_update_task(client,setup_database,test_project,test_user):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Test Task",
            "description": "Test Task",
            "status": "pending",
            "priority": "medium",
            "project_id": test_project.id
        }
    )
    assert response.status_code == 200
    task_id = response.json()["id"]
    response = await client.patch(
        f"/tasks/{task_id}",
        headers=headers,
        json={
            "title": "Updated Task",
            "description": "Updated Task"
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["description"] == "Updated Task"



@pytest.mark.asyncio
async def test_update_task_partial(client,setup_database,test_project,test_user):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Test Task",
            "description": "Test Task",
            "status": "pending",
            "priority": "medium",
            "project_id": test_project.id
        }
    )
    assert response.status_code == 200
    task_id = response.json()["id"]
    response = await client.patch(
        f"/tasks/{task_id}",
        headers=headers,
        json={
            "title": "Updated Task",
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["description"] == "Test Task"
    assert response.json()["status"] == "pending"
    assert response.json()["priority"] == "medium"


@pytest.mark.asyncio
async def test_delete_task(client,setup_database,test_project,test_user):
    response = await client.post(
        "/login",
        json={
            "email": test_user.email,
            "password": "test1234"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Test Task",
            "description": "Test Task",
            "status": "pending",
            "priority": "medium",
            "project_id": test_project.id
        }
    )
    assert response.status_code == 200
    task_id = response.json()["id"]
    response = await client.delete(
        f"/tasks/{task_id}",
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"
    response = await client.get(
        f"/tasks/{task_id}",
        headers=headers
    )
    assert response.status_code == 404

