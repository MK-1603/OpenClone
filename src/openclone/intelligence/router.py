"""OpenClone Deterministic Explainable Project Router."""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from src.openclone.intelligence.classifier import ProjectProfile
from src.openclone.intelligence.taxonomy import TaxonomyRegistry


ROOT = Path(__file__).resolve().parents[3]


@dataclass
class CapabilityItem:
    engine_id: str
    name: str
    status: str
    rationale: str
    dependencies: List[str] = field(default_factory=list)


@dataclass
class WorkflowStageItem:
    workflow_id: str
    name: str
    stage: int
    prerequisites: List[str] = field(default_factory=list)


@dataclass
class ApprovalGateItem:
    gate_id: str
    name: str
    approver_role: str
    criteria: List[str] = field(default_factory=list)


@dataclass
class RoutingDecision:
    project_id: str
    timestamp: str
    classification: Dict[str, Any]
    domains: Dict[str, List[str]]
    capabilities: List[CapabilityItem]
    workforce: Dict[str, List[str]]
    models: Dict[str, Any]
    workflows: List[WorkflowStageItem]
    approval_gates: List[ApprovalGateItem]
    verification_strategy: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "timestamp": self.timestamp,
            "classification": self.classification,
            "domains": self.domains,
            "capabilities": [
                {
                    "engine_id": c.engine_id,
                    "name": c.name,
                    "status": c.status,
                    "rationale": c.rationale,
                    "dependencies": c.dependencies,
                }
                for c in self.capabilities
            ],
            "workforce": self.workforce,
            "models": self.models,
            "workflows": [
                {
                    "workflow_id": w.workflow_id,
                    "name": w.name,
                    "stage": w.stage,
                    "prerequisites": w.prerequisites,
                }
                for w in self.workflows
            ],
            "approval_gates": [
                {
                    "gate_id": g.gate_id,
                    "name": g.name,
                    "approver_role": g.approver_role,
                    "criteria": g.criteria,
                }
                for g in self.approval_gates
            ],
            "verification_strategy": self.verification_strategy,
        }


