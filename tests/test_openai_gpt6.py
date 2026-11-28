"""OpenClone Model Intelligence Engine (MIE) — OpenAI GPT-6 Test Suite.

Validates the full modernization from legacy GPT-4o to GPT-6:
- Registry catalog (GPT-6.2 Sol, GPT-6.2 Astra, GPT-6.1 Terra, GPT-6 Luna)
- Backward-compatible alias resolution
- Responses API (/v1/responses) execution path
- Chat Completions parameter sanitization (stripping temperature for reasoning)
- Reasoning effort configuration (low, medium, high)
- Multimodal vision payload formatting
- Structured JSON Schema outputs
- SSE streaming token delivery
- Error handling (401, 429, 500, timeouts)
- Task router selection across GPT-6 models
"""

import json
from unittest.mock import MagicMock, patch
import urllib.error
import pytest

from src.openclone.mie.contracts import (
    ProviderAuthenticationError,
    ProviderError,
    ProviderRateLimitError,
    ProviderTimeoutError,
)
from src.openclone.mie.models import (
    MaturityStatus,
    RoutingMode,
    TaskCategory,
)
from src.openclone.mie.providers.openai import OpenAIProvider
from src.openclone.mie.registry import ModelRegistry
from src.openclone.mie.router import ModelRouter


# ============================================================================
# 1. MODEL REGISTRY & CATALOG TESTS
# ============================================================================

def test_registry_gpt6_catalog_preloaded():
    registry = ModelRegistry()

    # 1. GPT-6.2 Sol (Flagship Default)
    sol = registry.get("gpt-6.2-sol")
    assert sol is not None
    assert sol.model_family == "gpt-6"
    assert sol.capabilities.max_context_tokens == 256_000
    assert sol.capabilities.supports_responses_api is True
    assert sol.capabilities.supports_streaming is True
    assert sol.capabilities.reasoning_effort is True
    assert "low" in sol.capabilities.supported_reasoning_levels
    assert TaskCategory.BACKEND_API in sol.capabilities.strengths
    assert sol.pricing.input_price_per_m == 2.00
    assert sol.pricing.output_price_per_m == 8.00

    # 2. GPT-6.2 Astra (Deep Reasoning & Architecture)
    astra = registry.get("gpt-6.2-astra")
    assert astra is not None
    assert astra.model_family == "gpt-6"
    assert astra.quality_score >= 99.0
    assert astra.capabilities.max_output_tokens == 64_000
    assert TaskCategory.ARCHITECTURE_DESIGN in astra.capabilities.strengths
    assert TaskCategory.SECURITY_AUDIT in astra.capabilities.strengths

    # 3. GPT-6.1 Terra (Visual Reasoning & UI)
    terra = registry.get("gpt-6.1-terra")
    assert terra is not None
    assert terra.model_family == "gpt-6"
    assert terra.capabilities.vision is True
    assert TaskCategory.FRONTEND_UI in terra.capabilities.strengths

    # 4. GPT-6 Luna (High-Speed & Cost-Efficient)
    luna = registry.get("gpt-6-luna")
    assert luna is not None
    assert luna.model_family == "gpt-6"
    assert luna.latency_p50_ms <= 400.0
    assert luna.pricing.input_price_per_m <= 0.25
    assert TaskCategory.FAST_SCAFFOLDING in luna.capabilities.strengths


def test_registry_backward_compatible_aliases():
    registry = ModelRegistry()

    # Direct legacy lookup preserves record with alias link
    legacy_4o = registry.get("gpt-4o")
    assert legacy_4o is not None
    assert legacy_4o.alias_to == "gpt-6.2-sol"
    assert legacy_4o.model_family == "gpt-4"

    legacy_mini = registry.get("gpt-4o-mini")
    assert legacy_mini is not None
    assert legacy_mini.alias_to == "gpt-6-luna"

    # Alias-resolved lookup yields target model
    resolved_4o = registry.get("gpt-4o", resolve_alias=True)
    assert resolved_4o is not None
    assert resolved_4o.model_id == "gpt-6.2-sol"

    resolved_mini = registry.get("gpt-4o-mini", resolve_alias=True)
    assert resolved_mini is not None
    assert resolved_mini.model_id == "gpt-6-luna"


