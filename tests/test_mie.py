"""Unit and integration test suite for OpenClone Model Intelligence Engine (MIE).

Tests cover:
- Dynamic Model Registry & capability filtering
- Task Intelligence Classifier & requirement extraction
- Multi-dimensional Scoring Engine & routing mode weight distributions
- Tri-state Circuit Breakers & High Availability Engine
- Model Router end-to-end routing decisions & fallback chains
- Zero-dependency Provider Adapters (OpenAI, Anthropic, Gemini, Ollama) via mocked HTTP fixtures
- Telemetry, secret redaction, and hash-chained ledger
- MCP Server MIE tool endpoints
"""

import json
import sqlite3
import time
import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from src.openclone.mcp.server import OpenCloneMCPServer
from src.openclone.mie import (
    BaseProvider,
    CandidateScore,
    CircuitBreaker,
    CircuitBreakerOpenError,
    CircuitState,
    CompletionResponse,
    ExecutionMetrics,
    HighAvailabilityEngine,
    MieTelemetry,
    ModelCapabilities,
    ModelPricing,
    ModelRecord,
    ModelRegistry,
    ModelRouter,
    ProviderAuthenticationError,
    ProviderRateLimitError,
    ProviderTier,
    RoutingMode,
    TaskCategory,
    TaskClassifier,
    TaskRequirement,
    redact_secrets,
)
from src.openclone.mie.hosts import get_host_adapter
from src.openclone.mie.providers.anthropic import AnthropicProvider
from src.openclone.mie.providers.gemini import GeminiProvider
from src.openclone.mie.providers.ollama import OllamaProvider
from src.openclone.mie.providers.openai import OpenAIProvider


# ============================================================================
# 1. MODEL REGISTRY TESTS
# ============================================================================

def test_registry_preloads_canonical_catalog():
    registry = ModelRegistry(preload_defaults=True)
    models = registry.list_all()
    assert len(models) >= 10

    # Verify P0 models exist
    gpt4o = registry.get("gpt-4o")
    assert gpt4o is not None
    assert gpt4o.provider_id == "openai"
    assert gpt4o.tier == ProviderTier.P0_DIRECT
    assert gpt4o.capabilities.tool_calling is True

    claude = registry.get("claude-3-7-sonnet")
    assert claude is not None
    assert claude.capabilities.reasoning_effort is True

    gemini = registry.get("gemini-2.0-flash")
    assert gemini is not None
    assert gemini.capabilities.max_context_tokens >= 1_000_000


def test_registry_filter_candidates():
    registry = ModelRegistry(preload_defaults=True)
    req = TaskRequirement(
        task_id="t1",
        prompt="Design high level distributed microservices architecture",
        category=TaskCategory.ARCHITECTURE_DESIGN,
        requires_reasoning=True,
        min_context_tokens=100_000,
    )
    candidates = registry.filter_candidates(req)
    assert len(candidates) > 0
    # Every candidate must satisfy min context and have reasoning or elite score
    for c in candidates:
        assert c.capabilities.max_context_tokens >= 100_000


# ============================================================================
# 2. TASK CLASSIFIER TESTS
# ============================================================================

def test_classifier_security_audit():
    prompt = "Review this auth middleware for potential SQL injection and CWE-89 vulnerability."
    req = TaskClassifier.classify(prompt)
    assert req.category == TaskCategory.SECURITY_AUDIT
    assert req.requires_reasoning is True


def test_classifier_frontend_ui():
    prompt = "Create a responsive React modal with Tailwind CSS styling and accessibility."
    req = TaskClassifier.classify(prompt)
    assert req.category == TaskCategory.FRONTEND_UI


def test_classifier_database():
    prompt = "Write an optimized PostgreSQL schema migration with composite indexes."
    req = TaskClassifier.classify(prompt)
    assert req.category == TaskCategory.DATABASE_DATA


def test_classifier_debugging():
    prompt = "Fix NullPointerException crash traceback in transaction coordinator."
    req = TaskClassifier.classify(prompt)
    assert req.category == TaskCategory.DEBUGGING_RCA
    assert req.requires_reasoning is True


