import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.security import hash_password
from database import Base, get_db
from main import app
from models.project import Project
from models.user import User

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL)

TestingSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def setup_database():
    app.dependency_overrides[get_db] = override_get_db

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture
async def test_user():
    async with TestingSessionLocal() as session:
        user = User(
            name="test",
            email="test@example.com",
            password_hash=hash_password("test1234"),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest_asyncio.fixture
async def test_user2():
    async with TestingSessionLocal() as session:
        user = User(
            name="test2",
            email="test2@example.com",
            password_hash=hash_password("test12345"),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest_asyncio.fixture
async def test_project(test_user):
    async with TestingSessionLocal() as session:
        project = Project(
            name="test",
            description="test",
            owner_id=test_user.id,
        )
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project
