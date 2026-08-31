import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import APP_SETTINGS
from src.core.database.engine import DB_HANDLER, DatabaseHandler


def test_database_handler_initialization() -> None:
    """Check that handler correctly initializes SQLAlchemy objects."""
    assert DB_HANDLER.async_engine is not None
    assert DB_HANDLER.async_session_maker is not None


@pytest.mark.anyio
async def test_get_session_lifecycle() -> None:
    """Check that session generator works and yields correct object."""
    handler = DatabaseHandler(db_settings=APP_SETTINGS.DATABASE)

    async with handler.get_session() as session:
        assert isinstance(session, AsyncSession)
        assert session.is_active is True
        assert session.bind is handler.async_engine

        assert session.is_active is True

    await handler.dispose_engine()
