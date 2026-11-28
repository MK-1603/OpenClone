# OpenClone Global Engineering & Governance Standard
**Version:** 2.0.0 | **Scope:** Global Cross-Platform AI Software Engineering Specification  
**Canonical Identity:** OpenClone (`MK-1603/OpenClone`)  
**Architecture:** Deterministic Governance, Universal Engineering Intelligence & Phase 0 Planning

---

## 1. Mission & Architectural Purpose

The OpenClone Global layer provides a single, host-agnostic engineering intelligence and deterministic governance foundation that operates seamlessly across all modern AI development environments:
- **Google Antigravity:** Native plugin, sandboxed execution, and artifact viewing.
- **Visual Studio Code:** Dedicated Activity Bar panel, nonce-secured Webview, and REST gateway integration.
- **Cursor & Windsurf:** Rule-driven context guidance and MCP protocol bridging.
- **Claude Code & Terminal Agents:** CLI-independent execution harnesses and structured filesystem handoffs.
- **Generic MCP / OpenAPI Clients:** Universal JSON-RPC tool endpoints.

OpenClone is not another code-generation model. It is the **governed control plane** around the AI coding agent, ensuring that every project is engineered with immutable requirements, anti-slop design standards, multi-tenant security modeling, and reproducible verification.

---

## 2. Deterministic Precedence Hierarchy

When overlapping configurations or instructions arise, all AI agents and runtime systems MUST strictly adhere to this deterministic precedence order:

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Project Invariants: AGENTS.md, PROJECT.md (Root Level)   │
├─────────────────────────────────────────────────────────────┤
│ 2. Local IDE Directives: .cursor/rules/, .agents/rules/     │
├─────────────────────────────────────────────────────────────┤
│ 3. Active Approved Plan: PlanBuilder DAG & Task Digests     │
├─────────────────────────────────────────────────────────────┤
│ 4. Global Configuration: ~/.openclone/config.yaml           │
├─────────────────────────────────────────────────────────────┤
│ 5. Framework Baselines: framework/rules/ & Canonical Specs  │
└─────────────────────────────────────────────────────────────┘
```
*A higher layer strictly overrides a lower layer. No global default may silently override an explicit project governance contract.*

---

## 3. Universal Engineering Rules

All AI agents operating within an OpenClone-governed codebase MUST enforce the following four non-negotiable principles:

### 3.1 Strict Anti-Slop & Zero-Invention
- **No Speculative Architecture:** Never introduce microservices, databases, caches, message queues, or cloud infrastructure without evidence-backed requirements.
- **Production-Grade Completeness:** Never write placeholder comments (`// TODO`, `/* implement later */`), mock data, or skipped error paths into production runtime code.
- **Design Restraint:** UIs must strictly follow the 8-point typography scale, WCAG 2.2 AA contrast ratios, and design token hierarchies—no ambient purple blur blobs or generic card clichés.

### 3.2 Evidence-Backed Verification & Truthful Maturity
- Every task, bug fix, or refactor must be validated by running actual automated test suites and capturing tangible execution evidence.
- Never claim tests pass without executing the command and verifying the exit code.
- Maturity classification is strictly evidenced:
  `PROPOSED` $\rightarrow$ `SPECIFIED` $\rightarrow$ `IMPLEMENTED` $\rightarrow$ `TESTED` $\rightarrow$ `INTEGRATED` $\rightarrow$ `CERTIFIED`.

### 3.3 Security & Least Privilege Boundaries
- **Phase 0 Planning Boundary:** In Phase 0, all autonomous target-project code modifications (`execute=True` or `POST /api/v1/execution`) fail closed and are strictly rejected.
- **Secret Redaction:** Raw secrets, tokens, API keys, or private certificates must never be committed to source control, serialized into logs, or exposed to external AI prompts.
- **Workspace Boundaries:** Filesystem operations must remain strictly bounded to the workspace root. Directory traversal (`..`) is blocked.

### 3.4 Cryptographic Approval Ledger
- High-risk operations (production deployments, irreversible database mutations, schema destructions) halt until a verified cryptographic approval digest ($\ge 16$ characters) signed by an authorized human is committed to the append-only ledger.

---

## 4. Platform Subsystems & Architecture Matrix

| Subsystem | Namespace | Core Responsibility |
|---|---|---|
| **Central Orchestrator** | `openclone.planning.agent` | Canonical `OpenClonePlannerAgent` governing understanding, clarification, and handoff. |
| **Project Intelligence** | `openclone.intelligence` | Four-Set PIA architecture (Set A features, Set B gaps, Set C solutions, Set D blueprint). |
| **Engineering Intelligence** | `openclone.engineering` | 155 Canonical disciplines, knowledge graph, and dynamic domain activation. |
| **Identity & Brand** | `openclone.identity` | Automated naming, brand voice guidelines, color palettes, and SVG vector logo suites. |
| **Product Blueprint** | `openclone.blueprint` | UI inventory, user journeys, ASCII wireframes, interaction specifications, and traceability. |
| **DevOps & Infrastructure**| `openclone.devops` | DETI recommendations, database engine decoupling, connected accounts, and 21-state FSM. |
| **Security & STRIDE** | `openclone.security` | Planning-time threat modeling, asset trust boundaries, countermeasures, and verification checks. |
| **Connectors & Gateways** | `openclone.connectors` | REST API, SSE streams, OpenAPI specs, and MCP bridges for Claude, ChatGPT, and Cursor. |

---

## 5. Integrating OpenClone into Your Workflow

### Python API Integration
```python
from src.openclone.planning.agent import OpenClonePlannerAgent

# Initialize canonical central planner
planner = OpenClonePlannerAgent()

# Generate comprehensive Phase 0 Project Plan
plan_package = planner.plan_project(
    prompt="Design a real-time collaborative document platform with PostgreSQL and Next.js",
    project_name="CollabDoc",
)

# Inspect validated architectural artifacts
print("Planning Status:", plan_package["status"])
print("Generated Tasks:", plan_package["plan"]["task_count"])
```

### Visual Studio Code Extension
Install the official OpenClone VS Code Extension (`extensions/vscode`) to access the Activity Bar panel, interactive AI chat, active plan visualizer, workforce inspector, and audit ledger directly in your editor.

### Google Antigravity & Agent Environments
OpenClone exposes standard MCP and capability endpoints (`plugin.json`, `src/openclone/mcp/server.py`) enabling immediate plug-and-play integration into any MCP-compatible agent environment.

