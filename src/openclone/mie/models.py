"""OpenClone Model Intelligence Engine (MIE) — Data Models & Schemas.

Defines all core contracts, enums, dataclasses, and serialization helpers
for model registry, task classification, routing, scoring, and telemetry.
Zero external dependencies (standard library dataclasses & enums only).
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ProviderTier(str, Enum):
    """Categorization of model provider integration tiers."""
    P0_DIRECT = "P0_DIRECT"                # First-party direct APIs (OpenAI, Anthropic, Gemini, xAI)
    P1_CLOUD_PROXY = "P1_CLOUD_PROXY"      # Enterprise cloud brokers (Bedrock, Vertex, Azure, OpenRouter)
    P2_LOCAL_SPECIALIZED = "P2_LOCAL"      # Local / specialized inference (Ollama, vLLM, Groq, Mistral)


class TaskCategory(str, Enum):
    """14 deterministic categories for AI software engineering tasks."""
    ARCHITECTURE_DESIGN = "ARCHITECTURE_DESIGN"
    FRONTEND_UI = "FRONTEND_UI"
    BACKEND_API = "BACKEND_API"
    DATABASE_DATA = "DATABASE_DATA"
    SECURITY_AUDIT = "SECURITY_AUDIT"
    REFACTORING = "REFACTORING"
    TEST_ENGINEERING = "TEST_ENGINEERING"
    DEVOPS_INFRA = "DEVOPS_INFRA"
    DEBUGGING_RCA = "DEBUGGING_RCA"
    DOCUMENTATION_SPECS = "DOCUMENTATION_SPECS"
    FAST_SCAFFOLDING = "FAST_SCAFFOLDING"
    CODE_REVIEW = "CODE_REVIEW"
    ML_DATA_SCIENCE = "ML_DATA_SCIENCE"
    GENERAL_ORCHESTRATION = "GENERAL_ORCHESTRATION"


class RoutingMode(str, Enum):
    """Execution modes for model routing decisions."""
    BEST_QUALITY = "BEST_QUALITY"
    BALANCED = "BALANCED"
    LOW_LATENCY = "LOW_LATENCY"
    LOW_COST = "LOW_COST"
    HIGH_AVAILABILITY = "HIGH_AVAILABILITY"
    USER_SELECTED = "USER_SELECTED"
    POLICY_CONTROLLED = "POLICY_CONTROLLED"


class CircuitState(str, Enum):
    """Tri-state circuit breaker states for provider health."""
    CLOSED = "CLOSED"          # Normal operation: traffic routes to provider
    OPEN = "OPEN"              # Outage detected: traffic immediately trips to failover
    HALF_OPEN = "HALF_OPEN"    # Probe operation: trial canary request allowed


class MaturityStatus(str, Enum):
    """OpenClone verified maturity lifecycle states."""
    IMPLEMENTED = "IMPLEMENTED"
    VERIFIED = "VERIFIED"
    PARTIALLY_IMPLEMENTED = "PARTIALLY_IMPLEMENTED"
    PLANNED = "PLANNED"
    BLOCKED = "BLOCKED"


@dataclass
class ModelPricing:
    """Pricing rates in USD per 1 Million tokens."""
    input_price_per_m: float
    output_price_per_m: float

    def estimate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        input_cost = (prompt_tokens / 1_000_000.0) * self.input_price_per_m
        output_cost = (completion_tokens / 1_000_000.0) * self.output_price_per_m
        return round(input_cost + output_cost, 6)


@dataclass
class ModelCapabilities:
    """Declared capabilities, token limits, and task specializations."""
    reasoning_effort: bool = False
    supported_reasoning_levels: List[str] = field(default_factory=list)
    tool_calling: bool = True
    vision: bool = False
    json_schema: bool = True
    supports_responses_api: bool = True
    supports_streaming: bool = True
    max_context_tokens: int = 128_000
    max_output_tokens: int = 4_096
    strengths: List[TaskCategory] = field(default_factory=list)


@dataclass
class ModelRecord:
    """Authoritative registry record for a supported model."""
    model_id: str
    provider_id: str
    display_name: str
    tier: ProviderTier
    capabilities: ModelCapabilities
    pricing: ModelPricing
    model_family: str = "general"
    alias_to: Optional[str] = None
    quality_score: float = 90.0           # 0.0 to 100.0 scale
    latency_p50_ms: float = 800.0         # Baseline latency benchmark
    reliability_score: float = 99.0       # Historical SLA uptime percentage
    status: MaturityStatus = MaturityStatus.VERIFIED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "provider_id": self.provider_id,
            "display_name": self.display_name,
            "tier": self.tier.value,
            "capabilities": {
                "reasoning_effort": self.capabilities.reasoning_effort,
                "tool_calling": self.capabilities.tool_calling,
                "vision": self.capabilities.vision,
                "json_schema": self.capabilities.json_schema,
                "max_context_tokens": self.capabilities.max_context_tokens,
                "max_output_tokens": self.capabilities.max_output_tokens,
                "strengths": [s.value for s in self.capabilities.strengths],
            },
            "pricing": {
                "input_price_per_m": self.pricing.input_price_per_m,
                "output_price_per_m": self.pricing.output_price_per_m,
            },
            "quality_score": self.quality_score,
            "latency_p50_ms": self.latency_p50_ms,
            "reliability_score": self.reliability_score,
            "status": self.status.value,
        }


@dataclass
class TaskRequirement:
    """Parsed requirements extracted from an engineering task or prompt."""
    task_id: str
    prompt: str
    category: TaskCategory
    requires_reasoning: bool = False
    requires_tools: bool = False
    requires_vision: bool = False
    max_latency_ms: Optional[int] = None
    max_cost_usd: Optional[float] = None
    min_context_tokens: int = 4_000
    preferred_model: Optional[str] = None
    allowed_providers: Optional[List[str]] = None


@dataclass
class CandidateScore:
    """Detailed multi-dimensional evaluation score for a candidate model."""
    model: ModelRecord
    total_score: float
    dimension_scores: Dict[str, float]
    rationale: str


@dataclass
class RoutingDecision:
    """Deterministic routing decision with explanation and failover chain."""
    task_id: str
    selected_model: ModelRecord
    routing_mode: RoutingMode
    scores: List[CandidateScore]
    fallback_models: List[ModelRecord]
    provider_failover_targets: List[str]
    explanation: str
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "selected_model": self.selected_model.to_dict(),
            "routing_mode": self.routing_mode.value,
            "total_score": self.scores[0].total_score if self.scores else 0.0,
            "dimension_scores": self.scores[0].dimension_scores if self.scores else {},
            "fallback_models": [m.to_dict() for m in self.fallback_models],
            "provider_failover_targets": self.provider_failover_targets,
            "explanation": self.explanation,
            "timestamp": self.timestamp,
        }


@dataclass
class ExecutionMetrics:
    """Execution telemetry captured for audit and cost accounting."""
    request_id: str
    model_id: str
    provider_id: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    duration_ms: float
    success: bool
    error_type: Optional[str] = None
    circuit_state: CircuitState = CircuitState.CLOSED
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))


@dataclass
class HealthStatus:
    """Provider health and circuit breaker diagnostic state."""
    provider_id: str
    circuit_state: CircuitState
    failure_count: int
    success_count: int
    consecutive_failures: int
    last_failure_time: Optional[float] = None
    last_success_time: Optional[float] = None
    p95_latency_ms: float = 0.0
    is_available: bool = True
