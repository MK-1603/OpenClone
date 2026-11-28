# OpenClone Universal Platform Integration Architecture
## Component Architecture & Ecosystem Specifications

**Document Version:** 1.0.0  
**Status:** SPECIFIED / IMPLEMENTED  
**Canonical Product:** OpenClone 2.0  
**Target Capability:** Universal IDE and AI Platform Integration Ecosystem

---

## 1. Executive Overview

OpenClone 2.0 provides a universal, governed engineering intelligence and execution platform. The Universal Platform Integration Ecosystem enables OpenClone capabilities to be consumed seamlessly across diverse software engineering environments:

1. **Standalone CLI (`oc.exe` / `oc`)**: High-performance local and remote CLI binary.
2. **Google Antigravity IDE**: Deep native integration via MCP, custom skills, rules, and lifecycle agents.
3. **Visual Studio Code**: Extension-driven sidebar, project inspection, task planning, and MCP server connectivity.
4. **Cursor**: Context server integration via `.cursor/mcp.json` and governed prompt rules.
5. **JetBrains IDEs (IntelliJ, PyCharm, WebStorm, etc.)**: Tool and MCP integration via `.idea/mcp.json`.
6. **Zed Editor**: Context server and Agent Client Protocol (ACP) adapter interoperability via `settings.json`.
7. **External AI Platforms**: Versioned REST API and standardized JSON-RPC protocols.

All IDE integrations operate as non-intrusive presentation and context clients to the unified **OpenClone Gateway**. The central governance, cryptographic ledger, workforce control plane, and autonomous execution engine are strictly preserved and never duplicated.

---

## 2. Logical System Architecture

```text
                               +--------------------------------------------------+
                               |                 OPENCLONE PLATFORM               |
                               +--------------------------------------------------+
                                                        |
                     +----------------------------------+----------------------------------+
                     |                                  |                                  |
         +-----------------------+          +-----------------------+          +-----------------------+
         |    OPENCLONE CLI      |          |    OPENCLONE CORE     |          |    INTEGRATION HUB    |
         |  (oc / oc.exe / aisdf)|          |  Engineering Engines  |          |   Platform Registry   |
         +-----------------------+          +-----------------------+          +-----------------------+
                     |                                  |                                  |
                     +----------------------------------+----------------------------------+
                                                        |
                                            +-----------------------+
                                            |   OPENCLONE GATEWAY   |
                                            | (Policy & Auth Layer) |
                                            +-----------------------+
                                                        |
                        +-------------------------------+-------------------------------+
                        |                               |                               |
            +-----------------------+       +-----------------------+       +-----------------------+
            |      MCP SERVER       |       |      ACP ADAPTER      |       |       REST API        |
            | (Model Context Proto) |       | (Agent Client Proto)  |       |   (OpenAPI / HTTP)    |
            +-----------------------+       +-----------------------+       +-----------------------+
                        |                               |                               |
             +----------+----------+                    |                               |
             |          |          |                    |                               |
       Antigravity   VS Code    Cursor                 Zed                       External Platforms
        JetBrains                                (ACP Clients)                     & CI/CD Tools
```

---

## 3. Core Architectural Subsystems

### 3.1. Platform Discovery Engine
The `PlatformDiscoveryEngine` programmatically detects development environments installed on the user's host system without accessing undocumented private storage or collecting unrelated user files.

- **Inspection Target:** Platform binaries, configuration roots, active workspaces, and protocol support.
- **Supported Adapters:**
  - `AntigravityAdapter` (Checks `%USERPROFILE%\.gemini\antigravity`, plugins directory, and executable paths).
  - `VSCodeAdapter` (Checks `.vscode`, `%APPDATA%\Code`, and `code` CLI in PATH).
  - `CursorAdapter` (Checks `.cursor`, `%APPDATA%\Cursor`, and `cursor` CLI in PATH).
  - `JetBrainsAdapter` (Checks `.idea`, `%APPDATA%\JetBrains`, and toolbox installations).
  - `ZedAdapter` (Checks `.zed`, `%APPDATA%\Zed`, `%USERPROFILE%\.config\zed`, and `zed` CLI).
  - `GenericPlatformAdapter` (Custom/extensible adapter for third-party tools).

