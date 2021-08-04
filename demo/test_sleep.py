import pytest

from fastapi.testclient import TestClient
from httpx import AsyncClient
from demo.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_sleep_no_context():
    async with AsyncClient(app=app, base_url="http://localhost", timeout=10) as ac:
        response = await ac.get("/sleeps/no-context")
    assert response.status_code == 200
    assert response.json() == {"msg": "Slept beautifully", "success": True}


@pytest.mark.asyncio
async def test_sleep_exceed_timeout():
    # the default of 5 seconds is longer than the timeout in the app
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get("/sleeps/with-context")

    assert response.status_code == 200
    assert response.json() == {"msg": "Slept beautifully without Cancel", "success": True}


# This test basically doesn't work because the AsyncClient does not respect the timeout when injecting app
# server into the object
# @pytest.mark.asyncio
# async def test_sleep_below_timeout():
#     # 0.1 seconds is way lower than the timeout in the app
#     with pytest.raises(httpx.ReadTimeout):
#         async with AsyncClient(app=app, base_url="http://localhost", timeout=0.1) as ac:
#             response = await ac.get("/sleeps/with-context")
