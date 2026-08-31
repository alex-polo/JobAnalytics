from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel
from sqlalchemy import Result, delete, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert

from src.core.database import Base

from .interfaces import IBaseRepository

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession

ORM = TypeVar("ORM", bound=Base)  # O - SQLAlchemy Model (ORM)
T = TypeVar("T", bound=BaseModel)  # T - Domain Entity (Pydantic)
K = TypeVar("K")  # K - ID type


class SqlAlchemyBaseRepository[T, ORM, K](IBaseRepository[T, K]):
    """Base implementation for SQLAlchemy repositories."""

    def __init__(
        self, session: AsyncSession, model_orm: type[ORM], entity_class: type[T]
    ) -> None:
        """_summary."""
        self._session = session
        self._model_orm = model_orm
        self._entity_class = entity_class

    async def add(self, entity: T) -> T:
        """Persist a new entity to the storage."""
        data = entity.model_dump(exclude={"id"} if entity.id is None else set())  # type: ignore
        obj: ORM = self._model_orm(**data)
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return self._to_domain(obj)

    def _to_domain(self, orm_obj: ORM) -> T:
        """Convert ORM model to Domain Entity."""
        return self._entity_class.model_validate(orm_obj)  # type: ignore

    async def get_by_id(self, id: K) -> T | None:
        """Retrieve a single entity by its primary key."""
        query = select(self._model_orm).filter_by(id=id)
        result = await self._session.execute(query)
        obj: ORM | None = result.scalar_one_or_none()
        return self._to_domain(obj) if obj else None

    async def get_all(self, **filters: Any) -> Sequence[T]:  # noqa: ANN401
        """Retrieve a collection of entities on provided filters."""
        query = select(self._model_orm).filter_by(**filters)
        result = await self._session.execute(query)
        return [self._to_domain(obj) for obj in result.scalars().all()]

    async def update(self, id: K, **payload: Any) -> T | None:  # noqa: ANN401
        """Update an existing entity with the provided data."""
        if not payload:
            return await self.get_by_id(id)

        stmt = (
            update(self._model_orm)
            .filter_by(id=id)
            .values(**payload)
            .returning(self._model_orm)
        )
        result = await self._session.execute(stmt)
        obj = result.scalar_one_or_none()
        return self._to_domain(obj) if obj else None

    async def delete(self, id: K) -> K | None:
        """Delete an entity from the storage."""
        stmt = delete(self._model_orm).filter_by(id=id).returning(self._model_orm.id)  # type: ignore
        deleted_id: K | None = (await self._session.execute(stmt)).scalar_one_or_none()
        return deleted_id

    async def delete_many(self, ids: Sequence[K]) -> Sequence[K]:
        """Delete multiple records by IDs.

        Args:
            ids: List of record identifiers.

        Returns:
            Sequence of successfully deleted record IDs.
        """
        stmt = (
            delete(self._model_orm)
            .where(self._model_orm.id.in_(ids))  # type: ignore
            .returning(self._model_orm.id)  # type: ignore
        )
        result = await self._session.execute(stmt)
        deleted_ids = result.scalars().all()
        return list(deleted_ids)

    async def upsert(
        self,
        entity: T,
        index_elements: list[str],
        exclude_update: list[str] | None = None,
    ) -> K:
        """Perform an UPSERT (Insert or Update) operation.

        Args:
        entity: The domain entity to upsert.
        index_elements: Columns to check for conflicts.
        exclude_update: Columns that should NOT be updated on conflict.
        """
        data = entity.model_dump(  # type: ignore
            exclude={"id"} if entity.id is None else set(),  # type: ignore
            exclude_none=True,
        )
        stmt = pg_insert(self._model_orm).values(**data)

        forbidden_to_update: set[str] = set(index_elements) | set(exclude_update or [])

        update_data = {k: v for k, v in data.items() if k not in forbidden_to_update}

        if not update_data:
            if not index_elements:
                raise ValueError("Index elements cannot be empty for UPSERT operation")

            idx_element = index_elements[0]
            update_data = {idx_element: stmt.excluded[idx_element]}

        stmt = stmt.on_conflict_do_update(
            index_elements=index_elements,
            set_=update_data,
        )

        result: Result[tuple[K]] = await self._session.execute(
            stmt.returning(self._model_orm.id)  # type: ignore
        )

        return result.scalar_one()
