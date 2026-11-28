"""OpenClone Model Intelligence Engine (MIE) — Task Intelligence Classifier.

Deterministically classifies engineering tasks into 14 categories,
extracting complexity, context limits, reasoning, and tool requirements.
"""

from __future__ import annotations

import re
import uuid
from typing import List, Optional, Tuple

from src.openclone.mie.models import TaskCategory, TaskRequirement


class TaskClassifier:
    """Classifies user instructions and engineering tasks into structured requirements."""

    # Deterministic pattern matching rules for 14 categories
    CATEGORY_PATTERNS: List[Tuple[TaskCategory, List[str]]] = [
        (
            TaskCategory.SECURITY_AUDIT,
            [
                r"\b(security|vulnerability|cve|cwe|owasp|xss|sql injection|csrf|penetration|sanitize|auth bypass)\b",
                r"\b(secret leak|credential|exploit|threat model|audit rules)\b",
            ],
        ),
        (
            TaskCategory.ARCHITECTURE_DESIGN,
            [
                r"\b(architect(ure)?|high-level design|system design|adr|trade-off|monolith|microservice|distributed)\b",
                r"\b(blueprint|domain decomposition|tier architecture|subsystem topology)\b",
            ],
        ),
        (
            TaskCategory.FRONTEND_UI,
            [
                r"\b(frontend|react|vue|angular|css|html|tailwind|ui component|layout|responsive|a11y|accessibility)\b",
                r"\b(button|modal|navbar|viewport|canvas|dom|svg render)\b",
            ],
        ),
        (
            TaskCategory.DATABASE_DATA,
            [
                r"\b(database|sql|postgres|mysql|sqlite|schema migration|index(ing)?|query optimization|orm|prisma)\b",
                r"\b(bigquery|nosql|mongodb|foreign key|data model|ddl)\b",
            ],
        ),
        (
            TaskCategory.DEVOPS_INFRA,
            [
                r"\b(devops|docker|dockerfile|kubernetes|k8s|helm|ci/cd|github actions|pipeline|terraform|ansible)\b",
                r"\b(deploy(ment)?|container|nginx|ingress|aws|gcp|azure cloud)\b",
            ],
        ),
        (
            TaskCategory.TEST_ENGINEERING,
            [
                r"\b(unit test|integration test|mock|pytest|jest|test coverage|regression test|assert(ion)?)\b",
                r"\b(e2e test|fixture|test suite|tdd)\b",
            ],
        ),
        (
            TaskCategory.DEBUGGING_RCA,
            [
                r"\b(debug|traceback|exception|root cause|rca|stack trace|segfault|crash|bug fix|error log)\b",
                r"\b(memory leak|infinite loop|panic)\b",
            ],
        ),
        (
            TaskCategory.REFACTORING,
            [
                r"\b(refactor|clean code|code smell|dead code|anti-slop|simplify|dry|solid principle|technical debt)\b",
                r"\b(extract method|modernize syntax|restructure)\b",
            ],
        ),
        (
            TaskCategory.BACKEND_API,
            [
                r"\b(backend|api|rest|endpoint|grpc|graphql|controller|middleware|route handler|server)\b",
                r"\b(fastapi|flask|express|spring boot|payload|serialization)\b",
            ],
        ),
        (
            TaskCategory.DOCUMENTATION_SPECS,
            [
                r"\b(readme|documentation|docstring|api spec|openapi|swagger|manual|guide|release note)\b",
                r"\b(changelog|technical doc|specification)\b",
            ],
        ),
        (
            TaskCategory.FAST_SCAFFOLDING,
            [
                r"\b(scaffold|boilerplate|starter template|stub|quick script|crud skeleton)\b",
            ],
        ),
        (
            TaskCategory.CODE_REVIEW,
            [
                r"\b(code review|pr review|pull request audit|diff check|lint check)\b",
            ],
        ),
        (
            TaskCategory.ML_DATA_SCIENCE,
            [
                r"\b(machine learning|ml model|deep learning|pyspark|data pipeline|pandas|numpy|training script)\b",
                r"\b(pytorch|tensorflow|embedding|dataset)\b",
            ],
        ),
        (
            TaskCategory.GENERAL_ORCHESTRATION,
            [
                r"\b(orchestrat(e|ion)|workflow|agent coordination|lifecycle|execute task|plan)\b",
            ],
        ),
    ]

    @classmethod
    def classify(
        cls,
        prompt: str,
        task_id: Optional[str] = None,
        preferred_model: Optional[str] = None,
        allowed_providers: Optional[List[str]] = None,
    ) -> TaskRequirement:
        """Classify prompt text into structured TaskRequirement."""
        tid = task_id or f"task_{uuid.uuid4().hex[:10]}"
        lower_prompt = prompt.lower()

        detected_category = TaskCategory.BACKEND_API  # Default engineering fallback
        highest_match_count = 0

        for category, patterns in cls.CATEGORY_PATTERNS:
            match_count = 0
            for pat in patterns:
                matches = re.findall(pat, lower_prompt, flags=re.IGNORECASE)
                match_count += len(matches)
            if match_count > highest_match_count:
                highest_match_count = match_count
                detected_category = category

        # Extract reasoning requirement
        reasoning_keywords = [
            "deep thought", "reasoning", "complex logic", "proof", "formal verification",
            "step-by-step", "mathematical", "subtle bug", "security audit", "architecture trade-off"
        ]
        requires_reasoning = (
            detected_category in {TaskCategory.ARCHITECTURE_DESIGN, TaskCategory.SECURITY_AUDIT, TaskCategory.DEBUGGING_RCA}
            or any(k in lower_prompt for k in reasoning_keywords)
        )

        # Extract tools requirement
        requires_tools = any(k in lower_prompt for k in ["call tool", "mcp", "execute function", "terminal", "filesystem"])

        # Extract vision requirement
        requires_vision = any(k in lower_prompt for k in ["image", "screenshot", "diagram", "wireframe", "visual mockup"])

        # Context tokens estimation
        min_context = 4_000
        prompt_len = len(prompt)
        if prompt_len > 10_000:
            min_context = 64_000
        elif prompt_len > 4_000:
            min_context = 16_000

        if detected_category in {TaskCategory.ARCHITECTURE_DESIGN, TaskCategory.DEBUGGING_RCA, TaskCategory.SECURITY_AUDIT}:
            min_context = max(min_context, 32_000)

        return TaskRequirement(
            task_id=tid,
            prompt=prompt,
            category=detected_category,
            requires_reasoning=requires_reasoning,
            requires_tools=requires_tools,
            requires_vision=requires_vision,
            min_context_tokens=min_context,
            preferred_model=preferred_model,
            allowed_providers=allowed_providers,
        )
