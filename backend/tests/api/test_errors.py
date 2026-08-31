from typing import TYPE_CHECKING, Any

from httpx._models import Response

if TYPE_CHECKING:
    from httpx import AsyncClient, Response


async def test_error_404_path_not_found(client: AsyncClient) -> None:
    """Test request to non-existent path.

    http_exception_handler should handle this and return ErrorSchema.
    """
    non_existent_path = "/api/v1/non-existent-path"
    response: Response = await client.get(non_existent_path)

    assert response.status_code == 404

    data: dict[str, Any] = response.json()

    assert "error" in data

    error_obj: dict[str, Any] = data["error"]

    assert error_obj["code"] == "HTTP_404_ERROR"
    assert "not found" in error_obj["message"].lower()
    assert error_obj["path"] == non_existent_path
    assert error_obj["details"] is None
