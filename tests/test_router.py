import pytest
from httpx import AsyncClient, ASGITransport
from main import app



# async def test_lol():
#     assert 1 == 1

@pytest.mark.asyncio
async def test_add_date(async_client):
    response = await async_client.post("/table/add_date/", json={"path": "test_path", "date": "2023-07-30"})
    assert response.status_code == 200
    # data = response.json()
    # assert data["ok"] is True
    # assert "date_id" in data

# @pytest.mark.asyncio
# async def test_get_date(async_client):
#     response = await async_client.get("/table/get_date/")
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)

# import pytest
# from httpx import AsyncClient
# from main import app
#
# @pytest.fixture(scope="module")
# async def async_client():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         yield client
#
# @pytest.mark.asyncio
# async def test_add_date(async_client):
#     response = await async_client.post("/table/add_date/", json={"path": "test_path", "date": "2023-07-30"})
#     assert response.status_code == 200
#     assert response.json()["ok"] is True
#     assert "date_id" in response.json()
#
# @pytest.mark.asyncio
# async def test_get_date(async_client):
#     response = await async_client.get("/table/get_date/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)