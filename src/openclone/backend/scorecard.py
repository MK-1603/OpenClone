"""OpenClone Backend Production Readiness Scorecard.

Assesses systems across 15 mandatory engineering categories, providing
evidence-backed grading, defect identification, and release-gate verdicts.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional


class ScorecardStatus(str, enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    ACCEPTED_RISK = "ACCEPTED_RISK"


@dataclass
class CategoryAssessment:
    """Evaluation result for one of the 15 production categories."""
    category: str
    status: ScorecardStatus
    score: float  # 0.0 to 100.0
    evidence: str
    findings: List[str] = field(default_factory=list)
    remediations: List[str] = field(default_factory=list)


@dataclass
class ScorecardResult:
    """Consolidated production readiness report."""
    project_name: str
    overall_status: ScorecardStatus
    passed_categories: int
    failed_categories: int
    total_categories: int
    assessments: Dict[str, CategoryAssessment] = field(default_factory=dict)
    blocking_issues: List[str] = field(default_factory=list)


class BackendProductionScorecard:
    """Evaluates backend architecture and implementation across 15 production categories."""

    CATEGORIES = [
        "Architecture",
        "API",
        "Database",
        "Security",
        "Rate Limiting",
        "Caching",
        "Async Processing",
        "Distributed Systems",
        "Reliability",
        "Performance",
        "Observability",
        "Testing",
        "Deployment",
        "Data Governance",
        "Cost",
    ]

    @classmethod
    def evaluate(cls, project_name: str, audit_data: Dict[str, Any]) -> ScorecardResult:
        """Produce deterministic production readiness scorecard from audit findings."""
        assessments: Dict[str, CategoryAssessment] = {}
        blocking_issues: List[str] = []

        for cat in cls.CATEGORIES:
            data = audit_data.get(cat.lower().replace(" ", "_"), {})
            status_str = data.get("status", "FAIL")
            score = float(data.get("score", 0.0))
            evidence = data.get("evidence", "No evidence recorded")
            findings = data.get("findings", [])
            remediations = data.get("remediations", [])

            status = ScorecardStatus(status_str) if status_str in ScorecardStatus._value2member_map_ else ScorecardStatus.FAIL

            if status in [ScorecardStatus.FAIL, ScorecardStatus.BLOCKED]:
                blocking_issues.extend([f"[{cat}] {f}" for f in findings] or [f"[{cat}] Category failed without specific finding."])

            assessments[cat] = CategoryAssessment(
                category=cat,
                status=status,
                score=score,
                evidence=evidence,
                findings=findings,
                remediations=remediations,
            )

        passed = sum(1 for a in assessments.values() if a.status in [ScorecardStatus.PASS, ScorecardStatus.NOT_APPLICABLE, ScorecardStatus.ACCEPTED_RISK])
        failed = sum(1 for a in assessments.values() if a.status in [ScorecardStatus.FAIL, ScorecardStatus.BLOCKED])

        if failed == 0:
            overall = ScorecardStatus.PASS
        elif any(a.status == ScorecardStatus.BLOCKED for a in assessments.values()):
            overall = ScorecardStatus.BLOCKED
        else:
            overall = ScorecardStatus.FAIL

        return ScorecardResult(
            project_name=project_name,
            overall_status=overall,
            passed_categories=passed,
            failed_categories=failed,
            total_categories=len(cls.CATEGORIES),
            assessments=assessments,
            blocking_issues=blocking_issues,
        )

    @classmethod
    def generate_markdown(cls, result: ScorecardResult) -> str:
        """Format scorecard result into verified Markdown report."""
        lines = [
            f"# BACKEND PRODUCTION READINESS SCORECARD — {result.project_name}",
            f"**Overall Release Gate Verdict**: `{result.overall_status.value}`",
            f"**Passed**: {result.passed_categories}/{result.total_categories} | **Failed**: {result.failed_categories}/{result.total_categories}",
            "",
            "---",
            "",
            "## 1. 15-Category Production Assessment",
            "",
            "| Category | Status | Score | Observable Evidence | Remediation / Finding |",
            "|---|:---:|:---:|---|---|",
        ]
        for cat, a in result.assessments.items():
            finding_text = "; ".join(a.findings) if a.findings else "None"
            lines.append(f"| **{cat}** | `{a.status.value}` | {a.score:.1f}% | {a.evidence} | {finding_text} |")

        if result.blocking_issues:
            lines.extend([
                "",
                "---",
                "",
                "## 2. Blocking Production Issues",
                "",
            ])
            for b in result.blocking_issues:
                lines.append(f"- [x] **BLOCKER**: {b}")

        return "\n".join(lines) + "\n"
