from src.core.config.settings import APP_SETTINGS
from src.modules.matching_vacancy.domain import (
    AIPluginResumeMatchOutput,
    ResumeMatchInput,
)
from src.plugins.llm.client import build_clients
from src.plugins.llm.plugins import OpenAIPlugin


class MatchingPlugin(OpenAIPlugin[ResumeMatchInput, AIPluginResumeMatchOutput]):
    """Matching plugin."""

    def __init__(self) -> None:
        """Init plugin."""
        super().__init__(
            clients=build_clients(APP_SETTINGS.LLM_SETTINGS),
            prompt_name="resume_match",
            output_schema=AIPluginResumeMatchOutput,
        )
