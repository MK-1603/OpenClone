"""OpenClone Model Intelligence Engine (MIE) — High Availability Engine.

Implements tri-state circuit breakers (CLOSED, OPEN, HALF_OPEN),
bounded exponential backoff with full jitter, same-model provider failover,
and model-level fallback chain resolution.
"""

from __future__ import annotations

import random
import time
from typing import Dict, List, Optional, Tuple

from src.openclone.mie.contracts import CircuitBreakerOpenError
from src.openclone.mie.models import CircuitState, HealthStatus, ModelRecord


class CircuitBreaker:
    """Tri-state circuit breaker tracking failure rates for a provider or model."""

    def __init__(
        self,
        identifier: str,
        failure_threshold: int = 3,
        cooldown_seconds: float = 30.0,
        half_open_successes_needed: int = 1,
    ):
        self.identifier = identifier
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self.half_open_successes_needed = half_open_successes_needed

        self._state = CircuitState.CLOSED
        self._consecutive_failures = 0
        self._consecutive_successes = 0
        self._total_failures = 0
        self._total_successes = 0
        self._last_failure_time: Optional[float] = None
        self._last_success_time: Optional[float] = None
        self._tripped_at: Optional[float] = None

    @property
    def state(self) -> CircuitState:
        """Dynamically evaluate circuit state based on current time and cooldown."""
        if self._state == CircuitState.OPEN and self._tripped_at:
            elapsed = time.time() - self._tripped_at
            if elapsed >= self.cooldown_seconds:
                self._state = CircuitState.HALF_OPEN
        return self._state

    def can_execute(self) -> bool:
        """Return True if requests are permitted to pass to the target."""
        current_state = self.state
        if current_state == CircuitState.CLOSED:
            return True
        if current_state == CircuitState.HALF_OPEN:
            return True
        return False

    def check_execution_or_raise(self) -> None:
        """Raise CircuitBreakerOpenError if circuit breaker is OPEN."""
        if not self.can_execute():
            remaining = 0.0
            if self._tripped_at:
                elapsed = time.time() - self._tripped_at
                remaining = max(0.0, self.cooldown_seconds - elapsed)
            raise CircuitBreakerOpenError(provider_id=self.identifier, cooldown_remaining_s=remaining)

    def record_success(self) -> None:
        """Register a successful request, resetting failures or transitioning HALF_OPEN -> CLOSED."""
        self._total_successes += 1
        self._consecutive_failures = 0
        self._consecutive_successes += 1
        self._last_success_time = time.time()

        if self._state == CircuitState.HALF_OPEN:
            if self._consecutive_successes >= self.half_open_successes_needed:
                self._state = CircuitState.CLOSED
                self._tripped_at = None

    def record_failure(self) -> None:
        """Register a failed request, tripping circuit to OPEN if threshold reached."""
        self._total_failures += 1
        self._consecutive_successes = 0
        self._consecutive_failures += 1
        self._last_failure_time = time.time()

        if self._state == CircuitState.HALF_OPEN:
            # Immediate trip back to OPEN on probe failure with doubled cooldown
            self._state = CircuitState.OPEN
            self._tripped_at = time.time()
            self.cooldown_seconds = min(120.0, self.cooldown_seconds * 1.5)
        elif self._state == CircuitState.CLOSED:
            if self._consecutive_failures >= self.failure_threshold:
                self._state = CircuitState.OPEN
                self._tripped_at = time.time()

    def get_health_status(self) -> HealthStatus:
        """Return structured diagnostic health status."""
        return HealthStatus(
            provider_id=self.identifier,
            circuit_state=self.state,
            failure_count=self._total_failures,
            success_count=self._total_successes,
            consecutive_failures=self._consecutive_failures,
            last_failure_time=self._last_failure_time,
            last_success_time=self._last_success_time,
            is_available=self.can_execute(),
        )


class HighAvailabilityEngine:
    """Coordinates circuit breakers, failover targets, and fallback strategies."""

    # Canonical same-model cross-provider failover mapping
    PROVIDER_FAILOVER_MAP: Dict[str, List[str]] = {
        "anthropic": ["bedrock", "vertex", "openrouter"],
        "openai": ["azure", "openrouter"],
        "gemini": ["vertex", "openrouter"],
        "xai": ["openrouter"],
        "ollama": ["vllm"],
    }

    def __init__(self):
        self._provider_breakers: Dict[str, CircuitBreaker] = {}

    def get_circuit_breaker(self, provider_id: str) -> CircuitBreaker:
        """Get or initialize the circuit breaker for a provider."""
        if provider_id not in self._provider_breakers:
            self._provider_breakers[provider_id] = CircuitBreaker(identifier=provider_id)
        return self._provider_breakers[provider_id]

    def get_all_health(self) -> List[HealthStatus]:
        """Return diagnostic health statuses across all tracked providers."""
        return [cb.get_health_status() for cb in self._provider_breakers.values()]

    def get_same_model_failover(self, provider_id: str) -> List[str]:
        """Return ordered alternative providers hosting the exact same model."""
        return self.PROVIDER_FAILOVER_MAP.get(provider_id, ["openrouter"])

    @staticmethod
    def calculate_backoff(attempt: int, base_delay: float = 0.5, max_delay: float = 10.0) -> float:
        """Calculate bounded exponential backoff with full jitter."""
        temp = min(max_delay, base_delay * (2 ** attempt))
        return random.uniform(0.0, temp)