### 3.2. Platform Capability Registry
A centralized registry declaring the maturity and support profile of every platform:

| Platform | Identifier | Status | Supported Protocols | Config Target |
| :--- | :--- | :--- | :--- | :--- |
| **Google Antigravity** | `antigravity` | `VERIFIED` | MCP, Skills, Rules | `.gemini/antigravity/plugins/` |
| **VS Code** | `vscode` | `VERIFIED` | MCP, Extension, Tasks | `.vscode/mcp.json`, `package.json` |
| **Cursor** | `cursor` | `VERIFIED` | MCP, Rules | `.cursor/mcp.json` |
| **JetBrains** | `jetbrains` | `VERIFIED` | MCP, External Tools | `.idea/mcp.json` |
| **Zed** | `zed` | `VERIFIED` | ACP, MCP | `.config/zed/settings.json` |
| **Generic IDE** | `generic` | `EXPERIMENTAL` | MCP, REST | `.openclone/mcp.json` |

### 3.3. OpenClone Gateway
All external calls flow through the `IntegrationGateway`, which strictly enforces:
- **Authentication & Authorization:** Scoped access tokens (`read`, `plan`, `execute`, `admin`).
- **Policy Enforcement:** Default-deny policy requiring cryptographic human approval for destructive operations.
- **Secret Redaction:** Multi-pass regex filtering for API keys, AWS credentials, GitHub tokens, and passwords.
- **Audit Ledger Logging:** Every query, tool call, and state mutation is logged to the SQLite tamper-evident ledger.

### 3.4. Multi-Protocol Translation Layer
1. **MCP (Model Context Protocol):**
   - Implements JSON-RPC 2.0 stdio transport.
   - Provides standardized tools: repository inspection, project context retrieval, requirements analysis, plan generation, agent status, execution status, verification results, delivery reports, and governed task execution.
2. **ACP (Agent Client Protocol):**
   - Provides translation layer for editors adopting ACP (e.g. Zed Assistant).
   - Maps ACP session initialization, prompt submission, and notification streaming to OpenClone execution stages.
3. **REST API Gateway:**
   - OpenAPI-compliant endpoints serving `/api/v1/health`, `/api/v1/capabilities`, `/api/v1/projects`, `/api/v1/plans`, `/api/v1/execution`, and `/api/v1/integrations`.

---

## 4. Integration Lifecycle & Automation

The `IntegrationManager` manages the end-to-end integration lifecycle:

1. **Discovery:** `oc platforms discover` scans local storage for installed IDEs.
2. **Inspection:** `oc platforms inspect <platform>` evaluates configuration files, existing MCP registrations, and compatibility.
3. **Safety Backup:** Before altering any configuration file (e.g. `settings.json`, `mcp.json`), a timestamped backup is preserved in `.openclone/backups/`.
4. **Configuration Generation:** Generates valid, validated JSON configurations tailored to the target platform.
5. **Health Verification:** Executes an in-memory or stdio loopback check to verify that OpenClone responds correctly.
6. **Safe Removal:** `oc integrations remove <platform>` restores original configuration cleanly.

---

## 5. Security & Trust Model

- **No Privilege Escalation:** An IDE integration cannot grant permissions that OpenClone's governance layer prohibits.
- **Workspace Boundary Enforcement:** File inspection and tool execution are strictly confined to the authorized workspace root.
- **Explicit Approval Gates:** Operations classified as `MEDIUM_RISK` or `HIGH_RISK` halt until an authorized human approval record is validated.
- **Secret Zero-Leakage:** Environment variables and configuration files containing secrets are scrubbed before serialization.
