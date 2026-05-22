import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    r = await client.post("/auth/register", json={"email": "user@test.cl", "password": "pass123"})
    assert r.status_code == 201
    assert r.json()["email"] == "user@test.cl"

    r = await client.post("/auth/login", json={"email": "user@test.cl", "password": "pass123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


@pytest.mark.asyncio
async def test_duplicate_register(client):
    payload = {"email": "dup@test.cl", "password": "abc"}
    await client.post("/auth/register", json=payload)
    r = await client.post("/auth/register", json=payload)
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/auth/register", json={"email": "u@test.cl", "password": "correct"})
    r = await client.post("/auth/login", json={"email": "u@test.cl", "password": "wrong"})
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_me_requires_auth(client):
    r = await client.get("/auth/me")
    assert r.status_code == 401  # HTTPBearer returns 401 when no token


@pytest.mark.asyncio
async def test_me(client, auth_headers):
    r = await client.get("/auth/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["email"] == "test@example.com"
