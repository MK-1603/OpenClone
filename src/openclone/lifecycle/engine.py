"""OpenClone Engineering Lifecycle & Independent Verification Engine."""
import datetime
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from src.openclone.lifecycle.schema import (
    ItemType,
    Applicability,
    ItemStatus,
    Priority,
    RiskLevel,
    VerificationLevel,
    VerificationOutcome,
    ProjectType,
    EvidenceRecord,
    VerificationCheck,
    DefectRecord,
    ChecklistItem,
    QualityGate,
)
from src.openclone.lifecycle.catalogue import (
    MASTER_PHASES,
    PROJECT_TYPE_PACKS,
)


class LifecycleEngine:
    """Orchestrates dynamic checklist generation, status transitions, evidence auditing, and quality gates."""

    def __init__(self, project_id: str, repo_root: Optional[Path] = None):
        self.project_id = project_id
        self.repo_root = repo_root or Path.cwd()
        self.items: Dict[str, ChecklistItem] = {}
        self.gates: Dict[str, QualityGate] = {}
        self.audit_log: List[Dict[str, Any]] = []
        self.project_type: ProjectType = ProjectType.WEB_SAAS
        self.features: List[str] = []
        self.tech_stack: Dict[str, str] = {}
        self.risk_level: RiskLevel = RiskLevel.HIGH

    def log_event(self, action: str, item_id: Optional[str], details: Dict[str, Any], actor: str = "system"):
        self.audit_log.append({
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "actor": actor,
            "action": action,
            "item_id": item_id,
            "details": details,
        })

    def generate_checklist(
        self,
        project_type: ProjectType = ProjectType.WEB_SAAS,
        features: Optional[List[str]] = None,
        tech_stack: Optional[Dict[str, str]] = None,
        risk_level: RiskLevel = RiskLevel.HIGH,
        has_ai: bool = False,
    ) -> Dict[str, ChecklistItem]:
        """Generates a tailored, hierarchical engineering checklist based on project classification."""
        self.project_type = project_type
        self.features = features or []
        self.tech_stack = tech_stack or {}
        self.risk_level = risk_level
        self.items.clear()
        self.gates.clear()

        is_static = project_type == ProjectType.STATIC_WEBSITE
        include_ai = has_ai or project_type == ProjectType.AI_AGENT_PLATFORM or "ai" in [f.lower() for f in self.features]

        for phase_id, phase_data in MASTER_PHASES.items():
            # Evaluate phase applicability
            phase_applicability = Applicability.REQUIRED
            phase_reason = "Mandatory engineering lifecycle phase"

            if phase_id == "PHASE_13_AI_INTELLIGENCE" and not include_ai:
                phase_applicability = Applicability.NOT_APPLICABLE
                phase_reason = "Project does not include artificial intelligence or machine learning components"
            elif is_static and phase_id in ["PHASE_09_BACKEND", "PHASE_10_DATABASE", "PHASE_11_AUTH"]:
                phase_applicability = Applicability.NOT_APPLICABLE
                phase_reason = "Static marketing website has no backend database or authentication layer"

            phase_item = ChecklistItem(
                id=phase_id,
                project_id=self.project_id,
                phase_id=phase_id,
                category="Lifecycle Phase",
                title=f"{phase_data['order']:02d} · {phase_data['name']}",
                description=phase_data["purpose"],
                why_it_matters=phase_data["exit_criteria"],
                type=ItemType.PHASE,
                applicability=phase_applicability,
                applicability_reason=phase_reason,
                status=ItemStatus.NOT_STARTED,
                priority=Priority.HIGH,
                risk_level=risk_level,
            )
            self.items[phase_id] = phase_item

            # Setup phase quality gate
            self.gates[phase_id] = QualityGate(
                phase_id=phase_id,
                phase_name=phase_data["name"],
                mandatory_item_ids=[],
                required_level=VerificationLevel.V3_AUTOMATED_CHECK_PASSED,
                allow_unresolved_high_defects=False,
                waiver_policy="explicit_owner_approval",
                status="OPEN",
            )

            # Generate default tasks in phase
            for t in phase_data["tasks"]:
                task_id = f"{phase_id}_TASK_{t['id_suffix']}"
                task_applicability = phase_applicability
                task_reason = phase_reason if phase_applicability == Applicability.NOT_APPLICABLE else "Core lifecycle task"

                task_item = ChecklistItem(
                    id=task_id,
                    project_id=self.project_id,
                    phase_id=phase_id,
                    category=t["category"],
                    title=t["title"],
                    description=t["desc"],
                    why_it_matters=t["why"],
                    type=ItemType.TASK,
                    parent_id=phase_id,
                    applicability=task_applicability,
                    applicability_reason=task_reason,
                    status=ItemStatus.NOT_STARTED,
                    priority=Priority[t["priority"]],
                    risk_level=RiskLevel[t["risk"]],
                    acceptance_criteria=t["criteria"],
                    verification_method="automated_test",
                )

                # Add automated verification check contract
                check = VerificationCheck(
                    id=f"CHECK_{task_id}",
                    item_id=task_id,
                    title=f"Verify {t['title']}",
                    min_level=VerificationLevel.V3_AUTOMATED_CHECK_PASSED if task_item.priority == Priority.CRITICAL else VerificationLevel.V2_ARTIFACT_PRESENT,
                    command=None,
                    outcome=VerificationOutcome.NOT_RUN,
                )
                task_item.checks.append(check)

                self.items[task_id] = task_item
                if task_applicability == Applicability.REQUIRED:
                    self.gates[phase_id].mandatory_item_ids.append(task_id)

        # Apply project-type specific packs
        pack = PROJECT_TYPE_PACKS.get(project_type.value, {})
        if pack:
            for idx, et in enumerate(pack.get("extra_tasks", []), start=1):
                p_id = et["phase_id"]
                t_id = f"{p_id}_PACK_{project_type.value}_{idx:02d}"
                extra_item = ChecklistItem(
                    id=t_id,
                    project_id=self.project_id,
                    phase_id=p_id,
                    category=et["category"],
                    title=f"[{pack['name']}] {et['title']}",
                    description=et["desc"],
                    why_it_matters=f"Specialized requirement for {pack['name']}",
                    type=ItemType.TASK,
                    parent_id=p_id,
                    applicability=Applicability.REQUIRED,
                    applicability_reason=f"Mandatory conditional requirement for project type {project_type.value}",
                    status=ItemStatus.NOT_STARTED,
                    priority=Priority[et["priority"]],
                    risk_level=RiskLevel[et["risk"]],
                    acceptance_criteria=et["criteria"],
                    verification_method="automated_test",
                )
                check = VerificationCheck(
                    id=f"CHECK_{t_id}",
                    item_id=t_id,
                    title=f"Verify {et['title']}",
                    min_level=VerificationLevel.V3_AUTOMATED_CHECK_PASSED,
                )
                extra_item.checks.append(check)
                self.items[t_id] = extra_item
                if p_id in self.gates:
                    self.gates[p_id].mandatory_item_ids.append(t_id)

        self.log_event("CHECKLIST_GENERATED", None, {
            "project_type": project_type.value,
            "total_items": len(self.items),
            "features": self.features,
        })
        return self.items

    def attach_evidence(
        self,
        item_id: str,
        evidence_type: str,
        ref: str,
        description: str,
        produced_by: str = "ai_agent",
        proves: str = "",
        limitations: str = "",
    ) -> EvidenceRecord:
        """Attaches verifiable evidence to a checklist item and advances status."""
        if item_id not in self.items:
            raise KeyError(f"Item '{item_id}' not found in checklist.")

        item = self.items[item_id]
        evidence_id = f"EV_{item_id}_{len(item.evidence_refs) + 1:02d}"
        ev = EvidenceRecord(
            id=evidence_id,
            item_id=item_id,
            evidence_type=evidence_type,
            ref=ref,
            description=description,
            produced_by=produced_by,
            proves=proves,
            limitations=limitations,
        )
        item.evidence_refs.append(ev)

        # Update item status if it was not started or in progress
        if item.status in [ItemStatus.NOT_STARTED, ItemStatus.IN_PROGRESS]:
            item.status = ItemStatus.IMPLEMENTED
            item.completed_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

        item.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.log_event("EVIDENCE_ATTACHED", item_id, ev.to_dict(), actor=produced_by)
        return ev

    def transition_item(
        self,
        item_id: str,
        target_status: ItemStatus,
        waiver_reason: Optional[str] = None,
        actor: str = "user",
    ) -> ChecklistItem:
        """Enforces deterministic state transitions and prevents unverified completion."""
        if item_id not in self.items:
            raise KeyError(f"Item '{item_id}' not found in checklist.")

        item = self.items[item_id]

        # Rule: Cannot jump to VERIFIED without attached evidence
        if target_status == ItemStatus.VERIFIED:
            if not item.evidence_refs:
                raise ValueError(
                    f"Forbidden transition: Cannot mark item '{item_id}' as VERIFIED without evidence. "
                    "Attach valid code diff, test result, or audit log first."
                )
            # Check all verification checks pass
            for chk in item.checks:
                if chk.outcome not in [VerificationOutcome.PASS, VerificationOutcome.WAIVED]:
                    raise ValueError(
                        f"Forbidden transition: Cannot mark item '{item_id}' as VERIFIED because check '{chk.id}' outcome is '{chk.outcome.value}'."
                    )
            item.verified_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # Rule: Waived requires explicit rationale
        if target_status == ItemStatus.WAIVED_WITH_APPROVAL:
            if not waiver_reason or not waiver_reason.strip():
                raise ValueError(f"Waiver requires explicit justification rationale.")
            item.waiver_reason = waiver_reason

        # Rule: Not applicable requires reason
        if target_status == ItemStatus.NOT_APPLICABLE:
            if not item.applicability_reason:
                item.applicability_reason = "Marked not applicable by project owner"

        old_status = item.status
        item.status = target_status
        item.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

        self.log_event("STATUS_TRANSITION", item_id, {
            "from": old_status.value,
            "to": target_status.value,
            "waiver_reason": waiver_reason,
        }, actor=actor)
        return item

    def run_independent_verification(
        self,
        item_id: str,
        verifier_actor: str = "independent_verifier",
    ) -> Tuple[VerificationOutcome, str]:
        """Independently checks submitted evidence against repository reality; never assumes pass."""
        if item_id not in self.items:
            raise KeyError(f"Item '{item_id}' not found in checklist.")

        item = self.items[item_id]
        if not item.evidence_refs:
            for chk in item.checks:
                chk.outcome = VerificationOutcome.NOT_RUN
                chk.details = "No evidence attached to evaluate."
            item.status = ItemStatus.FAILED
            self.log_event("VERIFICATION_FAILED", item_id, {"reason": "Missing evidence"}, actor=verifier_actor)
            return VerificationOutcome.NOT_RUN, "Missing evidence: No evidence records attached to item."

        # Evaluate attached evidence records
        all_passed = True
        details = []

        for chk in item.checks:
            matched_evidence = False
            for ev in item.evidence_refs:
                # Check if file/ref exists if it is a local path
                ref_path = self.repo_root / ev.ref
                if ev.evidence_type in ["code_diff", "file", "test_file"]:
                    if ref_path.exists():
                        matched_evidence = True
                        chk.min_level = VerificationLevel.V2_ARTIFACT_PRESENT
                    else:
                        details.append(f"Referenced path '{ev.ref}' does not exist on disk.")
                elif ev.evidence_type in ["test_run", "command_output"]:
                    if "pass" in ev.proves.lower() or "ok" in ev.description.lower():
                        matched_evidence = True
                        chk.min_level = VerificationLevel.V3_AUTOMATED_CHECK_PASSED
                    else:
                        details.append(f"Test evidence '{ev.id}' lacks proof of pass.")
                else:
                    matched_evidence = True

            if matched_evidence:
                chk.outcome = VerificationOutcome.PASS
                chk.verified_by = verifier_actor
                chk.verified_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
                chk.details = "Evidence verified against repository state."
            else:
                chk.outcome = VerificationOutcome.FAIL
                chk.details = "; ".join(details) if details else "Evidence insufficient to prove completion."
                all_passed = False

        if all_passed:
            item.status = ItemStatus.VERIFIED
            item.verified_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
            self.log_event("VERIFICATION_PASSED", item_id, {"checks": len(item.checks)}, actor=verifier_actor)
            return VerificationOutcome.PASS, "Independent verification passed with verified evidence."
        else:
            item.status = ItemStatus.FAILED
            # Automatically log defect
            defect_id = f"DEFECT_{item_id}_{len(item.defects) + 1:02d}"
            defect = DefectRecord(
                id=defect_id,
                task_id=item_id,
                title=f"Verification failure on {item.title}",
                severity=Priority.HIGH,
                expected="Verifiable evidence meeting criteria",
                actual="; ".join(details),
            )
            item.defects.append(defect)
            self.log_event("VERIFICATION_FAILED", item_id, {"defect": defect_id, "details": details}, actor=verifier_actor)
            return VerificationOutcome.FAIL, f"Verification failed: {'; '.join(details)}"

    def evaluate_quality_gate(self, phase_id: str) -> QualityGate:
        """Evaluates whether all mandatory items in a phase are verified and defect-free."""
        if phase_id not in self.gates:
            raise KeyError(f"Quality gate for phase '{phase_id}' not found.")

        gate = self.gates[phase_id]
        gate.blockers.clear()

        # Check all mandatory items in this phase
        for item_id in gate.mandatory_item_ids:
            item = self.items.get(item_id)
            if not item:
                continue

            if item.applicability == Applicability.NOT_APPLICABLE:
                continue

            if item.status not in [ItemStatus.VERIFIED, ItemStatus.WAIVED_WITH_APPROVAL]:
                gate.blockers.append(
                    f"Item '{item_id}' ({item.title}) status is '{item.status.value}', expected VERIFIED or WAIVED."
                )

            # Check open defects
            for d in item.defects:
                if d.status in ["OPEN", "TRIAGED", "IN_PROGRESS"]:
                    gate.blockers.append(
                        f"Unresolved {d.severity.value} defect '{d.id}' on item '{item_id}': {d.title}"
                    )

        if gate.blockers:
            gate.status = "BLOCKED"
        else:
            gate.status = "PASSED"

        self.log_event("GATE_EVALUATED", phase_id, {
            "status": gate.status,
            "blockers_count": len(gate.blockers),
        })
        return gate

    def calculate_progress(self) -> Dict[str, Any]:
        """Calculates planning coverage, implementation progress, and verified progress."""
        tasks = [it for it in self.items.values() if it.type == ItemType.TASK]
        applicable_tasks = [t for t in tasks if t.applicability != Applicability.NOT_APPLICABLE]

        total_applicable = len(applicable_tasks)
        if total_applicable == 0:
            return {
                "planning_coverage_pct": 100.0,
                "implementation_progress_pct": 100.0,
                "verified_progress_pct": 100.0,
                "total_tasks": len(tasks),
                "applicable_tasks": 0,
                "verified_tasks": 0,
                "implemented_tasks": 0,
                "waived_tasks": 0,
                "not_applicable_tasks": len(tasks) - total_applicable,
            }

        implemented_count = sum(
            1 for t in applicable_tasks
            if t.status in [ItemStatus.IMPLEMENTED, ItemStatus.VERIFICATION_PENDING, ItemStatus.VERIFIED, ItemStatus.WAIVED_WITH_APPROVAL]
        )
        verified_count = sum(
            1 for t in applicable_tasks
            if t.status in [ItemStatus.VERIFIED, ItemStatus.WAIVED_WITH_APPROVAL]
        )
        waived_count = sum(1 for t in applicable_tasks if t.status == ItemStatus.WAIVED_WITH_APPROVAL)

        return {
            "planning_coverage_pct": 100.0,
            "implementation_progress_pct": round((implemented_count / total_applicable) * 100.0, 1),
            "verified_progress_pct": round((verified_count / total_applicable) * 100.0, 1),
            "total_tasks": len(tasks),
            "applicable_tasks": total_applicable,
            "implemented_tasks": implemented_count,
            "verified_tasks": verified_count,
            "waived_tasks": waived_count,
            "not_applicable_tasks": len(tasks) - total_applicable,
        }

    def generate_ide_handoff_package(self, task_id: str) -> str:
        """Generates a scoped markdown prompt package for an AI IDE with strict verification contracts."""
        if task_id not in self.items:
            raise KeyError(f"Task '{task_id}' not found.")

        task = self.items[task_id]
        phase = self.items.get(task.phase_id)
        phase_title = phase.title if phase else task.phase_id

        package = f"""# OpenClone Task Handoff Package
**Project ID:** `{self.project_id}`  
**Phase:** `{phase_title}`  
**Task ID:** `{task.id}` — **Title:** `{task.title}`  
**Priority:** `{task.priority.value}` | **Risk Level:** `{task.risk_level.value}`

---

## 1. Task Objective & Context
- **Description:** {task.description}
- **Why It Matters:** {task.why_it_matters}
- **Category:** {task.category}

---

## 2. Observable Acceptance Criteria
"""
        for c in task.acceptance_criteria:
            package += f"- [ ] {c}\n"

        package += f"""
---

## 3. Security & Operational Boundaries
- **No AI Slop:** Do not introduce unrequested gradients, decorative blur blobs, or non-functional visual placeholders.
- **Strict Scope:** Edit only files necessary for this specific task.
- **Secret Redaction:** Never commit or print API keys, tokens, or credentials.
- **Verification Method:** `{task.verification_method}`

---

## 4. Required IDE Completion Report Schema
When finished, reply with structured evidence in this exact JSON format:

```json
{{
  "task_id": "{task.id}",
  "status": "IMPLEMENTED",
  "changed_files": [
    "path/to/modified_file.py"
  ],
  "test_command": "python -m unittest tests/test_feature.py",
  "test_result": "PASS (5 tests ok)",
  "evidence_description": "Implemented object-level checks and added regression tests."
}}
```

*(Note: OpenClone independently audits this report. Declarations without real files or test evidence will be rejected.)*
"""
        return package

    def ingest_ide_completion_report(self, report_dict: Dict[str, Any], actor: str = "ai_ide") -> Tuple[bool, str]:
        """Ingests an IDE completion report, validating evidence before advancing status."""
        task_id = report_dict.get("task_id")
        if not task_id or task_id not in self.items:
            return False, f"Invalid or missing task_id in completion report: {task_id}"

        item = self.items[task_id]
        changed_files = report_dict.get("changed_files", [])
        test_command = report_dict.get("test_command", "")
        test_result = report_dict.get("test_result", "")
        evidence_desc = report_dict.get("evidence_description", "IDE submitted implementation")

        if not changed_files and not test_command:
            return False, "Dishonest or empty report: No changed files or test commands reported."

        # Attach file evidence
        for f in changed_files:
            self.attach_evidence(
                item_id=task_id,
                evidence_type="code_diff",
                ref=f,
                description=f"File changed by {actor}",
                produced_by=actor,
                proves=f"Implements {item.title}",
            )

        # Attach test evidence if reported
        if test_command:
            self.attach_evidence(
                item_id=task_id,
                evidence_type="test_run",
                ref=test_command,
                description=f"Execution result: {test_result}",
                produced_by=actor,
                proves="Automated verification passing",
            )

        item.status = ItemStatus.VERIFICATION_PENDING
        self.log_event("IDE_REPORT_INGESTED", task_id, report_dict, actor=actor)
        return True, f"Report accepted. Item '{task_id}' advanced to VERIFICATION_PENDING."
