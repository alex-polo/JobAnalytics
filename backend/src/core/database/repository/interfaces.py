from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence


class IBaseRepository[T, K](ABC):
    """Abstract base repository interface (Port).

    This interface defines a standard set of CRUD operations for
    entity, decoupling the application logic from specific database
    implementations (SQLAlchemy, MongoDB, etc.).
    """

    @abstractmethod
    async def get_by_id(self, id: K) -> T | None:
        """Retrieve a single entity by its primary key.

        Args:
            id: The unique identifier of the entity.

        Returns:
            The found entity instance or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, **filters: Any) -> Sequence[T]:  # noqa: ANN401
        """Retrieve a collection of entities based on provided filters.

        Args:
            **filters: Arbitrary filtering criteria

        Returns:
            A sequence of entity instances.
        """
        raise NotImplementedError

    @abstractmethod
    async def add(self, entity: T) -> T:
        """Persist a new entity to the storage.

        Args:
            entity: The domain entity instance to be created.

        Returns:
            The created entity instance, often with an assigned ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: K, **payload: Any) -> T | None:  # noqa: ANN401
        """Update an existing entity with the provided data.

        Args:
            id: The unique identifier of the entity to update.
            **payload: Key-value pairs of fields to be updated.

        Returns:
            The updated entity instance or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: K) -> K | None:
        """Remove an entity from the storage.

        Args:
            id: The unique identifier of the entity to remove.

        Returns:
            True if the entity was successfully deleted else False.
        """
        raise NotImplementedError

    async def delete_many(self, ids: Sequence[K]) -> Sequence[K]:
        """Remove multiple entities from the storage.

        Args:
            ids: The unique identifiers of the entities to remove.

        Returns:
            Sequence of successfully deleted entity IDs.
        """
        raise NotImplementedError
