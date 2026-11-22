# Generic MCP Client Adapter

OpenClone exposes its canonical capabilities, resources, and prompt workflows through the standard **Model Context Protocol (MCP)** specification (Protocol version `2024-11-05`).

## 1. Local stdio Transport

Any MCP client running on the local developer workstation (Claude Desktop, Antigravity, Cursor, Continue, or custom CLI agents) can connect via standard stdio:

```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "src.openclone.cli", "mcp"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

## 2. Server-Sent Events (SSE) / Streamable HTTP

For remote agent runtimes and cloud deployments, launch OpenClone in SSE server mode:

```bash
# Start SSE HTTP server on port 8000
python -m src.openclone.cli mcp --port 8000
```

Client configuration:
```json
{
  "mcpServers": {
    "openclone-remote": {
      "url": "http://localhost:8000/sse",
      "headers": {
        "Authorization": "Bearer oc_live_..."
      }
    }
  }
}
```

## 3. Supported MCP Primitives

- **Tools (15 canonical tools):**
  - Project Discovery & Context: `openclone_list_projects`, `openclone_get_project_context`, `openclone_search_project_knowledge`
  - Checklist & Tasks: `openclone_get_checklist`, `openclone_update_task_status`, `openclone_submit_implementation_report`
  - Evidence & Verification: `openclone_submit_evidence`, `openclone_request_verification`
  - Defects & Gates: `openclone_get_quality_gate`, `openclone_create_defect`
  - Handoff & Release: `openclone_generate_ide_handoff`, `openclone_get_release_readiness`, `openclone_approve_release_deployment`
  - Core Inspection: `openclone_get_status`, `openclone_get_guidance`
- **Resources (`resources/list`, `resources/read`):**
  - `openclone://project/overview`
  - `openclone://project/checklist`
  - `openclone://governance/rulebook`
  - `openclone://verification/policies`
- **Prompts (`prompts/list`, `prompts/get`):**
  - `openclone_plan_feature`
  - `openclone_implement_task`
  - `openclone_verify_feature`
  - `openclone_security_review`
