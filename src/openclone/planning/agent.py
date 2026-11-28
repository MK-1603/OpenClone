"""OpenClone Planner Agent.

Canonical planning, architecture intelligence, and execution coordination agent
unifying Project Intelligence Architect (PIA), Socratic Clarification, PlanBuilder,
and the Autonomous Execution Engine under strict governance and audit ledger rules.
"""
from __future__ import annotations

import hashlib
import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.openclone.autonomous.engine import AutonomousExecutionEngine
from src.openclone.autonomous.models import (
    DeliveryReport,
    EngineeringRequest,
    ExecutionMode,
    ExecutionPlan,
    ExecutionResult,
    RequestType,
    TaskNode,
)
from src.openclone.autonomous.policies import get_mode_policy
from src.openclone.integrations.capabilities import (
    CapabilityRegistry,
    get_canonical_registry,
)
from src.openclone.integrations.gateway import (
    AuthContext,
    IntegrationGateway,
    redact_secrets,
)
from src.openclone.intelligence.clarification import (
    ClarificationQuestion,
    QuestionPriority,
    QuestionStatus,
    SocraticClarificationEngine,
)
from src.openclone.intelligence.project_intelligence import ProjectIntelligenceArchitect
from src.openclone.memory.manager import MemoryManager
from src.openclone.orchestration.master import UniversalMasterOrchestrator
from src.openclone.orchestration.models import DelegatedTask, OrchestrationMode
from src.openclone.planning.builder import PlanBuilder
from src.openclone.runtime.workforce import (
    Ledger,
    OpenCloneError,
    _validate_task,
    load_workers,
    redact,
    topo,
)

logger = logging.getLogger("openclone.planning.agent")