class ProjectRouter:
    """Computes deterministic and explainable domain, capability, workforce, and workflow mappings."""

    ENGINE_CATALOGUE: Dict[str, str] = {
        "E-001": "Specification Engine",
        "E-002": "Architecture Engine",
        "E-003": "Data Integrity Engine",
        "E-004": "Security Controls Engine",
        "E-005": "Design Systems Engine",
        "E-006": "UX Research Engine",
        "E-007": "Accessibility Engine",
        "E-008": "API Contracts Engine",
        "E-010": "Testing & QA Engine",
        "E-013": "Dependency Engine",
        "E-014": "Performance Engineering Engine",
        "E-017": "Incident Response Engine",
        "E-018": "Documentation Engine",
        "E-021": "Disaster Recovery Engine",
        "E-022": "Supply Chain Security Engine",
        "E-029": "AI Governance Engine",
        "E-030": "Agent Verification Engine",
        "E-056": "Taste Skill Visual Engine",
    }

    WORKFLOW_CATALOGUE: Dict[str, str] = {
        "WF-001": "Project Discovery & Baseline Initialization",
        "WF-002": "Requirements Engineering & PRD Sign-off",
        "WF-003": "Task Decomposition & DAG Dependency Scheduling",
        "WF-004": "Deterministic Implementation & Minimal Diff Execution",
        "WF-005": "Security Assurance & Pinned Scanner Audit",
        "WF-006": "Automated Unit & Integration Verification",
        "WF-007": "Independent Verification Review (Goldfish Protocol)",
        "WF-008": "Accessibility & WCAG 2.2 AA Audit",
        "WF-009": "Human Approval Digest Binding",
        "WF-010": "Cryptographic Audit Ledger Sealing",
        "WF-011": "MIE Provider Health & Circuit Breaker Verification",
        "WF-012": "External Specialist Workforce Handoff",
        "WF-013": "Evidence-Linked Feature Verification Matrix",
        "WF-014": "Release Gate & Production Deployment Sign-off",
        "WF-015": "Post-Release Monitoring & Telemetry Baseline",
    }

    def __init__(self, taxonomy: Optional[TaxonomyRegistry] = None):
        self.taxonomy = taxonomy or TaxonomyRegistry()

    def route(self, profile: ProjectProfile) -> RoutingDecision:
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        all_types = [profile.primary_type] + profile.secondary_types + profile.supporting_types

        # 1. Domain Mapping
        domains = self._map_domains(all_types, profile.complexity.level)

        # 2. Capability Mapping
        capabilities = self._map_capabilities(all_types, profile.complexity.level)

        # 3. Workforce Composition (Minimum Effective Team)
        workforce = self._compose_workforce(all_types, profile.complexity.level)

        # 4. Model Intelligence Selection
        models = self._select_models(all_types, profile.complexity.level)

        # 5. Workflow Composition
        workflows = self._compose_workflows(all_types, profile.complexity.level)

        # 6. Approval Gates
        approval_gates = self._define_approval_gates(profile.complexity.level)

        # 7. Verification Strategy
        verification = self._define_verification_strategy(all_types, profile.complexity.level)

        return RoutingDecision(
            project_id=profile.project_id,
            timestamp=timestamp,
            classification=profile.to_dict(),
            domains=domains,
            capabilities=capabilities,
            workforce=workforce,
            models=models,
            workflows=workflows,
            approval_gates=approval_gates,
            verification_strategy=verification,
        )

    def _map_domains(self, types: List[str], complexity_level: str) -> Dict[str, List[str]]:
        mandatory: Set[str] = {"00-GOVERNANCE", "01-SPECIFICATION", "10-TESTING-AND-QA"}
        conditional: Set[str] = set()
        supporting: Set[str] = {"18-DOCUMENTATION"}

        for t_id in types:
            pt = self.taxonomy.get_type(t_id)
            if pt:
                mandatory.update(pt.default_domains)

        # Add architecture if non-mini
        if complexity_level != "MINI":
            mandatory.add("02-ARCHITECTURE")
            mandatory.add("04-SECURITY-CONTROLS")

        # Specific domain conditionals
        has_ai = any("rag" in t or "agent" in t or "ai" in t for t in types)
        has_data = any("data" in t or "etl" in t for t in types)
        has_os = any("linux" in t or "kernel" in t for t in types)

        if has_ai:
            mandatory.add("29-AI-GOVERNANCE")
            mandatory.add("30-AGENT-RULES-AND-VERIFICATION")
        if has_data:
            mandatory.add("03-DATA-INTEGRITY")
        if has_os:
            mandatory.add("22-SUPPLY-CHAIN-SECURITY")
            supporting.add("14-PERFORMANCE-ENGINEERING")

        # Exclusions for mini projects
        not_applicable: Set[str] = set()
        if complexity_level == "MINI":
            not_applicable.update([
                "11-PERMISSIONS-AND-ACCESS-CONTROL",
                "16-TELEMETRY-AND-OBSERVABILITY",
                "17-INCIDENT-RESPONSE",
                "20-RELEASE-READINESS",
                "21-DATA-MIGRATION-AND-ROLLBACK",
            ])

        optional: Set[str] = {"15-CODE-QUALITY", "24-DEVELOPER-EXPERIENCE"} - mandatory - supporting

        return {
            "mandatory": sorted(list(mandatory)),
            "conditional": sorted(list(conditional)),
            "supporting": sorted(list(supporting)),
            "optional": sorted(list(optional)),
            "not_applicable": sorted(list(not_applicable)),
        }

    def _map_capabilities(self, types: List[str], complexity_level: str) -> List[CapabilityItem]:
        caps: Dict[str, CapabilityItem] = {}

        # Universal core
        caps["E-001"] = CapabilityItem("E-001", self.ENGINE_CATALOGUE["E-001"], "OPERATIONAL", "PRD specification and contract traceability")
        caps["E-010"] = CapabilityItem("E-010", self.ENGINE_CATALOGUE["E-010"], "OPERATIONAL", "Automated test suite and regression harness")

        if complexity_level != "MINI":
            caps["E-002"] = CapabilityItem("E-002", self.ENGINE_CATALOGUE["E-002"], "OPERATIONAL", "Modular architecture and service boundaries")
            caps["E-004"] = CapabilityItem("E-004", self.ENGINE_CATALOGUE["E-004"], "OPERATIONAL", "Security controls and least-privilege boundaries")

        for t_id in types:
            pt = self.taxonomy.get_type(t_id)
            if pt:
                for eid in pt.mandatory_capabilities:
                    if eid in self.ENGINE_CATALOGUE and eid not in caps:
                        caps[eid] = CapabilityItem(eid, self.ENGINE_CATALOGUE[eid], "OPERATIONAL", f"Mandated by {pt.name}")

        return [caps[k] for k in sorted(caps.keys())]

    def _compose_workforce(self, types: List[str], complexity_level: str) -> Dict[str, List[str]]:
        native: Set[str] = set()
        external: Set[str] = set()
        ide: Set[str] = {"google-antigravity", "claude-code"}
        human: Set[str] = {"human-approval-authority"}
        missing: Set[str] = set()

        for t_id in types:
            pt = self.taxonomy.get_type(t_id)
            if pt:
                for role in pt.recommended_workforce:
                    # Categorize role origin
                    if role in ("frontend-engineer", "backend-engineer", "security-engineer", "database-architect", "qa-engineer", "mobile-engineer", "ui-designer", "accessibility-specialist"):
                        native.add(role)
                    elif role in ("fullstack-engineer", "devops-engineer", "eval-engineer", "rag-specialist", "agent-architect", "data-engineer"):
                        external.add(f"agency:{role}")
                    elif role in ("kernel-engineer", "systems-programmer", "compiler-engineer", "embedded-engineer", "firmware-engineer", "data-scientist", "game-engine-engineer", "research-software-engineer"):
                        # Specialized roles: mark native/human specialist fallback
                        native.add(role)
                        human.add(f"human-specialist:{role}-advisor")
                    else:
                        missing.add(role)

        # Enforce minimum effective team
        if complexity_level == "MINI":
            native = {r for r in native if r in ("frontend-engineer", "ui-designer", "accessibility-specialist")}
            external = set()

        return {
            "native_agents": sorted(list(native)),
            "external_agents": sorted(list(external)),
            "ide_agents": sorted(list(ide)),
            "human_specialists": sorted(list(human)),
            "missing_specialists": sorted(list(missing)),
        }

    def _select_models(self, types: List[str], complexity_level: str) -> Dict[str, Any]:
        has_visual = any("web" in t or "mobile" in t or "game" in t or "design" in t for t in types)
        is_high_complexity = complexity_level in ("LARGE", "ENTERPRISE", "RESEARCH_EXPERIMENTAL")

        primary = "gpt-6.2-astra" if is_high_complexity else "gpt-6.2-sol"
        fallback = ["gpt-6.2-sol", "claude-3-7-sonnet", "gemini-2.5-pro", "ollama:qwen2.5-coder"]

        task_allocations = {
            "architecture_reasoning": "gpt-6.2-astra",
            "implementation_code": "gpt-6.2-sol",
            "ui_visual_review": "gpt-6.1-terra" if has_visual else "gpt-6.2-sol",
            "offline_local_verification": "ollama:qwen2.5-coder",
        }

        return {
            "primary_model": primary,
            "fallback_chain": fallback,
            "task_allocations": task_allocations,
        }

    def _compose_workflows(self, types: List[str], complexity_level: str) -> List[WorkflowStageItem]:
        stages = [
            WorkflowStageItem("WF-001", self.WORKFLOW_CATALOGUE["WF-001"], stage=1),
            WorkflowStageItem("WF-002", self.WORKFLOW_CATALOGUE["WF-002"], stage=2, prerequisites=["WF-001"]),
            WorkflowStageItem("WF-003", self.WORKFLOW_CATALOGUE["WF-003"], stage=3, prerequisites=["WF-002"]),
            WorkflowStageItem("WF-009", self.WORKFLOW_CATALOGUE["WF-009"], stage=4, prerequisites=["WF-003"]),
            WorkflowStageItem("WF-004", self.WORKFLOW_CATALOGUE["WF-004"], stage=5, prerequisites=["WF-009"]),
            WorkflowStageItem("WF-006", self.WORKFLOW_CATALOGUE["WF-006"], stage=6, prerequisites=["WF-004"]),
            WorkflowStageItem("WF-007", self.WORKFLOW_CATALOGUE["WF-007"], stage=7, prerequisites=["WF-006"]),
        ]

        if complexity_level != "MINI":
            stages.append(WorkflowStageItem("WF-005", self.WORKFLOW_CATALOGUE["WF-005"], stage=8, prerequisites=["WF-006"]))
            stages.append(WorkflowStageItem("WF-010", self.WORKFLOW_CATALOGUE["WF-010"], stage=9, prerequisites=["WF-007"]))
            stages.append(WorkflowStageItem("WF-014", self.WORKFLOW_CATALOGUE["WF-014"], stage=10, prerequisites=["WF-010"]))

        return stages

    def _define_approval_gates(self, complexity_level: str) -> List[ApprovalGateItem]:
        gates = [
            ApprovalGateItem(
                "GATE_01_PRD_APPROVAL",
                "Requirements & PRD Human Approval Gate",
                "Human Owner / Product Lead",
                ["Scope boundaries confirmed", "All AC Given/When/Then testable", "Acceptance matrix signed off"],
            ),
            ApprovalGateItem(
                "GATE_02_PLAN_DIGEST",
                "Implementation Plan SHA-256 Digest Binding Gate",
                "Human Lead Architect",
                ["Plan hash verified", "Allowlisted files explicitly declared", "No unvetted dependencies"],
            ),
        ]
        if complexity_level in ("MEDIUM", "LARGE", "ENTERPRISE", "RESEARCH_EXPERIMENTAL"):
            gates.append(
                ApprovalGateItem(
                    "GATE_03_INDEPENDENT_VERIFICATION",
                    "Independent Verification Gate (Goldfish Protocol)",
                    "Independent Reviewer / Human Specialist",
                    ["Tests executed and captured in evidence", "100% requirements traceability verified", "No secret leaks or regressions"],
                )
            )
        return gates

    def _define_verification_strategy(self, types: List[str], complexity_level: str) -> List[str]:
        strategy = [
            "Deterministic automated unit tests via pytest / test runner",
            "Zero broken Markdown links via tools/check_links.py",
            "JSON Schema meta-validation via Draft 2020-12 validator",
            "SHA-256 evidence logging in local ledger",
        ]
        if any("web" in t for t in types):
            strategy.append("Taste Skill visual governance and WCAG 2.2 AA accessibility check")
        if any("security" in t or complexity_level in ("LARGE", "ENTERPRISE") for t in types):
            strategy.append("Pinned security scanner audit against security/scanners.lock.json")
        return strategy

    def resolve_software_architect(self, scope: str = "system", domain: str = "") -> str:
        """Resolve a unified Software Architect request to an existing registered worker."""
        return resolve_software_architect(scope, domain)


