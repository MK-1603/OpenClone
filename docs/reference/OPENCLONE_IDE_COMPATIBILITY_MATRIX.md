# OpenClone IDE Compatibility Matrix

**Component:** OpenClone Extension & Platform Integration Ecosystem  
**Version:** 2.0.0  
**Specification Reference:** [OPENCLONE_EXTENSION_ARCHITECTURE.md](../architecture/OPENCLONE_EXTENSION_ARCHITECTURE.md)  
**Status:** IMPLEMENTED / TESTED  

---

## 1. Overview & Support Tier Definitions

OpenClone provides a unified, zero-duplication platform integration model across major IDEs and AI coding platforms. Every integration delegates core tasks (planning, code execution, multi-agent workforce, diagnostics, verification) to the local or remote OpenClone Gateway / MCP runtime.

### Support Tiers

| Tier | Name | Meaning | Release Gate Requirements |
|---|---|---|---|
| **Tier 1** | Primary Native Support | First-class native extension with custom sidebar views, commands, and automated installation via `oc` CLI. | Full end-to-end automated tests, manifest schema validation, packaging pipeline. |
| **Tier 2** | Native Extension Support | Dedicated native extension package with commands and explorer views. | Automated package validation, protocol conformance tests. |
| **Tier 3** | Config / MCP Server Adapter | Native MCP configuration or plugin structure loaded by the host platform. | Validated MCP schema, configuration test, manual verification. |
| **Tier 4** | Planned / Experimental | Architecture specified; native adapter under active development. | Architectural contract defined, integration pending. |

---

## 2. Comprehensive Compatibility Matrix

| IDE / Platform | Target Version | Support Tier | Package Type | Installation Scope | Integration Protocol | Status |
|---|---|---|---|---|---|---|
| **Google Antigravity** | 2.0.0+ | **Tier 1** | Antigravity Plugin (`plugin.json`) | Global (`~/.gemini/config/plugins/openclone`) & Workspace (`.gemini/plugins/openclone`) | Antigravity Agent Plugin & MCP (`oc.exe mcp`) | **TESTED** |
| **Visual Studio Code** | 1.80.0+ | **Tier 1** | VS Code Extension (`.vsix`) | Global User Profile & Workspace Config (`.vscode/mcp.json`) | Language / MCP Client + Native Views | **TESTED** |
| **Cursor** | 0.30.0+ | **Tier 1** | Cursor/VS Code Compatible Extension | Global & Workspace (`.cursor/mcp.json`) | MCP Client + Extension Host | **TESTED** |
| **JetBrains IDEs** (IntelliJ, PyCharm, WebStorm) | 2023.2+ | **Tier 2** | JetBrains Plugin / MCP Server | Global Config & Project Tools | MCP Protocol (`oc mcp`) + External Tool | **IMPLEMENTED** |
| **Zed** | 0.120.0+ | **Tier 2** | Zed Extension / Context Server | Global (`~/.config/zed/settings.json`) | Model Context Protocol (MCP) | **IMPLEMENTED** |
| **Sublime Text / Neovim** | Any LSP/MCP capable | **Tier 3** | Stdio MCP Client Config | User / Project Config | Standard MCP JSON-RPC 2.0 | **IMPLEMENTED** |

---

## 3. Platform-Specific Integration Details

### 3.1 Google Antigravity (Primary Native)
- **Manifest:** `plugins/openclone-antigravity/plugin.json`
- **Capabilities:**
  - Skill: `skills/openclone-engineering/SKILL.md` for conversational task decomposition and execution.
  - Subagent: `agents/openclone-engineer.md` with full tool access and engineering role instructions.
  - Rules: `rules/AGENTS.md` operating contract ensuring deterministic quality and human approval gates.
  - Lifecycle Hook: `SessionStart` automated repository health audit (`hooks.json`).
  - Native MCP Server: Stdio connection launching `oc.exe mcp` with 43 registered tools.
- **CLI Commands:**
  ```bash
  oc platforms connect antigravity --global
  oc platforms status antigravity
  ```

### 3.2 Visual Studio Code & Cursor (Tier 1)
- **Manifest:** `extensions/vscode/package.json`
- **Capabilities:**
  - Activity Bar Icon (`resources/icon.svg`) with dedicated OpenClone container.
  - Explorer Views:
    - `openclone-status`: Live runtime connection and health indicator.
    - `openclone-plan`: Active project milestones, tasks, and state.
    - `openclone-workers`: Dynamic workforce roster and agent allocations.
    - `openclone-ledger`: Evidence ledger, audit events, and verification logs.
  - Palette Commands:
    - `OpenClone: Inspect Project` (`openclone.inspect`)
    - `OpenClone: Generate Engineering Plan` (`openclone.plan`)
    - `OpenClone: Execute Active Plan` (`openclone.run`)
    - `OpenClone: Verify Quality & Evidence` (`openclone.verify`)
    - `OpenClone: Connect Runtime Gateway` (`openclone.connect`)
- **CLI Commands:**
  ```bash
  oc platforms connect vscode
  oc platforms connect cursor
  ```

### 3.3 JetBrains IDEs & Zed (Tier 2)
- **Capabilities:**
  - Auto-generated MCP server configurations linking project directories to `oc.exe mcp`.
  - Stdio process supervisor maintaining responsive JSON-RPC 2.0 communication.
- **CLI Commands:**
  ```bash
  oc platforms connect jetbrains
  oc platforms connect zed
  ```

---

## 4. Verification & Testing Strategy

Each integration target is validated against:
1. **Manifest Integrity:** Validation against host schema requirements (Antigravity `plugin.json`, VS Code `package.json`, MCP `mcp_config.json`).
2. **Installation Idempotency:** Connecting multiple times without duplicate configurations or corrupted files.
3. **Rollback & Uninstallation:** Clean removal and restoration of backed-up configuration files (`oc platforms disconnect <platform>`).
4. **Protocol Conformance:** Zero packet drops, valid JSON-RPC 2.0 framing, deterministic tool responses across stdio streams.
