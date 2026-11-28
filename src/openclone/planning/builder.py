"""OpenClone Implementation Plan Builder.

Translates approved Set D blueprints and architecture specifications into
runtime-compliant tasks.json and ENGINEERING-PLAN.md DAGs.
"""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple

from src.openclone.engineering.roles import EngineeringRoleRegistry
from src.openclone.runtime.workforce import _validate_task, load_workers, topo


class PlanBuilder:
    """Builds and validates DAG execution plans matching the workforce runtime schema."""

    def __init__(self, registered_workers: Optional[Dict[str, Any]] = None):
        self.workers = registered_workers or load_workers()

    def build_plan(
        self,
        set_d_blueprint: Dict[str, Any],
        project_name: str = "OpenCloneProject",
        budget_usd: float = 50.0,
    ) -> Tuple[List[Dict[str, Any]], str]:
        """Convert Set D blueprint into runtime-validated tasks.json and ENGINEERING-PLAN.md."""
        features = set_d_blueprint.get("feature_catalogue", [])
        solutions = set_d_blueprint.get("solutions", [])
        tasks: List[Dict[str, Any]] = []

        # 1. Phase 1 Inception Gate (Gate A)
        tasks.append({
            "task_id": "PHASE-01-START",
            "title": f"Phase 1 Inception Approval Gate for {project_name}",
            "worker_id": "principal-architect",
            "action": "propose",
            "depends_on": [],
            "acceptance_criteria": "Formal cryptographic approval of Set D target blueprint and architecture decisions",
            "human_approval_required": True,
            "budget_usd": 0.0,
            "estimated_cost_usd": 0.0,
        })

        # 2. Project Repository Scaffold
        tasks.append({
            "task_id": "TASK-01-SCAFFOLD",
            "title": "Initialize Repository Scaffold and Core Dependencies",
            "worker_id": "backend-engineer",
            "action": "write",
            "depends_on": ["PHASE-01-START"],
            "acceptance_criteria": "Project directory initialized with pyproject.toml, package manifests, and environment boundaries",
            "human_approval_required": True,
            "budget_usd": round(budget_usd * 0.1, 2),
            "estimated_cost_usd": round(budget_usd * 0.05, 2),
        })

        last_task_id = "TASK-01-SCAFFOLD"
        feature_task_ids: List[str] = []

        # 3. Translate Features and Solutions into Engineering Tasks
        task_idx = 2
        for f in features:
            f_id = f.get("feature_id", f"FEAT-{task_idx:03d}")
            f_title = f.get("title", f"Feature {task_idx}")
            f_cat = f.get("category", "essential").lower()

            # Dynamic domain-aware workforce worker matching
            matched_worker = EngineeringRoleRegistry().match_role_for_task(f_title)
            worker_id = matched_worker if matched_worker in self.workers else ("frontend-engineer" if "ui" in f_title.lower() or "frontend" in f_title.lower() else "backend-engineer")
            clean_name = re.sub(r"[^A-Za-z0-9]", "-", f_title.upper())[:24].strip("-")
            t_id = f"TASK-{task_idx:02d}-{clean_name}"

            # Lookup matching acceptance criteria
            matching_sol = next((s for s in solutions if f_id in s.get("dependencies", [])), None)
            ac = matching_sol.get("acceptance_criteria", [f"Verified implementation of {f_title}"])[0] if matching_sol else f"Verified implementation of {f_title}"

            tasks.append({
                "task_id": t_id,
                "title": f"Implement {f_title} ({f_id})",
                "worker_id": worker_id,
                "action": "write",
                "depends_on": [last_task_id],
                "acceptance_criteria": ac,
                "human_approval_required": True,
                "budget_usd": round(budget_usd * 0.15, 2),
                "estimated_cost_usd": round(budget_usd * 0.08, 2),
            })
            last_task_id = t_id
            feature_task_ids.append(t_id)
            task_idx += 1

        # 4. Automated Test Verification Task
        verify_task_id = f"TASK-{task_idx:02d}-TEST-VERIFICATION"
        tasks.append({
            "task_id": verify_task_id,
            "title": "Execute Automated Test Verification and Regression Harness",
            "worker_id": "automation-test-engineer",
            "action": "execute",
            "command": ["pytest", "tests/", "-v"],
            "timeout_s": 300,
            "cwd": ".",
            "depends_on": feature_task_ids if feature_task_ids else ["TASK-01-SCAFFOLD"],
            "acceptance_criteria": "All unit, integration, and security regression tests pass with zero failures",
            "human_approval_required": True,
            "budget_usd": round(budget_usd * 0.1, 2),
            "estimated_cost_usd": round(budget_usd * 0.02, 2),
        })

        # 5. Phase 1 Completion Gate (Gate B)
        tasks.append({
            "task_id": "PHASE-01-COMPLETION",
            "title": f"Phase 1 Completion Acceptance Gate for {project_name}",
            "worker_id": "principal-architect",
            "action": "observe",
            "depends_on": [verify_task_id],
            "acceptance_criteria": "All child engineering tasks succeeded, verified test evidence recorded, milestone accepted by human authority",
            "human_approval_required": True,
            "budget_usd": 0.0,
            "estimated_cost_usd": 0.0,
        })

        # Validate every task against actual workforce runtime schema
        for t in tasks:
            _validate_task(t, self.workers)

        # Validate DAG acyclicity and compute order
        execution_order = topo(tasks)

        # Generate ENGINEERING-PLAN.md
        plan_md = self._render_engineering_plan(project_name, tasks, execution_order)

        return tasks, plan_md

    def _render_engineering_plan(
        self,
        project_name: str,
        tasks: List[Dict[str, Any]],
        order: List[str],
    ) -> str:
        """Render formal Markdown representation of the execution plan."""
        lines = [
            f"# ENGINEERING IMPLEMENTATION PLAN — {project_name}",
            "",
            "## 1. Plan Overview & Governance",
            "- **Runtime Engine:** OpenClone Workforce Runtime (`src/openclone/runtime/workforce.py`)",
            f"- **Total Tasks:** {len(tasks)}",
            f"- **Execution Topology:** {' -> '.join(order)}",
            "- **Phase Governance:** Two-Gate Milestone Model (Gate A: Start, Gate B: Completion)",
            "",
            "## 2. Implementation Task Breakdown",
            "| Task ID | Title | Assigned Worker | Action | Depends On | Human Approval | Budget (USD) |",
            "|---|---|---|---|---|---|---|",
        ]
        for t in tasks:
            deps = ", ".join(f"`{d}`" for d in t.get("depends_on", [])) if t.get("depends_on") else "None"
            lines.append(
                f"| `{t['task_id']}` | **{t['title']}** | `{t['worker_id']}` | `{t['action']}` | {deps} | {t.get('human_approval_required', True)} | ${t.get('budget_usd', 0.0):.2f} |"
            )

        lines.extend([
            "",
            "## 3. Acceptance Criteria & Verification Mandates",
        ])
        for t in tasks:
            lines.append(f"- **`{t['task_id']}`:** {t.get('acceptance_criteria', 'Pass')}")
            if t.get("command"):
                lines.append(f"  - *Command:* `{' '.join(t['command'])}` (Timeout: {t.get('timeout_s', 300)}s)")

        return "\n".join(lines)