def resolve_software_architect(scope: str = "system", domain: str = "") -> str:
    """Resolve a unified Software Architect request to an existing registered worker in the 72-worker registry.

    Hierarchy:
    - principal-architect: System-wide coherence, cross-cutting boundaries, architectural governance, ADRs.
    - solution-architect: Translating requirements into component topologies and solution design.
    - specialist architects: Domain-specific architecture (backend, frontend, database, api, integration, data).
    """
    s = scope.lower().strip()
    d = domain.lower().strip()

    if s in ("cross-system", "enterprise", "governance", "adr", "standards"):
        return "principal-architect"
    elif s in ("solution", "subsystem", "component-design", "topology"):
        return "solution-architect"
    elif d in ("backend", "server", "microservice", "services"):
        return "backend-architect"
    elif d in ("frontend", "ui", "web", "mobile-ui", "client"):
        return "frontend-architect"
    elif d in ("database", "sql", "storage", "cache", "data-model"):
        return "database-architect"
    elif d in ("api", "rest", "grpc", "graphql", "interface"):
        return "api-architect"
    elif d in ("integration", "event-streaming", "webhook", "events"):
        return "integration-architect"
    elif d in ("data", "etl", "analytics", "pipeline", "warehouse"):
        return "data-architect"

    return "principal-architect"