# ============================================================================
# 3. HIGH AVAILABILITY & CIRCUIT BREAKER TESTS
# ============================================================================

def test_circuit_breaker_tripping_and_recovery():
    cb = CircuitBreaker(identifier="test_provider", failure_threshold=3, cooldown_seconds=0.1)
    assert cb.state == CircuitState.CLOSED
    assert cb.can_execute() is True

    # 1 failure: remains closed
    cb.record_failure()
    assert cb.state == CircuitState.CLOSED

    # 2 failures: remains closed
    cb.record_failure()
    assert cb.state == CircuitState.CLOSED

    # 3 failures: trips to OPEN
    cb.record_failure()
    assert cb.state == CircuitState.OPEN
    assert cb.can_execute() is False

    with pytest.raises(CircuitBreakerOpenError):
        cb.check_execution_or_raise()

    # Wait for cooldown to transition to HALF_OPEN
    time.sleep(0.15)
    assert cb.state == CircuitState.HALF_OPEN
    assert cb.can_execute() is True

    # Success in HALF_OPEN resets to CLOSED
    cb.record_success()
    assert cb.state == CircuitState.CLOSED


def test_ha_failover_targets():
    ha = HighAvailabilityEngine()
    anthropic_failovers = ha.get_same_model_failover("anthropic")
    assert "bedrock" in anthropic_failovers
    assert "vertex" in anthropic_failovers


def test_exponential_backoff_jitter():
    ha = HighAvailabilityEngine()
    delay = ha.calculate_backoff(attempt=2, base_delay=0.5, max_delay=10.0)
    assert 0.0 <= delay <= 2.0


# ============================================================================
# 4. MODEL ROUTER TESTS
# ============================================================================

def test_model_router_best_quality_mode():
    router = ModelRouter()
    decision = router.route_task(
        prompt="Audit crypto vault contracts for flash loan vulnerabilities.",
        mode=RoutingMode.BEST_QUALITY,
    )
    assert decision.selected_model is not None
    # Best quality for security reasoning should select o1, claude-3-7-sonnet or similar
    assert decision.selected_model.quality_score >= 95.0
    assert len(decision.fallback_models) >= 1
    assert len(decision.provider_failover_targets) >= 1


def test_model_router_low_cost_mode():
    router = ModelRouter()
    decision = router.route_task(
        prompt="Generate quick README documentation and changelog.",
        mode=RoutingMode.LOW_COST,
    )
    assert decision.selected_model is not None
    combined_cost = (
        decision.selected_model.pricing.input_price_per_m + decision.selected_model.pricing.output_price_per_m
    )
    # Low cost mode should pick highly cost-effective model (e.g. gpt-4o-mini, gemini-flash, ollama)
    assert combined_cost <= 5.0


def test_model_router_user_preferred_override():
    router = ModelRouter()
    decision = router.route_task(
        prompt="Write a Python script.",
        mode=RoutingMode.BALANCED,
        preferred_model="gemini-2.0-flash",
    )
    assert decision.selected_model.model_id == "gemini-2.0-flash"


# ============================================================================
# 5. PROVIDER ADAPTERS (MOCKED HTTP) TESTS
# ============================================================================

def test_openai_provider_mocked_completion():
    provider = OpenAIProvider(api_key="sk-mock-key")
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "id": "chatcmpl-123",
        "choices": [{"message": {"content": "Hello OpenClone"}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5},
    }).encode("utf-8")
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        res = provider.complete("Say hi", model="gpt-4o")
        assert res.content == "Hello OpenClone"
        assert res.prompt_tokens == 10
        assert res.completion_tokens == 5
        assert res.model == "gpt-4o"


def test_openai_provider_auth_error():
    provider = OpenAIProvider(api_key="")
    with pytest.raises(ProviderAuthenticationError):
        provider.complete("Say hi")


def test_anthropic_provider_mocked_completion():
    provider = AnthropicProvider(api_key="sk-ant-mock-key")
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "id": "msg_123",
        "content": [{"type": "text", "text": "Anthropic response"}],
        "usage": {"input_tokens": 12, "output_tokens": 8},
        "stop_reason": "end_turn",
    }).encode("utf-8")
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        res = provider.complete("Say hi", model="claude-3-5-sonnet")
        assert res.content == "Anthropic response"
        assert res.prompt_tokens == 12
        assert res.completion_tokens == 8


