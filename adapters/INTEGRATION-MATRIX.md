# OpenClone Multi-IDE & Chatbot Integration Matrix
## Conformance & Capability Matrix across Supported Hosts

- **Framework Version:** `1.0.0`
- **MCP Server Protocol:** `2024-11-05`
- **Verification Date:** 2026-11-22
- **Status:** SPECIFIED, IMPLEMENTED & VERIFIED

---

## 1. Multi-Host Integration Matrix

| Host Environment | Integration Surface | Native Format | MCP Support | Skills / Workflows | Auth / Security Model | Local Install Method | Test Method | Status |
|---|---|---|---|---|---|---|---|---|
| **Google Antigravity** | Native Plugin & Workspace Config | `plugin.json` + `.antigravity-plugin/` | **YES** (stdio / `mcpServers`) | Native Antigravity Skills (`SKILL.md`) + Agents | Process isolation; least-privilege tool approval | Copy to plugins dir or use agy CLI | Local schema check & tool invocation | `INTEGRATED & VERIFIED` |
| **Claude Code** | CLI & Terminal Plugin | `.claude/` + `.mcp.json` | **YES** (stdio `mcpServers`) | `.claude/skills/` + `CLAUDE.md` | Sandboxed command execution & human confirmation | `claude mcp add openclone python -m src.openclone.mcp.server` | CLI probe & prompt verification | `INTEGRATED & VERIFIED` |
| **OpenAI Codex** | CLI, Desktop & VSCode Extension | `.agents/` + `mcp.json` | **YES** (stdio / SSE) | Codex agent rules & portable skills | Workspace boundary checks & token confirmation | Add `mcp.json` to project root | Stdio probe & unit test | `INTEGRATED & VERIFIED` |
| **Cursor** | Editor & Composer Agent | `.cursor/` + `.cursor/mcp.json` | **YES** (stdio MCP) | `.cursorrules` + `.cursor/rules/` | File-scoped permission model & safe prompts | Add to Settings > MCP or `.cursor/mcp.json` | Cursor Agent tool test | `INTEGRATED & VERIFIED` |
| **ChatGPT** | Hosted MCP & Custom GPT | Custom GPT + OpenAPI / SSE | **YES** (Remote Streamable HTTP / SSE) | Custom GPT System Instructions + Action Tools | OAuth 2.0 / Bearer token authentication | Connect via Custom GPT Actions or MCP Proxy | SSE endpoint probe & schema audit | `INTEGRATED & DOCUMENTED` |

---

## 2. Shared OpenClone MCP Service Capabilities

All five host adapters connect to the identical canonical OpenClone MCP service (`src/openclone/mcp/server.py`):

1. `openclone_get_status` — Framework status, version, test counts, domains, engines, roles.
2. `openclone_search_knowledge` — Keyword search across 31 domains, 56 engines, 14 workflows, blueprints.
3. `openclone_explain_concept` — Deep documentation and execution contracts for any ID (`E-XXX`, `WF-XXX`, etc.).
4. `openclone_run_workflow` — Inspection and phase checklist retrieval for workflows.
5. `openclone_validate_project` — Repository structural validation.
6. `openclone_get_guidance` — Taste Skill anti-slop rules, morphism tokens, deployment guides.
7. `openclone_list_capabilities` — Complete directory of domains, engines, workflows, workforce roles, and adapters.

---

## 3. Host-Specific Installation Quick Start

### Google Antigravity
Point Antigravity's plugin configuration to `adapters/antigravity/plugin`.

### Claude Code
Add to your project's `.mcp.json`:
```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "src.openclone.mcp.server"]
    }
  }
}
```

### Cursor
Add to `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "src.openclone.mcp.server"]
    }
  }
}
```

### OpenAI Codex
Add to `.codex/mcp.json` or root `mcp.json`:
```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "src.openclone.mcp.server"]
    }
  }
}
```

### ChatGPT
Deploy `src/openclone/mcp/server.py` with an SSE/HTTP gateway (e.g. FastAPI/Uvicorn), configure OAuth/Bearer token, and register as an Action in ChatGPT Custom GPT Builder using [`adapters/../global/hosts/chatgpt/custom-gpt-instructions.md`](../global/hosts/chatgpt/custom-gpt-instructions.md).
