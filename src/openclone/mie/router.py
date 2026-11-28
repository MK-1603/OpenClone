"""OpenClone Model Intelligence Engine (MIE) — Intelligent Multi-Mode Router.

Coordinates model discovery, task classification, multi-dimensional scoring,
circuit breaker validation, and fallback chain assembly.
"""

from __future__ import annotations

from typing import List, Optional

from src.openclone.mie.classifier import TaskClassifier
from src.openclone.mie.contracts import BaseProvider
from src.openclone.mie.evaluator import ModelEvaluator
from src.openclone.mie.ha import HighAvailabilityEngine
from src.openclone.mie.models import (
    ModelRecord,
    RoutingDecision,
    RoutingMode,
    TaskRequirement,
)
from src.openclone.mie.registry import ModelRegistry


class ModelRouter:
    """Principal routing engine for OpenClone model selection and dispatch."""

    def __init__(
        self,
        registry: Optional[ModelRegistry] = None,
        ha_engine: Optional[HighAvailabilityEngine] = None,
    ):
        self.registry = registry or ModelRegistry()
        self.ha = ha_engine or HighAvailabilityEngine()

    def route_task(
        self,
        prompt: str,
        mode: RoutingMode = RoutingMode.BALANCED,
        preferred_model: Optional[str] = None,
        allowed_providers: Optional[List[str]] = None,
    ) -> RoutingDecision:
        """Classify prompt, filter candidates, rank models, and produce a RoutingDecision."""
        req = TaskClassifier.classify(
            prompt=prompt,
            preferred_model=preferred_model,
            allowed_providers=allowed_providers,
        )
        return self.route(req, mode=mode)

    def route(
        self,
        req: TaskRequirement,
        mode: RoutingMode = RoutingMode.BALANCED,
    ) -> RoutingDecision:
        """Generate a RoutingDecision for a pre-parsed TaskRequirement."""
        candidates = self.registry.filter_candidates(req)
        if not candidates:
            # Fallback to all models if strict filtering returned empty
            candidates = self.registry.list_all()

        # Score and rank all candidate models
        ranked_scores = ModelEvaluator.rank_candidates(candidates, req, mode=mode)

        # Check circuit breakers to find the first healthy model
        selected_model: Optional[ModelRecord] = None
        fallback_models: List[ModelRecord] = []

        for candidate_score in ranked_scores:
            m = candidate_score.model
            cb = self.ha.get_circuit_breaker(m.provider_id)
            if cb.can_execute():
                if selected_model is None:
                    selected_model = m
                else:
                    fallback_models.append(m)
            else:
                # Add open circuit breaker models to the tail of fallbacks
                fallback_models.append(m)

        # If all candidates had open circuit breakers, pick top-ranked anyway (best effort)
        if selected_model is None and ranked_scores:
            selected_model = ranked_scores[0].model
            fallback_models = [s.model for s in ranked_scores[1:]]

        # Assemble same-model provider failover targets
        provider_failover = self.ha.get_same_model_failover(selected_model.provider_id) if selected_model else []

        explanation = (
            f"Selected '{selected_model.display_name}' for task '{req.category.value}' under '{mode.value}' mode. "
            f"Top score: {ranked_scores[0].total_score if ranked_scores else 0.0}. "
            f"Fallback chain configured with {len(fallback_models)} alternative models across {len(provider_failover)} failover targets."
        )

        return RoutingDecision(
            task_id=req.task_id,
            selected_model=selected_model,
            routing_mode=mode,
            scores=ranked_scores[:5],  # Keep top 5 scores
            fallback_models=fallback_models[:3],  # Keep top 3 fallbacks
            provider_failover_targets=provider_failover,
            explanation=explanation,
        )
