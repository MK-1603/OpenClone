# OpenClone MCP Integration Guide
## Model Context Protocol (MCP) Server Architecture & Usage

**Version:** 1.0.0  
**Target:** AI Assistants, IDEs, and External Coding Agents  
**Protocol Version:** MCP 2024-11-05 (JSON-RPC 2.0)

---

## 1. Overview

The OpenClone MCP Server exposes OpenClone engineering intelligence, workforce coordination, and autonomous execution capabilities as standardized tools, resources, and prompts over standard input/output (`stdio`) and programmatic transports.

---

## 2. Server Startup & CLI Commands

Start the MCP server using either the standalone CLI or the core package:

```bash
# Using standalone OpenClone CLI
oc mcp

# Using core OpenClone CLI
openclone mcp
```

### Server Characteristics:
- **Transport:** `stdio` (JSON-RPC 2.0)
- **Dependencies:** Pure Python Standard Library (Python 3.10+)
- **Security:** In-process secret redaction, path confinement within repository boundary, and policy verification.

---

## 3. Core MCP Tools Specification

The OpenClone MCP Server provides 9 core engineering tools:

### 3.1. `openclone_inspect_repository`
Performs structured, non-destructive inspection of the repository root, detecting git branch, tracking status, dependencies, package managers, and configuration health.

- **Parameters:**
  - `workspace_path` *(string, optional)*: Absolute path to workspace root. Defaults to current working directory.
- **Returns:** JSON object containing `git_branch`, `git_clean`, `file_count`, `package_type`, `frameworks`.

### 3.2. `openclone_get_project_context`
Retrieves comprehensive project governance and operational context, including active tasks, ledger status, workforce count, and compliance gates.

- **Parameters:**
  - `workspace_path` *(string, optional)*: Workspace root.
- **Returns:** JSON object detailing governance state, active project name, and ledger integrity.

### 3.3. `openclone_analyze_requirements`
Ingests an engineering request prompt and classifies intent, complexity, affected architectural layers, and recommended execution mode.

- **Parameters:**
  - `prompt` *(string, required)*: Developer request or requirement description.
- **Returns:** Intent classification (`FEATURE`, `BUGFIX`, `REFACTOR`, etc.), estimated complexity, and recommended worker contracts.

### 3.4. `openclone_generate_plan`
Generates a structured, validated task execution plan with topological dependency sequencing.

- **Parameters:**
  - `prompt` *(string, required)*: Requirement description.
  - `mode` *(string, optional)*: Execution mode (`Instant`, `Fast`, `Standard`, `Deep`, `Autonomous`).
- **Returns:** `ExecutionPlan` containing unique plan ID, task nodes, dependencies, and risk level.

### 3.5. `openclone_get_agent_status`
Retrieves workforce status, list of registered agent worker contracts, and their current workload.

- **Parameters:**
  - `filter_role` *(string, optional)*: Filter by worker contract role ID.
- **Returns:** List of active workers, roles, permissions, and capacity.

### 3.6. `openclone_get_execution_status`
Inspects real-time or historical task execution state from the cryptographic audit ledger.

- **Parameters:**
  - `execution_id` *(string, optional)*: Specific execution or request ID.
- **Returns:** Execution stage, task completion percentage, active retries, and errors.

### 3.7. `openclone_get_verification_results`
Fetches test results, quality gate metrics, link checks, and compliance scorecard.

- **Parameters:**
  - `workspace_path` *(string, optional)*: Workspace root.
- **Returns:** Verification status (`PASS`/`FAIL`), executed test count, passed test count, and failure details.

### 3.8. `openclone_get_delivery_report`
Generates or retrieves final delivery summary, change artifacts, and verification evidence for a completed request.

- **Parameters:**
  - `request_id` *(string, optional)*: Request identifier.
- **Returns:** Comprehensive `DeliveryReport` markdown and structured JSON summary.

### 3.9. `openclone_execute_task` (Governed)
Executes a bounded engineering operation under OpenClone governance policies.

- **Parameters:**
  - `prompt` *(string, required)*: Engineering prompt to execute.
  - `mode` *(string, optional)*: Execution mode (`Instant`, `Fast`, `Standard`, `Deep`, `Autonomous`).
  - `approval_digest` *(string, optional)*: Cryptographic human approval digest required for high-risk operations.
- **Returns:** `DeliveryReport` with execution results and verification summary.

---

## 4. Sample Client Configuration

### VS Code / Cursor (`mcp.json`):
```json
{
  "mcpServers": {
    "openclone": {
      "command": "oc.exe",
      "args": ["mcp"],
      "env": {
        "OPENCLONE_WORKSPACE": "${workspaceFolder}"
      }
    }
  }
}
```

### Claude Desktop (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "src.openclone.cli", "mcp"],
      "cwd": "D:\\New folder\\OpenClone"
    }
  }
}
```
