import importlib
from typing import Final

from .base import Prompt, PromptProvider

_PROMPTS_PACKAGE: Final[str] = "src.plugins.llm.prompts"


class PyPromptProvider(PromptProvider):
    """Promt provider from Python module <package>.<name>.."""

    def __init__(self, package: str = _PROMPTS_PACKAGE) -> None:
        """Init prompt provider."""
        self._package = package

    async def get(self, name: str) -> Prompt:
        """Return prompt by name into package."""
        module = importlib.import_module(f"{self._package}.{name}")
        try:
            return Prompt(
                system_role_text=module.SYSTEM_PROMPT,
                human_role_text=module.HUMAN_PROMPT,
                version=getattr(module, "PROMPT_VERSION", "1"),
                locale=getattr(module, "PROMPT_LOCALE", "ru"),
            )
        except AttributeError as e:
            raise KeyError(f"PROMPT not found in {name}") from e
