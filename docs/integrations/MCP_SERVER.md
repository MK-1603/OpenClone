# Model Context Protocol (MCP) Server Specification

OpenClone implements an official **Model Context Protocol (MCP)** server conforming to specification version `2024-11-05`.

---

## 1. Supported Transports

1. **Standard Input/Output (`stdio`):** Default transport for local developer workstations, IDE agents, and desktop AI clients (Claude Desktop, Antigravity, Cursor, Continue).
2. **Server-Sent Events (`SSE`):** HTTP streaming transport for remote deployments, containerized agents, and internal webhooks.

```bash
# Launch stdio MCP server:
openclone mcp

# Launch SSE HTTP server on port 8000:
openclone mcp --port 8000
```

---

## 2. MCP Primitives

### 2.1 Tools (`tools/list`, `tools/call`)
Exposes all 15 canonical capabilities as typed MCP tools with JSON Schema draft-07 input contracts:
- `openclone_list_projects`
- `openclone_get_project_context`
- `openclone_search_project_knowledge`
- `openclone_get_checklist`
- `openclone_update_task_status`
- `openclone_submit_implementation_report`
- `openclone_submit_evidence`
- `openclone_request_verification`
- `openclone_get_quality_gate`
- `openclone_create_defect`
- `openclone_generate_ide_handoff`
- `openclone_get_release_readiness`
- `openclone_approve_release_deployment`
- `openclone_get_status`
- `openclone_get_guidance`

### 2.2 Resources (`resources/list`, `resources/read`)
Provides structured, read-only project and governance context:
- `openclone://project/overview`: Runtime status, version, active branch, and metrics.
- `openclone://project/checklist`: Current 22-phase checklist and verification standing.
- `openclone://governance/rulebook`: Canonical AISDF rulebook, precedence rules, and approval rules.
- `openclone://verification/policies`: Verification levels (V0–V5), truth criteria, and gate rules.

### 2.3 Prompts (`prompts/list`, `prompts/get`)
Provides reusable engineering workflow guidance:
- `openclone_plan_feature`: Architecture planning prompt enforcing Given/When/Then criteria and anti-slop rules.
- `openclone_implement_task`: Scoped implementation instructions with file allow-lists.
- `openclone_verify_feature`: Independent verification review protocol inspecting observable evidence.
- `openclone_security_review`: Audit prompt testing against the 19-point SaaS security baseline.
