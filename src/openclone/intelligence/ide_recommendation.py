"""IDE & AI Platform Recommendation Engine.

Analyzes technology stack, project languages, target architecture, team workflows,
and local developer environments to recommend optimal IDEs and generate targeted configuration templates.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class PlatformID(str, enum.Enum):
    """Supported IDE and AI developer platforms."""
    CURSOR = "cursor"
    WINDSURF = "windsurf"
    ANTIGRAVITY = "antigravity"
    VSCODE = "vscode"
    JETBRAINS = "jetbrains"
    ZED = "zed"


@dataclass
class IdeRecommendation:
    """Tailored recommendation for an IDE / AI platform."""
    platform_id: PlatformID
    display_name: str
    match_score: float  # 0.0 - 1.0
    rationale: List[str]
    is_primary: bool
    config_templates_available: List[str]
    supported_features: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "platform_id": self.platform_id.value,
            "display_name": self.display_name,
            "match_score": round(self.match_score, 2),
            "rationale": self.rationale,
            "is_primary": self.is_primary,
            "config_templates_available": self.config_templates_available,
            "supported_features": self.supported_features,
        }


class IdeRecommendationEngine:
    """Evaluates project traits and tech decisions to score and recommend developer platforms."""

    def evaluate(
        self,
        project_profile: Optional[Any] = None,
        technologies: Optional[List[Any]] = None,
        requirements_text: str = "",
    ) -> List[IdeRecommendation]:
        """Produce ranked IDE recommendations based on project architecture and technologies."""
        tech_names: Set[str] = set()
        if technologies:
            for t in technologies:
                name = t.name if hasattr(t, "name") else (t.get("name") if isinstance(t, dict) else str(t))
                tech_names.add(name.lower())

        text_lower = (requirements_text or "").lower()
        recommendations: List[IdeRecommendation] = []

        # 1. Antigravity Evaluation (Deep agentic multi-agent systems, GCP/Google Cloud, Python SDK)
        ag_score = 0.80
        ag_reasons = ["Native multi-agent autonomous engineering framework support", "Full MCP server and tool orchestration"]
        if any(k in text_lower or k in tech_names for k in ["gemini", "gcp", "google", "agent", "subagent", "autonomous", "orchestration"]):
            ag_score += 0.18
            ag_reasons.append("Optimized for agentic loops, subagents, and Google ecosystem workflows.")
        recommendations.append(
            IdeRecommendation(
                platform_id=PlatformID.ANTIGRAVITY,
                display_name="Google Antigravity",
                match_score=min(1.0, ag_score),
                rationale=ag_reasons,
                is_primary=False,
                config_templates_available=[".gemini/skills", ".antigravity/rules"],
                supported_features=["Dynamic subagents", "Deterministic audit ledger", "Dual-lane memory"],
            )
        )

        # 2. Windsurf Evaluation (Codeium Cascade, full-flow refactoring, Python, web, Rust)
        ws_score = 0.85
        ws_reasons = ["Deep Cascade multi-file context tracking", "Zero-friction fast terminal iteration"]
        if any(k in text_lower or k in tech_names for k in ["python", "fastapi", "react", "typescript", "rust", "go"]):
            ws_score += 0.12
            ws_reasons.append("High context retention across complex multi-file application backends.")
        recommendations.append(
            IdeRecommendation(
                platform_id=PlatformID.WINDSURF,
                display_name="Windsurf AI Editor",
                match_score=min(1.0, ws_score),
                rationale=ws_reasons,
                is_primary=False,
                config_templates_available=[".windsurfrules", ".codeium/windsurf/mcp_config.json"],
                supported_features=["Cascade workflows", "Deterministic rules", "MCP client support"],
            )
        )

        # 3. Cursor Evaluation (.cursorrules, Composer, fast inline diffs)
        cursor_score = 0.88
        cursor_reasons = ["Industry standard AI Composer interface", "Fast inline diff visualization"]
        if any(k in text_lower or k in tech_names for k in ["nextjs", "react", "node", "typescript"]):
            cursor_score += 0.10
            cursor_reasons.append("Superior TypeScript / Web ecosystem completions.")
        recommendations.append(
            IdeRecommendation(
                platform_id=PlatformID.CURSOR,
                display_name="Cursor AI Editor",
                match_score=min(1.0, cursor_score),
                rationale=cursor_reasons,
                is_primary=False,
                config_templates_available=[".cursor/mcp.json", ".cursorrules"],
                supported_features=["Composer multi-file editing", "Custom MCP tool discovery"],
            )
        )

        # 4. VS Code Evaluation (Universal extensions, widespread enterprise IT compliance)
        vscode_score = 0.75
        vscode_reasons = ["Universal extension marketplace", "Standard enterprise governance compliance"]
        recommendations.append(
            IdeRecommendation(
                platform_id=PlatformID.VSCODE,
                display_name="Visual Studio Code",
                match_score=vscode_score,
                rationale=vscode_reasons,
                is_primary=False,
                config_templates_available=[".vscode/extensions.json", ".vscode/settings.json"],
                supported_features=["GitHub Copilot Chat", "Remote Containers / DevContainers"],
            )
        )

        # 5. JetBrains Evaluation (Java, Kotlin, C++, heavy monolithic OOP codebases)
        jb_score = 0.65
        jb_reasons = ["Unmatched static refactoring for Java, Kotlin, and C++ codebases"]
        if any(k in text_lower or k in tech_names for k in ["java", "kotlin", "spring", "c++", "csharp", ".net"]):
            jb_score += 0.30
            jb_reasons.append("Deep AST indexation and enterprise JVM tooling.")
        recommendations.append(
            IdeRecommendation(
                platform_id=PlatformID.JETBRAINS,
                display_name="JetBrains IDEs",
                match_score=min(1.0, jb_score),
                rationale=jb_reasons,
                is_primary=False,
                config_templates_available=[".idea/runConfigurations"],
                supported_features=["Deep JVM inspection", "JetBrains AI Assistant"],
            )
        )

        # Sort descending by match_score
        recommendations.sort(key=lambda r: r.match_score, reverse=True)
        if recommendations:
            recommendations[0].is_primary = True

        return recommendations
