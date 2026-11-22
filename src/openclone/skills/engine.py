"""OpenClone Skill Discovery, Selection, Loading, and Application Engine.
Implements the 8-stage skill lifecycle and conflict resolution.
"""
from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set

@dataclass
class Skill:
    id: str
    name: str
    version: str
    category: str
    description: str
    triggers: List[str] = field(default_factory=list)
    negative_triggers: List[str] = field(default_factory=list)
    precedence: int = 50  # Lower number = higher precedence
    required_actions: List[str] = field(default_factory=list)
    supported_environments: List[str] = field(default_factory=list)
    path: Optional[str] = None
    enabled: bool = True

class SkillRegistry:
    """Discovers, validates, and stores verified engineering skills."""
    def __init__(self, root: Optional[Path] = None):
        self.root = root or Path(__file__).resolve().parents[3]
        self.skills: Dict[str, Skill] = {}
        self._load_builtins()

    def _load_builtins(self):
        """Register built-in framework skills."""
        # 1. Taste Skill (Core Anti-Slop UI/UX)
        self.register(Skill(
            id="taste-skill",
            name="Taste Skill",
            version="2.6.0",
            category="design",
            description="Anti-AI-slop governance, visual hierarchy, responsive layout, and adaptive design intelligence.",
            triggers=["ui", "ux", "frontend", "design", "css", "component", "landing page", "dashboard", "style", "tailwind"],
            negative_triggers=["backend-only", "cli-only", "no-ui", "headless"],
            precedence=10,
            required_actions=[
                "Scan workspace for existing instruction files (.cursorrules, AGENTS.md)",
                "Audit UI against anti-slop patterns (excessive glassmorphism, blur blobs, generic purple gradients)",
                "Generate .taste-skill/design-plan.md and pass plan-check.mjs gate",
                "Verify responsive layout and WCAG 2.2 AA contrast across viewports",
            ],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            path="skills/taste-skill",
        ))

        # 2. Typography Standards Skill
        self.register(Skill(
            id="typography-standards",
            name="Typography Standards Skill",
            version="1.0.0",
            category="design",
            description="Type scale, fluid type, optical contrast, font pair harmony, and readable line lengths.",
            triggers=["typography", "fonts", "type scale", "headings", "readability", "text hierarchy"],
            negative_triggers=["backend-only", "database"],
            precedence=20,
            required_actions=[
                "Define semantic font roles (Display, Body, Monospace, Data)",
                "Apply Major Third or Perfect Fourth scale",
                "Enforce 45-75 character line lengths for body text",
            ],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            path="domains/05-UX-UI-ENGINEERING/HUMAN-CRAFTED-DESIGN-SYSTEM.md",
        ))

        # 3. Motion & Animation Skill
        self.register(Skill(
            id="motion-design",
            name="Motion & Animation Skill",
            version="1.0.0",
            category="design",
            description="Purposeful microinteractions, view transitions, physics easing, and reduced-motion compliance.",
            triggers=["motion", "animation", "transition", "microinteraction", "hover effect", "keyframes", "framer"],
            negative_triggers=["static-only", "email-template"],
            precedence=25,
            required_actions=[
                "Define duration and easing curves (<300ms for microinteractions)",
                "Implement @media (prefers-reduced-motion: reduce) fallback",
                "Animate only transform and opacity to prevent layout thrashing",
            ],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            path="docs/knowledge/motion-and-animation.md",
        ))

        # 4. SaaS Security Baseline Skill
        self.register(Skill(
            id="saas-security-baseline",
            name="SaaS Security Baseline Skill",
            version="1.0.0",
            category="security",
            description="19-point SaaS security verification, RLS, server authorization, rate limits, secret masking.",
            triggers=["security", "auth", "api", "database", "rls", "tenant", "saas", "production", "secrets"],
            negative_triggers=["prototype-only"],
            precedence=5,  # High priority security gate
            required_actions=[
                "Verify server-side authorization on all private API endpoints",
                "Enforce Row-Level Security (RLS) or tenant-scoped isolation",
                "Lock down CORS with explicit origins",
                "Ensure zero secrets in git commits, logs, or client bundles",
            ],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            path="docs/security/saas-security-baseline.md",
        ))

        # 5. Dynamic Pentest & Strix Adapter Skill
        self.register(Skill(
            id="strix-pentest-adapter",
            name="Strix Dynamic Pentest Adapter",
            version="1.0.0",
            category="security",
            description="AI-assisted dynamic API & application security testing with target allowlists.",
            triggers=["penetration test", "pentest", "dynamic scan", "dast", "strix", "vulnerability scan"],
            negative_triggers=["offline-only", "static-only"],
            precedence=15,
            required_actions=[
                "Verify written target authorization and allowlist",
                "Execute inside bounded container/Docker environment",
                "Triage confirmed findings and generate remediation tickets",
                "Retest and verify vulnerability elimination before release",
            ],
            supported_environments=["antigravity", "claude-code", "cli"],
            path="docs/integrations/strix-dynamic-testing.md",
        ))

        # 6. Backend System Architecture Skill
        self.register(Skill(
            id="backend-architecture",
            name="Backend System Architecture Skill",
            version="1.0.0",
            category="backend",
            description="580-topic backend knowledge, modular monoliths, caching, queues, transactions, idempotent APIs.",
            triggers=["backend", "database", "api", "rest", "graphql", "postgres", "sqlite", "redis", "queue", "architecture"],
            negative_triggers=["frontend-only", "static-site"],
            precedence=20,
            required_actions=[
                "Verify database migration rollback capability",
                "Enforce transactions on multi-step state mutations",
                "Implement structured JSON logging with credential redaction",
            ],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            path="docs/knowledge/backend-system-design-catalogue.md",
        ))

        # 7. AI & Context Engineering Skill
        self.register(Skill(
            id="ai-context-engineering",
            name="AI & Context Engineering Skill",
            version="1.0.0",
            category="ai",
            description="1,095-entry AI taxonomy, structured outputs, prompt evaluation, token budgets, and tool sandboxing.",
            triggers=["ai", "llm", "rag", "agent", "prompt", "mcp", "embeddings", "vector", "gemini", "openai", "claude"],
            negative_triggers=["no-ai", "crud-only"],
            precedence=20,
            required_actions=[
                "Enforce structured output schemas (JSON Schema / Pydantic)",
                "Apply token budget limits and rate-limit retry backoffs",
                "Implement prompt injection defenses and tool authorization checks",
            ],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            path="docs/knowledge/ai-engineering-catalogue.md",
        ))

    def register(self, skill: Skill):
        self.skills[skill.id] = skill

    def get(self, skill_id: str) -> Optional[Skill]:
        return self.skills.get(skill_id)

    def list_all(self) -> List[Skill]:
        return list(self.skills.values())

