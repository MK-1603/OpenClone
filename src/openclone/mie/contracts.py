"""OpenClone Model Intelligence Engine (MIE) — Provider Abstraction Contract.

Defines the canonical BaseProvider interface, response containers, and
standard exception hierarchy for all LLM providers and inference platforms.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from src.openclone.mie.models import ModelRecord, ProviderTier


class ProviderError(Exception):
    """Base exception for provider communication errors."""
    def __init__(self, message: str, provider_id: str, status_code: Optional[int] = None, retryable: bool = False):
        super().__init__(f"[{provider_id}] {message} (status: {status_code})")
        self.provider_id = provider_id
        self.status_code = status_code
        self.retryable = retryable


class ProviderRateLimitError(ProviderError):
    """Raised when an HTTP 429 rate limit is encountered."""
    def __init__(self, message: str, provider_id: str, retry_after_s: Optional[float] = None):
        super().__init__(message, provider_id, status_code=429, retryable=True)
        self.retry_after_s = retry_after_s


class ProviderAuthenticationError(ProviderError):
    """Raised when credentials or tokens are invalid (HTTP 401/403)."""
    def __init__(self, message: str, provider_id: str):
        super().__init__(message, provider_id, status_code=401, retryable=False)


class ProviderTimeoutError(ProviderError):
    """Raised when an inference connection or read times out."""
    def __init__(self, message: str, provider_id: str):
        super().__init__(message, provider_id, status_code=408, retryable=True)


class CircuitBreakerOpenError(ProviderError):
    """Raised when a request is blocked because the provider circuit breaker is OPEN."""
    def __init__(self, provider_id: str, cooldown_remaining_s: float):
        super().__init__(
            f"Circuit breaker is OPEN. Cooldown remaining: {cooldown_remaining_s:.1f}s",
            provider_id,
            status_code=503,
            retryable=False,
        )
        self.cooldown_remaining_s = cooldown_remaining_s


@dataclass
class CompletionResponse:
    """Standardized completion response container across all providers."""
    content: str
    model: str
    provider_id: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    finish_reason: str = "stop"
    duration_ms: float = 0.0
    cost_usd: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseProvider(ABC):
    """Canonical abstract base class for all OpenClone model API providers."""

    def __init__(self, provider_id: str, display_name: str, tier: ProviderTier):
        self.provider_id = provider_id
        self.display_name = display_name
        self.tier = tier

    @abstractmethod
    def is_configured(self) -> bool:
        """Check whether the necessary API keys, environment variables, or endpoints exist."""
        pass

    @abstractmethod
    def complete(
        self,
        prompt: str,
        model: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> CompletionResponse:
        """Execute a text/code completion against the provider.
        
        Must raise ProviderError or subclasses on failure.
        """
        pass

    @abstractmethod
    def list_supported_models(self) -> List[str]:
        """Return list of supported model identifiers."""
        pass

    def estimate_cost(self, prompt_tokens: int, completion_tokens: int, model: str) -> float:
        """Default fallback cost estimator (overridden by specific model pricing)."""
        return 0.0
