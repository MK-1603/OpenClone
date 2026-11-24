"""OpenClone Engineering Command Center Dashboard Service.

Provides a safe, local-only operational inspection service for OpenClone runtime.
Reads task DAGs, inspects the SQLite hash-chained ledger, surfaces workforce status,
and binds human approval gates to the authoritative runtime without direct database mutations.
"""
from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.openclone.runtime.workforce import Ledger, load_policy


@dataclass
class TaskSummary:
    task_id: str
    title: str
    worker_id: str
    status: str
    action: str
    budget_usd: float
    depends_on: List[str] = field(default_factory=list)
    has_approval: bool = False


@dataclass
class DashboardOverview:
    project_path: str
    total_tasks: int
    running_tasks: int
    completed_tasks: int
    failed_tasks: int
    pending_approvals: int
    ledger_events_count: int
    ledger_integrity_ok: bool
    tasks: List[TaskSummary] = field(default_factory=list)


class DashboardService:
    """Read-only and governed interaction layer connecting the UI to workforce runtime."""

    def __init__(self, project_path: Optional[Path] = None):
        self.project_path = (project_path or Path.cwd()).resolve()

    def get_overview(self) -> DashboardOverview:
        """Collect aggregated overview metrics from project ledger and plan."""
        db_path = self.project_path / ".aisdf" / "workforce.sqlite3"
        if not db_path.exists():
            return DashboardOverview(
                project_path=str(self.project_path),
                total_tasks=0,
                running_tasks=0,
                completed_tasks=0,
                failed_tasks=0,
                pending_approvals=0,
                ledger_events_count=0,
                ledger_integrity_ok=True,
                tasks=[],
            )

        ledger = Ledger(self.project_path)
        ok, problems, hashed_count, _ = ledger.verify_chain()

        tasks_rows = ledger.conn.execute("SELECT * FROM tasks").fetchall()
        tasks: List[TaskSummary] = []
        running = completed = failed = pending_approval = 0

        for r in tasks_rows:
            st = r["status"]
            if st in ("RUNNING", "IN_PROGRESS"):
                running += 1
            elif st == "SUCCEEDED":
                completed += 1
            elif st in ("FAILED", "BLOCKED"):
                failed += 1
            elif st in ("PLANNED", "APPROVED") and not r["approval_digest"]:
                pending_approval += 1

            deps = []
            try:
                deps = json.loads(r["depends_on"]) if r["depends_on"] else []
            except Exception:
                deps = []

            tasks.append(TaskSummary(
                task_id=r["task_id"],
                title=r["title"],
                worker_id=r["worker_id"],
                status=r["status"],
                action=r["action"],
                budget_usd=float(r["budget_usd"] or 0.0),
                depends_on=deps,
                has_approval=bool(r["approval_digest"]),
            ))

        ledger.close()

        return DashboardOverview(
            project_path=str(self.project_path),
            total_tasks=len(tasks),
            running_tasks=running,
            completed_tasks=completed,
            failed_tasks=failed,
            pending_approvals=pending_approval,
            ledger_events_count=hashed_count,
            ledger_integrity_ok=ok,
            tasks=tasks,
        )

    def get_task_dag(self) -> Dict[str, Any]:
        """Compute the DAG structure with execution tiers and dependency states."""
        overview = self.get_overview()
        nodes = []
        edges = []

        for t in overview.tasks:
            nodes.append({
                "id": t.task_id,
                "label": f"{t.task_id}: {t.title}",
                "status": t.status,
                "worker": t.worker_id,
            })
            for dep in t.depends_on:
                edges.append({"from": dep, "to": t.task_id})

        return {
            "project": str(self.project_path),
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes": nodes,
            "edges": edges,
        }

    def render_html_dashboard(self) -> str:
        """Generate a clean, standalone, dark/light responsive HTML developer dashboard."""
        overview = self.get_overview()
        dag = self.get_task_dag()

        task_rows = "\n".join([
            f"<tr><td><code>{t.task_id}</code></td><td>{t.title}</td><td><span class='badge badge-{t.status.lower()}'>{t.status}</span></td><td>{t.worker_id}</td><td>${t.budget_usd:.2f}</td></tr>"
            for t in overview.tasks
        ]) or "<tr><td colspan='5' class='empty-state'>No tasks currently registered in ledger.</td></tr>"

        integrity_badge = (
            "<span class='badge badge-success'>CRYPTOGRAPHICALLY VERIFIED</span>"
            if overview.ledger_integrity_ok
            else "<span class='badge badge-danger'>INTEGRITY VIOLATION DETECTED</span>"
        )

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>OpenKryvex Engineering Command Center</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    :root {{
      --bg: #0d1117; --surface: #161b22; --border: #30363d;
      --text: #e6edf3; --text-muted: #8b949e; --primary: #2f81f7;
      --success: #238636; --danger: #da3633; --warning: #d29922;
    }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 24px; }}
    .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 16px; margin-bottom: 24px; }}
    .header h1 {{ margin: 0; font-size: 20px; font-weight: 600; display: flex; align-items: center; gap: 8px; }}
    .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
    .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 16px; }}
    .card h3 {{ margin: 0 0 8px 0; font-size: 13px; color: var(--text-muted); text-transform: uppercase; }}
    .card .value {{ font-size: 28px; font-weight: 700; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px; }}
    th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid var(--border); }}
    th {{ color: var(--text-muted); font-weight: 600; }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; text-transform: uppercase; }}
    .badge-success {{ background: rgba(35, 134, 54, 0.2); color: #3fb950; border: 1px solid var(--success); }}
    .badge-danger {{ background: rgba(218, 54, 51, 0.2); color: #f85149; border: 1px solid var(--danger); }}
    .badge-succeeded {{ background: rgba(35, 134, 54, 0.2); color: #3fb950; }}
    .badge-planned {{ background: rgba(139, 148, 158, 0.2); color: var(--text-muted); }}
    .badge-running {{ background: rgba(47, 129, 247, 0.2); color: var(--primary); }}
    .empty-state {{ text-align: center; color: var(--text-muted); padding: 32px 0; }}
  </style>
</head>
<body>
  <div class="header">
    <h1>OpenKryvex Engineering Command Center</h1>
    <div>Ledger Status: {integrity_badge}</div>
  </div>

  <div class="metrics-grid">
    <div class="card"><h3>Total Tasks</h3><div class="value">{overview.total_tasks}</div></div>
    <div class="card"><h3>Active Tasks</h3><div class="value" style="color:var(--primary);">{overview.running_tasks}</div></div>
    <div class="card"><h3>Completed</h3><div class="value" style="color:#3fb950;">{overview.completed_tasks}</div></div>
    <div class="card"><h3>Failed / Blocked</h3><div class="value" style="color:#f85149;">{overview.failed_tasks}</div></div>
    <div class="card"><h3>Chained Events</h3><div class="value">{overview.ledger_events_count}</div></div>
  </div>

  <div class="card">
    <h3 style="margin-bottom:12px;">Active Task DAG & Execution Status</h3>
    <table>
      <thead>
        <tr><th>Task ID</th><th>Title</th><th>Status</th><th>Assigned Worker</th><th>Budget</th></tr>
      </thead>
      <tbody>
        {task_rows}
      </tbody>
    </table>
  </div>
</body>
</html>
"""
