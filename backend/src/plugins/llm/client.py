from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI

from src.core.config.classes import LLMSClientConfig

if TYPE_CHECKING:
    from src.core.config import LLMSClientConfig, LLMSettings


def build_client(cfg: LLMSClientConfig, settings: LLMSettings) -> ChatOpenAI:
    """Build ChatOpenAI for one OpenAI-compatible endpoint."""
    return ChatOpenAI(
        model=cfg.model_name,
        base_url=cfg.base_url,
        api_key=cfg.api_key,
        temperature=settings.temperature,
        timeout=settings.timeout_seconds,
        max_retries=settings.max_retries,
    )


def build_clients(settings: LLMSettings) -> list[ChatOpenAI]:
    """Build clients ordered by priority."""
    ordered: list[LLMSClientConfig] = sorted(
        settings.openai_endpoints, key=lambda p: p.priority
    )
    return [build_client(cfg=cfg, settings=settings) for cfg in ordered]
