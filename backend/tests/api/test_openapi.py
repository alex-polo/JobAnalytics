from typing import TYPE_CHECKING

from src.core.config.settings import APP_SETTINGS

if TYPE_CHECKING:
    from httpx import AsyncClient, Response


async def test_openapi_json_schema_format(client: AsyncClient) -> None:
    """Check OpenAPI JSON schema format and ErrorSchema presence."""
    url: str = APP_SETTINGS.PROJECT.openapi_url
    response: Response = await client.get(url)

    assert response.status_code == 200

    schema = response.json()

    assert schema["info"]["title"] == APP_SETTINGS.PROJECT.title

    assert "ErrorSchema" in schema["components"]["schemas"]
    assert "ErrorDetail" in schema["components"]["schemas"]


async def test_swagger_ui_is_reachable(client: AsyncClient) -> None:
    """Check that Swagger UI (HTML) page is reachable."""
    url: str = APP_SETTINGS.PROJECT.docs_url
    response: Response = await client.get(url)

    assert response.status_code == 200
    assert "swagger-ui" in response.text.lower()
