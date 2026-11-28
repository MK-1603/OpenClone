# OpenClone AI Tool & Multi-Host Adapters
## Universal Multi-Host Plugin Distribution

**Product:** OpenClone Engineering Platform  
**Target Hosts:** Google Antigravity, Claude Code, OpenAI Codex, Cursor, Gemini CLI, VS Code, Generic MCP  
**Zero-Clone Policy:** End users install OpenClone directly via native host plugin/marketplace mechanisms without manual source checkouts.

See [`../docs/universal-installation.md`](../docs/universal-installation.md) for full step-by-step instructions.

---

## 1. Supported Host Adapters

| Directory | Target Host | Primary Packaging Surface | End-User Install Command | Status |
|---|---|---|---|---|
| [`antigravity/`](antigravity/) | Google Antigravity | `plugin.json` (Root & Adapter) | `agy plugin install https://github.com/MK-1603/OpenClone` | `VERIFIED` |
| [`claude-code/`](claude-code/) | Claude Code | `.claude-plugin/plugin.json` + `marketplace.json` | `/plugin marketplace add MK-1603/OpenClone` | `VERIFIED` |
| [`codex/`](codex/) | OpenAI Codex | `plugin.json` + `.agents/plugins/marketplace.json` | `codex plugin marketplace add MK-1603/OpenClone` | `VERIFIED` |
| [`cursor/`](cursor/) | Cursor | `.cursor/rules/openclone.mdc` + `.cursor/mcp.json` | Settings > MCP (`python -m src.openclone.cli mcp`) | `VERIFIED` |
| [`generic-mcp/`](generic-mcp/) | Any MCP Client | `mcp.json` (stdio JSON-RPC) | Add command: `python -m src.openclone.cli mcp` | `VERIFIED` |

---

## 2. Canonical Capability Core Architecture

```text
                 OpenClone GitHub Repository
                            |
                Canonical OpenClone Core
                            |
       +--------------------+--------------------+
       |                    |                    |
  Skills/Workflows     MCP Capability API    Knowledge/Rules
       |                    |                    |
       +--------------------+--------------------+
                            |
                 Security + Policy Gateway
                            |
                  Host Adapter Layer
                            |
       +----------+---------+---------+----------+
       |          |         |         |          |
  Antigravity  Claude     Codex    Cursor     Other Hosts
   Plugin      Plugin    Plugin   Adapter     Adapters
```

All adapters connect to the identical canonical OpenClone capability core and MCP service (`src/openclone/mcp/server.py`).
