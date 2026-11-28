"""OpenClone Model Intelligence Engine (MIE) — xAI Native HTTP Provider.

Zero-dependency HTTP client for xAI Grok API (grok-2, grok-2-mini).
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


class XAIProvider(BaseProvider):
    """Zero-dependency HTTP client for xAI Grok API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        super().__init__(
            provider_id="xai",
            display_name="xAI Grok",
            tier=ProviderTier.P0_DIRECT,
        )
        self.api_key = api_key or os.getenv("XAI_API_KEY", "")
        self.base_url = (base_url or "https://api.x.ai/v1").rstrip("/")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def complete(
        self,
        prompt: str,
        model: str = "grok-2",
        options: Optional[Dict[str, Any]] = None,
    ) -> CompletionResponse:
        if not self.is_configured():
            raise ProviderAuthenticationError(
                "Missing xAI API key. Set XAI_API_KEY.",
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
                usage = raw.get("usage", {})

                return CompletionResponse(
                    content=content,
                    model=model,
                    provider_id=self.provider_id,
                    prompt_tokens=usage.get("prompt_tokens", 0),
                    completion_tokens=usage.get("completion_tokens", 0),
                    finish_reason=choice.get("finish_reason", "stop"),
                    duration_ms=round(duration_ms, 2),
                    metadata={"id": raw.get("id")},
                )
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            if e.code in {401, 403}:
                raise ProviderAuthenticationError(f"xAI auth error: {body}", provider_id=self.provider_id)
            elif e.code == 429:
                raise ProviderRateLimitError(f"xAI rate limited: {body}", provider_id=self.provider_id)
            else:
                raise ProviderError(f"xAI HTTP {e.code}: {body}", provider_id=self.provider_id, status_code=e.code, retryable=(e.code >= 500))
        except urllib.error.URLError as e:
            raise ProviderTimeoutError(f"xAI connection error: {e.reason}", provider_id=self.provider_id)
        except Exception as e:
            raise ProviderError(f"Unexpected error: {str(e)}", provider_id=self.provider_id)

    def list_supported_models(self) -> List[str]:
        return ["grok-2", "grok-2-mini"]
