import logging
from typing import TYPE_CHECKING

from sqlalchemy.dialects.postgresql import insert

from src.modules.sources.infrastructure.models import SourceORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

log = logging.getLogger(__name__)

INITIAL_SOURCES = [
    {
        "name": "HeadHunter",
        "code": "hh",
        "base_url": "https://hh.ru/search/vacancy",
        "is_active": True,
    },
    {
        "name": "Habr Career",
        "code": "habr",
        "base_url": "https://career.habr.com/vacancies",
        "is_active": True,
    },
]


async def seed_sources(async_sessionmaker: async_sessionmaker[AsyncSession]) -> None:
    """Populate sources table with initial data."""
    async with async_sessionmaker() as session:
        for source_data in INITIAL_SOURCES:
            stmt = insert(SourceORM).values(**source_data)

            stmt = stmt.on_conflict_do_update(
                index_elements=["code"],
                set_={
                    "name": stmt.excluded.name,
                    "base_url": stmt.excluded.base_url,
                    "is_active": source_data["is_active"],
                },
            )

            await session.execute(stmt)
            log.info(f"Upserted source: {source_data['code']}")

        await session.commit()
        log.info("Sources seeding completed successfully.")
