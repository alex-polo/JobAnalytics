from typing import TYPE_CHECKING

import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


@pytest.fixture(scope="module")
async def client() -> AsyncGenerator[AsyncClient]:
    """AsyncClient for testing FastAPI application."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as ac:
        yield ac


# Example of a second client for authorized requests if needed
@pytest.fixture(scope="module")
async def auth_client(client: AsyncClient) -> AsyncGenerator[AsyncClient]:  # noqa: RUF029
    """Client with pre-set authorization token."""
    client.headers.update({"Authorization": "Bearer fake-token"})
    yield client
