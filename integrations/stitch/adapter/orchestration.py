"""UI/UX Engineering and Google Stitch Orchestrator.
Coordinates the end-to-end design pipeline:
Design Brief Analysis -> 3-Concept Differentiation -> Concept Selection ->
Stitch MCP Execution -> React/Native Frontend Generation -> 10-Dimension Visual QA.
"""
from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.openclone.skills.ui_ux_engineering import (
    UIUXEngineeringEngine,
    DesignArchetype,
    DesignBrief,
    DesignConcept,
    ConceptComparisonReport,
    VisualQAScorecard,
)
from .discovery import StitchDiscovery
from .loader import StitchSkillLoader
from .mcp_client import StitchMCPClient, StitchMCPConfig


@dataclass
class OrchestrationPlan:
    """Execution plan for an end-to-end Stitch UI/UX design workflow."""
    task_id: str
    requirement: str
    archetype: str
    design_brief: Optional[DesignBrief]
    concept_report: Optional[ConceptComparisonReport]
    anti_slop_violations: List[str]
    selected_stitch_skills: List[str]
    stitch_operations: List[Dict[str, Any]]
    frontend_framework: str = "react"
    visual_qa_scorecard: Optional[VisualQAScorecard] = None
    design_tokens: Dict[str, Any] = field(default_factory=dict)
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "requirement": self.requirement,
            "archetype": self.archetype,
            "design_brief": self.design_brief.to_dict() if self.design_brief else None,
            "concept_report": self.concept_report.to_dict() if self.concept_report else None,
            "anti_slop_violations": self.anti_slop_violations,
            "selected_stitch_skills": self.selected_stitch_skills,
            "stitch_operations": self.stitch_operations,
            "frontend_framework": self.frontend_framework,
            "visual_qa_scorecard": self.visual_qa_scorecard.to_dict() if self.visual_qa_scorecard else None,
            "design_tokens": self.design_tokens,
            "summary": self.summary,
        }


class StitchDesignOrchestrator:
    """Orchestrates OpenClone UI/UX Engineering with Google Stitch skills."""

    def __init__(
        self,
        ui_engine: Optional[UIUXEngineeringEngine] = None,
        mcp_client: Optional[StitchMCPClient] = None,
        loader: Optional[StitchSkillLoader] = None,
    ):
        self.ui_engine = ui_engine or UIUXEngineeringEngine()
        self.mcp_client = mcp_client or StitchMCPClient()
        self.loader = loader or StitchSkillLoader()

    def analyze_brief(self, prompt: str, project_name: str = "Project") -> DesignBrief:
        """Synthesize an inspectable 12-dimension design brief."""
        return self.ui_engine.synthesize_design_brief(prompt, project_name)

    def generate_concepts(self, brief: DesignBrief) -> ConceptComparisonReport:
        """Generate 3 distinct concepts and select the optimal direction."""
        return self.ui_engine.generate_three_concepts(brief)

    def plan_workflow(
        self,
        requirement: str,
        source_code_path: Optional[str] = None,
        framework: str = "react",
        project_name: str = "Project",
    ) -> OrchestrationPlan:
        """Create a complete governed design execution plan with 3-concept differentiation."""
        # 1. Synthesize Design Brief
        brief = self.analyze_brief(requirement, project_name)
        selected_archetype = brief.recommended_archetypes[0] if brief.recommended_archetypes else DesignArchetype.SAAS_ADMIN_APP

        # 2. Generate and evaluate 3 distinct concepts
        concept_report = self.generate_concepts(brief)

        # 3. Audit existing code / prompt for anti-slop violations
        violations = []
        if source_code_path and Path(source_code_path).exists():
            for f in Path(source_code_path).rglob("*"):
                if f.is_file() and f.suffix in [".tsx", ".jsx", ".html", ".css"]:
                    try:
                        content = f.read_text(encoding="utf-8", errors="ignore")
                        _, flagged = self.ui_engine.audit_anti_slop(content, selected_archetype)
                        violations.extend(flagged)
                    except Exception:
                        pass
        else:
            _, flagged = self.ui_engine.audit_anti_slop(requirement, selected_archetype)
            violations = flagged

        # 4. Select Stitch skills based on workflow
        selected_skills = []
        operations = []

        if source_code_path:
            selected_skills.extend([
                "stitch-extract-design-md",
                "stitch-extract-static-html",
                "stitch-code-to-design",
            ])
            operations.append({
                "phase": "Extract Design System",
                "skill": "stitch-extract-design-md",
                "action": "Scan source directory to extract tokens into .stitch/DESIGN.md",
            })
            operations.append({
                "phase": "Extract Static HTML",
                "skill": "stitch-extract-static-html",
                "action": "Capture standalone HTML representation of running application",
            })

        # Design system & prompt enhancement
        selected_skills.extend([
            "stitch-enhance-prompt",
            "stitch-taste-design",
            "stitch-generate-design",
        ])
        operations.append({
            "phase": "Prompt Refinement",
            "skill": "stitch-enhance-prompt",
            "action": f"Enhance prompt with {selected_archetype.value} UI/UX vocabulary and token rules",
        })
        operations.append({
            "phase": "Generate Design Variants",
            "skill": "stitch-generate-design",
            "action": f"Invoke Stitch MCP generate_screen_from_text for '{concept_report.selected_concept_id}'",
        })

        # Build phase
        if framework == "react_native":
            selected_skills.append("stitch-react-native")
            operations.append({
                "phase": "Component Compilation",
                "skill": "stitch-react-native",
                "action": "Transform Stitch HTML designs into React Native StyleSheet components",
            })
        else:
            selected_skills.append("stitch-react-components")
            operations.append({
                "phase": "Component Compilation",
                "skill": "stitch-react-components",
                "action": "Transform Stitch HTML designs into modular React components with design tokens",
            })

        # 5. Tokens & Summary
        tokens = self.ui_engine.generate_design_system_tokens(selected_archetype)
        summary = (
            f"Orchestrated Stitch workflow for [{selected_archetype.value}]: "
            f"Brief synthesized, 3 concepts evaluated, selected '{concept_report.selected_concept_id}'. "
            f"{len(selected_skills)} skills selected, {len(operations)} phases planned. "
            f"Anti-slop rules enforced: {len(violations)} issues flagged."
        )

        return OrchestrationPlan(
            task_id="stitch-plan-001",
            requirement=requirement,
            archetype=selected_archetype.value,
            design_brief=brief,
            concept_report=concept_report,
            anti_slop_violations=violations,
            selected_stitch_skills=selected_skills,
            stitch_operations=operations,
            frontend_framework=framework,
            design_tokens=tokens,
            summary=summary,
        )

    def evaluate_implementation_qa(
        self,
        component_code: str,
        archetype_str: str = "saas_admin_app",
    ) -> VisualQAScorecard:
        """Run 10-dimension Visual QA on generated code."""
        try:
            archetype = DesignArchetype(archetype_str)
        except ValueError:
            archetype = DesignArchetype.SAAS_ADMIN_APP

        return self.ui_engine.evaluate_visual_qa(component_code, archetype)
