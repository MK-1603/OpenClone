# AI Tool & Multi-IDE Host Adapters

OpenClone core is provider-neutral and IDE-independent. Each adapter connects to the identical shared OpenClone MCP Service (`src/openclone/mcp/server.py`) and loads the canonical project contract (`PROJECT.md`) and operating contract (`AGENTS.md`) using native host discovery and configuration files.

See [`INTEGRATION-MATRIX.md`](INTEGRATION-MATRIX.md) for the complete multi-host capability and conformance matrix.

| Environment | Integration Surface | MCP Configuration | Primary Instruction Entry | Additional Adapter Assets |
|---|---|---|---|---|
| **Google Antigravity** | Native Plugin & Workspace Config | `plugin.json` (`mcpServers`) | `AGENTS.md` / `GEMINI.md` | `.agents/rules/aisdf.md`, `.agents/skills/aisdf/SKILL.md` |
| **Claude Code** | CLI & Terminal Plugin | `.mcp.json` | `CLAUDE.md` | `.claude/skills/aisdf/SKILL.md`, `CLAUDE.template.md` |
| **OpenAI Codex** | CLI, Desktop & VSCode Extension | `mcp.json` | `AGENTS.md` | `.agents/skills/aisdf/SKILL.md` |
| **Cursor** | Editor & Composer Agent | `.cursor/mcp.json` | `AGENTS.md` | `.cursor/rules/aisdf.mdc`, `aisdf-project-rule.template.mdc` |
| **ChatGPT** | Hosted MCP & Custom GPT | Remote HTTPS / SSE | Custom GPT Instructions | [`chatgpt/README.md`](chatgpt/README.md), [`../global/hosts/chatgpt/custom-gpt-instructions.md`](../global/hosts/chatgpt/custom-gpt-instructions.md) |

Adapters do not grant permissions or prove host compatibility. Always inspect existing instructions before installing; merge rather than overwrite. See [PROJECT.md and AGENTS.md](../docs/guides/project-lifecycle/PROJECT-AND-AGENT-FILES.md).
