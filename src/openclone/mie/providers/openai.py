"""OpenClone Model Intelligence Engine (MIE) — OpenAI Native HTTP Provider.

Zero-dependency HTTP client for OpenAI GPT-6 models, Responses API,
Chat Completions, reasoning tiers, multimodal vision, and OpenAI-compatible
endpoints (Groq, vLLM, OpenRouter, Together AI).
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Iterator, List, Optional

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

    CANONICAL_MODELS: List[str] = [
        "gpt-6.2-sol",
        "gpt-6.2-astra",
        "gpt-6.1-terra",
        "gpt-6-luna",
        "gpt-4o",
        "gpt-4o-mini",
        "o1",
        "o3-mini",
    ]

    LEGACY_ALIASES: Dict[str, str] = {
        "gpt-4o": "gpt-6.2-sol",
        "gpt-4o-mini": "gpt-6-luna",
        "gpt-4-turbo": "gpt-6.2-sol",
        "gpt-4": "gpt-6.2-sol",
    }

    REASONING_MODELS: set[str] = {
        "gpt-6.2-astra",
        "o1",
        "o3-mini",
    }

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

    def resolve_model_alias(self, model: str) -> str:
        """Resolve legacy model names to active GPT-6 equivalents."""
        return self.LEGACY_ALIASES.get(model, model)

    def complete(
        self,
        prompt: str,
        model: str = "gpt-6.2-sol",
        options: Optional[Dict[str, Any]] = None,
    ) -> CompletionResponse:
        """Send completion request via Responses API or Chat Completions."""
        if not self.is_configured():
            raise ProviderAuthenticationError(
                f"Missing API key for {self.display_name}. Set OPENAI_API_KEY.",
                provider_id=self.provider_id,
            )

        opts = options or {}

        # Check for explicit Responses API routing
        use_responses = opts.get("use_responses_api", False) or opts.get("api_type") == "responses"
        if use_responses:
            return self._complete_responses_api(prompt, model, opts)
        return self._complete_chat_completions(prompt, model, opts)

    def _complete_responses_api(
        self,
        prompt: str,
        model: str,
        opts: Dict[str, Any],
    ) -> CompletionResponse:
        """Dispatch request to OpenAI Responses API (/v1/responses)."""
        timeout = opts.get("timeout_s", 60.0)
        url = f"{self.base_url}/responses"

        # Build payload according to Responses API contract
        payload: Dict[str, Any] = {
            "model": model,
        }

        # Handle multimodal input or text prompt
        images = opts.get("images")
        if images:
            content_items: List[Dict[str, Any]] = [{"type": "text", "text": prompt}]
            for img in images:
                if isinstance(img, str):
                    content_items.append({"type": "image_url", "image_url": {"url": img}})
                elif isinstance(img, dict):
                    content_items.append(img)
            payload["input"] = [{"role": "user", "content": content_items}]
        elif opts.get("input"):
            payload["input"] = opts["input"]
        else:
            payload["input"] = prompt

        # Reasoning configuration
        reasoning_effort = opts.get("reasoning_effort")
        if reasoning_effort or model in self.REASONING_MODELS:
            effort = reasoning_effort or "medium"
            payload["reasoning"] = {"effort": effort}

        # Structured outputs
        if "response_format" in opts:
            payload["response_format"] = opts["response_format"]
        elif "json_schema" in opts:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": opts["json_schema"],
            }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "OpenClone-MIE/2.0.0",
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

                # Extract content from Responses API schema
                content = ""
                if "output_text" in raw:
                    content = raw["output_text"]
                elif "output" in raw:
                    output_val = raw["output"]
                    if isinstance(output_val, str):
                        content = output_val
                    elif isinstance(output_val, list) and output_val:
                        first = output_val[0]
                        if isinstance(first, dict):
                            content_parts = first.get("content", [])
                            if isinstance(content_parts, list) and content_parts:
                                content = content_parts[0].get("text", "")
                            else:
                                content = first.get("text", "")
                elif "choices" in raw and raw["choices"]:
                    content = raw["choices"][0].get("message", {}).get("content", "")

                usage = raw.get("usage", {})
                prompt_tokens = usage.get("input_tokens") or usage.get("prompt_tokens") or 0
                completion_tokens = usage.get("output_tokens") or usage.get("completion_tokens") or 0
                finish_reason = raw.get("status") or "completed"

                return CompletionResponse(
                    content=content,
                    model=model,
                    provider_id=self.provider_id,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    finish_reason=str(finish_reason),
                    duration_ms=round(duration_ms, 2),
                    metadata={
                        "id": raw.get("id"),
                        "api_endpoint": "/v1/responses",
                        "reasoning": raw.get("reasoning"),
                    },
                )
        except urllib.error.HTTPError as e:
            self._handle_http_error(e)
        except urllib.error.URLError as e:
            raise ProviderTimeoutError(f"Connection error or timeout: {e.reason}", provider_id=self.provider_id)
        except Exception as e:
            raise ProviderError(f"Unexpected error: {str(e)}", provider_id=self.provider_id)

    def _complete_chat_completions(
        self,
        prompt: str,
        model: str,
        opts: Dict[str, Any],
    ) -> CompletionResponse:
        """Dispatch request to OpenAI Chat Completions API (/v1/chat/completions)."""
        timeout = opts.get("timeout_s", 60.0)
        url = f"{self.base_url}/chat/completions"

        # Format messages with support for vision and structured blocks
        images = opts.get("images")
        if opts.get("messages"):
            messages = opts["messages"]
        elif images:
            content_items: List[Dict[str, Any]] = [{"type": "text", "text": prompt}]
            for img in images:
                if isinstance(img, str):
                    content_items.append({"type": "image_url", "image_url": {"url": img}})
                elif isinstance(img, dict):
                    content_items.append({"type": "image_url", "image_url": img})
            messages = [{"role": "user", "content": content_items}]
        else:
            messages = [{"role": "user", "content": prompt}]

        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
        }

        # Check reasoning model constraints
        is_reasoning_model = (
            model in self.REASONING_MODELS
            or model.startswith("o1")
            or model.startswith("o3")
            or "astra" in model
        )

        max_tokens = opts.get("max_tokens", 4096)
        if is_reasoning_model or opts.get("reasoning_effort"):
            # Reasoning models strictly reject custom temperature and top_p
            payload["max_completion_tokens"] = max_tokens
            if opts.get("reasoning_effort"):
                payload["reasoning_effort"] = opts["reasoning_effort"]
        else:
            payload["temperature"] = opts.get("temperature", 0.2)
            payload["max_tokens"] = max_tokens

        # Structured outputs
        if "response_format" in opts:
            payload["response_format"] = opts["response_format"]
        elif "json_schema" in opts:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": opts["json_schema"],
            }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "OpenClone-MIE/2.0.0",
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
                    metadata={
                        "id": raw.get("id"),
                        "system_fingerprint": raw.get("system_fingerprint"),
                        "api_endpoint": "/v1/chat/completions",
                    },
                )
        except urllib.error.HTTPError as e:
            self._handle_http_error(e)
        except urllib.error.URLError as e:
            raise ProviderTimeoutError(f"Connection error or timeout: {e.reason}", provider_id=self.provider_id)
        except Exception as e:
            raise ProviderError(f"Unexpected error: {str(e)}", provider_id=self.provider_id)

    def stream(
        self,
        prompt: str,
        model: str = "gpt-6.2-sol",
        options: Optional[Dict[str, Any]] = None,
    ) -> Iterator[str]:
        """Stream completion tokens in SSE format."""
        if not self.is_configured():
            raise ProviderAuthenticationError(
                f"Missing API key for {self.display_name}. Set OPENAI_API_KEY.",
                provider_id=self.provider_id,
            )

        opts = options or {}
        timeout = opts.get("timeout_s", 60.0)
        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
        }

        if model in self.REASONING_MODELS or model.startswith("o1") or model.startswith("o3"):
            payload["max_completion_tokens"] = opts.get("max_tokens", 4096)
        else:
            payload["temperature"] = opts.get("temperature", 0.2)
            payload["max_tokens"] = opts.get("max_tokens", 4096)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "OpenClone-MIE/2.0.0",
        }

        req = urllib.request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                for line in resp:
                    decoded = line.decode("utf-8").strip()
                    if not decoded or not decoded.startswith("data: "):
                        continue
                    data_str = decoded[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                        text_chunk = delta.get("content", "")
                        if text_chunk:
                            yield text_chunk
                    except json.JSONDecodeError:
                        continue
        except urllib.error.HTTPError as e:
            self._handle_http_error(e)
        except urllib.error.URLError as e:
            raise ProviderTimeoutError(f"Connection error or timeout: {e.reason}", provider_id=self.provider_id)
        except Exception as e:
            raise ProviderError(f"Unexpected error: {str(e)}", provider_id=self.provider_id)

    def _handle_http_error(self, e: urllib.error.HTTPError) -> None:
        """Categorize HTTP status codes into typed ProviderErrors."""
        body = e.read().decode("utf-8", errors="replace")
        if e.code in (401, 403):
            raise ProviderAuthenticationError(f"Authentication failed: {body}", provider_id=self.provider_id)
        elif e.code == 429:
            raise ProviderRateLimitError(f"Rate limited (429): {body}", provider_id=self.provider_id)
        else:
            raise ProviderError(
                f"HTTP {e.code}: {body}",
                provider_id=self.provider_id,
                status_code=e.code,
                retryable=(e.code >= 500),
            )

    def list_supported_models(self) -> List[str]:
        """Return list of supported OpenAI models."""
        return list(self.CANONICAL_MODELS)
