"""OpenClone Model Intelligence Engine (MIE) — Dynamic Model Registry.

Maintains canonical metadata, capabilities, context limits, pricing,
and lifecycle states for all supported AI models.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional

from src.openclone.mie.models import (
    MaturityStatus,
    ModelCapabilities,
    ModelPricing,
    ModelRecord,
    ProviderTier,
    TaskCategory,
    TaskRequirement,
)


class ModelRegistry:
    """Central registry of all available AI models across providers."""

    def __init__(self, preload_defaults: bool = True):
        self._models: Dict[str, ModelRecord] = {}
        if preload_defaults:
            self._preload_canonical_catalog()

    def register(self, record: ModelRecord) -> None:
        """Register or update a model record in the catalog."""
        self._models[record.model_id] = record

    def get(self, model_id: str, resolve_alias: bool = False) -> Optional[ModelRecord]:
        """Retrieve model record by identifier, or None if not found.

        If resolve_alias is True and the record has alias_to, resolves to the target model.
        """
        rec = self._models.get(model_id)
        if rec and resolve_alias and rec.alias_to:
            target = self._models.get(rec.alias_to)
            if target:
                return target
        return rec

    def list_all(self) -> List[ModelRecord]:
        """Return all registered model records."""
        return list(self._models.values())

    def find_by_provider(self, provider_id: str) -> List[ModelRecord]:
        """Return all models belonging to a specific provider."""
        return [m for m in self._models.values() if m.provider_id == provider_id]

    def filter_candidates(self, req: TaskRequirement) -> List[ModelRecord]:
        """Filter candidate models based on hard constraints from TaskRequirement."""
        candidates: List[ModelRecord] = []
        for model in self._models.values():
            # Check provider whitelist if specified
            if req.allowed_providers and model.provider_id not in req.allowed_providers:
                continue

            # Check minimum context window
            if model.capabilities.max_context_tokens < req.min_context_tokens:
                continue

            # Check reasoning requirement
            if req.requires_reasoning and not model.capabilities.reasoning_effort:
                # Still allow top-tier general models as fallback
                if model.quality_score < 94.0:
                    continue

            # Check tools requirement
            if req.requires_tools and not model.capabilities.tool_calling:
                continue

            # Check vision requirement
            if req.requires_vision and not model.capabilities.vision:
                continue

            candidates.append(model)
        return candidates

    def _preload_canonical_catalog(self) -> None:
        """Seed registry with authoritative industry models as of 2026."""
        canonical_records = [
            # --- OpenAI Tier 0 — GPT-6 Canonical Family & Reasoning ---
            ModelRecord(
                model_id="gpt-6.2-sol",
                provider_id="openai",
                display_name="OpenAI GPT-6.2 Sol (Adaptive Reasoning & Default)",
                tier=ProviderTier.P0_DIRECT,
                model_family="gpt-6",
                capabilities=ModelCapabilities(
                    reasoning_effort=True,
                    supported_reasoning_levels=["low", "medium", "high"],
                    tool_calling=True,
                    vision=True,
                    json_schema=True,
                    supports_responses_api=True,
                    supports_streaming=True,
                    max_context_tokens=256_000,
                    max_output_tokens=32_768,
                    strengths=[
                        TaskCategory.BACKEND_API,
                        TaskCategory.FRONTEND_UI,
                        TaskCategory.GENERAL_ORCHESTRATION,
                        TaskCategory.REFACTORING,
                        TaskCategory.DATABASE_DATA,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=2.00, output_price_per_m=8.00),
                quality_score=98.0,
                latency_p50_ms=850.0,
                reliability_score=99.9,
                status=MaturityStatus.VERIFIED,
            ),
            ModelRecord(
                model_id="gpt-6.2-astra",
                provider_id="openai",
                display_name="OpenAI GPT-6.2 Astra (Deep Reasoning & Architecture)",
                tier=ProviderTier.P0_DIRECT,
                model_family="gpt-6",
                capabilities=ModelCapabilities(
                    reasoning_effort=True,
                    supported_reasoning_levels=["low", "medium", "high"],
                    tool_calling=True,
                    vision=True,
                    json_schema=True,
                    supports_responses_api=True,
                    supports_streaming=True,
                    max_context_tokens=256_000,
                    max_output_tokens=64_000,
                    strengths=[
                        TaskCategory.ARCHITECTURE_DESIGN,
                        TaskCategory.SECURITY_AUDIT,
                        TaskCategory.DEBUGGING_RCA,
                        TaskCategory.CODE_REVIEW,
                        TaskCategory.ML_DATA_SCIENCE,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=5.00, output_price_per_m=20.00),
                quality_score=99.5,
                latency_p50_ms=2800.0,
                reliability_score=99.8,
                status=MaturityStatus.VERIFIED,
            ),
            ModelRecord(
                model_id="gpt-6.1-terra",
                provider_id="openai",
                display_name="OpenAI GPT-6.1 Terra (Visual Reasoning & UI)",
                tier=ProviderTier.P0_DIRECT,
                model_family="gpt-6",
                capabilities=ModelCapabilities(
                    reasoning_effort=False,
                    supported_reasoning_levels=[],
                    tool_calling=True,
                    vision=True,
                    json_schema=True,
                    supports_responses_api=True,
                    supports_streaming=True,
                    max_context_tokens=200_000,
                    max_output_tokens=16_384,
                    strengths=[
                        TaskCategory.FRONTEND_UI,
                        TaskCategory.DOCUMENTATION_SPECS,
                        TaskCategory.CODE_REVIEW,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=1.75, output_price_per_m=7.00),
                quality_score=96.5,
                latency_p50_ms=720.0,
                reliability_score=99.7,
                status=MaturityStatus.VERIFIED,
            ),
            ModelRecord(
                model_id="gpt-6-luna",
                provider_id="openai",
                display_name="OpenAI GPT-6 Luna (High-Speed & Cost-Efficient)",
                tier=ProviderTier.P0_DIRECT,
                model_family="gpt-6",
                capabilities=ModelCapabilities(
                    reasoning_effort=False,
                    supported_reasoning_levels=[],
                    tool_calling=True,
                    vision=True,
                    json_schema=True,
                    supports_responses_api=True,
                    supports_streaming=True,
                    max_context_tokens=128_000,
                    max_output_tokens=16_384,
                    strengths=[
                        TaskCategory.FAST_SCAFFOLDING,
                        TaskCategory.DOCUMENTATION_SPECS,
                        TaskCategory.TEST_ENGINEERING,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=0.20, output_price_per_m=0.80),
                quality_score=91.5,
                latency_p50_ms=320.0,
                reliability_score=99.8,
                status=MaturityStatus.VERIFIED,
            ),
            ModelRecord(
                model_id="gpt-4o",
                provider_id="openai",
                display_name="OpenAI GPT-4o (Legacy — Aliased to GPT-6.2 Sol)",
                tier=ProviderTier.P0_DIRECT,
                model_family="gpt-4",
                alias_to="gpt-6.2-sol",
                capabilities=ModelCapabilities(
                    reasoning_effort=False,
                    tool_calling=True,
                    vision=True,
                    json_schema=True,
                    supports_responses_api=False,
                    supports_streaming=True,
                    max_context_tokens=128_000,
                    max_output_tokens=16_384,
                    strengths=[
                        TaskCategory.FRONTEND_UI,
                        TaskCategory.BACKEND_API,
                        TaskCategory.FAST_SCAFFOLDING,
                        TaskCategory.GENERAL_ORCHESTRATION,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=2.50, output_price_per_m=10.00),
                quality_score=95.0,
                latency_p50_ms=750.0,
                reliability_score=99.6,
                status=MaturityStatus.VERIFIED,
            ),
            ModelRecord(
                model_id="gpt-4o-mini",
                provider_id="openai",
                display_name="OpenAI GPT-4o-mini (Legacy — Aliased to GPT-6 Luna)",
                tier=ProviderTier.P0_DIRECT,
                model_family="gpt-4",
                alias_to="gpt-6-luna",
                capabilities=ModelCapabilities(
                    reasoning_effort=False,
                    tool_calling=True,
                    vision=True,
                    json_schema=True,
                    supports_responses_api=False,
                    supports_streaming=True,
                    max_context_tokens=128_000,
                    max_output_tokens=16_384,
                    strengths=[
                        TaskCategory.DOCUMENTATION_SPECS,
                        TaskCategory.FAST_SCAFFOLDING,
                        TaskCategory.TEST_ENGINEERING,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=0.15, output_price_per_m=0.60),
                quality_score=87.0,
                latency_p50_ms=380.0,
                reliability_score=99.8,
                status=MaturityStatus.VERIFIED,
            ),
            ModelRecord(
                model_id="o1",
                provider_id="openai",
                display_name="OpenAI o1 (Full Reasoning)",
                tier=ProviderTier.P0_DIRECT,
                capabilities=ModelCapabilities(
                    reasoning_effort=True,
                    tool_calling=True,
                    vision=True,
                    json_schema=True,
                    max_context_tokens=200_000,
                    max_output_tokens=100_000,
                    strengths=[
                        TaskCategory.ARCHITECTURE_DESIGN,
                        TaskCategory.SECURITY_AUDIT,
                        TaskCategory.DEBUGGING_RCA,
                        TaskCategory.ML_DATA_SCIENCE,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=15.00, output_price_per_m=60.00),
                quality_score=98.5,
                latency_p50_ms=4500.0,
                reliability_score=99.4,
                status=MaturityStatus.VERIFIED,
            ),
            ModelRecord(
                model_id="o3-mini",
                provider_id="openai",
                display_name="OpenAI o3-mini (Reasoning & Coding)",
                tier=ProviderTier.P0_DIRECT,
                capabilities=ModelCapabilities(
                    reasoning_effort=True,
                    tool_calling=True,
                    vision=False,
                    json_schema=True,
                    max_context_tokens=200_000,
                    max_output_tokens=100_000,
                    strengths=[
                        TaskCategory.BACKEND_API,
                        TaskCategory.DATABASE_DATA,
                        TaskCategory.TEST_ENGINEERING,
                        TaskCategory.REFACTORING,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=1.10, output_price_per_m=4.40),
                quality_score=96.5,
                latency_p50_ms=1800.0,
                reliability_score=99.5,
                status=MaturityStatus.VERIFIED,
            ),
            # --- Anthropic Tier 0 ---
            ModelRecord(
                model_id="claude-3-7-sonnet",
                provider_id="anthropic",
                display_name="Anthropic Claude 3.7 Sonnet (Hybrid Reasoning)",
                tier=ProviderTier.P0_DIRECT,
                capabilities=ModelCapabilities(
                    reasoning_effort=True,
                    tool_calling=True,
                    vision=True,
                    json_schema=True,
                    max_context_tokens=200_000,
                    max_output_tokens=64_000,
                    strengths=[
                        TaskCategory.ARCHITECTURE_DESIGN,
                        TaskCategory.REFACTORING,
                        TaskCategory.SECURITY_AUDIT,
                        TaskCategory.CODE_REVIEW,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=3.00, output_price_per_m=15.00),
                quality_score=99.0,
                latency_p50_ms=1200.0,
                reliability_score=99.7,
                status=MaturityStatus.VERIFIED,
            ),
            ModelRecord(
                model_id="claude-3-5-sonnet",
                provider_id="anthropic",
                display_name="Anthropic Claude 3.5 Sonnet",
                tier=ProviderTier.P0_DIRECT,
                capabilities=ModelCapabilities(
                    reasoning_effort=False,
                    tool_calling=True,
                    vision=True,
                    json_schema=True,
                    max_context_tokens=200_000,
                    max_output_tokens=8_192,
                    strengths=[
                        TaskCategory.FRONTEND_UI,
                        TaskCategory.BACKEND_API,
                        TaskCategory.REFACTORING,
                        TaskCategory.CODE_REVIEW,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=3.00, output_price_per_m=15.00),
                quality_score=97.5,
                latency_p50_ms=850.0,
                reliability_score=99.7,
                status=MaturityStatus.VERIFIED,
            ),
            ModelRecord(
                model_id="claude-3-5-haiku",
                provider_id="anthropic",
                display_name="Anthropic Claude 3.5 Haiku",
                tier=ProviderTier.P0_DIRECT,
                capabilities=ModelCapabilities(
                    reasoning_effort=False,
                    tool_calling=True,
                    vision=False,
                    json_schema=True,
                    max_context_tokens=200_000,
                    max_output_tokens=8_192,
                    strengths=[
                        TaskCategory.DOCUMENTATION_SPECS,
                        TaskCategory.FAST_SCAFFOLDING,
                        TaskCategory.TEST_ENGINEERING,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=0.80, output_price_per_m=4.00),
                quality_score=89.0,
                latency_p50_ms=390.0,
                reliability_score=99.8,
                status=MaturityStatus.VERIFIED,
            ),
            # --- Google Gemini Tier 0 ---
            ModelRecord(
                model_id="gemini-2.0-flash",
                provider_id="gemini",
                display_name="Google Gemini 2.0 Flash",
                tier=ProviderTier.P0_DIRECT,
                capabilities=ModelCapabilities(
                    reasoning_effort=True,
                    tool_calling=True,
                    vision=True,
                    json_schema=True,
                    max_context_tokens=1_048_576,
                    max_output_tokens=8_192,
                    strengths=[
                        TaskCategory.FAST_SCAFFOLDING,
                        TaskCategory.DEVOPS_INFRA,
                        TaskCategory.DEBUGGING_RCA,
                        TaskCategory.GENERAL_ORCHESTRATION,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=0.10, output_price_per_m=0.40),
                quality_score=93.0,
                latency_p50_ms=320.0,
                reliability_score=99.8,
                status=MaturityStatus.VERIFIED,
            ),
            ModelRecord(
                model_id="gemini-1.5-pro",
                provider_id="gemini",
                display_name="Google Gemini 1.5 Pro (2M Context)",
                tier=ProviderTier.P0_DIRECT,
                capabilities=ModelCapabilities(
                    reasoning_effort=True,
                    tool_calling=True,
                    vision=True,
                    json_schema=True,
                    max_context_tokens=2_097_152,
                    max_output_tokens=8_192,
                    strengths=[
                        TaskCategory.ARCHITECTURE_DESIGN,
                        TaskCategory.DEBUGGING_RCA,
                        TaskCategory.DOCUMENTATION_SPECS,
                        TaskCategory.ML_DATA_SCIENCE,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=1.25, output_price_per_m=5.00),
                quality_score=96.0,
                latency_p50_ms=1100.0,
                reliability_score=99.5,
                status=MaturityStatus.VERIFIED,
            ),
            # --- xAI Tier 0 ---
            ModelRecord(
                model_id="grok-2",
                provider_id="xai",
                display_name="xAI Grok 2",
                tier=ProviderTier.P0_DIRECT,
                capabilities=ModelCapabilities(
                    reasoning_effort=False,
                    tool_calling=True,
                    vision=True,
                    json_schema=True,
                    max_context_tokens=131_072,
                    max_output_tokens=8_192,
                    strengths=[
                        TaskCategory.BACKEND_API,
                        TaskCategory.CODE_REVIEW,
                        TaskCategory.DEVOPS_INFRA,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=2.00, output_price_per_m=10.00),
                quality_score=93.5,
                latency_p50_ms=900.0,
                reliability_score=99.1,
                status=MaturityStatus.VERIFIED,
            ),
            # --- Tier 2 / Local Inference ---
            ModelRecord(
                model_id="ollama/qwen2.5-coder-32b",
                provider_id="ollama",
                display_name="Qwen 2.5 Coder 32B (Local)",
                tier=ProviderTier.P2_LOCAL_SPECIALIZED,
                capabilities=ModelCapabilities(
                    reasoning_effort=False,
                    tool_calling=True,
                    vision=False,
                    json_schema=True,
                    max_context_tokens=32_768,
                    max_output_tokens=8_192,
                    strengths=[
                        TaskCategory.BACKEND_API,
                        TaskCategory.FAST_SCAFFOLDING,
                        TaskCategory.TEST_ENGINEERING,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=0.0, output_price_per_m=0.0),
                quality_score=91.0,
                latency_p50_ms=650.0,
                reliability_score=98.5,
                status=MaturityStatus.VERIFIED,
            ),
            ModelRecord(
                model_id="ollama/deepseek-r1-70b",
                provider_id="ollama",
                display_name="DeepSeek R1 Distill 70B (Local Reasoning)",
                tier=ProviderTier.P2_LOCAL_SPECIALIZED,
                capabilities=ModelCapabilities(
                    reasoning_effort=True,
                    tool_calling=False,
                    vision=False,
                    json_schema=True,
                    max_context_tokens=65_536,
                    max_output_tokens=8_192,
                    strengths=[
                        TaskCategory.ARCHITECTURE_DESIGN,
                        TaskCategory.SECURITY_AUDIT,
                        TaskCategory.DEBUGGING_RCA,
                    ],
                ),
                pricing=ModelPricing(input_price_per_m=0.0, output_price_per_m=0.0),
                quality_score=95.5,
                latency_p50_ms=2200.0,
                reliability_score=98.0,
                status=MaturityStatus.VERIFIED,
            ),
        ]

        for record in canonical_records:
            self.register(record)
