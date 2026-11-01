from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

In = TypeVar("In", bound=BaseModel)
Out = TypeVar("Out", bound=BaseModel)


class LLMResponse[Out](BaseModel, frozen=True):
    """Результат LLM + метрики."""

    data: Out
    prompt_name: str
    prompt_version: str | None
    prompt_locale: str | None
    total_tokens: int
    latency_ms: int
    input_tokens: int
    output_tokens: int
    model_name: str
    finish_reason: str


class IAIPlugin[In, Out](ABC):
    """Base class for AI plugins."""

    @abstractmethod
    async def execute(self, payload: In) -> LLMResponse[Out]:
        """Execute plugin with payload."""
        ...
