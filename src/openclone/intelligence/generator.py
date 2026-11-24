"""OpenClone One-Click Idea-to-Project Package Generator.

Accepts a natural-language project idea, prompt, or PRD, and coordinates classification,
technology selection, workforce assembly, and 8-layer template composition to produce
a complete, governed project package.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.openclone.intelligence.blueprints import BlueprintManager
from src.openclone.intelligence.classifier import ProjectClassifier, ProjectProfile
from src.openclone.intelligence.composer import ProjectTemplateComposer
from src.openclone.intelligence.router import ProjectRouter, RoutingDecision
from src.openclone.intelligence.taxonomy import TaxonomyRegistry
from src.openclone.intelligence.technology import TechnologyDecision, TechnologyIntelligenceEngine


class ProjectPackageGenerator:
    """End-to-end generator producing governed project specifications from an idea or prompt."""

    def __init__(
        self,
        taxonomy: Optional[TaxonomyRegistry] = None,
        classifier: Optional[ProjectClassifier] = None,
        router: Optional[ProjectRouter] = None,
        tech_engine: Optional[TechnologyIntelligenceEngine] = None,
        composer: Optional[ProjectTemplateComposer] = None,
    ):
        self.taxonomy = taxonomy or TaxonomyRegistry()
        self.classifier = classifier or ProjectClassifier(self.taxonomy)
        self.router = router or ProjectRouter(self.taxonomy)
        self.tech_engine = tech_engine or TechnologyIntelligenceEngine()
        self.composer = composer or ProjectTemplateComposer()
        self.blueprint_mgr = BlueprintManager()

    def generate(
        self,
        prompt: str,
        project_name: str = "project",
        output_dir: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """Generate complete project package dict and optionally write to disk."""
        # 1. Multi-label Project Classification
        profile = self.classifier.classify_text(prompt, project_name=project_name)

        # 2. Technology Stack Evaluation
        decisions = self.tech_engine.evaluate(profile, requirements_text=prompt)

        # 3. Deterministic Domain & Workforce Routing
        routing = self.router.route(profile)

        # 4. 8-Layer Composable Template Generation
        project_md = self.composer.compose_project_md(profile, decisions, routing)
        build_prompt_md = self.composer.compose_build_prompt(profile, decisions, routing)
        agent_instructions_md = self.composer.compose_agent_instructions(profile, routing)
        env_example = self.composer.compose_env_example(decisions)

        # Implementation Plan
        impl_plan_lines = [
            f"# IMPLEMENTATION PLAN — {profile.project_name}",
            "",
            "## Phase Overview",
            "1. **Phase 1: Environment & Setup** — Validate dependencies, `.env.example`, and test runner.",
            "2. **Phase 2: Core Domain Implementation** — Implement core models and functional business logic.",
            "3. **Phase 3: Integration & Contracts** — Wire API routes, database schemas, and external providers.",
            "4. **Phase 4: Security & Quality Gates** — Run test suite, secret scanner, and responsive layout audits.",
            "5. **Phase 5: Final Review & Handoff** — Complete independent verification and prepare deployment readiness report.",
            "",
            "## Active Workflows",
        ]
        for wf in routing.workflows:
            impl_plan_lines.append(f"- `Stage {wf.stage}`: **{wf.workflow_id}** ({wf.name})")
        impl_plan_md = "\n".join(impl_plan_lines)

        # Acceptance Matrix
        acceptance_lines = [
            f"# ACCEPTANCE MATRIX — {profile.project_name}",
            "",
            "| ID | Requirement | Verification Method | Status | Responsible Role |",
            "|---|---|---|---|---|",
            "| ACC-01 | Environment initialization without missing variables | Automated check | PENDING | DevOps Engineer |",
            f"| ACC-02 | Core {profile.primary_type} functional capability | Unit test suite | PENDING | QA Engineer |",
            "| ACC-03 | Zero exposed credentials in git repository | `tools/scan_secrets.py` | PENDING | Security Engineer |",
            "| ACC-04 | Responsive layout verified (320px–1440px) | Component test | PENDING | Frontend Engineer |",
            "| ACC-05 | Independent verification checklist satisfied | EGM review | PENDING | Independent Verifier |",
            "",
        ]
        acceptance_matrix_md = "\n".join(acceptance_lines)

        # Security Plan
        security_plan_lines = [
            f"# SECURITY PLAN — {profile.project_name}",
            "",
            f"- **Data Sensitivity Classification:** `{profile.data_sensitivity}`",
            f"- **Reliability Tier:** `{profile.reliability_tier}`",
            "",
            "## Mandatory Controls",
            "1. **Secret Scanning:** Pre-commit and CI automated secret detection with fail-closed gates.",
            "2. **Token Redaction:** All sensitive keys masked in stdout/stderr and audit trails.",
            "3. **Least Privilege:** Subprocesses run with isolated sandbox permissions and strict timeouts.",
            "4. **Input Validation:** All boundary inputs validated against strict Pydantic/Zod schemas.",
            "",
        ]
        security_plan_md = "\n".join(security_plan_lines)

        # Synchronized Machine-Readable PROJECT-PROFILE.yaml
        profile_dict = profile.to_dict()
        profile_yaml_lines = [
            "# Synchronized OpenClone Machine-Readable Project Profile",
            f"project_id: \"{profile.project_id}\"",
            f"project_name: \"{profile.project_name}\"",
            f"primary_family: \"{profile.primary_family}\"",
            f"primary_type: \"{profile.primary_type}\"",
            f"secondary_types: {json.dumps(profile.secondary_types)}",
            f"supporting_disciplines: {json.dumps(profile.supporting_disciplines)}",
            f"classification_confidence: {profile.classification_confidence}",
            "complexity:",
            f"  level: \"{profile.complexity.level}\"",
            f"  rationale: \"{profile.complexity.rationale}\"",
            f"delivery_targets: {json.dumps(profile.delivery_targets)}",
            f"deployment_model: \"{profile.deployment_model}\"",
            f"ai_dependency: \"{profile.ai_dependency}\"",
            f"data_sensitivity: \"{profile.data_sensitivity}\"",
            f"reliability_tier: \"{profile.reliability_tier}\"",
            f"unresolved_questions: {json.dumps(profile.unresolved_questions)}",
            "conditional_profiles:",
        ]
        for cp_key, cp_val in profile.conditional_profiles.items():
            profile_yaml_lines.append(f"  {cp_key}: {json.dumps(cp_val)}")
        project_profile_yaml = "\n".join(profile_yaml_lines)

        package_artifacts = {
            "PROJECT.md": project_md,
            "BUILD_PROMPT.md": build_prompt_md,
            "AGENT_INSTRUCTIONS.md": agent_instructions_md,
            "IMPLEMENTATION_PLAN.md": impl_plan_md,
            "ACCEPTANCE_MATRIX.md": acceptance_matrix_md,
            "SECURITY_PLAN.md": security_plan_md,
            "PROJECT-PROFILE.yaml": project_profile_yaml,
            ".env.example": env_example,
        }

        # Write to disk if output_dir specified
        if output_dir:
            out_p = Path(output_dir)
            out_p.mkdir(parents=True, exist_ok=True)
            for fname, content in package_artifacts.items():
                (out_p / fname).write_text(content, encoding="utf-8")

        return {
            "profile": profile_dict,
            "technologies": [d.to_dict() for d in decisions],
            "routing": routing.to_dict(),
            "artifacts": package_artifacts,
        }
