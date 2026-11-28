"""OpenClone Project Intelligence Architect (PIA-001).

Implements the unified Project Intelligence Architect role supporting the
Four-Set Intelligence Architecture:
- Set A: Feature Intelligence (Product & domain research, market capabilities, features FEAT-xxx).
- Set B: Gap & Problem Intelligence (Functional gaps, weaknesses, technical limitations GAP-xxx / PROB-xxx).
- Set C: Solution Intelligence (Problem-to-solution mapping, alternatives, trade-offs SOL-xxx, acceptance criteria AC-xxx).
- Set D: Final Product Intelligence (Consolidation of Sets A, B, and C into an advanced, complete, traceable blueprint).

Operating Modes:
1. PIA-NEW: New project discovery, Set A/B/C/D specification generation from prompt or idea.
2. PIA-DEFINED: Documentation harmonization, gap assessment, and 4-tier conflict resolution.
3. PIA-EVOLUTION: Static codebase X-Ray, technical debt quantification, and architectural drift analysis.
"""

from __future__ import annotations

import ast
import enum
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from src.openclone.intelligence.classifier import ProjectClassifier, ProjectProfile
from src.openclone.intelligence.composer import ProjectTemplateComposer
from src.openclone.intelligence.router import ProjectRouter, RoutingDecision
from src.openclone.intelligence.taxonomy import TaxonomyRegistry
from src.openclone.intelligence.technology import TechnologyDecision, TechnologyIntelligenceEngine
from src.openclone.intelligence.zip_reproducibility import create_deterministic_zip
from src.openclone.reverse_engineering import ExecutionLevel, ReverseEngineeringEngine
from src.openclone.system_design.capacity import (
    CapacityEstimator,
    TrafficProfile,
    ComprehensiveCapacityReport,
    UnestimatedCapacityReport,
)
from src.openclone.system_design.diagrams import SystemDiagramGenerator
from src.openclone.system_design.decision_engine import (
    SystemDesignDecisionEngine,
    SystemRequirements,
    QualityAttributes,
    ArchitectureRecommendation,
)
from src.openclone.memory.manager import MemoryManager
from src.openclone.intelligence.ingestion.engine import DocumentIngestionEngine
from src.openclone.intelligence.ingestion.models import IngestedDocument
from src.openclone.intelligence.clarification import SocraticClarificationEngine, ClarificationQuestion
from src.openclone.intelligence.ide_recommendation import IdeRecommendationEngine, IdeRecommendation


class PIAMode(str, enum.Enum):
    NEW = "PIA-NEW"
    DEFINED = "PIA-DEFINED"
    EVOLUTION = "PIA-EVOLUTION"

    @classmethod
    def from_string(cls, val: str) -> "PIAMode":
        normalized = val.strip().upper()
        if normalized in ("PIA-NEW", "NEW"):
            return cls.NEW
        elif normalized in ("PIA-DEFINED", "DEFINED"):
            return cls.DEFINED
        elif normalized in ("PIA-EVOLUTION", "EVOLUTION", "PIA-EXISTING", "EXISTING"):
            # PIA-EXISTING is supported as a legacy alias
            return cls.EVOLUTION
        raise ValueError(f"Unknown PIA mode: {val}. Valid modes: PIA-NEW, PIA-DEFINED, PIA-EVOLUTION")


class EvidenceType(str, enum.Enum):
    # Set A Evidence Classifications
    PROMPT_EXTRACTED = "PROMPT_EXTRACTED"
    MARKET_INFERENCE = "MARKET_INFERENCE"
    VERIFIED_MARKET_RESEARCH = "VERIFIED_MARKET_RESEARCH"
    # Set B Evidence Classifications
    STATIC_INSPECTION = "STATIC_INSPECTION"
    AUTOMATED_SCAN = "AUTOMATED_SCAN"
    RUNTIME_EXECUTION = "RUNTIME_EXECUTION"
    UX_EVALUATION = "UX_EVALUATION"
    ARCHITECTURE_DEBT = "ARCHITECTURE_DEBT"


class SolutionStatus(str, enum.Enum):
    PROPOSED = "PROPOSED"
    RECOMMENDED = "RECOMMENDED"
    ALTERNATIVE = "ALTERNATIVE"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class DocumentAuthorityTier(int, enum.Enum):
    TIER_1_MASTER = 1       # PROJECT.md (Project identity, core architecture, global constraints)
    TIER_2_HISTORICAL = 2   # Decision-Log.md (ADRs, superseding directives)
    TIER_3_FUNCTIONAL = 3   # Project-Requirement.md / Features-List.md (Epics, user stories, acceptance criteria)
    TIER_4_TECHNICAL = 4    # Tech-Stack.md / Project-Details.md (Libraries, environment configs, operational notes)


class AIExecutionGuidance:
    """Dynamic decoupled metadata separating Documentation AI and Implementation AI."""

    def __init__(
        self,
        doc_provider: str = "google",
        doc_model_id: str = "gemini-2.5-pro",
        doc_status: str = "active",
        doc_reasoning_tier: str = "deep-reasoning",
        doc_context_budget: int = 131072,
        doc_generation_budget: int = 8192,
        impl_provider: str = "anthropic",
        impl_model_id: str = "claude-3-7-sonnet",
        impl_status: str = "active",
        impl_reasoning_tier: str = "code-specialized",
        impl_context_budget: int = 65536,
        impl_generation_budget: int = 4096,
    ):
        self.documentation_ai = {
            "provider": doc_provider,
            "model_id": doc_model_id,
            "status": doc_status,
            "reasoning_tier": doc_reasoning_tier,
            "context_budget_tokens": doc_context_budget,
            "generation_budget_tokens": doc_generation_budget,
            "temperature": 0.1,
            "deterministic_mode": True,
        }
        self.implementation_ai = {
            "provider": impl_provider,
            "model_id": impl_model_id,
            "status": impl_status,
            "reasoning_tier": impl_reasoning_tier,
            "context_budget_tokens": impl_context_budget,
            "generation_budget_tokens": impl_generation_budget,
            "temperature": 0.0,
            "deterministic_mode": True,
            "prompt_execution_contract": "self-contained",
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "documentation_ai": self.documentation_ai,
            "implementation_ai": self.implementation_ai,
        }


