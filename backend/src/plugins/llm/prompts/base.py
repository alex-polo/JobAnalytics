from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Prompt:
    """Promt plus metadata."""

    system_role_text: str
    human_role_text: str
    version: str
    locale: str = "ru"


class PromptProvider(Protocol):
    """Interface for LLM prompt provider."""

    async def get(self, name: str) -> Prompt:
        """Return prompt by name."""
        ...
