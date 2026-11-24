"""OpenClone Composable 8-Layer Project Template Composer.

Composes tailored, non-duplicated project specifications and engineering packages from:
1. Universal project foundation
2. Engineering family template
3. Project archetype template
4. Capability templates
5. Delivery-target template
6. Security and risk profile
7. Technology profile
8. Deployment and operations profile
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.openclone.intelligence.classifier import ProjectProfile
from src.openclone.intelligence.router import RoutingDecision
from src.openclone.intelligence.technology import TechnologyDecision


class ProjectTemplateComposer:
    """Composes modular, conditional project packages across 8 distinct architectural layers."""

    def compose_project_md(
        self,
        profile: ProjectProfile,
        decisions: List[TechnologyDecision],
        routing: RoutingDecision,
    ) -> str:
        """Compose canonical human-readable PROJECT.md matching the 25 required sections."""
        lines: List[str] = []

        # Layer 1: Universal Foundation & Identity
        lines.append(f"# PROJECT.md — {profile.project_name}")
        lines.append("")
        lines.append(f"- **Project ID:** `{profile.project_id}`")
        lines.append("- **Status:** SPECIFIED — PENDING HUMAN APPROVAL")
        lines.append(f"- **Primary Engineering Family:** `{profile.primary_family}`")
        lines.append(f"- **Primary Archetype:** `{profile.primary_type}`")
        if profile.secondary_types:
            lines.append(f"- **Secondary Archetypes:** {', '.join(f'`{s}`' for s in profile.secondary_types)}")
        lines.append(f"- **Supporting Engineering Disciplines:** {', '.join(f'`{d}`' for d in profile.supporting_disciplines)}")
        lines.append(f"- **Complexity:** `{profile.complexity.level}` ({profile.complexity.rationale})")
        lines.append(f"- **Delivery Targets:** {', '.join(f'`{t}`' for t in profile.delivery_targets)}")
        lines.append(f"- **Deployment Model:** `{profile.deployment_model}`")
        lines.append(f"- **AI Dependency:** `{profile.ai_dependency}`")
        lines.append(f"- **Data Sensitivity:** `{profile.data_sensitivity}`")
        lines.append(f"- **Reliability Tier:** `{profile.reliability_tier}`")
        lines.append(f"- **Classification Confidence:** `{profile.classification_confidence}`")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Section 1. Summary
        lines.append("## 1. Summary")
        lines.append(f"Universal engineering specification for **{profile.project_name}**. Governed by OpenClone universal engineering standards.")
        lines.append("")

        # Section 2. Problem statement and evidence
        lines.append("## 2. Problem statement and evidence")
        lines.append(f"{profile.classification_rationale}")
        if profile.unresolved_questions:
            lines.append("\n**Unresolved Questions Requiring Human Clarification:**")
            for q in profile.unresolved_questions:
                lines.append(f"- [ ] {q}")
        lines.append("")

        # Section 3. Goals and non-goals
        lines.append("## 3. Goals and non-goals")
        lines.append("### Goals")
        lines.append("- Deliver verified production capability matching canonical specifications.")
        lines.append("- Enforce strict zero-leakage, least-privilege security controls.")
        lines.append("- Ensure responsive UI, accessibility, and high performance across all designated targets.")
        lines.append("### Non-goals")
        lines.append("- No AI slope, unrequested abstractions, or speculative dependencies.")
        lines.append("- No automated production deployment without explicit human authorization.")
        lines.append("")

        # Section 4. Users and stakeholders
        lines.append("## 4. Users and stakeholders")
        lines.append(f"- Primary Operators: Engineering team, Project Owner.")
        lines.append(f"- End Users: Users accessing {', '.join(profile.delivery_targets)}.")
        lines.append("")

        # Section 5. Existing-system baseline
        lines.append("## 5. Existing-system baseline")
        lines.append("- Baseline revision: Clean repository state.")
        lines.append("- Working tree checked before modifying files.")
        lines.append("")

        # Section 6. Features and functions inventory
        lines.append("## 6. Features and functions inventory")
        lines.append(f"1. Core `{profile.primary_type}` workflows.")
        for s in profile.secondary_types:
            lines.append(f"2. Integrated `{s}` subsystem capabilities.")
        lines.append("")

        # Section 7. User journeys
        lines.append("## 7. User journeys")
        lines.append(f"- Entry: User initiates interaction via {profile.delivery_targets[0]}.")
        lines.append("- Action: State mutated via validated API contracts and business logic.")
        lines.append("- Outcome: Predictable confirmation, audit event recorded, and telemetry updated.")
        lines.append("")

        # Section 8. Functional requirements
        lines.append("## 8. Functional requirements")
        lines.append("- **FR-01:** System must initialize with zero missing environment errors.")
        lines.append(f"- **FR-02:** System must provide core functionality for {profile.primary_type}.")
        lines.append("- **FR-03:** All external integrations must use fail-closed circuit breakers.")
        lines.append("")

        # Section 9. Non-functional requirements
        lines.append("## 9. Non-functional requirements")
        lines.append(f"- **NFR-01 (Reliability):** Adhere to {profile.reliability_tier} tier uptime requirements.")
        lines.append(f"- **NFR-02 (Security):** Data sensitivity `{profile.data_sensitivity}` encrypted in transit and at rest.")
        lines.append("- **NFR-03 (Performance):** Sub-second response times for interactive user operations.")
        lines.append("")

        # Section 10. Domain rules
        lines.append("## 10. Domain rules")
        for domain_code, cap_list in routing.domains.items():
            lines.append(f"- **Domain `{domain_code}`:** Activated capabilities: {', '.join(cap_list)}")
        lines.append("")

        # Section 11. Data lifecycle (Layer 6: Security & Risk)
        lines.append("## 11. Data lifecycle")
        lines.append(f"- **Classification:** `{profile.data_sensitivity}`")
        lines.append("- **Retention:** Bounded operational logs; secrets redacted on ingest.")
        lines.append("- **Purge:** Explicit deletion API compliance.")
        lines.append("")

        # Section 12. Architecture & Layer 2/3/4 Blueprints
        lines.append("## 12. Architecture")
        lines.append(f"- **Primary Architecture Pattern:** `{profile.primary_family}` / `{profile.primary_type}`")
        lines.append(f"- **Deployment Model:** `{profile.deployment_model}`")
        lines.append("")

        # Conditional Architecture Sections based on profile
        if "os_systems" in profile.conditional_profiles:
            os_p = profile.conditional_profiles["os_systems"]
            lines.append("### OS & Systems Architecture")
            lines.append(f"- Target Architecture: `{os_p.get('target_arch')}`")
            lines.append(f"- Kernel Base: `{os_p.get('kernel_base')}`")
            lines.append(f"- Bootloader / Init: `{os_p.get('bootloader')}` / `{os_p.get('init_system')}`")
            lines.append("")
        elif "embedded_hardware" in profile.conditional_profiles:
            emb_p = profile.conditional_profiles["embedded_hardware"]
            lines.append("### Embedded & Hardware Architecture")
            lines.append(f"- Target MCU: `{emb_p.get('target_mcu')}`")
            lines.append(f"- RTOS Kernel: `{emb_p.get('rtos')}`")
            lines.append(f"- RAM Limit: `{emb_p.get('memory_limit_kb')} KB`")
            lines.append("")
        elif "ml" in profile.conditional_profiles:
            ml_p = profile.conditional_profiles["ml"]
            lines.append("### Machine Learning Pipeline Architecture")
            lines.append(f"- Target Variable: `{ml_p.get('target_variable')}`")
            lines.append(f"- Leakage Controls: `{ml_p.get('leakage_controls')}`")
            lines.append(f"- Baseline: `{ml_p.get('baseline_model')}`")
            lines.append("")

        # Section 13. Technology and dependencies (Layer 7: Technology Profile)
        lines.append("## 13. Technology and dependencies")
        for d in decisions:
            lines.append(f"### {d.category}: {d.selected_technology} ({d.version})")
            lines.append(f"- **License:** `{d.license}`")
            lines.append(f"- **Rationale:** {d.selection_rationale}")
            lines.append(f"- **Alternatives Evaluated:** {', '.join(d.alternatives_evaluated)}")
            lines.append(f"- **Compatibility Evidence:** {d.compatibility_evidence}")
            lines.append(f"- **Cost Assumptions:** {d.cost_assumptions}")
            lines.append("")

        # Section 14. APIs and integrations
        lines.append("## 14. APIs and integrations")
        lines.append("- REST / JSON contracts validated at system boundary.")
        lines.append("- Fail-closed rate limiting and bearer token authentication.")
        lines.append("")

        # Section 15. UX and accessibility
        lines.append("## 15. UX and accessibility")
        if "web_browser" in profile.delivery_targets or "android" in profile.delivery_targets or "ios" in profile.delivery_targets:
            lines.append("- **Standard:** Mandatory Responsive UI Engineering Standard (320px–1440px+).")
            lines.append("- **Touch Targets:** Minimum 44x44px for touch interactions.")
            lines.append("- **Accessibility:** WCAG 2.1 AA compliant color contrast and ARIA labels.")
        else:
            lines.append("- Non-visual / headless / systems interface: accessible CLI help text and stdout/stderr stream separation.")
        lines.append("")

        # Section 16. Security and privacy
        lines.append("## 16. Security and privacy")
        lines.append("- **Environment:** Zero hardcoded credentials in source control.")
        lines.append("- **Validation:** `tools/scan_secrets.py` passing across all commits.")
        lines.append("- **Redaction:** SHA-256 hash-chained audit logging with token masking.")
        lines.append("")

        # Section 17. Scope and constraints
        lines.append("## 17. Scope and constraints")
        lines.append("- No AI slope or speculative microservices.")
        lines.append("- Keep all code changes within approved task boundaries.")
        lines.append("")

        # Section 18. Acceptance criteria
        lines.append("## 18. Acceptance criteria")
        lines.append("1. All unit and integration test suites pass.")
        lines.append("2. Secret scanner returns 0 exposed credentials.")
        lines.append("3. Static and responsive layout verified across targets.")
        lines.append("4. Verification report generated with exact command evidence.")
        lines.append("")

        # Section 19. Gaps and defects
        lines.append("## 19. Gaps and defects")
        lines.append("- None detected at specification phase.")
        lines.append("")

        # Section 20. Risks
        lines.append("## 20. Risks")
        lines.append(f"- Scope drift risk: Mitigated by `{profile.complexity.level}` complexity gating.")
        lines.append("")

        # Section 21. Build, test and operations (Layer 8: Deployment & Operations)
        lines.append("## 21. Build, test and operations")
        lines.append("- **Test Command:** `python -m pytest tests/`")
        lines.append("- **Secret Scan:** `python tools/scan_secrets.py`")
        lines.append("- **Repository Audit:** `python tools/validate_repository.py`")
        lines.append("")

        # Section 22. Agent permissions
        lines.append("## 22. Agent permissions")
        lines.append("- Read workspace files: ALLOWED.")
        lines.append("- Edit approved task files: ALLOWED.")
        lines.append("- Run read-only diagnostic commands: ALLOWED.")
        lines.append("- Production deployment / external network access / force-push: PROHIBITED WITHOUT HUMAN APPROVAL.")
        lines.append("")

        # Section 23. Decisions and approvals
        lines.append("## 23. Decisions and approvals")
        lines.append("| Date | Decision | Approver | Status |")
        lines.append("|---|---|---|---|")
        lines.append("| Specification Phase | Architecture & Taxonomy Classification | Lead Architect | SPECIFIED |")
        lines.append("")

        # Section 24. Traceability
        lines.append("## 24. Traceability")
        lines.append(f"- Canonical Taxonomy Registry: `framework/registries/project-taxonomy.json`")
        lines.append(f"- Activated Capabilities: {', '.join(c.engine_id for c in routing.capabilities[:8])}")
        lines.append("")

        # Section 25. Change history
        lines.append("## 25. Change history")
        lines.append("- Initial specification compiled by OpenClone Universal Project Intelligence Engine v2.0.0.")
        lines.append("")

        return "\n".join(lines)

    def compose_build_prompt(
        self,
        profile: ProjectProfile,
        decisions: List[TechnologyDecision],
        routing: RoutingDecision,
    ) -> str:
        """Compose BUILD_PROMPT.md requiring target agent to inspect actual codebase first."""
        lines: List[str] = []
        lines.append(f"# BUILD PROMPT: {profile.project_name}")
        lines.append(f"## OpenClone Governed Implementation Directive")
        lines.append("")
        lines.append("**CRITICAL RULE: MANDATORY SESSION PRE-FLIGHT**")
        lines.append("Before modifying or creating any code, you MUST:")
        lines.append("1. Confirm current working directory and git status (`git status --short`).")
        lines.append("2. Read `PROJECT.md` and `AGENT_INSTRUCTIONS.md`.")
        lines.append("3. Inspect existing files, dependencies, and test fixtures.")
        lines.append("4. Never overwrite user changes or introduce unnecessary dependencies (No AI Slope).")
        lines.append("")
        lines.append("### Project Summary")
        lines.append(f"- **Project Name:** {profile.project_name}")
        lines.append(f"- **Primary Family:** {profile.primary_family} -> `{profile.primary_type}`")
        lines.append(f"- **Complexity:** {profile.complexity.level}")
        lines.append(f"- **Delivery Targets:** {', '.join(profile.delivery_targets)}")
        lines.append(f"- **Deployment Model:** {profile.deployment_model}")
        lines.append("")
        lines.append("### Selected Technology Stack")
        for d in decisions:
            lines.append(f"- **{d.category}:** {d.selected_technology} ({d.version}) — License: {d.license}")
        lines.append("")
        lines.append("### Minimum Effective Workforce Team")
        for team_name, role_list in routing.workforce.items():
            lines.append(f"- **{team_name}:** {', '.join(role_list)}")
        lines.append("")
        lines.append("### Acceptance Verification Requirements")
        lines.append("You must run all relevant unit tests and secret scans before declaring completion.")
        lines.append("Capture exact test outputs and exit codes.")
        lines.append("")
        return "\n".join(lines)

    def compose_agent_instructions(self, profile: ProjectProfile, routing: RoutingDecision) -> str:
        """Compose AGENT_INSTRUCTIONS.md."""
        lines: List[str] = []
        lines.append(f"# AGENT INSTRUCTIONS — {profile.project_name}")
        lines.append("")
        lines.append("## Operating Principles")
        lines.append("1. **Truthful Evidence:** Never claim a test passed or feature works without running it.")
        lines.append("2. **Least Privilege:** Do not request elevated permissions unless strictly necessary.")
        lines.append("3. **Bounded Work Units:** Complete work in small, incremental, verifiable steps.")
        lines.append("4. **Anti-Slop Standard:** Follow Taste Skill tokens and responsive layout (320px–1440px).")
        lines.append("5. **No Hallucinated Tools:** Only use existing, verified tools and adapters.")
        lines.append("")
        lines.append("## Active Workforce Roles")
        for team, roles in routing.workforce.items():
            lines.append(f"- **{team}:** {', '.join(roles)}")
        lines.append("")
        return "\n".join(lines)

    def compose_env_example(self, decisions: List[TechnologyDecision]) -> str:
        """Compose clean .env.example with placeholders only."""
        lines: List[str] = []
        lines.append("# OpenClone Centralized Environment Template")
        lines.append("# DO NOT COMMIT ACTUAL SECRETS TO VERSION CONTROL")
        lines.append("")
        seen_vars = set()
        for d in decisions:
            if d.required_env_vars:
                lines.append(f"# {d.category} — {d.selected_technology}")
                for var in d.required_env_vars:
                    if var not in seen_vars:
                        seen_vars.add(var)
                        lines.append(f"{var}=your_{var.lower()}_here")
                lines.append("")
        if not seen_vars:
            lines.append("# No external API keys or secrets required for core operation.")
            lines.append("ENVIRONMENT=development")
            lines.append("DEBUG=true")
            lines.append("")
        return "\n".join(lines)
