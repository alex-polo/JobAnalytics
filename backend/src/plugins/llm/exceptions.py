from src.plugins.exceptions import BasePluginError


class BaseLLMError(BasePluginError):
    """Base LLM error."""


class LLMTimeoutError(BaseLLMError):
    """LLM timeout error."""


class LMResponseError(BaseLLMError):
    """LLM response error."""


class LLMTransientError(BaseLLMError):
    """Retryable: rate limit, timeout, connection."""


class LLMPermanentError(BaseLLMError):
    """Non-retryable: auth, bad request, invalid response."""


class LLMNotReturnedError(BaseLLMError):
    """LLM not returned error."""


class AllProvidersFailedError(BaseLLMError):
    """All providers failed."""