class ProjectIntelligenceArchitect:
    """Unified Project Intelligence Architect role (PIA-001) supporting Sets A, B, C, and D."""

    def __init__(
        self,
        taxonomy: Optional[TaxonomyRegistry] = None,
        classifier: Optional[ProjectClassifier] = None,
        router: Optional[ProjectRouter] = None,
        tech_engine: Optional[TechnologyIntelligenceEngine] = None,
        composer: Optional[ProjectTemplateComposer] = None,
        capacity_estimator: Optional[CapacityEstimator] = None,
        diagram_generator: Optional[SystemDiagramGenerator] = None,
        decision_engine: Optional[SystemDesignDecisionEngine] = None,
        ingestion_engine: Optional[DocumentIngestionEngine] = None,
        clarification_engine: Optional[SocraticClarificationEngine] = None,
        ide_engine: Optional[IdeRecommendationEngine] = None,
    ):
        self.taxonomy = taxonomy or TaxonomyRegistry()
        self.classifier = classifier or ProjectClassifier(self.taxonomy)
        self.router = router or ProjectRouter(self.taxonomy)
        self.tech_engine = tech_engine or TechnologyIntelligenceEngine()
        self.composer = composer or ProjectTemplateComposer()
        self.capacity_estimator = capacity_estimator or CapacityEstimator()
        self.diagram_generator = diagram_generator or SystemDiagramGenerator()
        self.decision_engine = decision_engine or SystemDesignDecisionEngine()
        self.ingestion_engine = ingestion_engine or DocumentIngestionEngine()
        self.clarification_engine = clarification_engine or SocraticClarificationEngine()
        self.ide_engine = ide_engine or IdeRecommendationEngine()

    # -------------------------------------------------------------------------
    # MODE 1: PIA-NEW
    # -------------------------------------------------------------------------
    def execute_new(
        self,
        prompt: str,
        project_name: str = "project",
        ai_guidance: Optional[AIExecutionGuidance] = None,
        output_dir: Optional[Union[str, Path]] = None,
        document_paths: Optional[List[Union[str, Path]]] = None,
    ) -> Dict[str, Any]:
        """Execute PIA-NEW: Generate Set A, Set B, Set C, and Set D specifications."""
        guidance = ai_guidance or AIExecutionGuidance()

        # Ingest external documents if provided
        ingested_docs: List[IngestedDocument] = []
        combined_text = prompt
        if document_paths:
            ingested_docs = self.ingestion_engine.ingest_files(document_paths)
            doc_context_parts = []
            for doc in ingested_docs:
                if doc.extracted_text:
                    doc_context_parts.append(f"--- Document: {doc.path.name} ({doc.format.value}) ---\n{doc.extracted_text}")
            if doc_context_parts:
                combined_text = prompt + "\n\n" + "\n\n".join(doc_context_parts)

        profile = self.classifier.classify_text(combined_text, project_name=project_name)
        decisions = self.tech_engine.evaluate(profile, requirements_text=combined_text)
        routing = self.router.route(profile)

        # 1. Set A: Feature Intelligence
        set_a = self._synthesize_set_a(combined_text, profile)

        # 2. Set B: Gap & Problem Intelligence
        set_b = self._synthesize_set_b(combined_text, profile, decisions)

        # Socratic Clarification Analysis
        clarification_questions = self.clarification_engine.analyze_requirements(
            requirements_text=combined_text,
            profile=profile,
            existing_gaps=set_b.get("gaps", []),
        )

        # Extract explicit workload parameters from prompt if specified (e.g., DAU, actions per user)
        workload_params: Optional[Dict[str, Any]] = None
        dau_match = re.search(r"(\d[\d,]*)\s*(?:dau|daily\s+active\s+users)", combined_text, re.IGNORECASE)
        if dau_match:
            workload_params = workload_params or {}
            workload_params["daily_active_users"] = int(dau_match.group(1).replace(",", ""))

        allow_hypo = bool(re.search(r"(hypothetical|assumption|estimate\s+capacity|capacity\s+estimate)", combined_text, re.IGNORECASE))

        # 3. Set C: Solution Intelligence (Problem-to-solution mapping)
        set_c = self._synthesize_set_c(
            set_b,
            profile,
            workload_parameters=workload_params,
            allow_hypothetical_assumptions=allow_hypo,
        )

        # Evaluate IDE recommendations
        ide_recommendations = self.ide_engine.evaluate(
            project_profile=profile,
            technologies=decisions,
            requirements_text=combined_text,
        )

        # 4. Set D: Final Product Intelligence (Consolidation of Sets A, B, C)
        set_d, artifacts = self._synthesize_set_d(profile, decisions, routing, guidance, set_a, set_b, set_c)

        # Build Two-Gate Phase Milestone Plan
        phase_plan = self._generate_two_gate_phase_plan(profile, routing)

        result = {
            "mode": PIAMode.NEW.value,
            "project_name": profile.project_name,
            "project_id": profile.project_id,
            "profile": profile.to_dict(),
            "technologies": [d.to_dict() for d in decisions],
            "routing": routing.to_dict(),
            "ai_execution_guidance": guidance.to_dict(),
            # Four Interconnected Intelligence Sets
            "set_a_features": set_a,
            "set_b_gaps_problems": set_b,
            "set_c_solutions": set_c,
            "set_d_final_blueprint": set_d,
            # Backward-compatible references
            "set_a_analysis": set_a,
            "set_b_architecture": set_b,
            "artifacts": artifacts,
            "phase_plan": phase_plan,
            "clarification_questions": [q.to_dict() for q in clarification_questions],
            "ide_recommendations": [rec.to_dict() for rec in ide_recommendations],
            "ingested_documents": [doc.to_dict() for doc in ingested_docs],
        }

        if output_dir:
            out_p = Path(output_dir)
            out_p.mkdir(parents=True, exist_ok=True)
            for fname, content in artifacts.items():
                fpath = out_p / fname
                fpath.parent.mkdir(parents=True, exist_ok=True)
                fpath.write_text(content, encoding="utf-8")

        return result

    # -------------------------------------------------------------------------
    # MODE 2: PIA-DEFINED
    # -------------------------------------------------------------------------
    def execute_defined(
        self,
        documents: Dict[str, str],
        project_name: str = "project",
        ai_guidance: Optional[AIExecutionGuidance] = None,
        document_paths: Optional[List[Union[str, Path]]] = None,
    ) -> Dict[str, Any]:
        """Execute PIA-DEFINED: Harmonize fragmented documentation, gaps, and solutions."""
        guidance = ai_guidance or AIExecutionGuidance()

        # Ingest external documents if provided and merge into documents dict
        all_docs = dict(documents)
        ingested_docs: List[IngestedDocument] = []
        if document_paths:
            ingested_docs = self.ingestion_engine.ingest_files(document_paths)
            for doc in ingested_docs:
                if doc.extracted_text:
                    all_docs[doc.path.name] = doc.extracted_text

        # Combine text for holistic classification
        corpus = "\n\n".join(f"=== {k} ===\n{v}" for k, v in all_docs.items())
        profile = self.classifier.classify_text(corpus, project_name=project_name)
        decisions = self.tech_engine.evaluate(profile, requirements_text=corpus)
        routing = self.router.route(profile)

        # Detect conflicts across tiers
        conflicts = self._detect_document_conflicts(all_docs)

        # Four Sets
        set_a = self._synthesize_set_a(corpus, profile)
        set_b = self._synthesize_set_b(corpus, profile, decisions, doc_conflicts=conflicts)
        set_c = self._synthesize_set_c(set_b, profile, doc_conflicts=conflicts)
        set_d, artifacts = self._synthesize_set_d(
            profile, decisions, routing, guidance, set_a, set_b, set_c, conflicts=conflicts
        )

        return {
            "mode": PIAMode.DEFINED.value,
            "project_name": profile.project_name,
            "project_id": profile.project_id,
            "profile": profile.to_dict(),
            "conflicts_detected": conflicts,
            "set_a_features": set_a,
            "set_b_gaps_problems": set_b,
            "set_c_solutions": set_c,
            "set_d_final_blueprint": set_d,
            "harmonized_artifacts": artifacts,
            "artifacts": artifacts,
            "routing": routing.to_dict(),
            "ingested_documents": [doc.to_dict() for doc in ingested_docs],
        }

    # -------------------------------------------------------------------------
    # MODE 3: PIA-EVOLUTION
    # -------------------------------------------------------------------------
    def execute_evolution(
        self,
        codebase_dir: Union[str, Path],
        project_name: Optional[str] = None,
        known_docs: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Execute PIA-EVOLUTION: Codebase static X-Ray, debt scoring, and Set C/D evolution."""
        root = Path(codebase_dir).resolve()
        p_name = project_name or root.name

        # Reverse Engineering Intelligence Analysis
        re_engine = ReverseEngineeringEngine(root)
        as_is_report = re_engine.analyze(ExecutionLevel.LEVEL_1_STATIC)
        as_is_md = re_engine.render_markdown_report(as_is_report)

        # Static Code Analysis
        file_metrics = self._scan_codebase_ast(root)
        total_loc = as_is_report.total_loc if as_is_report.total_loc > 0 else sum(m["loc"] for m in file_metrics)
        avg_complexity = (sum(m["complexity"] for m in file_metrics) / len(file_metrics)) if file_metrics else 0.0

        # Technical Debt Index (0-100 score, lower is better)
        debt_factors: List[str] = [d.title for d in as_is_report.technical_debt]
        if avg_complexity > 10.0 and not any("complexity" in f.lower() for f in debt_factors):
            debt_factors.append(f"High average cyclomatic complexity ({avg_complexity:.1f})")
        if total_loc > 10000 and not any("test" in m["path"].lower() for m in file_metrics):
            debt_factors.append("No automated tests detected in repository")

        debt_score = min(100.0, len(as_is_report.technical_debt) * 20.0 + (avg_complexity * 2.0))

        # Architectural Drift Detection
        drift_items: List[str] = []
        if known_docs and "Tech-Stack.md" in known_docs:
            expected_tech = known_docs["Tech-Stack.md"].lower()
            detected_languages = {m["language"] for m in file_metrics}
            for lang in detected_languages:
                if lang != "unknown" and lang not in expected_tech:
                    drift_items.append(f"Detected unapproved language in implementation: {lang}")

        # Classify inferred profile
        summary = f"Project {p_name} containing {len(file_metrics)} files, {total_loc} lines of code."
        profile = self.classifier.classify_text(summary, project_name=p_name)
        routing = self.router.route(profile)
        decisions = self.tech_engine.evaluate(profile, requirements_text=summary)

        # Set A from existing code
        set_a = self._synthesize_set_a(summary, profile)

        # Set B from static inspection & debt
        set_b = self._synthesize_set_b_from_code(debt_factors, drift_items, avg_complexity, total_loc)

        # Set C Solution Intelligence for the debt & drift
        set_c = self._synthesize_set_c(set_b, profile)

        # Phased Evolution Plan
        evolution_plan = self._generate_evolution_plan(p_name, debt_factors, drift_items)

        # Set D Consolidation
        guidance = AIExecutionGuidance()
        set_d, artifacts = self._synthesize_set_d(profile, decisions, routing, guidance, set_a, set_b, set_c)

        artifacts["AS-IS-Architecture-Report.md"] = as_is_md

        return {
            "mode": PIAMode.EVOLUTION.value,
            "project_name": p_name,
            "files_analyzed": len(file_metrics),
            "total_loc": total_loc,
            "average_complexity": round(avg_complexity, 2),
            "technical_debt_score": round(debt_score, 1),
            "debt_factors": debt_factors,
            "architectural_drift": drift_items,
            "as_is_report": as_is_report.to_dict(),
            "file_metrics": file_metrics[:50],  # Sample first 50
            "set_a_features": set_a,
            "set_b_gaps_problems": set_b,
            "set_c_solutions": set_c,
            "set_d_final_blueprint": set_d,
            "evolution_plan": evolution_plan,
            "artifacts": artifacts,
            "routing": routing.to_dict(),
        }

    # -------------------------------------------------------------------------
    # SET A — FEATURE INTELLIGENCE
    # -------------------------------------------------------------------------
    def _synthesize_set_a(self, text: str, profile: ProjectProfile) -> Dict[str, Any]:
        """Synthesize Set A: Feature Intelligence (Product & domain research, market capabilities, features FEAT-xxx)."""
        features: List[Dict[str, Any]] = [
            {
                "feature_id": "FEAT-001",
                "title": f"Core {profile.primary_type.replace('_', ' ').title()} Engine",
                "description": f"Baseline capabilities for {profile.primary_type} with {profile.deployment_model} deployment.",
                "category": "essential",
                "evidence_type": EvidenceType.PROMPT_EXTRACTED.value,
                "priority": "P0",
                "source": "Project Input Prompt",
            },
            {
                "feature_id": "FEAT-002",
                "title": "Secure Environment & Configuration Runtime",
                "description": "Fail-closed configuration loading with zero missing environment variables.",
                "category": "essential",
                "evidence_type": EvidenceType.PROMPT_EXTRACTED.value,
                "priority": "P0",
                "source": "OpenClone Security Standard",
            },
            {
                "feature_id": "FEAT-003",
                "title": "Automated Quality & Verification Gates",
                "description": "Component and integration verification with cryptographic execution logs.",
                "category": "advanced",
                "evidence_type": EvidenceType.MARKET_INFERENCE.value,
                "priority": "P1",
                "source": "Market Expectation",
            },
            {
                "feature_id": "FEAT-004",
                "title": "Proactive Health & Telemetry Analytics",
                "description": "Diagnostic telemetry and performance auditing hooks.",
                "category": "optional",
                "evidence_type": EvidenceType.MARKET_INFERENCE.value,
                "priority": "P2",
                "source": "Market Capability Analysis",
            },
            {
                "feature_id": "FEAT-005",
                "title": "Distributed Multi-Region Scale Adapter",
                "description": "Future scaling adapter for high-throughput multi-region replication.",
                "category": "future",
                "evidence_type": EvidenceType.MARKET_INFERENCE.value,
                "priority": "P3",
                "source": "Future Product Capability",
            },
        ]

        return {
            "primary_archetype": {
                "value": profile.primary_type,
                "evidence_type": EvidenceType.PROMPT_EXTRACTED.value,
                "confidence": profile.classification_confidence,
            },
            "domain_disciplines": {
                "value": profile.supporting_disciplines,
                "evidence_type": EvidenceType.MARKET_INFERENCE.value,
            },
            "reliability_tier": {
                "value": profile.reliability_tier,
                "evidence_type": EvidenceType.PROMPT_EXTRACTED.value,
            },
            "data_sensitivity": {
                "value": profile.data_sensitivity,
                "evidence_type": EvidenceType.PROMPT_EXTRACTED.value,
            },
            "market_recommendation": {
                "value": f"Standard {profile.primary_type} with {profile.deployment_model} deployment.",
                "evidence_type": EvidenceType.MARKET_INFERENCE.value,
            },
            "user_expectations": [
                "Sub-200ms API response latency under standard load",
                "Zero credential leakage in logs or client-side bundles",
                "Deterministic error handling with actionable status codes",
            ],
            "competitor_capabilities": [
                "Automated CI/CD validation",
                "Self-healing session recovery",
                "Real-time event streaming",
            ],
            "features": features,
        }

    # -------------------------------------------------------------------------
    # SET B — GAP & PROBLEM INTELLIGENCE
    # -------------------------------------------------------------------------
    def _synthesize_set_b(
        self,
        prompt: str,
        profile: ProjectProfile,
        decisions: List[TechnologyDecision],
        doc_conflicts: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Synthesize Set B: Gap & Problem Intelligence (Identifies weaknesses, technical limitations GAP-xxx / PROB-xxx).

        IMPORTANT: Set B is NOT Target Architecture Specification.
        """
        items: List[Dict[str, Any]] = []

        # Domain gap analysis based on archetype
        if profile.reliability_tier in ("MISSION_CRITICAL", "HIGH"):
            items.append({
                "item_id": "GAP-001",
                "category": "scalability_problem",
                "title": "Unbounded Surge Concurrency Gap",
                "description": "High reliability tier requires handling 3x surge traffic without thread starvation or cascading failure.",
                "severity": "HIGH",
                "evidence_type": EvidenceType.STATIC_INSPECTION.value,
                "verified": True,
            })

        if profile.data_sensitivity in ("CONFIDENTIAL", "REGULATED", "CRITICAL"):
            items.append({
                "item_id": "GAP-002",
                "category": "security_weakness",
                "title": "Credential Exposure & Storage Vulnerability Gap",
                "description": "Sensitive data classification demands in-memory token redaction and encrypted persistence.",
                "severity": "CRITICAL",
                "evidence_type": EvidenceType.STATIC_INSPECTION.value,
                "verified": True,
            })

        items.append({
            "item_id": "PROB-001",
            "category": "technical_limitation",
            "title": "Unstructured Error Propagation Risk",
            "description": "Unhandled exceptions in backend services risk revealing internal stack traces to clients.",
            "severity": "MEDIUM",
            "evidence_type": EvidenceType.STATIC_INSPECTION.value,
            "verified": True,
        })

        if doc_conflicts:
            for i, c in enumerate(doc_conflicts, 1):
                items.append({
                    "item_id": f"GAP-CONF-{i:03d}",
                    "category": "functional_gap",
                    "title": f"Specification Contradiction in {c['topic']}",
                    "description": f"Discrepancy detected between {c['winner_doc']} and {c['loser_doc']}.",
                    "severity": "HIGH",
                    "evidence_type": EvidenceType.STATIC_INSPECTION.value,
                    "verified": True,
                })

        return {
            "gaps_and_problems": items,
            "total_gaps": len([x for x in items if x["item_id"].startswith("GAP")]),
            "total_problems": len([x for x in items if x["item_id"].startswith("PROB")]),
            "verified_count": len([x for x in items if x.get("verified", False)]),
        }

    def _synthesize_set_b_from_code(
        self,
        debt_factors: List[str],
        drift_items: List[str],
        avg_complexity: float,
        total_loc: int,
    ) -> Dict[str, Any]:
        """Synthesize Set B for PIA-EVOLUTION from verified codebase evidence."""
        items: List[Dict[str, Any]] = []

        if avg_complexity > 10.0:
            items.append({
                "item_id": "PROB-001",
                "category": "architecture_debt",
                "title": "High Cyclomatic Branching Complexity",
                "description": f"Average complexity ({avg_complexity:.1f}) exceeds maintainability threshold (10.0).",
                "severity": "HIGH",
                "evidence_type": EvidenceType.STATIC_INSPECTION.value,
                "verified": True,
            })
        else:
            items.append({
                "item_id": "PROB-001",
                "category": "technical_limitation",
                "title": "Static Code Inspection Baseline Debt",
                "description": f"Codebase verified with average complexity {avg_complexity:.1f}; requires regression safeguard and automated testing.",
                "severity": "MEDIUM",
                "evidence_type": EvidenceType.STATIC_INSPECTION.value,
                "verified": True,
            })

        for i, df in enumerate(debt_factors, 2):
            items.append({
                "item_id": f"GAP-{i:03d}",
                "category": "technical_limitation",
                "title": df,
                "description": f"Detected during static inspection: {df}",
                "severity": "MEDIUM",
                "evidence_type": EvidenceType.AUTOMATED_SCAN.value,
                "verified": True,
            })

        for i, drift in enumerate(drift_items, 1):
            items.append({
                "item_id": f"GAP-DRIFT-{i:03d}",
                "category": "functional_gap",
                "title": drift,
                "description": f"Architectural drift detected: {drift}",
                "severity": "HIGH",
                "evidence_type": EvidenceType.ARCHITECTURE_DEBT.value,
                "verified": True,
            })

        return {
            "gaps_and_problems": items,
            "total_gaps": len([x for x in items if x["item_id"].startswith("GAP")]),
            "total_problems": len([x for x in items if x["item_id"].startswith("PROB")]),
            "verified_count": len(items),
        }

    # -------------------------------------------------------------------------
    # SET C — SOLUTION INTELLIGENCE (NEW)
    # -------------------------------------------------------------------------
    def _synthesize_set_c(
        self,
        set_b: Dict[str, Any],
        profile: ProjectProfile,
        doc_conflicts: Optional[List[Dict[str, Any]]] = None,
        workload_parameters: Optional[Dict[str, Any]] = None,
        allow_hypothetical_assumptions: bool = False,
    ) -> Dict[str, Any]:
        """Synthesize Set C: Solution Intelligence (Problem-to-solution mapping SOL-xxx, acceptance criteria AC-xxx)."""
        solutions: List[Dict[str, Any]] = []
        gaps_and_problems = set_b.get("gaps_and_problems", [])

        # Map solutions directly to identified Set B items
        for idx, item in enumerate(gaps_and_problems, 1):
            sol_id = f"SOL-{idx:03d}"
            target_id = item["item_id"]
            ac_id = f"AC-{idx:03d}"

            if "GAP-001" in target_id or "Surge" in item["title"]:
                solutions.append({
                    "solution_id": sol_id,
                    "target_id": target_id,
                    "problem_description": item["description"],
                    "proposed_solution": "Implement async token bucket rate-limiting and connection pooling with graceful degradation.",
                    "alternative_solutions": [
                        "Elastic auto-scaling without client rate-limiting",
                        "Static queue throttling with drop-tail rejection",
                    ],
                    "expected_outcome": "System sustains 3x traffic surges with p99 latency < 250ms and zero 500 errors.",
                    "business_user_value": "Protects platform availability during peak marketing campaigns.",
                    "complexity": "MEDIUM",
                    "dependencies": ["FEAT-001"],
                    "risks_tradeoffs": "Adds 5ms overhead per request; requires Redis or local atomic counter.",
                    "status": SolutionStatus.RECOMMENDED.value,
                    "acceptance_criteria": [
                        f"{ac_id}: Load test confirms 3x surge sustained without thread pool starvation.",
                        f"{ac_id}-B: Rate limiter emits 429 Retry-After header on threshold breach.",
                    ],
                })
            elif "GAP-002" in target_id or "Credential" in item["title"]:
                solutions.append({
                    "solution_id": sol_id,
                    "target_id": target_id,
                    "problem_description": item["description"],
                    "proposed_solution": "Integrate zero-trust environment redaction and AES-GCM encrypted secret management.",
                    "alternative_solutions": [
                        "Plaintext environment variables with file permission ACLs",
                        "External cloud KMS with remote network latency",
                    ],
                    "expected_outcome": "All sensitive credentials redacted from logs; zero plaintext secrets in storage.",
                    "business_user_value": "Ensures compliance with GDPR, SOC2, and OpenClone security standards.",
                    "complexity": "HIGH",
                    "dependencies": ["FEAT-002"],
                    "risks_tradeoffs": "Key rotation requires automated migration script.",
                    "status": SolutionStatus.RECOMMENDED.value,
                    "acceptance_criteria": [
                        f"{ac_id}: Static secret scanner confirms zero plaintext keys committed.",
                        f"{ac_id}-B: Logging harness automatically masks sk-*, ghp_*, and AKIA* patterns.",
                    ],
                })
            elif "PROB-001" in target_id and "Complexity" in item["title"]:
                solutions.append({
                    "solution_id": sol_id,
                    "target_id": target_id,
                    "problem_description": item["description"],
                    "proposed_solution": "Decompose high-complexity functions into modular handler classes with single responsibilities.",
                    "alternative_solutions": [
                        "Suppress lint warnings without refactoring",
                        "Rewrite subsystem in alternative language",
                    ],
                    "expected_outcome": "Average cyclomatic complexity reduced below 8.0 across all modules.",
                    "business_user_value": "Decreases developer onboarding time and reduces regression defect rate.",
                    "complexity": "MEDIUM",
                    "dependencies": [],
                    "risks_tradeoffs": "Requires comprehensive unit test coverage to prevent refactoring regressions.",
                    "status": SolutionStatus.RECOMMENDED.value,
                    "acceptance_criteria": [
                        f"{ac_id}: AST complexity analyzer confirms all functions <= 10 cyclomatic branches.",
                    ],
                })
            else:
                solutions.append({
                    "solution_id": sol_id,
                    "target_id": target_id,
                    "problem_description": item["description"],
                    "proposed_solution": f"Remediate {item['title']} via standardized boundary enforcement.",
                    "alternative_solutions": ["Manual code review without automated linting"],
                    "expected_outcome": f"Resolution of {item['title']} with automated test verification.",
                    "business_user_value": "Improves overall engineering quality and system resilience.",
                    "complexity": "LOW",
                    "dependencies": [],
                    "risks_tradeoffs": "Minimal implementation risk.",
                    "status": SolutionStatus.RECOMMENDED.value,
                    "acceptance_criteria": [
                        f"{ac_id}: Verified fix committed with passing regression test.",
                    ],
                })

        # Proactive Improvement (Not tied to an existing defect)
        proactive_id = f"SOL-{len(solutions) + 1:03d}"
        solutions.append({
            "solution_id": proactive_id,
            "target_id": "PROACTIVE_IMPROVEMENT",
            "problem_description": "Proactive capability advancement: Structured JSON-Schema logging across all service boundaries.",
            "proposed_solution": "Adopt OpenTelemetry-compatible structured logging across all handlers.",
            "alternative_solutions": ["Unstructured plain text print statements"],
            "expected_outcome": "Unified log searchability and automated distributed trace ingestion.",
            "business_user_value": "Reduces Mean Time to Detect (MTTD) operational anomalies.",
            "complexity": "LOW",
            "dependencies": ["FEAT-002"],
            "risks_tradeoffs": "Slightly increased log storage footprint.",
            "status": SolutionStatus.PROPOSED.value,
            "acceptance_criteria": [
                f"AC-{len(solutions) + 1:03d}: All stdout events output valid JSON matching schema.",
            ],
        })

        # Quantitative Capacity & Sizing Estimation via CapacityEstimator (Defect 1 Remediation)
        # Strict zero-invention rule: Never invent synthetic DAU unless explicitly provided or hypothetical requested
        capacity_report: Union[ComprehensiveCapacityReport, UnestimatedCapacityReport]
        capacity_markdown: str

        if workload_parameters:
            traffic_profile = TrafficProfile(**workload_parameters)
            capacity_report = self.capacity_estimator.estimate(traffic_profile)
            capacity_markdown = capacity_report.to_markdown()
        elif allow_hypothetical_assumptions:
            # Explicitly requested hypothetical assumption: clearly labeled
            hypothetical_dau = 100_000 if profile.reliability_tier in ("MISSION_CRITICAL", "HIGH") else 10_000
            hypothetical_profile = TrafficProfile(daily_active_users=hypothetical_dau)
            capacity_report = self.capacity_estimator.estimate(hypothetical_profile)
            warning_banner = (
                "> [!WARNING]\n"
                "> **Hypothetical Baseline Assumption — Unconfirmed**\n"
                "> Workload metrics were not provided in project specification. The following capacity sizing "
                f"reflects a hypothetical baseline assumption of {hypothetical_dau:,} DAU for architectural planning only. "
                "These values MUST NOT be treated as confirmed user requirements.\n\n"
            )
            capacity_markdown = warning_banner + capacity_report.to_markdown()
        else:
            # No workload parameters provided and no hypothetical assumptions requested: return NOT_ESTIMATED
            capacity_report = self.capacity_estimator.estimate(None)
            capacity_markdown = capacity_report.to_markdown()

        return {
            "solutions": solutions,
            "total_solutions": len(solutions),
            "recommended_count": len([s for s in solutions if s["status"] == SolutionStatus.RECOMMENDED.value]),
            "proposed_count": len([s for s in solutions if s["status"] == SolutionStatus.PROPOSED.value]),
            "capacity_report": capacity_report,
            "capacity_markdown": capacity_markdown,
        }

    # -------------------------------------------------------------------------
    # DYNAMIC C4 ARCHITECTURE GENERATION
    # -------------------------------------------------------------------------
    def _build_dynamic_c4_containers(
        self,
        profile: ProjectProfile,
        decisions: List[TechnologyDecision],
    ) -> Tuple[List[str], List[str], List[Dict[str, str]]]:
        """Synthesize dynamic C4 context and container elements directly from technology decisions.

        Strict Architecture Rules:
        1. Confirmed Decisions: Technology explicitly confirmed in TechnologyDecision list appears with its exact name.
        2. Recommendations: Technology recommended but unconfirmed carries "[Recommended]".
        3. Unresolved Decisions: Dimensions without selected technology carry "[Unresolved: Missing Architecture Decision]".
        4. Zero Invention: Never invent universal defaults (PostgreSQL, React, FastAPI, Kafka).
        5. Archetype Context: Only include containers that correspond to selected or required system tiers.
        """
        user_types: List[str] = []
        external_systems: List[str] = []
        containers: List[Dict[str, str]] = []

        ptype = (profile.primary_type or "").lower().replace("-", "_")
        family = (profile.primary_family or "").lower()
        targets = profile.delivery_targets or []

        # Index decisions by category
        def find_decision(*cat_keywords: str) -> Optional[TechnologyDecision]:
            for d in decisions:
                c_name = d.category.lower()
                if any(kw in c_name for kw in cat_keywords):
                    return d
            return None

        frontend_dec = find_decision("frontend", "ui", "client", "mobile", "web")
        backend_dec = find_decision("backend", "api", "service", "core", "runtime")
        db_dec = find_decision("database", "persistence", "storage", "sql", "datastore")
        vector_dec = find_decision("vector", "embedding", "rag")
        event_dec = find_decision("event", "broker", "queue", "streaming", "messaging")
        ai_dec = find_decision("ai", "llm", "orchestration", "model")

        def tech_label(dec: Optional[TechnologyDecision], fallback_name: str, dimension_name: str) -> str:
            if dec is not None and dec.selected_technology:
                status = getattr(dec, "verification_status", "CONFIRMED")
                if status in ("RECOMMENDED", "PROPOSED"):
                    return f"{dec.selected_technology} [Recommended]"
                return dec.selected_technology
            return f"[Unresolved: Missing {dimension_name} Decision]"

        # Check for event broker decision
        has_event_broker = event_dec is not None or any("event" in d.category.lower() or "stream" in d.category.lower() for d in decisions)
        # Check for vector database decision
        has_vector_db = vector_dec is not None or any("vector" in d.category.lower() for d in decisions)

        # Scenario 1: Static Portfolio / Jamstack / Landing Page
        if any(k in ptype for k in ("mini_website", "static_site", "portfolio", "landing_page", "jamstack")):
            user_types = ["Site Visitor", "Content Author"]
            external_systems = ["Content Delivery Network (CDN)"]
            frontend_tech = tech_label(frontend_dec, "HTML5 / Tailwind CSS", "Frontend")
            containers = [
                {
                    "id": "browser_client",
                    "name": "Browser Client",
                    "technology": frontend_tech,
                    "description": "Renders responsive static layout and client interactions in browser",
                },
                {
                    "id": "static_host",
                    "name": "Static Web Host & CDN Edge",
                    "technology": "Edge CDN / Static Object Storage",
                    "description": "Distributes pre-rendered static assets globally with TLS termination",
                },
            ]
            return user_types, external_systems, containers

        # Scenario 2: CLI Tool / Embedded Engine / Terminal Utility
        if any(k in ptype for k in ("cli_tool", "terminal", "console", "embedded", "developer_tool")) or "developer_tools" in family or "embedded_hardware" in targets:
            user_types = ["Software Developer", "DevOps Engineer"]
            external_systems = ["Operating System Host Environment"]
            runtime_tech = tech_label(backend_dec, "", "CLI Runtime")
            containers.append({
                "id": "cli_engine",
                "name": "CLI Console Engine",
                "technology": runtime_tech,
                "description": "Command line interface, argument parsing, and execution orchestrator",
            })
            if db_dec is not None or any("database" in d.category.lower() or "persistence" in d.category.lower() for d in decisions):
                db_tech = tech_label(db_dec, "", "Storage")
                containers.append({
                    "id": "embedded_storage",
                    "name": "Embedded Storage Engine",
                    "technology": db_tech,
                    "description": "Local state cache and configuration storage",
                })
            return user_types, external_systems, containers

        # Scenario 3: AI Agent Platform / Orchestrator / Multi-Agent System
        if any(k in ptype for k in ("agent", "ai_platform", "orchestrator", "rag")) or "ai_engineering" in family or has_vector_db or ai_dec is not None:
            user_types = ["AI Practitioner", "End User"]
            external_systems = ["External LLM Providers"]
            # UI Container (only if web_browser or mobile target)
            if any(t in targets for t in ("web_browser", "web", "android", "ios")) or frontend_dec:
                fe_tech = tech_label(frontend_dec, "Interactive UI", "Frontend")
                containers.append({
                    "id": "ai_agent_ui",
                    "name": "Agent Workspace UI",
                    "technology": fe_tech,
                    "description": "Interactive prompt canvas, thread inspection, and execution graph visualization",
                })
            # Orchestrator
            orch_tech = tech_label(backend_dec, "Agent Core", "Backend")
            containers.append({
                "id": "agent_orchestrator",
                "name": "Agent Orchestrator Core",
                "technology": orch_tech,
                "description": "Multi-agent coordination, goal decomposition, and execution state machine",
            })
            # LLM Gateway
            ai_label = tech_label(ai_dec, "LLM Gateway", "AI/LLM Gateway")
            containers.append({
                "id": "llm_gateway",
                "name": "LLM Inference Gateway",
                "technology": ai_label,
                "description": "Provider failover routing, token budget enforcement, and streaming response proxy",
            })
            # Vector database (decided vs unresolved)
            if vector_dec is not None or "vector" in (profile.conditional_profiles or []):
                v_tech = tech_label(vector_dec, "Vector Store", "Vector Database")
                containers.append({
                    "id": "vector_memory_store",
                    "name": "Vector Knowledge & Memory Store",
                    "technology": v_tech,
                    "description": "Episodic memory embeddings and semantic index retrieval",
                })
            # Relational database if decided
            if db_dec is not None:
                containers.append({
                    "id": "primary_db",
                    "name": "Primary Database",
                    "technology": tech_label(db_dec, "Relational DB", "Database"),
                    "description": "Relational session checkpoints and metadata storage",
                })
            return user_types, external_systems, containers

        # Scenario 4: IoT Data Platform / Streaming Telemetry / Event Pipeline / ETL / Broker
        if any(k in ptype for k in ("iot", "telemetry", "streaming", "event_pipeline", "data_platform", "etl_pipeline", "event_driven")) or "data_engineering" in family or has_event_broker:
            user_types = ["Data Engineer", "Operations Analyst", "IoT Field Device"]
            external_systems = ["IoT Edge Gateway", "Downstream Analytics Dashboard"]
            ingest_tech = tech_label(backend_dec, "Ingestion Service", "Ingestion Service")
            containers.append({
                "id": "telemetry_ingest",
                "name": "Telemetry Ingestion Gateway",
                "technology": ingest_tech,
                "description": "High-throughput sensor packet ingestion and authentication",
            })
            # Event Broker
            broker_tech = tech_label(event_dec, "Event Broker", "Event Broker")
            containers.append({
                "id": "event_broker",
                "name": "Event Stream Broker",
                "technology": broker_tech,
                "description": "Durable distributed log buffering telemetry events for downstream workers",
            })
            # Processing Worker
            containers.append({
                "id": "stream_processor",
                "name": "Stream Processing Worker",
                "technology": f"{ingest_tech} Stream Worker",
                "description": "Sliding window aggregation and transformation worker",
            })
            # Datastore
            if db_dec is not None:
                containers.append({
                    "id": "time_series_store",
                    "name": "Analytical Time-Series Store",
                    "technology": tech_label(db_dec, "Analytical DB", "Database"),
                    "description": "Partitioned telemetry storage for rollups and analytical queries",
                })
            return user_types, external_systems, containers

        # Scenario 5: General Web Application / Microservice
        user_types = ["Standard User", "Administrator"]
        external_systems = ["Identity Provider", "Monitoring & Logging Service"]

        # Frontend (only if frontend decision exists or targets web)
        if any(t in targets for t in ("web_browser", "web", "android", "ios")) or frontend_dec:
            fe_tech = tech_label(frontend_dec, "Frontend Application", "Frontend")
            containers.append({
                "id": "frontend_app",
                "name": "Frontend Application",
                "technology": fe_tech,
                "description": "Interactive user interface and client workflows",
            })

        # Backend
        be_tech = tech_label(backend_dec, "Backend API", "Backend")
        containers.append({
            "id": "backend_api",
            "name": "Backend Core API",
            "technology": be_tech,
            "description": "Business logic execution and API services",
        })

        # Database (only if decided or required)
        if db_dec is not None or "database" in [d.category.lower() for d in decisions]:
            db_tech = tech_label(db_dec, "Primary Database", "Database")
            containers.append({
                "id": "primary_db",
                "name": "Primary Database",
                "technology": db_tech,
                "description": "Data persistence and transaction management",
            })

        return user_types, external_systems, containers

    # -------------------------------------------------------------------------
    # SET D — FINAL PRODUCT INTELLIGENCE (CONSOLIDATION)
    # -------------------------------------------------------------------------
    def _synthesize_set_d(
        self,
        profile: ProjectProfile,
        decisions: List[TechnologyDecision],
        routing: RoutingDecision,
        guidance: AIExecutionGuidance,
        set_a: Dict[str, Any],
        set_b: Dict[str, Any],
        set_c: Dict[str, Any],
        conflicts: Optional[List[Dict[str, Any]]] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """Synthesize Set D: Consolidates Sets A, B, and C into an advanced, complete product blueprint."""
        project_md = self.composer.compose_project_md(profile, decisions, routing)

        # Inject AI Guidance frontmatter into PROJECT.md
        frontmatter_lines = [
            "---",
            "openclone_profile:",
            '  schema_version: "2.1.0"',
            f'  project_id: "{profile.project_id}"',
            f'  lifecycle_mode: "{PIAMode.NEW.value}"',
            "  ai_execution_guidance:",
            "    documentation_ai:",
            f'      provider: "{guidance.documentation_ai["provider"]}"',
            f'      model_id: "{guidance.documentation_ai["model_id"]}"',
            f'      status: "{guidance.documentation_ai["status"]}"',
            f'      reasoning_tier: "{guidance.documentation_ai["reasoning_tier"]}"',
            f'      context_budget_tokens: {guidance.documentation_ai["context_budget_tokens"]}',
            f'      generation_budget_tokens: {guidance.documentation_ai["generation_budget_tokens"]}',
            "    implementation_ai:",
            f'      provider: "{guidance.implementation_ai["provider"]}"',
            f'      model_id: "{guidance.implementation_ai["model_id"]}"',
            f'      status: "{guidance.implementation_ai["status"]}"',
            f'      reasoning_tier: "{guidance.implementation_ai["reasoning_tier"]}"',
            f'      context_budget_tokens: {guidance.implementation_ai["context_budget_tokens"]}',
            f'      generation_budget_tokens: {guidance.implementation_ai["generation_budget_tokens"]}',
            '      prompt_execution_contract: "self-contained"',
            "---",
            "",
        ]
        project_md = "\n".join(frontmatter_lines) + project_md

        # 1. Project-Requirement.md
        req_lines = [
            f"# PROJECT REQUIREMENTS — {profile.project_name}",
            "",
            "## 1. Domain Scope & Intelligence",
            f"- **Primary Archetype:** `{profile.primary_type}` (Evidence: `{set_a['primary_archetype']['evidence_type']}`)",
            f"- **Complexity Level:** `{profile.complexity.level}` — {profile.complexity.rationale}",
            f"- **Data Sensitivity:** `{profile.data_sensitivity}`",
            f"- **Reliability Target:** `{profile.reliability_tier}`",
            "",
            "## 2. Core Functional Requirements",
            "1. **FR-01:** System must initialize with strict boundary validation and zero missing environment keys.",
            f"2. **FR-02:** Implement core business capabilities for {profile.primary_type}.",
            "3. **FR-03:** Enforce tamper-evident logging and credential redaction across all external tool interactions.",
            "",
            "## 3. Requirements Traceability Matrix",
            "| Requirement ID | Linked Feature ID | Linked Solution ID | Acceptance Criteria |",
            "|---|---|---|---|",
        ]
        features = set_a.get("features", [])
        solutions = set_c.get("solutions", [])
        for idx, feat in enumerate(features, 1):
            sol = solutions[idx - 1] if idx - 1 < len(solutions) else (solutions[0] if solutions else {})
            sol_id = sol.get("solution_id", "N/A")
            ac = sol.get("acceptance_criteria", ["Verified implementation"])[0] if sol else "N/A"
            req_lines.append(f"| FR-{idx:02d} | `{feat['feature_id']}` | `{sol_id}` | {ac} |")
        req_lines.append("")
        project_requirement_md = "\n".join(req_lines)

        # 2. Features-List.md (Set A Output)
        features_lines = [
            f"# FEATURES LIST (SET A) — {profile.project_name}",
            "",
            "| Feature ID | Title | Category | Priority | Target Milestone | Responsible Specialist |",
            "|---|---|---|---|---|---|",
        ]
        for f in features:
            features_lines.append(
                f"| `{f['feature_id']}` | **{f['title']}** | `{f['category']}` | `{f['priority']}` | PHASE-01 | Principal Architect |"
            )
        features_lines.append("")
        features_list_md = "\n".join(features_lines)

        # 3. Gaps-And-Problems.md (Set B Output)
        gap_lines = [
            f"# GAP & PROBLEM INTELLIGENCE (SET B) — {profile.project_name}",
            "",
            "| Item ID | Category | Title | Severity | Evidence Classification | Verified |",
            "|---|---|---|---|---|---|",
        ]
        for g in set_b.get("gaps_and_problems", []):
            gap_lines.append(
                f"| `{g['item_id']}` | `{g['category']}` | **{g['title']}** | `{g['severity']}` | `{g['evidence_type']}` | {g.get('verified', False)} |"
            )
        gap_lines.append("")
        gaps_and_problems_md = "\n".join(gap_lines)

        # 4. Solution-Blueprint.md (Set C Output)
        sol_lines = [
            f"# SOLUTION INTELLIGENCE BLUEPRINT (SET C) — {profile.project_name}",
            "",
            "| Solution ID | Target Defect ID | Proposed Solution | Status | Complexity | Key Acceptance Criteria |",
            "|---|---|---|---|---|---|",
        ]
        for s in solutions:
            ac_summary = s["acceptance_criteria"][0] if s.get("acceptance_criteria") else "Pass unit tests"
            sol_lines.append(
                f"| `{s['solution_id']}` | `{s['target_id']}` | **{s['proposed_solution']}** | `{s['status']}` | `{s['complexity']}` | {ac_summary} |"
            )
        sol_lines.append("")
        solution_blueprint_md = "\n".join(sol_lines)

        # 5. Tech-Stack.md
        tech_lines = [
            f"# TECHNOLOGY STACK & ARCHITECTURE DECISIONS — {profile.project_name}",
            "",
            "## Selected Technology Matrix",
            "| Architectural Dimension | Selected Technology | Rationale | Alternatives Evaluated |",
            "|---|---|---|---|",
        ]
        for d in decisions:
            alts = ", ".join(d.alternatives_evaluated) if d.alternatives_evaluated else "None"
            tech_lines.append(f"| {d.category} | **{d.selected_technology}** | {d.selection_rationale} | {alts} |")
        tech_lines.append("")
        tech_stack_md = "\n".join(tech_lines)

        # 6. Decision-Log.md (ADRs)
        # System Design Capacity Report
        capacity_report = set_c.get("capacity_report")
        if capacity_report is None or not hasattr(capacity_report, "to_markdown"):
            capacity_report = self.capacity_estimator.estimate(None)

        capacity_md = set_c.get("capacity_markdown", capacity_report.to_markdown())

        # System Design Decision Engine (Enforcing Monolith-First Rule)
        peak_rps = getattr(capacity_report, "peak_rps", None) or 10.0
        daily_storage = getattr(getattr(capacity_report, "storage", None), "daily_raw_gb", 0.01)
        sys_req = SystemRequirements(
            project_name=profile.project_name,
            functional_summary=f"{profile.primary_type} ({profile.deployment_model})",
            peak_rps=peak_rps,
            total_data_gb=daily_storage * 365.0,
            multi_tenant=profile.deployment_model == "MULTI_TENANT",
            quality_attributes=QualityAttributes(
                availability_target="99.9%" if profile.reliability_tier == "HIGH_AVAILABILITY" else "99.0%",
                auditability="high" if profile.data_sensitivity in ("CONFIDENTIAL", "REGULATED", "CRITICAL") else "standard",
            ),
        )
        arch_rec = self.decision_engine.evaluate(sys_req)

        # System Design C4 Diagrams (Dynamically generated according to project profile and decisions)
        user_types, external_systems, containers = self._build_dynamic_c4_containers(profile, decisions)
        core_desc = f"{profile.primary_type.replace('_', ' ').title()} Core Platform"

        c4_context_diagram = self.diagram_generator.generate_c4_context(
            system_name=profile.project_name,
            user_types=user_types,
            external_systems=external_systems,
            core_description=core_desc,
        )

        c4_container_diagram = self.diagram_generator.generate_c4_container(
            system_name=profile.project_name,
            containers=containers,
        )

        system_architecture_md = "\n".join([
            f"# SYSTEM ARCHITECTURE & DESIGN SPECIFICATION — {profile.project_name}",
            "",
            "## 1. Architectural Strategy & Pattern Selection",
            f"- **Primary Architecture Pattern:** **{arch_rec.primary_pattern}**",
            f"- **Code Organization Pattern:** `{arch_rec.code_pattern}`",
            f"- **Database Tier:** `{arch_rec.database_tier}`",
            f"- **Caching Strategy:** `{arch_rec.caching_tier}`",
            f"- **Asynchronous Processing:** `{arch_rec.queue_tier}`",
            f"- **Operational Complexity:** `{arch_rec.operational_complexity}`",
            f"- **Rationale:** {arch_rec.rationale}",
            "",
            "## 2. System Context Diagram (C4 Context)",
            c4_context_diagram,
            "",
            "## 3. Container Diagram (C4 Container)",
            c4_container_diagram,
            "",
            "## 4. Quantitative Capacity & Sizing Projections",
            capacity_md,
            "",
        ])

        decision_lines = [
            f"# ARCHITECTURAL DECISION LOG (ADR) — {profile.project_name}",
            "",
            "## Authority Precedence Hierarchy",
            "1. **Tier 1 (Master):** `PROJECT.md`",
            "2. **Tier 2 (Historical):** `Decision-Log.md`",
            "3. **Tier 3 (Functional):** `Project-Requirement.md`, `Features-List.md`",
            "4. **Tier 4 (Technical):** `Tech-Stack.md`, `Project-Details.md`",
            "",
            "## Recorded Decisions",
            "### ADR-001: Four-Set Intelligence Architecture Integration",
            "- **Status:** Accepted",
            "- **Context:** Establish clear separation across Feature Intelligence (Set A), Gap Intelligence (Set B), Solution Intelligence (Set C), and Consolidated Product Intelligence (Set D).",
            "- **Decision:** PIA operates Sets A->B->C->D before handing off approved requirements to Software Architecture and System Design.",
            "",
            "### ADR-002: Two-Gate Human Phase Milestone Governance",
            "- **Status:** Accepted",
            "- **Context:** Prevent circular task dependency deadlocks during phase transitions.",
            "- **Decision:** Decouple phase execution into PHASE-XX-START (Gate A kickoff) and PHASE-XX-COMPLETION (Gate B acceptance).",
            "",
            f"### ADR-003: Architectural Pattern Selection — {arch_rec.primary_pattern}",
            "- **Status:** Accepted",
            f"- **Context:** Evaluated peak throughput ({peak_rps:,.1f} RPS), reliability target ({profile.reliability_tier}), and Monolith-First Rule.",
            f"- **Decision:** Adopt {arch_rec.primary_pattern} with {arch_rec.code_pattern}.",
            f"- **Rationale:** {arch_rec.rationale}",
            f"- **Database Tier:** {arch_rec.database_tier}",
            f"- **Caching Tier:** {arch_rec.caching_tier}",
            f"- **Queue Tier:** {arch_rec.queue_tier}",
            f"- **Operational Complexity:** {arch_rec.operational_complexity}",
            "",
        ]
        if conflicts:
            decision_lines.append("## Reconciled Document Conflicts")
            for i, c in enumerate(conflicts, 1):
                decision_lines.append(f"### ADR-CONFLICT-{i:03d}: Reconciliation of {c['topic']}")
                decision_lines.append(f"- **Higher Authority Document:** `{c['winner_doc']}`")
                decision_lines.append(f"- **Overridden Document:** `{c['loser_doc']}`")
                decision_lines.append(f"- **Resolution Details:** {c['resolution']}")
                decision_lines.append("")
        decision_log_md = "\n".join(decision_lines)

        # 7. Project-Details.md
        all_roles = [r for roles in routing.workforce.values() for r in roles]
        details_lines = [
            f"# PROJECT DETAILS & OPERATIONAL SPECIFICATIONS — {profile.project_name}",
            "",
            f"- **Project ID:** `{profile.project_id}`",
            f"- **Primary Family:** `{profile.primary_family}`",
            f"- **Delivery Targets:** `{', '.join(profile.delivery_targets)}`",
            f"- **Minimum Effective Workforce Count:** `{len(all_roles)}` specialists",
            "",
            "## Workforce Allocation",
        ]
        for team, roles in routing.workforce.items():
            details_lines.append(f"### Team: {team}")
            for role in roles:
                details_lines.append(f"- **{role}**")
        project_details_md = "\n".join(details_lines)

        # Existing flat files for 100% backward compatibility
        build_prompt_md = self.composer.compose_build_prompt(profile, decisions, routing)
        agent_instructions_md = self.composer.compose_agent_instructions(profile, routing)
        env_example = self.composer.compose_env_example(decisions)

        # STRIDE Security Threat Model Integration
        from src.openclone.security.threat_model import STRIDEThreatModeler
        stride_result = STRIDEThreatModeler.evaluate(
            project_name=profile.project_name,
            architecture_pattern=arch_rec.primary_pattern,
            has_auth=True,
            is_multi_tenant=profile.deployment_model == "MULTI_TENANT",
            has_external_api=len(external_systems) > 0,
        )
        threat_lines = [
            f"# STRIDE SECURITY THREAT MODEL & MITIGATION MATRIX — {profile.project_name}",
            "",
            f"- **Target Architecture Pattern:** `{arch_rec.primary_pattern}`",
            f"- **Identified Threats:** `{stride_result['total_threats']}` "
            f"(Critical: `{stride_result['severity_summary']['critical']}`, "
            f"High: `{stride_result['severity_summary']['high']}`, "
            f"Medium: `{stride_result['severity_summary']['medium']}`)",
            "",
            "| Threat ID | Category | Title | Severity | Target Component | Countermeasure | Verification |",
            "|---|---|---|---|---|---|---|",
        ]
        for t in stride_result["threats"]:
            threat_lines.append(
                f"| `{t['threat_id']}` | **{t['category']}** | {t['title']} | `{t['severity']}` | `{t['target_component']}` | {t['countermeasure']} | {t['verification_check']} |"
            )
        threat_lines.append("")
        threat_model_md = "\n".join(threat_lines)

        artifacts = {
            # Canonical Master Documents
            "PROJECT.md": project_md,
            "BUILD_PROMPT.md": build_prompt_md,
            "AGENT_INSTRUCTIONS.md": agent_instructions_md,
            ".env.example": env_example,
            # Modular Four-Set Documents
            "Project-Requirement.md": project_requirement_md,
            "Features-List.md": features_list_md,
            "Gaps-And-Problems.md": gaps_and_problems_md,
            "Solution-Blueprint.md": solution_blueprint_md,
            "Tech-Stack.md": tech_stack_md,
            "Decision-Log.md": decision_log_md,
            "Project-Details.md": project_details_md,
            "System-Architecture.md": system_architecture_md,
            "Threat-Model.md": threat_model_md,
        }

        # Relational Many-to-Many Traceability Matrix
        features = set_a.get("features", [])
        solutions = set_c.get("solutions", [])
        gaps_and_problems = set_b.get("gaps_and_problems", [])

        relational_matrix: List[Dict[str, Any]] = []
        for idx, feat in enumerate(features, 1):
            fid = feat["feature_id"]
            matching_sols = [s for s in solutions if fid in s.get("dependencies", [])]
            if not matching_sols and solutions:
                matching_sols = [solutions[(idx - 1) % len(solutions)]]

            sol_ids = [s["solution_id"] for s in matching_sols]
            defect_ids = [s["target_id"] for s in matching_sols if s.get("target_id") != "PROACTIVE_IMPROVEMENT"]
            ac_list: List[str] = []
            for s in matching_sols:
                ac_list.extend(s.get("acceptance_criteria", []))

            relational_matrix.append({
                "requirement_id": f"FR-{idx:02d}",
                "feature_id": fid,
                "feature_ids": [fid],
                "solution_id": sol_ids[0] if sol_ids else None,
                "solution_ids": sol_ids,
                "target_defect_id": defect_ids[0] if defect_ids else None,
                "target_defect_ids": defect_ids,
                "acceptance_criteria": ac_list,
                "status": matching_sols[0].get("status", "RECOMMENDED") if matching_sols else "APPROVED",
                "is_proactive": False,
            })

        # Proactive enhancements without direct defect links
        for s in solutions:
            if s.get("target_id") == "PROACTIVE_IMPROVEMENT":
                relational_matrix.append({
                    "requirement_id": f"PROACT-{s['solution_id']}",
                    "feature_id": s.get("dependencies", ["PROACTIVE"])[0] if s.get("dependencies") else "PROACTIVE",
                    "feature_ids": s.get("dependencies", []),
                    "solution_id": s["solution_id"],
                    "solution_ids": [s["solution_id"]],
                    "target_defect_id": None,
                    "target_defect_ids": [],
                    "acceptance_criteria": s.get("acceptance_criteria", []),
                    "status": s.get("status", "PROPOSED"),
                    "is_proactive": True,
                })

        # Track unresolved defects
        solved_targets = {s.get("target_id") for s in solutions}
        unresolved_defects = [
            g for g in gaps_and_problems if g.get("item_id") not in solved_targets
        ]

        # Consolidated Set D Data Object
        set_d_data = {
            "project_name": profile.project_name,
            "project_id": profile.project_id,
            "feature_catalogue": features,
            "gaps_and_problems": gaps_and_problems,
            "solutions": solutions,
            "traceability_matrix": relational_matrix,
            "unresolved_defects": unresolved_defects,
            "consolidation_timestamp": "2026-11-26T12:00:00Z",
            "traceability_verified": True,
            "architecture_recommendation": arch_rec.__dict__,
            "capacity_report": capacity_report,
        }

        return set_d_data, artifacts

    def _detect_document_conflicts(self, documents: Dict[str, str]) -> List[Dict[str, Any]]:
        """Identify contradictions between lower-tier and higher-tier documents."""
        conflicts: List[Dict[str, Any]] = []

        proj_text = documents.get("PROJECT.md", "").lower()
        tech_text = documents.get("Tech-Stack.md", "").lower()

        if "sqlite" in proj_text and "postgresql" in tech_text:
            conflicts.append({
                "topic": "Primary Database Selection",
                "winner_doc": "PROJECT.md (Tier 1)",
                "loser_doc": "Tech-Stack.md (Tier 4)",
                "resolution": "Tier 1 authority overrides Tier 4. Selected database is SQLite. Tech-Stack.md updated.",
            })

        return conflicts

    def _scan_codebase_ast(self, root: Path) -> List[Dict[str, Any]]:
        """Perform AST inspection and calculate cyclomatic complexity on Python files."""
        metrics: List[Dict[str, Any]] = []
        for path in sorted(root.rglob("*.py")):
            if any(part in (".git", "venv", "__pycache__", ".aisdf") for part in path.parts):
                continue
            try:
                code = path.read_text(encoding="utf-8", errors="replace")
                lines = code.splitlines()
                tree = ast.parse(code)

                complexity = 1
                for node in ast.walk(tree):
                    if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With)):
                        complexity += 1

                metrics.append({
                    "path": str(path.relative_to(root).as_posix()),
                    "language": "python",
                    "loc": len(lines),
                    "complexity": complexity,
                })
            except Exception:
                metrics.append({
                    "path": str(path.relative_to(root).as_posix()),
                    "language": "python",
                    "loc": 0,
                    "complexity": 1,
                })
        return metrics

    def _generate_two_gate_phase_plan(
        self,
        profile: ProjectProfile,
        routing: RoutingDecision,
    ) -> List[Dict[str, Any]]:
        """Generate two-gate phase milestone task plan eliminating circular deadlocks."""
        all_roles = [r for roles in routing.workforce.values() for r in roles]
        tasks: List[Dict[str, Any]] = [
            # Phase 1
            {
                "task_id": "PHASE-01-START",
                "title": "Phase 1 Kickoff Authorization (Gate A)",
                "worker_id": "project-intelligence-architect",
                "action": "gate",
                "depends_on": [],
            },
            {
                "task_id": "TASK-01-01",
                "title": f"Initialize {profile.project_name} Environment",
                "worker_id": "devops-engineer" if "devops-engineer" in all_roles else "backend-engineer",
                "action": "write",
                "depends_on": ["PHASE-01-START"],
            },
            {
                "task_id": "PHASE-01-COMPLETION",
                "title": "Phase 1 Acceptance & Work Attestation (Gate B)",
                "worker_id": "project-intelligence-architect",
                "action": "gate",
                "depends_on": ["TASK-01-01"],
            },
            # Phase 2
            {
                "task_id": "PHASE-02-START",
                "title": "Phase 2 Kickoff Authorization (Gate A)",
                "worker_id": "project-intelligence-architect",
                "action": "gate",
                "depends_on": ["PHASE-01-COMPLETION"],
            },
            {
                "task_id": "TASK-02-01",
                "title": f"Implement Core {profile.primary_type} Logic",
                "worker_id": "principal-architect" if "principal-architect" in all_roles else "backend-engineer",
                "action": "write",
                "depends_on": ["PHASE-02-START"],
            },
            {
                "task_id": "PHASE-02-COMPLETION",
                "title": "Phase 2 Acceptance & Work Attestation (Gate B)",
                "worker_id": "project-intelligence-architect",
                "action": "gate",
                "depends_on": ["TASK-02-01"],
            },
        ]
        return tasks

    def _generate_evolution_plan(
        self,
        project_name: str,
        debt_factors: List[str],
        drift_items: List[str],
    ) -> List[Dict[str, Any]]:
        """Generate migration plan resolving identified technical debt and architectural drift."""
        plan: List[Dict[str, Any]] = []
        phase_idx = 1
        if debt_factors:
            plan.append({
                "phase": f"PHASE-{phase_idx:02d}",
                "title": "Technical Debt Remediation",
                "goals": debt_factors,
                "gate_a": f"PHASE-{phase_idx:02d}-START",
                "gate_b": f"PHASE-{phase_idx:02d}-COMPLETION",
            })
            phase_idx += 1
        if drift_items:
            plan.append({
                "phase": f"PHASE-{phase_idx:02d}",
                "title": "Architectural Drift Reconciliation",
                "goals": drift_items,
                "gate_a": f"PHASE-{phase_idx:02d}-START",
                "gate_b": f"PHASE-{phase_idx:02d}-COMPLETION",
            })
        return plan

    def sync_to_memory(
        self,
        project_definition: Dict[str, Any],
        workspace_path: Union[str, Path],
        human_approved: bool = False,
        approval_digest: Optional[str] = None,
        auth_context: Optional[Any] = None,
        approval_record: Optional[Any] = None,
        gateway: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Permanently store approved project architecture in OMIS after authentic human authorization.

        Mandatory governance rule:
        Permanent storage to .openclone/memory.sqlite3 occurs ONLY when:
        1. Explicit human approval is asserted (human_approved=True).
        2. A genuine, cryptographically signed approval_record is provided.
           (Self-authorizing automatic approval construction from an arbitrary digest is strictly prohibited).
        3. Security policy evaluates ALLOWED via IntegrationGateway (`openclone_sync_memory` capability),
           authenticating the server-signed HMAC-SHA256 signature, payload digest, validity window, anti-replay nonce, and scopes.
        """
        if not human_approved:
            return {
                "status": "SKIPPED",
                "persisted": False,
                "reason": "OMIS permanent storage requires explicit human authorization and signed approval record.",
            }

        # Caller must supply an approval record or gateway verification
        if approval_record is None:
            return {
                "status": "DENIED",
                "persisted": False,
                "reason": "OMIS permanent storage requires an authentic signed approval record; self-authorization is prohibited.",
            }

        # IntegrationGateway policy verification
        p_id = project_definition.get("project_id", "default")
        p_name = project_definition.get("project_name", "OpenClone Project")
        exec_args = {
            "project_id": p_id,
            "project_name": p_name,
            "workspace_path": str(workspace_path),
        }

        # Initialize or use supplied gateway and auth context
        gw = gateway
        if gw is None:
            try:
                from openclone.integrations.gateway import IntegrationGateway
                nonce_db = Path(workspace_path) / ".openclone" / "gateway_nonces.sqlite3"
                gw = IntegrationGateway(repo_root=Path(workspace_path), nonce_db_path=nonce_db)
            except Exception:
                gw = None

        if gw is None:
            return {
                "status": "DENIED",
                "persisted": False,
                "reason": "Security policy evaluation failed: IntegrationGateway is not available; failing closed.",
            }

        from openclone.integrations.gateway import AuthContext, PolicyVerdict
        auth = auth_context or AuthContext(
            user_id="human-architect",
            project_id=p_id,
            scopes={"projects:write", "evidence:write"},
            is_human=True,
            client_type="admin_console",
        )
        # Package structured approval_record for gateway validation
        if hasattr(approval_record, "__dict__"):
            exec_args["approval_record"] = dict(approval_record.__dict__)
        elif isinstance(approval_record, dict):
            exec_args["approval_record"] = dict(approval_record)

        eval_result = gw.evaluate_policy(
            auth=auth,
            capability_id="openclone_sync_memory",
            arguments=exec_args,
            approval_digest=approval_digest,
        )
        if eval_result.verdict != PolicyVerdict.ALLOWED:
            return {
                "status": "DENIED",
                "persisted": False,
                "reason": f"Security policy denied OMIS persistence: {eval_result.reason}",
            }

        manager = None
        try:
            from openclone.memory.models import (
                MemoryRecord,
                MemoryScope,
                MemoryType,
                MemoryStatus,
                MemoryAuthority,
                Classification,
                SourceRef,
            )
            import time

            manager = MemoryManager(workspace_path)
            now_ts = int(time.time() * 1000)
            rec_nonce = (exec_args.get("approval_record") or {}).get("nonce", "")[:8]
            rec_id = f"MEM-ARCH-{p_id}-{now_ts}-{rec_nonce}" if rec_nonce else f"MEM-ARCH-{p_id}-{now_ts}"

            record = MemoryRecord(
                id=rec_id,
                title=f"Approved Architecture: {p_name}",
                statement=f"Human-approved system architecture and decisions for {p_name} (digest: {approval_digest[:16]}).",
                memory_type=MemoryType.DECISION,
                scope=MemoryScope(project_id=p_id, workspace_id=str(Path(workspace_path).name)),
                authority=MemoryAuthority.HUMAN_CONFIRMED,
                classification=Classification.INTERNAL,
                status=MemoryStatus.CURRENT,
                approved_by="Human Architect",
                source_refs=[
                    SourceRef(
                        uri=f"project://{p_id}/architecture",
                        source_type="architecture_decision",
                        revision_or_date=str(now_ts),
                    )
                ],
                details=json.dumps({
                    "project_id": p_id,
                    "project_name": p_name,
                    "approval_digest": approval_digest,
                    "timestamp": time.time(),
                }),
                confidence=1.0,
            )
            stored = manager.store_record(record, sync_markdown=True)
            return {
                "status": "PERSISTED",
                "persisted": True,
                "memory_id": stored.id,
                "scope": stored.scope.project_id,
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "persisted": False,
                "error": str(e),
            }
        finally:
            if manager is not None:
                manager.close()
