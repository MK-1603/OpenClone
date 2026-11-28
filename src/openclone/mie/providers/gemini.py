"""OpenClone Model Intelligence Engine (MIE) — Google Gemini Native HTTP Provider.

Zero-dependency HTTP client for Google Gemini Developer API (Gemini 2.0 Flash & 1.5 Pro).
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


class GeminiProvider(BaseProvider):
    """Zero-dependency HTTP client for Google Gemini REST API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        super().__init__(
            provider_id="gemini",
            display_name="Google Gemini",
            tier=ProviderTier.P0_DIRECT,
        )
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.base_url = (base_url or "https://generativelanguage.googleapis.com/v1beta").rstrip("/")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def complete(
        self,
        prompt: str,
        model: str = "gemini-2.0-flash",
        options: Optional[Dict[str, Any]] = None,
    ) -> CompletionResponse:
        if not self.is_configured():
            raise ProviderAuthenticationError(
                "Missing Gemini API key. Set GEMINI_API_KEY.",
                provider_id=self.provider_id,
            )

        opts = options or {}
        max_tokens = opts.get("max_tokens", 8192)
        temperature = opts.get("temperature", 0.2)
        timeout = opts.get("timeout_s", 60.0)

        # Normalize model format: e.g. models/gemini-2.0-flash:generateContent
        clean_model = model if not model.startswith("models/") else model.replace("models/", "")
        url = f"{self.base_url}/models/{clean_model}:generateContent?key={self.api_key}"

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }

        headers = {
            "Content-Type": "application/json",
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

                text_content = ""
                candidates = raw.get("candidates", [])
                finish_reason = "stop"
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    text_content = "".join(p.get("text", "") for p in parts)
                    finish_reason = candidates[0].get("finishReason", "STOP")

                usage = raw.get("usageMetadata", {})
                prompt_tokens = usage.get("promptTokenCount", 0)
                completion_tokens = usage.get("candidatesTokenCount", 0)

                return CompletionResponse(
                    content=text_content,
                    model=model,
                    provider_id=self.provider_id,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    finish_reason=finish_reason,
                    duration_ms=round(duration_ms, 2),
                    metadata={"modelVersion": raw.get("modelVersion")},
                )
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            if e.code in {400, 403}:
                raise ProviderAuthenticationError(f"Gemini API auth error: {body}", provider_id=self.provider_id)
            elif e.code == 429:
                raise ProviderRateLimitError(f"Gemini quota/rate limit: {body}", provider_id=self.provider_id)
            else:
                raise ProviderError(f"Gemini HTTP {e.code}: {body}", provider_id=self.provider_id, status_code=e.code, retryable=(e.code >= 500))
        except urllib.error.URLError as e:
            raise ProviderTimeoutError(f"Gemini connection timeout: {e.reason}", provider_id=self.provider_id)
        except Exception as e:
            raise ProviderError(f"Unexpected error: {str(e)}", provider_id=self.provider_id)

    def list_supported_models(self) -> List[str]:
        return ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]
