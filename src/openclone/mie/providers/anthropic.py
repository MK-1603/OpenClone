"""OpenClone Model Intelligence Engine (MIE) — Anthropic Native HTTP Provider.

Zero-dependency HTTP client for Anthropic Messages API (Claude 3.7 / 3.5 Sonnet & Haiku).
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


class AnthropicProvider(BaseProvider):
    """Zero-dependency HTTP client for Anthropic Messages API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        super().__init__(
            provider_id="anthropic",
            display_name="Anthropic",
            tier=ProviderTier.P0_DIRECT,
        )
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        self.base_url = (base_url or "https://api.anthropic.com/v1").rstrip("/")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def complete(
        self,
        prompt: str,
        model: str = "claude-3-5-sonnet-20241022",
        options: Optional[Dict[str, Any]] = None,
    ) -> CompletionResponse:
        if not self.is_configured():
            raise ProviderAuthenticationError(
                "Missing Anthropic API key. Set ANTHROPIC_API_KEY.",
                provider_id=self.provider_id,
            )

        opts = options or {}
        max_tokens = opts.get("max_tokens", 4096)
        temperature = opts.get("temperature", 0.2)
        timeout = opts.get("timeout_s", 60.0)

        # Normalize canonical names
        model_name_map = {
            "claude-3-7-sonnet": "claude-3-7-sonnet-20250219",
            "claude-3-5-sonnet": "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku": "claude-3-5-haiku-20241022",
        }
        actual_model = model_name_map.get(model, model)

        url = f"{self.base_url}/messages"
        payload = {
            "model": actual_model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
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

                # Anthropic content blocks: [{"type": "text", "text": "..."}]
                text_content = ""
                for block in raw.get("content", []):
                    if block.get("type") == "text":
                        text_content += block.get("text", "")

                usage = raw.get("usage", {})
                prompt_tokens = usage.get("input_tokens", 0)
                completion_tokens = usage.get("output_tokens", 0)

                return CompletionResponse(
                    content=text_content,
                    model=model,
                    provider_id=self.provider_id,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    finish_reason=raw.get("stop_reason", "end_turn"),
                    duration_ms=round(duration_ms, 2),
                    metadata={"id": raw.get("id"), "role": raw.get("role")},
                )
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            if e.code in {401, 403}:
                raise ProviderAuthenticationError(f"Anthropic auth failed: {body}", provider_id=self.provider_id)
            elif e.code == 429:
                raise ProviderRateLimitError(f"Anthropic rate limited: {body}", provider_id=self.provider_id)
            else:
                raise ProviderError(f"Anthropic HTTP {e.code}: {body}", provider_id=self.provider_id, status_code=e.code, retryable=(e.code >= 500))
        except urllib.error.URLError as e:
            raise ProviderTimeoutError(f"Anthropic connection error: {e.reason}", provider_id=self.provider_id)
        except Exception as e:
            raise ProviderError(f"Unexpected error: {str(e)}", provider_id=self.provider_id)

    def list_supported_models(self) -> List[str]:
        return ["claude-3-7-sonnet", "claude-3-5-sonnet", "claude-3-5-haiku"]
