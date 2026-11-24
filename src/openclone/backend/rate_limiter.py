"""OpenClone Rate Limiting and Traffic Management Engine.

Implements Token Bucket, Sliding Window Counter, and Fixed Window algorithms
with differentiated endpoint policies, standard headers, and fail-safe strategies.
"""
from __future__ import annotations

import enum
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


class RateLimitAlgorithm(str, enum.Enum):
    FIXED_WINDOW = "FIXED_WINDOW"
    SLIDING_WINDOW_COUNTER = "SLIDING_WINDOW_COUNTER"
    TOKEN_BUCKET = "TOKEN_BUCKET"
    LEAKY_BUCKET = "LEAKY_BUCKET"


@dataclass
class RateLimitPolicy:
    """Configurable rate limiting policy for a specific tier or endpoint."""
    name: str
    limit: int
    window_seconds: int
    algorithm: RateLimitAlgorithm = RateLimitAlgorithm.SLIDING_WINDOW_COUNTER
    burst_capacity: Optional[int] = None

    def __post_init__(self):
        if self.burst_capacity is None:
            self.burst_capacity = self.limit


@dataclass
class RateLimitDecision:
    """Evaluation result for an incoming request under rate limiting policy."""
    allowed: bool
    limit: int
    remaining: int
    reset_after_seconds: float
    retry_after_seconds: Optional[int] = None
    headers: Dict[str, str] = field(default_factory=dict)