# ============================================================================
# 2. OPENAI PROVIDER TESTS (UNIT & MOCKED HTTP)
# ============================================================================

def test_provider_initialization_defaults():
    provider = OpenAIProvider(api_key="sk-test-mock-key")
    assert provider.is_configured() is True
    assert "gpt-6.2-sol" in provider.list_supported_models()
    assert "gpt-6.2-astra" in provider.list_supported_models()
    assert "gpt-6.1-terra" in provider.list_supported_models()
    assert "gpt-6-luna" in provider.list_supported_models()
    assert provider.resolve_model_alias("gpt-4o") == "gpt-6.2-sol"
    assert provider.resolve_model_alias("gpt-4o-mini") == "gpt-6-luna"


def test_provider_chat_completions_default():
    provider = OpenAIProvider(api_key="sk-test-key")
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "id": "chatcmpl-gpt6-01",
        "choices": [{"message": {"content": "GPT-6 output generated."}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 15, "completion_tokens": 20},
    }).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp) as mock_urlopen:
        res = provider.complete("Implement authentication middleware", model="gpt-6.2-sol")
        assert res.content == "GPT-6 output generated."
        assert res.model == "gpt-6.2-sol"
        assert res.prompt_tokens == 15
        assert res.completion_tokens == 20
        assert res.metadata["api_endpoint"] == "/v1/chat/completions"

        # Verify request parameters
        req_sent = mock_urlopen.call_args[0][0]
        sent_body = json.loads(req_sent.data.decode("utf-8"))
        assert sent_body["model"] == "gpt-6.2-sol"
        assert sent_body["messages"][0]["content"] == "Implement authentication middleware"


def test_provider_responses_api_execution():
    provider = OpenAIProvider(api_key="sk-test-key")
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "id": "resp-001",
        "output_text": "Responses API direct answer.",
        "usage": {"input_tokens": 40, "output_tokens": 60},
        "status": "completed",
    }).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp) as mock_urlopen:
        res = provider.complete(
            "Design system blueprint",
            model="gpt-6.2-astra",
            options={"use_responses_api": True, "reasoning_effort": "high"},
        )
        assert res.content == "Responses API direct answer."
        assert res.prompt_tokens == 40
        assert res.completion_tokens == 60
        assert res.metadata["api_endpoint"] == "/v1/responses"

        # Verify endpoint and body
        req_sent = mock_urlopen.call_args[0][0]
        assert req_sent.full_url.endswith("/responses")
        sent_body = json.loads(req_sent.data.decode("utf-8"))
        assert sent_body["model"] == "gpt-6.2-astra"
        assert sent_body["reasoning"]["effort"] == "high"


def test_provider_reasoning_parameter_sanitization():
    """Ensure temperature and top_p are stripped for reasoning models to avoid 400 Bad Request."""
    provider = OpenAIProvider(api_key="sk-test-key")
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "choices": [{"message": {"content": "Reasoned architecture."}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 10},
    }).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp) as mock_urlopen:
        provider.complete(
            "Analyze security vulnerability",
            model="gpt-6.2-astra",
            options={"temperature": 0.7, "max_tokens": 8000, "reasoning_effort": "high"},
        )
        req_sent = mock_urlopen.call_args[0][0]
        sent_body = json.loads(req_sent.data.decode("utf-8"))

        # Temperature must be removed; max_completion_tokens used instead
        assert "temperature" not in sent_body
        assert sent_body["max_completion_tokens"] == 8000
        assert sent_body["reasoning_effort"] == "high"


def test_provider_multimodal_vision_payload():
    provider = OpenAIProvider(api_key="sk-test-key")
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "choices": [{"message": {"content": "Wireframe has navbar and sidebar."}}],
        "usage": {"prompt_tokens": 50, "completion_tokens": 20},
    }).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp) as mock_urlopen:
        res = provider.complete(
            "Analyze this floorplan wireframe",
            model="gpt-6.1-terra",
            options={"images": ["https://assets.openclone.dev/mockups/dashboard.png"]},
        )
        assert res.content == "Wireframe has navbar and sidebar."

        req_sent = mock_urlopen.call_args[0][0]
        sent_body = json.loads(req_sent.data.decode("utf-8"))
        content_parts = sent_body["messages"][0]["content"]
        assert len(content_parts) == 2
        assert content_parts[0]["type"] == "text"
        assert content_parts[1]["type"] == "image_url"
        assert content_parts[1]["image_url"]["url"] == "https://assets.openclone.dev/mockups/dashboard.png"


