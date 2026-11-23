"""OpenClone Model Intelligence Engine (MIE) — OpenAI Native HTTP Provider.

Zero-dependency HTTP client for OpenAI and OpenAI-compatible endpoints
(Groq, vLLM, OpenRouter, Together AI).
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

from src.openclone.mie.contracts import (
    BaseProvider,
    CompletionResponse,
    ProviderAuthenticationError,
    ProviderError,
    ProviderRateLimitError,
    ProviderTimeoutError,
)
from src.openclone.mie.models import ProviderTier


class OpenAIProvider(BaseProvider):
    """Zero-dependency HTTP client for OpenAI and OpenAI-compatible APIs."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        provider_id: str = "openai",
        display_name: str = "OpenAI",
        tier: ProviderTier = ProviderTier.P0_DIRECT,
    ):
        super().__init__(provider_id=provider_id, display_name=display_name, tier=tier)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = (base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")

    def is_configured(self) -> bool:
        """Return True if an API key is available or base URL is custom local."""
        return bool(self.api_key) or "localhost" in self.base_url or "127.0.0.1" in self.base_url

    def complete(
        self,
        prompt: str,
        model: str = "gpt-4o",
        options: Optional[Dict[str, Any]] = None,
    ) -> CompletionResponse:
        """Send chat completion request using standard library urllib."""
        if not self.is_configured():
            raise ProviderAuthenticationError(
                f"Missing API key for {self.display_name}. Set OPENAI_API_KEY.",
                provider_id=self.provider_id,
            )

        opts = options or {}
        temperature = opts.get("temperature", 0.2)
        max_tokens = opts.get("max_tokens", 4096)
        timeout = opts.get("timeout_s", 60.0)

        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        # Reasoning models (o1, o3-mini) do not accept custom temperature
        if model.startswith("o1") or model.startswith("o3"):
            payload.pop("temperature", None)
            payload.pop("max_tokens", None)
            payload["max_completion_tokens"] = max_tokens

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "OpenClone-MIE/1.0.0",
        }

        req = urllib.request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        start_time = time.time()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                duration_ms = (time.time() - start_time) * 1000.0
                raw = json.loads(resp.read().decode("utf-8"))

                choice = raw.get("choices", [{}])[0]
                content = choice.get("message", {}).get("content", "")
                finish_reason = choice.get("finish_reason", "stop")
                usage = raw.get("usage", {})
                prompt_tokens = usage.get("prompt_tokens", 0)
                completion_tokens = usage.get("completion_tokens", 0)

                return CompletionResponse(
                    content=content,
                    model=model,
                    provider_id=self.provider_id,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    finish_reason=finish_reason,
                    duration_ms=round(duration_ms, 2),
                    metadata={"id": raw.get("id"), "system_fingerprint": raw.get("system_fingerprint")},
                )
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            if e.code == 401 or e.code == 403:
                raise ProviderAuthenticationError(f"Authentication failed: {body}", provider_id=self.provider_id)
            elif e.code == 429:
                raise ProviderRateLimitError(f"Rate limited (429): {body}", provider_id=self.provider_id)
            else:
                raise ProviderError(f"HTTP {e.code}: {body}", provider_id=self.provider_id, status_code=e.code, retryable=(e.code >= 500))
        except urllib.error.URLError as e:
            raise ProviderTimeoutError(f"Connection error or timeout: {e.reason}", provider_id=self.provider_id)
        except Exception as e:
            raise ProviderError(f"Unexpected error: {str(e)}", provider_id=self.provider_id)

    def list_supported_models(self) -> List[str]:
        return ["gpt-4o", "gpt-4o-mini", "o1", "o3-mini"]
