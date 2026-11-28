# OpenClone Global IDE Extension Architecture
## Unified Architecture for Antigravity, Visual Studio Code, Cursor, JetBrains, and Zed

**Document Version:** 1.0.0  
**Status:** SPECIFIED / IMPLEMENTED  
**Canonical Product:** OpenClone 2.0  
**Component:** OpenClone Global IDE Extension Ecosystem

---

## 1. Executive Summary

The **OpenClone Global IDE Extension Ecosystem** establishes OpenClone as a universal, cross-platform engineering companion accessible directly within all major development environments:

- **Google Antigravity IDE**: Deep native plugin with Model Context Protocol (MCP) server, specialized skills, deterministic governance rules, and custom subagents.
- **Visual Studio Code**: Native extension contributing an Activity Bar container, Explorer views (Plan, Workforce, Ledger), commands, and MCP client connectivity.
- **Cursor AI Editor**: Context server integration via `.cursor/mcp.json` and `.cursorrules` prompt governance.
- **JetBrains IDEs (IntelliJ, PyCharm, WebStorm, etc.)**: External tools and MCP integration via `.idea/mcp.json`.
- **Zed Editor**: Context server and Agent Client Protocol (ACP) adapter interoperability via `settings.json`.

All extensions connect to a **single shared OpenClone Core and Gateway**, eliminating duplicate engines and maintaining centralized governance.

---

## 2. Logical Architecture Diagram

```text
              +-----------------------------------------------+
              |                OPENCLONE CORE                 |
              |  - Autonomous Execution Engine (12 Stages)    |
              |  - Workforce Control Plane (72 Roles)         |
              |  - Cryptographic Ledger (SQLite SHA-256)      |
              |  - Model Intelligence Engine (MIE Catalog)    |
              +-----------------------------------------------+
                                      |
                                      v
              +-----------------------------------------------+
              |              OPENCLONE GATEWAY                |
              |  - Default-Deny Policy & Scopes               |
              |  - Multi-Pass Secret Redaction                |
              |  - Human Approval Verification                |
              +-----------------------------------------------+
                                      |
              +-----------------------+-----------------------+
              |                                               |
              v                                               v
  +-----------------------+                       +-----------------------+
  |      MCP SERVER       |                       |      ACP ADAPTER      |
  | (Model Context Proto) |                       | (Agent Client Proto)  |
  +-----------------------+                       +-----------------------+
              |                                               |
      +-------+-------+-------+                               |
      |               |       |                               |
      v               v       v                               v
+-----------+   +-----------+ +-----------+             +-----------+
|Antigravity|   |  VS Code  | |  Cursor   |             |    Zed    |
|  Plugin   |   | Extension | | JetBrains |             | Context   |
+-----------+   +-----------+ +-----------+             +-----------+
```

---

## 3. Host-Specific Platform Adapters

### 3.1. Google Antigravity Plugin (`plugins/openclone-antigravity/`)
Conforms strictly to the official Antigravity plugin manifest specification:
- **`plugin.json`**: Declares plugin identity, description, logo, suggested prompts, and author metadata.
- **`mcp_config.json`**: Registers the OpenClone MCP stdio server command (`oc.exe mcp`).
- **`skills/openclone-engineering/SKILL.md`**: Custom procedural knowledge guide for Antigravity agents.
- **`agents/openclone-engineer.md`**: Specialized autonomous engineering agent definition.
- **`rules/AGENTS.md`**: Non-negotiable deterministic rules (no speculative claims without test evidence, mandatory ledger hashing, boundary confinement).
- **`assets/logo.svg`**: Vector branding compliant with Antigravity UI guidelines.

### 3.2. Visual Studio Code Extension (`extensions/vscode/`)
Built with the standard VS Code Extension API:
- **`package.json`**: Extension manifest contributing:
  - Activity Bar container: `openclone-explorer`
  - Views: `openclone.planView`, `openclone.workersView`, `openclone.ledgerView`, `openclone.statusView`
  - Commands: `openclone.inspect`, `openclone.plan`, `openclone.run`, `openclone.verify`
- **`src/extension.js`**: Activation logic, TreeDataProvider implementations, and status bar item.
- **VSIX Packaging**: Compiled via `@vscode/vsce` into `openclone-vscode-2.0.0.vsix`.

### 3.3. Cursor & JetBrains Adapters
- **Cursor**: Workspace `.cursor/mcp.json` and user global config, with `.cursorrules` governance file.
- **JetBrains**: Workspace `.idea/mcp.json` mapping OpenClone tools into the JetBrains AI Assistant tool index.

### 3.4. Zed Adapter
- **Zed**: Configures `context_servers` in `.zed/settings.json` and supports ACP JSON-RPC message translation.

---

## 4. Global vs. Workspace Installation Model

The `IntegrationManager` provides two distinct installation targets:

| Target Scope | Flag | Antigravity Path | VS Code Path | Cursor Path |
| :--- | :--- | :--- | :--- | :--- |
| **Global / User-Level** | `--global` | `~/.gemini/config/plugins/openclone/` | `~/.vscode/extensions/` | `~/.cursor/` |
| **Workspace-Level** | default | `<workspace>/.gemini/plugins/openclone/` | `<workspace>/.vscode/mcp.json` | `<workspace>/.cursor/mcp.json` |

### Safety Invariants:
1. **Zero-Clobber Backups:** Before modifying any configuration file, a timestamped copy is preserved in `.openclone/backups/`.
2. **Atomic Writes:** Files are written and validated before updating active pointers.
3. **Clean Uninstallation:** Removing an integration restores previous settings without affecting unrelated plugins or extensions.
