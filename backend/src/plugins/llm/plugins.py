import logging
import time
from typing import TYPE_CHECKING, Any

from langchain_core.prompts import ChatPromptTemplate
from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
)
from pydantic import BaseModel

from .base import IAIPlugin, LLMResponse
from .exceptions import AllProvidersFailedError, LLMNotReturnedError, LLMPermanentError
from .prompts.registry import get_prompt_provider

if TYPE_CHECKING:
    from collections.abc import Sequence

    from langchain_core.language_models import BaseChatModel

    from .prompts.base import Prompt

log = logging.getLogger(__name__)


class OpenAIPlugin[In: BaseModel, Out: BaseModel](IAIPlugin[In, Out]):
    """AI plugin backed by OpenAI-compatible endpoints with fallback."""

    def __init__(
        self,
        clients: Sequence[BaseChatModel],
        prompt_name: str,
        output_schema: type[Out],
    ) -> None:
        """Init plugin."""
        if not clients:
            raise ValueError("At least one LLM client is required")
        self._clients = clients
        self._prompt_name = prompt_name
        self._output_schema = output_schema

    async def _build_prompt(self) -> tuple[Prompt, ChatPromptTemplate]:
        """Build prompt."""
        prompt_meta = await get_prompt_provider().get(self._prompt_name)
        prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_meta.system_role_text),
            ("human", prompt_meta.human_role_text),
        ])
        return prompt_meta, prompt

    async def execute(self, payload: In) -> LLMResponse[Out]:
        """Execute plugin with payload."""
        prompt_meta, prompt = await self._build_prompt()
        return await self._ainvoke(prompt, prompt_meta, payload)

    async def _ainvoke(
        self,
        prompt: ChatPromptTemplate,
        prompt_meta: Prompt,
        payload: In,
    ) -> LLMResponse[Out]:
        """Analyze vacancy using LLM."""
        last_error: Exception | None = None
        for idx, client in enumerate(self._clients):
            try:
                structured_llm = client.with_structured_output(
                    self._output_schema,
                    include_raw=True,
                )
                pipeline = prompt | structured_llm

                start_time = time.perf_counter()
                raw_data: dict[str, Any] = await pipeline.ainvoke(payload.model_dump())  # type: ignore
                latency_ms = int((time.perf_counter() - start_time) * 1000)

                ai_message = raw_data["raw"]
                ai_result = raw_data["parsed"]

                if ai_result is None:
                    raise LLMNotReturnedError(
                        f"parsing failed: {raw_data.get('parsing_error')}"
                    )
                response_meta = ai_message.response_metadata or {}

                usage_metadata = ai_message.usage_metadata or {}
                input_tokens = usage_metadata.get("input_tokens", 0)
                output_tokens = usage_metadata.get("output_tokens", 0)
                total_tokens = usage_metadata.get("total_tokens", 0)

                return LLMResponse(
                    data=ai_result,
                    latency_ms=latency_ms,
                    prompt_name=self._prompt_name,
                    prompt_version=prompt_meta.version,
                    prompt_locale=prompt_meta.locale,
                    total_tokens=total_tokens,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    model_name=response_meta.get("model_name", "Unknown"),
                    finish_reason=response_meta.get("finish_reason", "Unknown"),
                )

            except (RateLimitError, APITimeoutError, APIConnectionError) as e:
                log.warning("LLM provider #%d transient error: %s", idx, e)
                last_error = e
                continue
            except LLMNotReturnedError as e:
                log.warning("LLM provider #%d did not return a result: %s", idx, e)
                last_error = e
                continue
            except (AuthenticationError, BadRequestError) as e:
                log.error("LLM provider #%d permanent error: %s", idx, e)
                raise LLMPermanentError(str(e)) from e
            except LLMPermanentError:
                raise
            except Exception as e:
                log.exception("LLM provider #%d unexpected error", idx)
                raise LLMPermanentError(str(e)) from e

        raise AllProvidersFailedError(str(last_error)) from last_error