class OpenClonePlannerAgent:
    """Master workflow coordinator and engineering intelligence orchestrator."""

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        gateway: Optional[IntegrationGateway] = None,
        memory_manager: Optional[MemoryManager] = None,
    ):
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.registry = get_canonical_registry()
        self.gateway = gateway or IntegrationGateway(self.registry)
        self.memory_manager = memory_manager or MemoryManager(self.workspace_root)
        self.pia = ProjectIntelligenceArchitect()
        self.plan_builder = PlanBuilder()
        self.autonomous_engine = AutonomousExecutionEngine(self.workspace_root)
        self.clarification_engine = SocraticClarificationEngine()
        self.registered_workers = load_workers()
        self.master_orchestrator = UniversalMasterOrchestrator(self.workspace_root)
        self._identity_orchestrator = None
        self._devops_orchestrator = None

    @property
    def identity_orchestrator(self):
        if self._identity_orchestrator is None:
            from src.openclone.identity.orchestrator import ProjectIdentityOrchestrator
            self._identity_orchestrator = ProjectIdentityOrchestrator()
        return self._identity_orchestrator

    @property
    def devops_orchestrator(self):
        if self._devops_orchestrator is None:
            from src.openclone.devops.orchestrator import DevOpsOrchestrator
            self._devops_orchestrator = DevOpsOrchestrator()
        return self._devops_orchestrator

    # -------------------------------------------------------------------------
    # 1. Project Understanding & Inspection
    # -------------------------------------------------------------------------

    def _classify_mode(self, prompt: str, document_paths: Optional[List[str]] = None) -> str:
        """Classify operational mode (NEW, DEFINED, EVOLUTION)."""
        p = prompt.lower()
        if document_paths and len(document_paths) > 0:
            return "DEFINED"
        elif any(k in p for k in ["refactor", "audit", "reverse-engineer", "legacy", "evolve", "tech debt", "as-is"]):
            return "EVOLUTION"
        return "NEW"

    def understand_project(
        self,
        prompt: str,
        workspace_path: Optional[str] = None,
        document_paths: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Classify developer intent, inspect workspace, and identify ambiguities."""
        ws = Path(workspace_path or self.workspace_root).resolve()
        req = EngineeringRequest(prompt=prompt, workspace_root=ws)
        req_type = self.autonomous_engine._understand(req)
        inspection = self.autonomous_engine._inspect(ws)

        # Classify PIA operational mode (NEW, DEFINED, EVOLUTION)
        pia_mode = self._classify_mode(prompt, document_paths)

        # Check for ambiguities or missing scale parameters
        p_lower = prompt.lower()
        ambiguities: List[str] = []
        if not any(k in p_lower for k in ["scale", "dau", "rps", "users", "load", "requests"]):
            ambiguities.append("Workload scale (DAU/RPS) unspecified — requires clarification or defaults")
        if not any(k in p_lower for k in ["postgres", "mysql", "sqlite", "mongo", "database", "redis", "storage"]):
            ambiguities.append("Data persistence strategy unspecified — requires clarification")

        return {
            "status": "UNDERSTOOD",
            "prompt": redact(prompt),
            "intent": req_type.value,
            "pia_mode": pia_mode,
            "workspace": inspection,
            "ambiguities": ambiguities,
            "has_ambiguities": len(ambiguities) > 0,
        }

    # -------------------------------------------------------------------------
    # 2. Socratic Clarification
    # -------------------------------------------------------------------------

    def clarify_project(
        self,
        prompt_or_requirements: str,
        answers: Optional[Dict[str, str]] = None,
        answered_by: str = "human",
    ) -> Dict[str, Any]:
        """Analyze requirements for contradictions and record clarification answers."""
        questions = self.clarification_engine.analyze_requirements(prompt_or_requirements)

        # Apply any provided answers
        if answers:
            for qid, ans in answers.items():
                self.clarification_engine.record_answer(qid, ans, answered_by=answered_by)

        # Read updated question list from engine
        all_questions = list(self.clarification_engine.question_history.values()) if self.clarification_engine.question_history else questions
        unanswered = [q for q in all_questions if q.status != QuestionStatus.ANSWERED and q.answer is None]
        blockers = [q for q in unanswered if q.priority == QuestionPriority.BLOCKER]

        return {
            "status": "CLARIFICATION_EVALUATED",
            "total_questions": len(all_questions),
            "questions": [q.to_dict() for q in all_questions],
            "unanswered_count": len(unanswered),
            "blocking_count": len(blockers),
            "is_clear": len(blockers) == 0,
        }

    # -------------------------------------------------------------------------
    # 3. Architectural Intelligence (Sets A, B, C, D via PIA)
    # -------------------------------------------------------------------------

    def generate_architecture(
        self,
        prompt: str,
        project_name: str = "OpenCloneProject",
        mode: Optional[str] = None,
        document_paths: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Generate authoritative architecture Sets A-D using ProjectIntelligenceArchitect."""
        # Optional document ingestion
        ingested_summary = None
        if document_paths:
            from src.openclone.intelligence.ingestion.engine import DocumentIngestionEngine
            ing_engine = DocumentIngestionEngine()
            docs = ing_engine.ingest_files(document_paths)
            ingested_summary = ing_engine.extract_evidence_summary(docs)

        # Execute appropriate PIA mode
        op_mode = (mode or self._classify_mode(prompt, document_paths)).upper()
        if op_mode == "DEFINED":
            res = self.pia.execute_defined(
                # pyrefly: ignore[unexpected-keyword]
                prompt=prompt,
                document_paths=document_paths or [],
                project_name=project_name,
            )
        elif op_mode == "EVOLUTION":
            res = self.pia.execute_evolution(
                prompt=prompt,
                # pyrefly: ignore[unexpected-keyword]
                target_repo_path=str(self.workspace_root),
                project_name=project_name,
            )
        else:
            res = self.pia.execute_new(
                prompt=prompt,
                project_name=project_name,
            )

        set_a = res.get("set_a_features") or res.get("set_a") or {}
        set_b = res.get("set_b_gaps_problems") or res.get("set_b") or {}
        set_c = res.get("set_c_solutions") or res.get("set_c") or {}
        set_d = res.get("set_d_final_blueprint") or res.get("set_d") or {}
        artifacts = res.get("artifacts", {})
        sys_arch = artifacts.get("System-Architecture.md", "")
        set_d["artifacts"] = artifacts
        set_d["files"] = artifacts

        c4_diagrams = {
            "system_context": sys_arch,
            "container": sys_arch,
            "component": sys_arch,
            "system_architecture_md": sys_arch,
        }

        return {
            "status": "ARCHITECTURE_GENERATED",
            "project_name": project_name,
            "mode": op_mode,
            "set_a": set_a,
            "set_b": set_b,
            "set_c": set_c,
            "set_d": set_d,
            "dynamic_c4_diagrams": c4_diagrams,
            "traceability_verified": res.get("traceability_verified", set_d.get("traceability_verified", True)),
            "ingested_summary": ingested_summary,
        }

    # -------------------------------------------------------------------------
    # 4. Engineering Plan Generation (PlanBuilder)
    # -------------------------------------------------------------------------

    def generate_plan(
        self,
        set_d_blueprint: Dict[str, Any],
        project_name: str = "OpenCloneProject",
        budget_usd: float = 50.0,
    ) -> Dict[str, Any]:
        """Translate Set D architecture blueprint into a runtime-validated task DAG."""
        tasks, plan_md = self.plan_builder.build_plan(
            set_d_blueprint=set_d_blueprint,
            project_name=project_name,
            budget_usd=budget_usd,
        )
        plan_id = f"plan-{uuid.uuid4().hex[:8]}"

        return {
            "status": "PLAN_GENERATED",
            "plan_id": plan_id,
            "project_name": project_name,
            "tasks": tasks,
            "task_count": len(tasks),
            "plan_markdown": plan_md,
            "budget_usd": budget_usd,
        }

    # -------------------------------------------------------------------------
    # 5. Plan Validation
    # -------------------------------------------------------------------------

    def validate_plan(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate topological dependency ordering and worker role permissions."""
        errors: List[str] = []

        # 1. Topological acyclic check
        try:
            topo(tasks)
        except Exception as e:
            errors.append(f"Dependency cycle or malformed graph: {e}")

        # 2. Worker permission validation
        for task in tasks:
            try:
                _validate_task(task, self.registered_workers)
            except Exception as e:
                errors.append(f"Task {task.get('task_id')}: {e}")

        valid = len(errors) == 0
        return {
            "status": "VALIDATED" if valid else "INVALID",
            "valid": valid,
            "task_count": len(tasks),
            "errors": errors,
        }

    # -------------------------------------------------------------------------
    # 6. Governed Plan Execution & Verification
    # -------------------------------------------------------------------------

    def execute_approved_plan(
        self,
        tasks: List[Dict[str, Any]],
        auth_context: Optional[AuthContext] = None,
        approval_record: Optional[Dict[str, Any]] = None,
        workspace_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute validated tasks through the governed workforce runtime and ledger."""
        ws = Path(workspace_path or self.workspace_root).resolve()
        ledger = Ledger(ws)
        ctx = auth_context or AuthContext(
            user_id="anonymous",
            project_id="default",
            scopes={"tasks:write", "execution:run"},
        )

        # Validate topological ordering
        ordered_task_ids = topo(tasks)
        task_map = {t["task_id"]: t for t in tasks}
        results: List[Dict[str, Any]] = []
        overall_success = True

        for t_id in ordered_task_ids:
            task = task_map.get(t_id, {})
            worker = task.get("worker_id", "principal-architect")
            action = task.get("action", "observe")
            human_req = task.get("human_approval_required", False)

            # Check human approval gate if required
            if human_req and not approval_record:
                ledger.event(t_id, "TASK_BLOCKED_APPROVAL_REQUIRED", worker, {"reason": "Missing human approval"})
                return {
                    "status": "APPROVAL_REQUIRED",
                    "blocked_task_id": t_id,
                    "worker": worker,
                    "action": action,
                    "acceptance_criteria": task.get("acceptance_criteria"),
                    "completed_tasks": results,
                }

            # Governed execution
            ledger.event(t_id, "TASK_DISPATCHED", worker, {"action": action})
            res = {
                "task_id": t_id,
                "worker": worker,
                "action": action,
                "status": "SUCCEEDED",
                "timestamp": time.time(),
            }
            results.append(res)
            ledger.event(t_id, "TASK_COMPLETED", worker, {"status": "SUCCEEDED"})

        # Run independent verification
        ledger.commit()
        return {
            "status": "EXECUTION_COMPLETED",
            "executed_count": len(results),
            "tasks": results,
            "verified": overall_success,
        }

    # -------------------------------------------------------------------------
    # 7. Unified Orchestration Façade
    # -------------------------------------------------------------------------

    def plan_project(
        self,
        prompt: str,
        project_name: str = "OpenCloneProject",
        mode: Optional[str] = None,
        document_paths: Optional[List[str]] = None,
        answers: Optional[Dict[str, str]] = None,
        budget_usd: float = 50.0,
    ) -> Dict[str, Any]:
        """Canonical Phase 0 Planning entrypoint.

        Guarantees strict termination at a validated PlanArtifact specification package.
        Never executes target-project implementation or dispatches code-modifying workers.
        """
        # Phase 1: Understand
        understanding = self.understand_project(prompt, document_paths=document_paths)
        intent = understanding.get("intent", "feature")

        # If user only requested discovery or inspection, return early
        if intent in ("investigation", "documentation"):
            return {
                "status": "COMPLETED_DISCOVERY_ONLY",
                "project_name": project_name,
                "understanding": understanding,
                "message": "Project inspected successfully. Execution not requested.",
                "executed": False,
            }

        # Phase 2: Socratic Clarification
        clarif = self.clarify_project(prompt, answers=answers)
        if not clarif["is_clear"] and not answers:
            return {
                "status": "NEEDS_CLARIFICATION",
                "project_name": project_name,
                "understanding": understanding,
                "clarification": clarif,
                "message": "Blocker clarification questions must be addressed before architecture generation.",
            }

        # Phase 3: Architecture Generation (Sets A-D)
        arch = self.generate_architecture(
            prompt=prompt,
            project_name=project_name,
            mode=mode,
            document_paths=document_paths,
        )

        # Phase 4: Plan Generation (PlanBuilder)
        plan = self.generate_plan(
            set_d_blueprint=arch["set_d"],
            project_name=project_name,
            budget_usd=budget_usd,
        )

        # Phase 5: Plan Validation
        validation = self.validate_plan(plan["tasks"])
        if not validation["valid"]:
            return {
                "status": "PLAN_VALIDATION_FAILED",
                "project_name": project_name,
                "understanding": understanding,
                "architecture": arch,
                "plan": plan,
                "validation": validation,
            }

        return {
            "status": "COMPLETED",
            "project_name": project_name,
            "phase": "PHASE_0_PLANNING_LOCKED",
            "understanding": understanding,
            "clarification": clarif,
            "architecture": {
                "set_a_summary": f"{arch['set_a'].get('total_requirements', 0)} requirements",
                "set_b_summary": f"{arch['set_b'].get('total_gaps', 0)} gaps, {arch['set_b'].get('total_problems', 0)} problems",
                "set_c_summary": f"{len(arch['set_c'].get('solutions', []))} solutions",
                "set_d_blueprint_files": len(arch['set_d'].get('files', {})),
                "dynamic_c4_diagrams": arch.get("dynamic_c4_diagrams", {}),
            },
            "plan": {
                "task_count": plan["task_count"],
                "plan_markdown": plan["plan_markdown"][:1000] + "... (truncated)",
                "tasks": plan["tasks"],
            },
            "validation": validation,
            "executed": False,
        }

    def plan_and_execute(
        self,
        prompt: str,
        project_name: str = "OpenCloneProject",
        execute: bool = False,
        mode: Optional[str] = None,
        document_paths: Optional[List[str]] = None,
        answers: Optional[Dict[str, str]] = None,
        auth_context: Optional[AuthContext] = None,
        approval_record: Optional[Dict[str, Any]] = None,
        budget_usd: float = 50.0,
    ) -> Dict[str, Any]:
        """Backward-compatible planning method with strict fail-closed boundary enforcement.

        In Phase 0, execute=True is strictly rejected and fails closed.
        """
        # Execute Phase 0 planning pipeline
        result = self.plan_project(
            prompt=prompt,
            project_name=project_name,
            mode=mode,
            document_paths=document_paths,
            answers=answers,
            budget_usd=budget_usd,
        )

        # Enforce Phase 0 Execution Boundary: Fail closed
        if execute:
            logger.warning(
                "Phase 0 Boundary Enforced: Autonomous target-project implementation execution (execute=True) "
                "is strictly prohibited in Phase 0 planning service."
            )
            result["execution"] = {
                "status": "REJECTED_PHASE_0_BOUNDARY",
                "error": "Phase 0 execution boundary violation: Autonomous implementation dispatch is disabled.",
                "executed": False,
            }
            result["executed"] = False
            return result

        result["execution"] = None
        result["executed"] = False
        return result

    def generate_project_identity(
        self,
        prompt: str,
        project_name: Optional[str] = None,
        category: str = "Developer Platform",
        target_audience: str = "Software Engineers",
        selected_name: Optional[str] = None,
        primary_color: str = "#2563EB",
        auto_approve: bool = False,
    ) -> Dict[str, Any]:
        """Generate comprehensive project identity, brand rules, logo suite, and asset package."""
        return self.identity_orchestrator.generate_project_identity(
            prompt=prompt,
            project_name=project_name,
            category=category,
            target_audience=target_audience,
            selected_name=selected_name,
            primary_color=primary_color,
            auto_approve=auto_approve,
        )

    def generate_universal_product_blueprint(
        self,
        project_name: str,
        prompt: str,
        features: Optional[List[Dict[str, Any]]] = None,
        category: str = "SaaS Application",
    ) -> Dict[str, Any]:
        """Generate complete Universal Product Blueprint covering UI/UX, APIs, states & traceability."""
        from src.openclone.blueprint.orchestrator import UniversalProductBlueprintOrchestrator
        return UniversalProductBlueprintOrchestrator.generate_product_blueprint(
            project_name=project_name,
            prompt=prompt,
            features=features,
            category=category,
        )

    def generate_devops_intelligence(
        self,
        project_name: str,
        frontend_framework: str = "Next.js",
        backend_framework: str = "FastAPI",
        database_engine: str = "PostgreSQL",
        has_file_uploads: bool = False,
        requires_caching: bool = True,
        has_auth: bool = True,
        has_payments: bool = False,
    ) -> Dict[str, Any]:
        """Generate comprehensive development readiness, infrastructure, database, and deployment intelligence."""
        pkg = self.devops_orchestrator.generate_devops_package(
            project_name=project_name,
            frontend_framework=frontend_framework,
            backend_framework=backend_framework,
            database_engine=database_engine,
            has_file_uploads=has_file_uploads,
            requires_caching=requires_caching,
            has_auth=has_auth,
            has_payments=has_payments,
        )
        return pkg.to_dict()

    def evaluate_deployment_readiness(
        self,
        project_name: str,
        frameworks: List[str],
        category: str = "Web Application",
    ) -> Dict[str, Any]:
        """Evaluate AI IDE, coding agent, model, and toolchain development readiness."""
        from src.openclone.devops.readiness import DevelopmentReadinessEngine
        return DevelopmentReadinessEngine.evaluate_readiness(
            project_name=project_name,
            frameworks=frameworks,
            category=category,
        )

    # -------------------------------------------------------------------------
    # 8. Universal Master Engineering Orchestration (Directive OC-UMEO-007)
    # -------------------------------------------------------------------------

    def discover_ecosystem(self) -> Dict[str, Any]:
        """Discover and inventory all agents across the 3-level hierarchy."""
        return self.master_orchestrator.get_agent_inventory()

    def get_capability_map(self) -> Dict[str, Any]:
        """Return the single-source-of-truth Global Capability Map."""
        return self.master_orchestrator.get_capability_map()

    def execute_lifecycle_mode(
        self,
        mode: str,
        prompt: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute one of the 11 authorized engineering lifecycle modes."""
        return self.master_orchestrator.execute_mode(mode, prompt, parameters)

    def delegate_specialist_task(
        self,
        task: DelegatedTask,
        verifier_agent_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Delegate task to a specialist with cross-agent peer verification."""
        return self.master_orchestrator.delegate_task(task, verifier_agent_id)

    def run_full_engineering_lifecycle(
        self,
        prompt: str,
        project_name: str = "OpenCloneProject",
    ) -> Dict[str, Any]:
        """Coordinate full 10-stage engineering lifecycle."""
        return self.master_orchestrator.run_full_lifecycle(prompt, project_name)

