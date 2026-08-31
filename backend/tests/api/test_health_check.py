"""Tests for API endpoints."""

from typing import TYPE_CHECKING

from fastapi import status

if TYPE_CHECKING:
    from httpx import AsyncClient, Response


async def test_health_check(client: AsyncClient) -> None:
    """Test health check endpoint."""
    response: Response = await client.get("/api/v1/utils/health-check")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}
