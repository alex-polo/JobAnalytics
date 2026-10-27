import logging
from typing import TYPE_CHECKING

from langchain_gigachat.chat_models import GigaChat
from langchain_openai import ChatOpenAI

from src.core.config import LLMSClientConfig, LLMSettings

if TYPE_CHECKING:
    from src.core.config import LLMSClientConfig, LLMSettings

log = logging.getLogger(__name__)


def build_client(cfg: LLMSClientConfig, settings: LLMSettings) -> ChatOpenAI | GigaChat:
    """Build ChatOpenAI for one OpenAI-compatible endpoint."""
    log.info(cfg)
    if cfg.provider == "gigachat":
        return GigaChat(
            model=cfg.model_name,
            base_url=cfg.base_url,
            scope=cfg.scope,
            credentials=cfg.api_key.get_secret_value(),
            temperature=settings.temperature,
            timeout=settings.timeout_seconds,
            max_retries=settings.max_retries,
            verify_ssl_certs=cfg.verify_ssl,
        )
    elif cfg.provider == "openai":
        return ChatOpenAI(
            model=cfg.model_name,
            base_url=cfg.base_url,
            api_key=cfg.api_key,
            temperature=settings.temperature,
            timeout=settings.timeout_seconds,
            max_retries=settings.max_retries,
        )
    else:
        raise ValueError(f"Unknown provider name: {cfg.model_name}")


def build_clients(settings: LLMSettings) -> list[ChatOpenAI | GigaChat]:
    """Build clients ordered by priority."""
    ordered: list[LLMSClientConfig] = sorted(
        settings.openai_endpoints, key=lambda p: p.priority
    )
    return [build_client(cfg=cfg, settings=settings) for cfg in ordered]