class SkillSelector:
    """Deterministically selects, ranks, and resolves conflicts among skills."""
    def __init__(self, registry: SkillRegistry):
        self.registry = registry

    def select(self, task_description: str, environment: str = "all") -> Dict[str, Any]:
        text = task_description.lower()
        selected: List[Skill] = []
        skipped: List[Dict[str, str]] = []

        for skill in self.registry.list_all():
            if not skill.enabled:
                skipped.append({"skill_id": skill.id, "reason": "Skill disabled"})
                continue

            # Check environment compatibility
            if environment != "all" and skill.supported_environments and environment not in skill.supported_environments:
                skipped.append({"skill_id": skill.id, "reason": f"Environment '{environment}' not supported"})
                continue

            # Check negative triggers
            has_negative = any(neg in text for neg in skill.negative_triggers)
            if has_negative:
                skipped.append({"skill_id": skill.id, "reason": "Excluded by negative trigger"})
                continue

            # Check positive triggers
            matched_triggers = [t for t in skill.triggers if t in text]
            if matched_triggers:
                selected.append(skill)
            else:
                skipped.append({"skill_id": skill.id, "reason": "No trigger keywords matched"})

        # Sort selected by precedence (lower number = higher priority)
        selected.sort(key=lambda s: s.precedence)

        return {
            "task": task_description,
            "selected_skills": selected,
            "skipped_skills": skipped,
            "total_selected": len(selected),
            "total_skipped": len(skipped),
        }

class SkillReportGenerator:
    """Generates markdown reports for skill selection and application."""
    @staticmethod
    def generate_selection_report(task_id: str, selection_result: Dict[str, Any]) -> str:
        lines = [
            f"# SKILL_SELECTION_REPORT — Task {task_id}",
            f"**Task Description**: {selection_result['task']}",
            f"**Total Selected**: {selection_result['total_selected']} | **Total Skipped**: {selection_result['total_skipped']}",
            "",
            "---",
            "",
            "## 1. Selected Skills (Precedence Ordered)",
            "",
            "| Skill ID | Display Name | Precedence | Path | Required Deliverables |",
            "|---|---|:---:|---|---|",
        ]
        for s in selection_result["selected_skills"]:
            actions_summary = "; ".join(s.required_actions[:2])
            lines.append(f"| `{s.id}` | **{s.name}** | {s.precedence} | `{s.path}` | {actions_summary} |")

        lines.extend([
            "",
            "---",
            "",
            "## 2. Skipped Skills & Rationale",
            "",
            "| Skill ID | Reason |",
            "|---|---|",
        ])
        for sk in selection_result["skipped_skills"]:
            lines.append(f"| `{sk['skill_id']}` | {sk['reason']} |")

        return "\n".join(lines) + "\n"

    @staticmethod
    def generate_application_report(task_id: str, applied_records: List[Dict[str, Any]]) -> str:
        lines = [
            f"# SKILL_APPLICATION_REPORT — Task {task_id}",
            "**Traceable Execution Ledger for Applied Engineering Skills**",
            "",
            "---",
            "",
            "| Task ID | Skill ID | Selection Reason | Loaded Source | Required Actions Completed | Evidence Reference | Status |",
            "|---|---|---|---|---|---|:---:|",
        ]
        for r in applied_records:
            status = r.get("status", "APPLIED")
            lines.append(
                f"| `{task_id}` | `{r['skill_id']}` | {r.get('reason', 'Trigger match')} | `{r.get('source', '')}` | {r.get('actions_completed', 'All')} | {r.get('evidence', 'Tests passed')} | `{status}` |"
            )
        return "\n".join(lines) + "\n"
