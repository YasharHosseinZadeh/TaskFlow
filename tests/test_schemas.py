from models.task import TaskPriority,TaskStatus
from schemas.user import UserCreate
from schemas.task import TaskCreate
import pytest
from pydantic import ValidationError

def test_user_create():
    user = UserCreate(
        name="Alex",
        email="alex@example.com",
        password= "mypassword123"
    )
    assert user.name == "Alex"
    assert user.email == "alex@example.com"
    assert user.password == "mypassword123"


def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        user = UserCreate(
            name="Alex",
            email="not-an-email",
            password= "mypassword123"
        )


def test_user_create_short_password():
    with pytest.raises(ValidationError):
        user = UserCreate(
            name="Alex",
            email="alex@example.com",
            password= "abc"
        )


def test_task_create_defaults():
    task = TaskCreate(
        title="title",
        project_id= 1
    )
    assert task.title == "title"
    assert task.project_id == 1
    assert task.priority == TaskPriority.MEDIUM
    assert task.status == TaskStatus.PENDING


def test_task_create_empty_title():
    with pytest.raises(ValidationError):
        user = TaskCreate(
            title="",
            project_id=1
        )
