from typing import TYPE_CHECKING, Self

from src.plugins.base import ISourcePlugin

if TYPE_CHECKING:
    from src.plugins.base import ISourcePlugin


class SourcePluginRegistry:
    """Registry for source plugins."""

    _instance: Self | None = None

    def __init__(self) -> None:
        """Init registry."""
        self._plugins: dict[str, ISourcePlugin] = {}

    @classmethod
    def get_instance(cls) -> Self:
        """Get instance of registry."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register(self, source_type: str, plugin: ISourcePlugin) -> None:
        """Register plugin for source type."""
        self._plugins[source_type] = plugin

    def get(self, source_type: str) -> ISourcePlugin:
        """Get plugin by source type."""
        plugin: ISourcePlugin | None = self._plugins.get(source_type)
        if plugin is None:
            raise ValueError(f"Not found plugin for source type: {source_type}")
        return plugin

    def has(self, source_type: str) -> bool:
        """Check if plugin for source type is registered."""
        return source_type in self._plugins

    def get_all_types(self) -> list[str]:
        """Get all registered source types."""
        return list(self._plugins.keys())
