"""Execution mode policies for controlled autonomous engineering operations."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from src.openclone.autonomous.models import ExecutionMode


@dataclass(frozen=True)
class ExecutionModePolicy:
    """Deterministic governance and resource policy for an execution mode."""
    mode: ExecutionMode
    planning_depth: str       # "minimal", "lightweight", "full", "exhaustive", "adaptive"
    max_tasks: int
    model_tier: str           # "fast", "balanced", "reasoning", "frontier"
    reasoning_budget: str     # "minimal", "standard", "extended", "maximum"
    token_budget: int
    time_budget_seconds: int
    max_retries: int
    verification_depth: str   # "syntax", "unit", "standard", "comprehensive", "independent_egm"
    require_human_approval_for: tuple[str, ...]  # Risk levels that halt for human sign-off


_POLICIES: Dict[ExecutionMode, ExecutionModePolicy] = {
    ExecutionMode.INSTANT: ExecutionModePolicy(
        mode=ExecutionMode.INSTANT,
        planning_depth="minimal",
        max_tasks=1,
        model_tier="fast",
        reasoning_budget="minimal",
        token_budget=16_000,
        time_budget_seconds=120,
        max_retries=1,
        verification_depth="syntax",
        require_human_approval_for=("HIGH", "CRITICAL"),
    ),
    ExecutionMode.FAST: ExecutionModePolicy(
        mode=ExecutionMode.FAST,
        planning_depth="lightweight",
        max_tasks=3,
        model_tier="balanced",
        reasoning_budget="standard",
        token_budget=64_000,
        time_budget_seconds=300,
        max_retries=2,
        verification_depth="unit",
        require_human_approval_for=("HIGH", "CRITICAL"),
    ),
    ExecutionMode.STANDARD: ExecutionModePolicy(
        mode=ExecutionMode.STANDARD,
        planning_depth="full",
        max_tasks=10,
        model_tier="reasoning",
        reasoning_budget="extended",
        token_budget=256_000,
        time_budget_seconds=900,
        max_retries=3,
        verification_depth="standard",
        require_human_approval_for=("MEDIUM", "HIGH", "CRITICAL"),
    ),
    ExecutionMode.DEEP: ExecutionModePolicy(
        mode=ExecutionMode.DEEP,
        planning_depth="exhaustive",
        max_tasks=25,
        model_tier="frontier",
        reasoning_budget="maximum",
        token_budget=512_000,
        time_budget_seconds=1800,
        max_retries=4,
        verification_depth="comprehensive",
        require_human_approval_for=("LOW", "MEDIUM", "HIGH", "CRITICAL"),
    ),
    ExecutionMode.AUTONOMOUS: ExecutionModePolicy(
        mode=ExecutionMode.AUTONOMOUS,
        planning_depth="adaptive",
        max_tasks=20,
        model_tier="frontier",
        reasoning_budget="extended",
        token_budget=512_000,
        time_budget_seconds=1800,
        max_retries=3,
        verification_depth="independent_egm",
        require_human_approval_for=("HIGH", "CRITICAL"),
    ),
}


def get_mode_policy(mode: ExecutionMode) -> ExecutionModePolicy:
    """Retrieve the authoritative execution mode policy."""
    return _POLICIES.get(mode, _POLICIES[ExecutionMode.STANDARD])
