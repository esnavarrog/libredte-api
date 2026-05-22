import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.models import User
from app.auth.service import create_access_token, hash_password
from app.db import Base, get_db
from app.main import app

TEST_DB = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(TEST_DB)
TestSession = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_db() -> AsyncSession:  # type: ignore[return]
    async with TestSession() as session:
        yield session


@pytest.fixture
async def client():
    app.dependency_overrides[get_db] = override_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
async def auth_headers(client):
    async with TestSession() as session:
        user = User(email="test@example.com", hashed_password=hash_password("secret"))
        session.add(user)
        await session.commit()
    token = create_access_token("test@example.com")
    return {"Authorization": f"Bearer {token}"}
