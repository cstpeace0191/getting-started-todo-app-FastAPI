import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from src.main import app

ITEMS = [
    {"id": "1", "name": "Done item", "completed": True},
    {"id": "2", "name": "Open item", "completed": False},
    {"id": "3", "name": "Another done item", "completed": True},
]

COMPLETED_ITEMS = [item for item in ITEMS if item["completed"]]
INCOMPLETE_ITEMS = [item for item in ITEMS if not item["completed"]]


@pytest.mark.asyncio
async def test_get_items_filters_completed_true():
    with patch("src.persistence.get_items", new_callable=AsyncMock, return_value=ITEMS):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/items", params={"completed": "true"})

        assert response.status_code == 200
        assert response.json() == COMPLETED_ITEMS


@pytest.mark.asyncio
async def test_get_items_filters_completed_false():
    with patch("src.persistence.get_items", new_callable=AsyncMock, return_value=ITEMS):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/items", params={"completed": "false"})

        assert response.status_code == 200
        assert response.json() == INCOMPLETE_ITEMS


@pytest.mark.asyncio
async def test_get_items_without_filter_returns_all_items():
    with patch("src.persistence.get_items", new_callable=AsyncMock, return_value=ITEMS):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/items")

        assert response.status_code == 200
        assert response.json() == ITEMS


@pytest.mark.asyncio
async def test_get_items_invalid_completed_value_returns_422():
    with patch("src.persistence.get_items", new_callable=AsyncMock, return_value=ITEMS):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/items", params={"completed": "maybe"})

        assert response.status_code == 422