class RateLimiter:
    """In-memory deterministic rate limiter supporting multiple algorithms and client keys."""

    # Default Canonical Endpoint Policies
    POLICIES: Dict[str, RateLimitPolicy] = {
        "auth_login": RateLimitPolicy(
            name="auth_login", limit=5, window_seconds=60,
            algorithm=RateLimitAlgorithm.SLIDING_WINDOW_COUNTER, burst_capacity=5
        ),
        "auth_password_reset": RateLimitPolicy(
            name="auth_password_reset", limit=3, window_seconds=300,
            algorithm=RateLimitAlgorithm.SLIDING_WINDOW_COUNTER, burst_capacity=3
        ),
        "api_search": RateLimitPolicy(
            name="api_search", limit=30, window_seconds=60,
            algorithm=RateLimitAlgorithm.TOKEN_BUCKET, burst_capacity=45
        ),
        "api_standard": RateLimitPolicy(
            name="api_standard", limit=100, window_seconds=60,
            algorithm=RateLimitAlgorithm.SLIDING_WINDOW_COUNTER, burst_capacity=120
        ),
        "api_ai_inference": RateLimitPolicy(
            name="api_ai_inference", limit=15, window_seconds=60,
            algorithm=RateLimitAlgorithm.TOKEN_BUCKET, burst_capacity=20
        ),
        "expensive_export": RateLimitPolicy(
            name="expensive_export", limit=5, window_seconds=300,
            algorithm=RateLimitAlgorithm.FIXED_WINDOW, burst_capacity=5
        ),
    }

    def __init__(self):
        # Sliding window / fixed window store: client_key -> list of timestamp floats
        self._request_timestamps: Dict[str, List[float]] = {}
        # Token bucket store: client_key -> (current_tokens: float, last_updated: float)
        self._token_buckets: Dict[str, Tuple[float, float]] = {}

    def is_allowed(
        self,
        client_key: str,
        policy_name: str = "api_standard",
        custom_policy: Optional[RateLimitPolicy] = None,
        now: Optional[float] = None,
    ) -> RateLimitDecision:
        """Evaluate if request from client_key is allowed under the policy."""
        current_time = now if now is not None else time.time()
        policy = custom_policy or self.POLICIES.get(policy_name, self.POLICIES["api_standard"])

        key = f"{client_key}:{policy.name}"

        if policy.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
            return self._evaluate_token_bucket(key, policy, current_time)
        elif policy.algorithm == RateLimitAlgorithm.FIXED_WINDOW:
            return self._evaluate_fixed_window(key, policy, current_time)
        else:
            return self._evaluate_sliding_window(key, policy, current_time)

    def _evaluate_sliding_window(
        self, key: str, policy: RateLimitPolicy, now: float
    ) -> RateLimitDecision:
        window_start = now - policy.window_seconds
        timestamps = self._request_timestamps.get(key, [])
        # Evict timestamps outside active sliding window
        valid_timestamps = [t for t in timestamps if t > window_start]

        if len(valid_timestamps) < policy.limit:
            valid_timestamps.append(now)
            self._request_timestamps[key] = valid_timestamps
            remaining = policy.limit - len(valid_timestamps)
            reset_after = max(0.0, policy.window_seconds - (now - valid_timestamps[0]))

            headers = {
                "RateLimit-Limit": str(policy.limit),
                "RateLimit-Remaining": str(remaining),
                "RateLimit-Reset": str(int(reset_after)),
            }
            return RateLimitDecision(
                allowed=True,
                limit=policy.limit,
                remaining=remaining,
                reset_after_seconds=reset_after,
                headers=headers,
            )
        else:
            self._request_timestamps[key] = valid_timestamps
            oldest = valid_timestamps[0]
            retry_after = max(1, int(policy.window_seconds - (now - oldest)))

            headers = {
                "RateLimit-Limit": str(policy.limit),
                "RateLimit-Remaining": "0",
                "RateLimit-Reset": str(retry_after),
                "Retry-After": str(retry_after),
            }
            return RateLimitDecision(
                allowed=False,
                limit=policy.limit,
                remaining=0,
                reset_after_seconds=float(retry_after),
                retry_after_seconds=retry_after,
                headers=headers,
            )

    def _evaluate_token_bucket(
        self, key: str, policy: RateLimitPolicy, now: float
    ) -> RateLimitDecision:
        capacity = float(policy.burst_capacity or policy.limit)
        fill_rate = policy.limit / policy.window_seconds  # tokens per second

        if key not in self._token_buckets:
            tokens, last_refill = capacity, now
        else:
            tokens, last_refill = self._token_buckets[key]
            # Refill tokens proportional to elapsed time
            elapsed = max(0.0, now - last_refill)
            tokens = min(capacity, tokens + (elapsed * fill_rate))
            last_refill = now

        if tokens >= 1.0:
            tokens -= 1.0
            self._token_buckets[key] = (tokens, last_refill)
            remaining = int(tokens)
            reset_after = (capacity - tokens) / fill_rate

            headers = {
                "RateLimit-Limit": str(policy.limit),
                "RateLimit-Remaining": str(remaining),
                "RateLimit-Reset": str(int(reset_after)),
            }
            return RateLimitDecision(
                allowed=True,
                limit=policy.limit,
                remaining=remaining,
                reset_after_seconds=reset_after,
                headers=headers,
            )
        else:
            self._token_buckets[key] = (tokens, last_refill)
            required = 1.0 - tokens
            retry_after = max(1, int(required / fill_rate) + 1)

            headers = {
                "RateLimit-Limit": str(policy.limit),
                "RateLimit-Remaining": "0",
                "RateLimit-Reset": str(retry_after),
                "Retry-After": str(retry_after),
            }
            return RateLimitDecision(
                allowed=False,
                limit=policy.limit,
                remaining=0,
                reset_after_seconds=float(retry_after),
                retry_after_seconds=retry_after,
                headers=headers,
            )

    def _evaluate_fixed_window(
        self, key: str, policy: RateLimitPolicy, now: float
    ) -> RateLimitDecision:
        window_id = int(now // policy.window_seconds)
        window_key = f"{key}:{window_id}"
        count = len(self._request_timestamps.get(window_key, []))

        reset_after = float((window_id + 1) * policy.window_seconds - now)

        if count < policy.limit:
            stamps = self._request_timestamps.get(window_key, [])
            stamps.append(now)
            self._request_timestamps[window_key] = stamps
            remaining = policy.limit - (count + 1)
            headers = {
                "RateLimit-Limit": str(policy.limit),
                "RateLimit-Remaining": str(remaining),
                "RateLimit-Reset": str(int(reset_after)),
            }
            return RateLimitDecision(
                allowed=True,
                limit=policy.limit,
                remaining=remaining,
                reset_after_seconds=reset_after,
                headers=headers,
            )
        else:
            retry_after = max(1, int(reset_after))
            headers = {
                "RateLimit-Limit": str(policy.limit),
                "RateLimit-Remaining": "0",
                "RateLimit-Reset": str(retry_after),
                "Retry-After": str(retry_after),
            }
            return RateLimitDecision(
                allowed=False,
                limit=policy.limit,
                remaining=0,
                reset_after_seconds=reset_after,
                retry_after_seconds=retry_after,
                headers=headers,
            )
