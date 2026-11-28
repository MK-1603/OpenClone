"""OpenClone Model Intelligence Engine (MIE) — Multi-Dimensional Scoring Engine.

Scores candidate models against task requirements across 6 criteria:
1. Task Suitability & Correctness (30%)
2. Code Quality & Idiomatic Output (20%)
3. Provider Reliability & Uptime (20%)
4. Latency & Time-to-First-Token (10%)
5. Cost Efficiency & Token Value (10%)
6. Tool Execution & Schema Adherence (10%)
"""

from __future__ import annotations

from typing import Dict, List

from src.openclone.mie.models import (
    CandidateScore,
    ModelRecord,
    RoutingMode,
    TaskRequirement,
)


class ModelEvaluator:
    """Evaluates and ranks candidate models using weighted multi-dimensional scoring."""

    # Baseline weight distributions across routing modes
    MODE_WEIGHTS: Dict[RoutingMode, Dict[str, float]] = {
        RoutingMode.BALANCED: {
            "suitability": 0.30,
            "quality": 0.20,
            "reliability": 0.20,
            "latency": 0.10,
            "cost": 0.10,
            "tool": 0.10,
        },
        RoutingMode.BEST_QUALITY: {
            "suitability": 0.35,
            "quality": 0.45,
            "reliability": 0.20,
            "latency": 0.00,
            "cost": 0.00,
            "tool": 0.00,
        },
        RoutingMode.LOW_LATENCY: {
            "suitability": 0.20,
            "quality": 0.20,
            "reliability": 0.10,
            "latency": 0.40,
            "cost": 0.05,
            "tool": 0.05,
        },
        RoutingMode.LOW_COST: {
            "suitability": 0.25,
            "quality": 0.15,
            "reliability": 0.10,
            "latency": 0.05,
            "cost": 0.40,
            "tool": 0.05,
        },
        RoutingMode.HIGH_AVAILABILITY: {
            "suitability": 0.25,
            "quality": 0.25,
            "reliability": 0.45,
            "latency": 0.05,
            "cost": 0.00,
            "tool": 0.00,
        },
        RoutingMode.USER_SELECTED: {
            "suitability": 0.20,
            "quality": 0.20,
            "reliability": 0.40,
            "latency": 0.10,
            "cost": 0.10,
            "tool": 0.00,
        },
        RoutingMode.POLICY_CONTROLLED: {
            "suitability": 0.30,
            "quality": 0.25,
            "reliability": 0.25,
            "latency": 0.10,
            "cost": 0.10,
            "tool": 0.00,
        },
    }

    @classmethod
    def evaluate(
        cls,
        candidate: ModelRecord,
        req: TaskRequirement,
        mode: RoutingMode = RoutingMode.BALANCED,
    ) -> CandidateScore:
        """Score an individual candidate model against task requirement and routing mode."""
        weights = cls.MODE_WEIGHTS.get(mode, cls.MODE_WEIGHTS[RoutingMode.BALANCED])

        # 1. Suitability score (0.0 to 100.0)
        suitability = 70.0
        if req.category in candidate.capabilities.strengths:
            suitability += 25.0
        if req.requires_reasoning and candidate.capabilities.reasoning_effort:
            suitability += 5.0
        suitability = min(100.0, suitability)

        # 2. Quality score (0.0 to 100.0)
        quality = candidate.quality_score

        # 3. Reliability score (0.0 to 100.0)
        reliability = candidate.reliability_score

        # 4. Latency score (faster = higher, normalized: 200ms -> 100, 3000ms -> 30)
        p50 = max(100.0, candidate.latency_p50_ms)
        latency_score = max(10.0, min(100.0, 100.0 - (p50 / 35.0)))

        # 5. Cost score (cheaper = higher, normalized: $0/M -> 100, $60/M -> 20)
        combined_price = candidate.pricing.input_price_per_m + candidate.pricing.output_price_per_m
        cost_score = max(15.0, min(100.0, 100.0 - (combined_price * 1.2)))

        # 6. Tool execution score
        tool_score = 90.0 if candidate.capabilities.tool_calling else 20.0
        if candidate.capabilities.json_schema:
            tool_score = min(100.0, tool_score + 10.0)

        dimension_scores = {
            "suitability": round(suitability, 1),
            "quality": round(quality, 1),
            "reliability": round(reliability, 1),
            "latency": round(latency_score, 1),
            "cost": round(cost_score, 1),
            "tool": round(tool_score, 1),
        }

        # Weighted calculation
        total = sum(dimension_scores[dim] * weights[dim] for dim in weights)

        # Special bonus if user explicitly preferred this model
        if req.preferred_model and candidate.model_id == req.preferred_model:
            total += 15.0

        rationale = (
            f"Suitability: {dimension_scores['suitability']}, Quality: {dimension_scores['quality']}, "
            f"Reliability: {dimension_scores['reliability']}, Latency: {dimension_scores['latency']}, "
            f"Cost: {dimension_scores['cost']}"
        )

        return CandidateScore(
            model=candidate,
            total_score=round(total, 2),
            dimension_scores=dimension_scores,
            rationale=rationale,
        )

    @classmethod
    def rank_candidates(
        cls,
        candidates: List[ModelRecord],
        req: TaskRequirement,
        mode: RoutingMode = RoutingMode.BALANCED,
    ) -> List[CandidateScore]:
        """Score and sort all candidate models in descending order of total score."""
        scored = [cls.evaluate(m, req, mode) for m in candidates]
        scored.sort(key=lambda s: s.total_score, reverse=True)
        return scored
