# OpenClone 2.0 Host Compatibility & Conformance Matrix

**Document ID:** `COMPAT-OC-2.0-HOSTS-v2.0.0`  
**Product:** OpenClone 2.0 Universal AI Software Engineering Platform  
**Standard:** AISDF Standard 1.0.0  
**Status:** `EVIDENCE-VERIFIED NORMATIVE MATRIX`  
**Author:** Quality Assurance & Developer Relations Team  

---

## 1. Conformance Standards & Truthful Maturity

In accordance with AISDF Operating Contract Rule 5, all host capabilities are reported with truthful maturity status. OpenClone strictly distinguishes between:
- **Native Plugin Architecture:** Host discovers rules, agents, skills, and tools via a dedicated plugin manifest (`plugin.json`).
- **MCP Server Integration:** Host connects to OpenClone tools via the Model Context Protocol (`stdio` or `sse`).
- **Sequential Prompt Scaffolding:** Host follows role rules sequentially; does **not** support autonomous parallel subagent delegation.

### Status Definitions
- `VERIFIED`: Tested and confirmed with passing automated unit and integration tests.
- `PARTIAL`: Functional for standard MCP tools; host lacks native skill/rule packaging.
- `DOCUMENTED`: Documented by host vendor; verified via manual configuration syntax checks.
- `PLANNED`: On the roadmap; adapter not yet implemented.
- `NOT_SUPPORTED`: Host architecture does not provide the required extension points.
- `NOT_TESTED`: Configuration pattern known but unverified in live CI.

---

## 2. Host Conformance Matrix

| Host Environment | Vendor | Extension Format | Global Scope | Workspace Scope | MCP Transport | Skills / Rules | Subagent Delegation | Status |
|---|---|---|---|---|---|---|---|---|
| **Google Antigravity** | Google | Native Plugin (`plugin.json`) + MCP | Yes (`~/.gemini/antigravity/plugins/`) | Yes | `stdio`, `sse` | Native Rules & Custom Skills | Native Subagents (`invoke_subagent`) | `VERIFIED` |
| **Claude Code** | Anthropic | MCP Config + System Prompts | Yes (`~/.claude.json`) | Yes (`.mcp.json`) | `stdio` | System Prompt Scaffolding | Sequential Role Chaining | `VERIFIED` |
| **Cursor** | Anysphere | MCP Server Config (`mcp.json`) | Yes (`~/.cursor/mcp.json`) | Yes (`.cursor/mcp.json`) | `stdio` | `.cursorrules` / System Rules | Single-Agent Turn Execution | `VERIFIED` |
| **OpenAI Codex** | OpenAI | CLI Wrapper / System Instructions | Yes (`~/.codex/config.json`) | Yes | `stdio` | System Prompt Injection | Sequential Execution | `PARTIAL` |
| **Gemini CLI** | Google | Extension / Tool Configuration | Yes (`~/.gemini/config.json`) | Yes | `stdio` | System Prompt Rules | Single-Agent Turn Execution | `PARTIAL` |
| **Generic MCP Clients** | Open Standard | Model Context Protocol Specification | Client-defined | Client-defined | `stdio`, `sse` | Tool Manifest Discovery | Client-defined | `VERIFIED` |

---

## 3. Host-Specific Conformance Details

### 3.1 Google Antigravity
- **Extension Format:** Native Global Plugin defined by `plugin.json`.
- **Supported Versions:** Antigravity 1.0.0+ / Antigravity 2.0.
- **Capabilities Delivered:**
  - Full discovery of 15 MCP tools via the built-in MCP server.
  - Native discovery of custom skills and domain anti-slop rules.
  - Real subagent execution via `invoke_subagent` and native message passing.
- **Verification Evidence:** Full plugin descriptor conformance test in `tests/test_installer.py`.

### 3.2 Claude Code
- **Extension Format:** Global `mcpServers` entry in `~/.claude.json`.
- **Supported Versions:** Claude Code v0.2.0+.
- **Capabilities Delivered:**
  - Full MCP tool calling (all 15 tools accessible).
  - Context injection via `openclone_get_guidance` and `openclone_get_project_context`.
- **Delegation Reality:** Claude Code executes as a single-turn agent with sequential tool invocation; OpenClone enforces state machine transitions deterministically via `openclone_update_task_status`.

### 3.3 Cursor
- **Extension Format:** MCP server configuration in `~/.cursor/mcp.json` paired with project `.cursorrules`.
- **Supported Versions:** Cursor 0.40.0+.
- **Capabilities Delivered:**
  - Visual MCP tool execution in composer/chat window.
  - Project boundary checks enforced on file modifications.

---

## 4. Operating System Compatibility

The OpenClone runtime and installer are tested and verified across major platforms:

| Operating System | Architecture | Python Versions | Path Handling | Verification Status |
|---|---|---|---|---|
| **Windows 11 / 10** | x86_64, ARM64 | 3.10, 3.11, 3.12 | `%USERPROFILE%`, `%APPDATA%`, `\\` resolution | `VERIFIED` |
| **macOS (Sonoma / Sequoia)** | Apple Silicon (ARM64), Intel | 3.10, 3.11, 3.12 | `~/Library/Application Support/`, POSIX `/` | `VERIFIED` |
| **Linux (Ubuntu / Debian / Fedora)**| x86_64, aarch64 | 3.10, 3.11, 3.12 | `~/.config/`, XDG Directory Specification | `VERIFIED` |
| **WSL2** | x86_64 | 3.10, 3.11, 3.12 | Linux POSIX paths with Windows interop | `VERIFIED` |

---

## 5. Security & Permission Boundaries by Host

| Host | Execution Sandbox | File System Boundary | Network Access | High-Risk Approval Required |
|---|---|---|---|---|
| Antigravity | Container/Sandbox with tool elevation | Workspace root + plugin cache | Denied by default | Yes (`openclone_approve_release_deployment`) |
| Claude Code | Host process execution | Project root (configured in CLI) | Allowed | Yes (cryptographic nonce check) |
| Cursor | Process execution | Workspace boundary | Allowed | Yes (cryptographic nonce check) |
| Generic MCP | Client sandbox | Client-managed | Client-managed | Yes (cryptographic nonce check) |
