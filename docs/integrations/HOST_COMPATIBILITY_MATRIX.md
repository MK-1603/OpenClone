# Global AI Host Compatibility Matrix

In accordance with OpenClone truthfulness standards, compatibility states reflect observable test evidence:

- `VERIFIED`: Tested with observable command and automated test passing.
- `IMPLEMENTED`: Code and adapter package implemented and verified in test harness.
- `DOCUMENTED`: Setup package and configuration schema defined and tested locally.
- `PLANNED`: Target host scheduled for dedicated integration in roadmap.

---

## 1. Compatibility Ledger

| Host Tool | Primary Integration Surface | Supported Transports | Supported Primitives | Auth Flow | Compatibility Status | Test Evidence |
|---|---|---|---|---|:---:|---|
| **Google Antigravity** | MCP / Native Plugin | stdio / local JSON-RPC | Tools, Resources, Prompts, Rules | Local process | `VERIFIED` | `test_mcp_server.py`, `adapters/antigravity/` |
| **Claude Code & Desktop** | MCP Server | stdio | Tools, Resources, Prompts | Local process | `VERIFIED` | `test_mcp_server.py`, `adapters/claude-code/` |
| **Cursor Composer** | MCP Server / Rules | stdio | Tools, Prompts, MDC Rules | Local process | `VERIFIED` | `adapters/cursor/`, `.cursor/mcp.json` |
| **OpenAI Codex** | MCP Server / Skills | stdio | Tools, Prompts | Local process | `VERIFIED` | `adapters/codex/`, `mcp.json` |
| **ChatGPT (Web)** | Remote MCP / OpenAPI | Streamable HTTP / REST | Actions, OpenAPI 3.1 Tools | Bearer / OAuth 2.1 | `IMPLEMENTED` | `adapters/chatgpt/openapi.json` |
| **VS Code / Continue** | MCP Extension | stdio | Tools, Prompts | Local process | `DOCUMENTED` | `adapters/vscode/mcp.json` |
| **Generic MCP Clients** | Model Context Protocol | stdio / SSE | Tools, Resources, Prompts | Bearer Token / stdio | `VERIFIED` | `test_universal_integrations.py` |

---

## 2. Capability Matrix Across Verified Hosts

| Feature / Primitive | Antigravity | Claude Code | Cursor | Codex | ChatGPT | Generic MCP |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **MCP Tools (15 Tools)** | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: (REST) | :white_check_mark: |
| **MCP Resources** | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: (Unsupported by Host) | :white_check_mark: |
| **MCP Prompts** | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: (Unsupported by Host) | :white_check_mark: |
| **Taste Skill Anti-Slop** | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| **Lifecycle Checklists** | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| **Evidence Verification** | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| **Cryptographic Sign-Off** | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
