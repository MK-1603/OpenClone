# Engineering Command Center

**Version:** 2.0.0  
**Classification:** Observability & Operations Manual  
**Status:** IMPLEMENTED  

---

## 1. Overview

The Engineering Command Center provides real-time, browser-based visibility into multi-agent execution graphs, workforce resource consumption, test execution telemetry, and human approval queues. It functions without external node dependencies, CDN assets, or cloud telemetry agents.

Module implementation: `src/openclone/dashboard/service.py`

---

## 2. Core Capabilities

### 2.1 Directed Acyclic Graph (DAG) Visualization
Transforms sequential and parallel agent tasks recorded in `workforce.sqlite3` into a dependency DAG:
- **Nodes:** Individual tasks characterized by role, status (`QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`, `PENDING_APPROVAL`), and duration.
- **Edges:** Explicit parent-child task dependencies (`parent_task_id`).
- **Interactive Inspection:** Clicking a node displays the raw JSON execution logs, standard output streams, and tool call traces.

### 2.2 Metric Telemetry
Tracks real-time system metrics directly from the host environment:
- **Total Completed Tasks:** Global count across active workforce sessions.
- **Success Rate Percentage:** Ratio of passing executions against total completed tasks.
- **Resource Utilization:** Host CPU, memory footprint, and SQLite disk storage consumption.
- **Active Agent Roster:** Real-time breakdown of agents currently holding execution locks.

### 2.3 Responsive Theme Engine
The Command Center features a zero-dependency CSS layout supporting:
- Light and Dark modes with automatic OS theme detection (`prefers-color-scheme`).
- Fully accessible semantic HTML elements (WCAG AA compliant).
- Responsive mobile and desktop grid breakpoints.

---

## 3. Architecture & Integration

```
+-------------------------------------------------------------------------+
|                        Browser Client (HTML5 / CSS3)                    |
+------------------------------------+------------------------------------+
                                     |
                                     | HTTP GET /dashboard
                                     v
+-------------------------------------------------------------------------+
|                  DashboardService (Python stdlib)                       |
|                                                                         |
|  +----------------------+  +--------------------+  +------------------+ |
|  | Task DAG Aggregator  |  | Metrics Calculator |  | HTML UI Renderer | |
|  +-----------+----------+  +---------+----------+  +--------+---------+ |
|              |                       |                      |           |
+--------------+-----------------------+----------------------+-----------+
                                       |
                                       v
+-------------------------------------------------------------------------+
|                       workforce.sqlite3 (WAL Mode)                      |
+-------------------------------------------------------------------------+
```

---

## 4. Launching the Command Center

```python
from openclone.dashboard.service import DashboardService

# Initialize dashboard service backed by existing workforce SQLite database
service = DashboardService(db_path="runtime/openclone_runtime/workforce.sqlite3")

# Retrieve aggregated overview data model
overview = service.get_overview()
print(f"Total Tasks: {overview.total_tasks}, Success Rate: {overview.success_rate}%")

# Generate standalone HTML dashboard
html_content = service.render_html()
with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)
```