def test_gemini_provider_mocked_completion():
    provider = GeminiProvider(api_key="mock-gemini-key")
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "candidates": [{
            "content": {"parts": [{"text": "Gemini response"}]},
            "finishReason": "STOP",
        }],
        "usageMetadata": {"promptTokenCount": 15, "candidatesTokenCount": 20},
    }).encode("utf-8")
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        res = provider.complete("Say hi", model="gemini-2.0-flash")
        assert res.content == "Gemini response"
        assert res.prompt_tokens == 15
        assert res.completion_tokens == 20


def test_ollama_provider_mocked_completion():
    provider = OllamaProvider()
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "response": "Local Ollama code",
        "prompt_eval_count": 50,
        "eval_count": 30,
        "done": True,
    }).encode("utf-8")
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        res = provider.complete("Write code", model="qwen2.5-coder:32b")
        assert res.content == "Local Ollama code"
        assert res.prompt_tokens == 50
        assert res.completion_tokens == 30


# ============================================================================
# 6. TELEMETRY & SECRET REDACTION TESTS
# ============================================================================

def test_secret_redaction():
    # Construct synthetic test tokens dynamically at runtime to prevent triggering static secret scanners
    fake_sk = "sk-" + "1234567890" * 3
    fake_google_key = "AIza" + "SyD" + "0" * 32
    text = f"Authorization: Bearer {fake_sk} and api_key='{fake_google_key}'"
    clean = redact_secrets(text)
    assert fake_sk not in clean
    assert fake_google_key not in clean
    assert "[REDACTED]" in clean

    # Verify standalone tokens without Bearer or key= prefixes are also redacted
    standalone = redact_secrets(f"raw keys: {fake_sk} and {fake_google_key}")
    assert fake_sk not in standalone
    assert fake_google_key not in standalone
    assert "[REDACTED-KEY]" in standalone


def test_telemetry_ledger_recording(tmp_path):
    db_file = str(tmp_path / "test_mie.sqlite3")
    telemetry = MieTelemetry(db_path=db_file)

    metric = ExecutionMetrics(
        request_id="req_001",
        model_id="gpt-4o",
        provider_id="openai",
        prompt_tokens=100,
        completion_tokens=50,
        total_tokens=150,
        cost_usd=0.00075,
        duration_ms=450.0,
        success=True,
    )
    entry_hash = telemetry.record_execution(metric)
    assert len(entry_hash) == 64

    stats = telemetry.get_summary_stats()
    assert stats["total_requests"] == 1
    assert stats["total_prompt_tokens"] == 100
    assert stats["total_cost_usd"] == 0.0008


# ============================================================================
# 7. HOST ADAPTERS & MCP SERVER INTEGRATION TESTS
# ============================================================================

def test_host_adapters():
    antigravity = get_host_adapter("antigravity")
    assert antigravity.metadata.display_name == "Google Antigravity"
    assert "gemini-2.0-flash" in antigravity.metadata.native_model_affinity

    claude_code = get_host_adapter("claude_code")
    assert "claude-3-5-sonnet" in claude_code.metadata.native_model_affinity


def test_mcp_server_mie_tools():
    server = OpenCloneMCPServer()

    # 1. openclone_route_model
    route_res = server.call_tool("openclone_route_model", {
        "prompt": "Create a database schema for user accounts with PostgreSQL.",
        "mode": "BALANCED",
    })
    assert "selected_model" in route_res
    assert "fallback_models" in route_res
    assert "explanation" in route_res

    # 2. openclone_list_models
    list_res = server.call_tool("openclone_list_models", {"provider": "openai"})
    assert list_res["count"] >= 3
    assert all(m["provider_id"] == "openai" for m in list_res["models"])

    # 3. openclone_model_health
    health_res = server.call_tool("openclone_model_health", {})
    assert "health" in health_res
    assert len(health_res["health"]) >= 1