def test_provider_structured_output_schema():
    provider = OpenAIProvider(api_key="sk-test-key")
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "choices": [{"message": {"content": "{\"status\": \"approved\"}"}}],
        "usage": {"prompt_tokens": 20, "completion_tokens": 10},
    }).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    schema = {
        "name": "AuditResult",
        "schema": {
            "type": "object",
            "properties": {"status": {"type": "string"}},
            "required": ["status"],
        },
    }

    with patch("urllib.request.urlopen", return_value=mock_resp) as mock_urlopen:
        res = provider.complete(
            "Audit file",
            model="gpt-6.2-sol",
            options={"json_schema": schema},
        )
        req_sent = mock_urlopen.call_args[0][0]
        sent_body = json.loads(req_sent.data.decode("utf-8"))
        assert sent_body["response_format"]["type"] == "json_schema"
        assert sent_body["response_format"]["json_schema"] == schema


def test_provider_streaming_tokens():
    provider = OpenAIProvider(api_key="sk-test-key")
    sse_lines = [
        b'data: {"choices": [{"delta": {"content": "def "}}]}\n\n',
        b'data: {"choices": [{"delta": {"content": "login():"}}]}\n\n',
        b'data: {"choices": [{"delta": {"content": " pass"}}]}\n\n',
        b'data: [DONE]\n\n',
    ]

    mock_resp = MagicMock()
    mock_resp.__iter__.return_value = sse_lines
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        chunks = list(provider.stream("Write login function", model="gpt-6.2-sol"))
        assert chunks == ["def ", "login():", " pass"]


# ============================================================================
# 3. ERROR HANDLING & RESILIENCE
# ============================================================================

def test_provider_error_handling():
    provider = OpenAIProvider(api_key="sk-test-key")

    # 401 Unauthorized
    err_401 = urllib.error.HTTPError("url", 401, "Unauthorized", {}, MagicMock(read=lambda: b"Invalid API key"))
    with patch("urllib.request.urlopen", side_effect=err_401):
        with pytest.raises(ProviderAuthenticationError):
            provider.complete("test")

    # 429 Rate Limit
    err_429 = urllib.error.HTTPError("url", 429, "Too Many Requests", {}, MagicMock(read=lambda: b"Quota exceeded"))
    with patch("urllib.request.urlopen", side_effect=err_429):
        with pytest.raises(ProviderRateLimitError):
            provider.complete("test")

    # 500 Server Error
    err_500 = urllib.error.HTTPError("url", 500, "Internal Server Error", {}, MagicMock(read=lambda: b"Crash"))
    with patch("urllib.request.urlopen", side_effect=err_500):
        with pytest.raises(ProviderError) as exc_info:
            provider.complete("test")
        assert exc_info.value.retryable is True

    # Timeout
    err_timeout = urllib.error.URLError("Connection timed out")
    with patch("urllib.request.urlopen", side_effect=err_timeout):
        with pytest.raises(ProviderTimeoutError):
            provider.complete("test")


# ============================================================================
# 4. MODEL ROUTER INTEGRATION WITH GPT-6
# ============================================================================

def test_router_selects_gpt6_astra_for_deep_architecture():
    router = ModelRouter()
    # When restricted to OpenAI provider, deep architecture task should route to GPT-6.2 Astra
    decision = router.route_task(
        prompt="Design a distributed high-availability microservice architecture and security audit threat model.",
        mode=RoutingMode.BEST_QUALITY,
        allowed_providers=["openai"],
    )
    assert decision.selected_model.model_id == "gpt-6.2-astra"
    assert decision.selected_model.capabilities.reasoning_effort is True


def test_router_selects_gpt6_luna_for_scaffolding():
    router = ModelRouter()
    # Fast scaffolding with low-cost mode on OpenAI routes to GPT-6 Luna
    decision = router.route_task(
        prompt="Generate quick boilerplate starter template CRUD skeleton stubs.",
        mode=RoutingMode.LOW_COST,
        allowed_providers=["openai"],
    )
    assert decision.selected_model.model_id == "gpt-6-luna"
    assert decision.selected_model.pricing.input_price_per_m <= 0.25
