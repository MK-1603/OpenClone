# OpenClone Standalone CLI Architecture
## High-Performance, Minimal, and Professional Command-Line Experience

**Document Version:** 1.0.0  
**Status:** IMPLEMENTED / TESTED  
**Canonical Product:** OpenClone 2.0  
**Component:** OpenClone CLI (`oc` / `oc.exe`)

---

## 1. Executive Summary

The **OpenClone CLI (`oc` / `oc.exe`)** is a standalone, lightweight, and professional command-line application providing direct access to OpenClone engineering intelligence, workforce coordination, and autonomous execution.

The CLI embodies a **Zero-Duplication Architecture**:
- It acts strictly as a presentation, interaction, and connection client.
- It directly delegates to the core OpenClone Autonomous Execution Engine, Workforce Control Plane, and Integration Gateway.
- It introduces zero parallel execution platforms or redundant intelligence engines.

---

## 2. Dual Operating Modes

```text
                               +-------------------------------------+
                               |           OPENCLONE CLI             |
                               |          (oc / oc.exe)              |
                               +-------------------------------------+
                                                  |
                         +------------------------+------------------------+
                         |                                                 |
             [Arguments Provided]                                  [Zero Arguments]
                         |                                                 |
                         v                                                 v
           +---------------------------+                     +---------------------------+
           |       COMMAND MODE        |                     |     INTERACTIVE MODE      |
           | Direct Non-Interactive    |                     | Clean Terminal Menu Loop  |
           | Fast Scripting & CI/CD    |                     | Keyboard-Driven Actions   |
           +---------------------------+                     +---------------------------+
                         |                                                 |
                         +------------------------+------------------------+
                                                  |
                                                  v
                               +-------------------------------------+
                               |         CONNECTION MANAGER          |
                               |      (Hybrid Local / Remote)        |
                               +-------------------------------------+
                                        |                   |
                                        v                   v
                               +-----------------+ +-----------------+
                               |  Local Runtime  | | Remote Gateway  |
                               |   (In-Process)  | |  (HTTPS / WSS)  |
                               +-----------------+ +-----------------+
```

### 2.1. Command Mode
Direct commands optimized for scripting, developer muscle memory, and CI/CD pipelines:
- `oc inspect`: Fast, non-destructive repository and git context inspection.
- `oc plan <prompt>`: Decomposes requirements into structured task plans with dependency graphs.
- `oc run <prompt>`: Executes governed engineering operations with tamper-evident audit evidence.
- `oc agents`: Lists registered workforce contracts, capacities, and permissions.
- `oc models`: Queries the Model Intelligence Engine catalog and routing tiers.
- `oc providers`: Checks connectivity and health of AI providers (OpenAI, Anthropic, Google, Local).
- `oc workflows`: Lists the 15 standard engineering workflows (WF-001 through WF-015).
- `oc verify`: Runs test suites, link verification, and release quality gates.
- `oc connect`: Manages local, remote, and hybrid runtime targets.
- `oc platforms`: Discovers and connects IDEs (Antigravity, VS Code, Cursor, JetBrains, Zed).
- `oc integrations`: Installs or removes platform integration packages with automatic backups.
- `oc config`: Manages user and system configuration settings.
- `oc doctor`: Inspects toolchains, Python runtimes, and installation health.
- `oc update`: Checks for, applies, or rolls back platform updates.

### 2.2. Interactive Mode
When invoked without arguments (`oc`), launches a clean, non-cluttered interactive terminal:
```text
OpenClone CLI v2.0.0 — Universal AI Engineering Interface
Runtime: local (ACTIVE) | Workspace: D:\New folder\OpenClone
========================================================================
  [1]   Project Overview & Context Inspection
  [2]   Plan Engineering Task
  [3]   Execute Governed Engineering Task
  [4]   Agent Workforce Monitoring (72 Workers)
  [5]   AI Models & Providers Catalog
  [6]   Standard Engineering Workflows (WF-001 - WF-015)
  [7]   Quality Gates & Verification
  [8]   IDE & Platform Integrations
  [9]   Runtime Connections (Local / Remote)
  [10]  Diagnostics & System Health (Doctor)
  [11]  Platform Updates & Configuration
  [0]   Exit OpenClone CLI

Selection [0-11] or 'q' to quit:
```

---

## 3. Visual Design System

The visual design is built on minimal terminal principles:
- **Neutral Palette:** High-contrast white for primary content, subtle gray dividers (`#666666`), and dark backgrounds.
- **Limited Accent Accents:** Cyan for actions and selections, green for verified passes, amber for warnings, and red for errors.
- **Compact Badges:** Standard status markers: `[PASS]`, `[FAIL]`, `[WARN]`, `[INFO]`, `[ACTIVE]`.
- **Zero AI Clutter:** No multi-line ASCII art logos, no animation delays, no nested menus that obscure the terminal buffer.
- **Graceful Fallback:** Automatically detects `NO_COLOR`, non-tty pipes, or dumb terminals to output clean plain text.

---

## 4. Hybrid Connection Architecture

The `ConnectionManager` allows seamless toggling between local and remote OpenClone engines:
- **Local Target:** Direct Python in-process invocation of `AutonomousExecutionEngine` and `WorkforceControlPlane`.
- **Remote Target:** REST / MCP client over HTTPS with Bearer token authentication, TLS verification, and health check validation.
- **Runtime Target Banner:** Before executing mutations or planning, the CLI clearly renders the active target:
  ```text
  Runtime: local (ACTIVE) | Workspace: D:\New folder\OpenClone
  ------------------------------------------------------------------------
  ```

---

## 5. Standalone Packaging & Distribution (Retired)

> **Deprecation Notice:** The standalone CLI (`oc`, `oc.exe`, `oc.cmd`), PyInstaller spec (`oc.spec`), and Inno Setup CLI installer (`openclone_cli_installer.iss`) have been retired. OpenClone is now distributed exclusively as an extension-first Universal AI Engineering Platform via the Visual Studio Code Extension (`OpenClone-2.0.0.vsix`), Google Antigravity Plugin, and Python Core runtime package.

---

## 6. Verification Evidence

- `tests/test_oc_cli.py`: 12/12 passing tests covering Command Mode, Interactive Mode, Connection Manager, and UI formatting.
- Complete regression test suite: 410/410 tests passing (100% pass rate).
- Repository validation and link checks: 0 errors and 0 broken links across 995 Markdown files.
