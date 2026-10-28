import jwt
from core.security import (hash_password, verify_password, create_access_token,
SECRET_KEY,decode_access_token
                           )
from models.task import TaskPriority,TaskStatus
from schemas.user import UserCreate
from schemas.task import TaskCreate
import pytest
from pydantic import ValidationError
from datetime import datetime, timedelta,timezone



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


def test_functions_password():
    password = "test1234"
    wrong_password = "TEst1234"
    hashed_password= hash_password(password)
    assert verify_password(password, hashed_password)
    assert not verify_password(wrong_password, hashed_password)



def test_create_access_token():
    user_id = 1
    token = create_access_token(user_id)
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"]
   )
    assert payload["sub"] == str(user_id)
    assert payload["exp"] is not None


def test_decode_access_token():
    user_id = 1
    token = create_access_token(user_id)
    result = decode_access_token(token)
    assert result["sub"] == str(user_id)
    assert result["exp"] is not None


def test_decode_access_invalid_token():
    token = "shgfjwfwfiwwwbwy2327hjb27ef"
    with pytest.raises(ValueError):
        result = decode_access_token(token)


def test_decode_access_expired_token():
    user_id = 1
    expire = datetime.now(timezone.utc) - timedelta(minutes=30)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    with pytest.raises(ValueError):
         decode_access_token(token)
