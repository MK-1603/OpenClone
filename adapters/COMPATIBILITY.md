# Tool Compatibility & Host Integration Matrix

OpenClone is tool-independent by design: the shared contract is Markdown (`AGENTS.md`, `PROJECT.md`), the Model Context Protocol (MCP) service (`src/openclone/mcp/server.py`), and the local runtime CLI (`python openclone.py` / `python aisdf.py`). **"Works with any tool" is not claimed unconditionally. Each integration must be earned and verified** (`adapters/CONFORMANCE.md` and [`adapters/INTEGRATION-MATRIX.md`](INTEGRATION-MATRIX.md)).

Integration levels:
- **I0** none/untested
- **I1** rules file only (the tool can read `AGENTS.md` / `PROJECT.md`)
- **I2** assisted handoff (a human carries context and results)
- **I3** tool runs `python openclone.py` / `python aisdf.py` commands under human approval
- **I4** native adapter implementing MCP tool protocol or `runtime/adapters/WORKER-ADAPTER-CONTRACT.md` with recorded evidence.

| Host Tool / Platform | Level Claimed | Verification Status | MCP Server Connection | Notes |
|---|---|---|---|---|
| **Google Antigravity** | **I4** (MCP + Native Plugin) | `VERIFIED` | stdio / `plugin.json` | Native Antigravity Plugin with full skills, rules, and MCP tools |
| **Claude Code** | **I4** (MCP + CLI Plugin) | `VERIFIED` | stdio / `.mcp.json` | Runs OpenClone MCP server; uses `CLAUDE.md` bridge |
| **Cursor** | **I4** (MCP + Composer Rules) | `VERIFIED` | stdio / `.cursor/mcp.json` | Direct tool invocation in Cursor Composer & Agent |
| **OpenAI Codex** | **I4** (MCP + Agent Package) | `VERIFIED` | stdio / `mcp.json` | Codex portable agent skills and MCP tool surface |
| **ChatGPT** | **I4** (Remote MCP / Custom GPT) | `DOCUMENTED` | Remote HTTPS / SSE | Connects via Remote MCP gateway or Custom GPT Actions |
| Any CLI/IDE reading `AGENTS.md` | I1 (untested) | `PROPOSED` | N/A | Plain Markdown entry prompt |

Rows move up only when `adapters/CONFORMANCE.md` has been run and the result is committed under `adapters/conformance-results/`.
