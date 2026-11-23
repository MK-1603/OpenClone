"""OpenClone Model Intelligence Engine (MIE) — Local Ollama Native HTTP Provider.

Zero-dependency HTTP client for locally hosted inference on Ollama (localhost:11434).
Zero external API keys required; loopback communication only.
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
    ProviderError,
    ProviderTimeoutError,
)
from src.openclone.mie.models import ProviderTier


class OllamaProvider(BaseProvider):
    """Zero-dependency HTTP client for local Ollama daemon."""

    def __init__(
        self,
        base_url: Optional[str] = None,
    ):
        super().__init__(
            provider_id="ollama",
            display_name="Ollama (Local)",
            tier=ProviderTier.P2_LOCAL_SPECIALIZED,
        )
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")

    def is_configured(self) -> bool:
        """Always considered configured as a local fallback service."""
        return True

    def complete(
        self,
        prompt: str,
        model: str = "qwen2.5-coder:32b",
        options: Optional[Dict[str, Any]] = None,
    ) -> CompletionResponse:
        opts = options or {}
        temperature = opts.get("temperature", 0.2)
        timeout = opts.get("timeout_s", 120.0)

        # Strip prefix if passed as ollama/model
        clean_model = model.replace("ollama/", "")

        url = f"{self.base_url}/api/generate"
        payload = {
            "model": clean_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
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

                return CompletionResponse(
                    content=raw.get("response", ""),
                    model=model,
                    provider_id=self.provider_id,
                    prompt_tokens=raw.get("prompt_eval_count", 0),
                    completion_tokens=raw.get("eval_count", 0),
                    finish_reason="stop" if raw.get("done") else "length",
                    duration_ms=round(duration_ms, 2),
                    metadata={"total_duration": raw.get("total_duration")},
                )
        except urllib.error.URLError as e:
            raise ProviderTimeoutError(
                f"Ollama local daemon unreachable at {self.base_url}: {e.reason}",
                provider_id=self.provider_id,
            )
        except Exception as e:
            raise ProviderError(f"Ollama execution error: {str(e)}", provider_id=self.provider_id)

    def list_supported_models(self) -> List[str]:
        return ["qwen2.5-coder-32b", "llama3.3", "deepseek-r1-70b"]
