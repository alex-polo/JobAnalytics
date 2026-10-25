from typing import TYPE_CHECKING

from src.plugins.llm.prompts.providers import PyPromptProvider

if TYPE_CHECKING:
    from .base import PromptProvider


class PromptRegistry:
    """Class registry for prompt providers."""

    def __init__(self) -> None:
        """Init registry."""
        self._provider: PromptProvider = PyPromptProvider()

    def set(self, provider: PromptProvider) -> None:
        """Set prompt provider."""
        self._provider = provider

    def get(
        self,
    ) -> PromptProvider:
        """Get prompt provider."""
        return self._provider


_regitry = PromptRegistry()

get_prompt_provider = _regitry.get
set_prompt_provider = _regitry.get

__all__ = (
    "get_prompt_provider",
    "set_prompt_provider",
)
