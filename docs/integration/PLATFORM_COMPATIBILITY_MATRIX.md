# OpenClone Platform Compatibility Matrix
## Universal IDE, Editor, and AI Platform Support Matrix

**Version:** 1.0.0  
**Last Updated:** November 2026  
**Canonical Product:** OpenClone 2.0

---

## 1. Ecosystem Support Tiers

OpenClone evaluates platform integration support according to five formal maturity tiers:

- **`VERIFIED`**: Full end-to-end integration automated and verified against unit and integration test suites.
- **`PARTIALLY_SUPPORTED`**: Core protocol supported; manual configuration or specific environment prerequisites required.
- **`EXPERIMENTAL`**: Prototype adapter operational; subject to upstream platform protocol revisions.
- **`PROPOSED`**: Architectural contract defined; implementation planned for future release.
- **`UNSUPPORTED`**: Platform lacks necessary extensibility hooks or security boundaries.

---

## 2. Platform Compatibility Matrix

| Platform Identifier | Platform Name | Status | Supported Protocols | Minimum Version | Config Target | Automatic Setup |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `antigravity` | Google Antigravity IDE | `VERIFIED` | MCP, Plugin Skills, Rules | 1.0+ | `.gemini/antigravity/` | Yes (`oc platforms connect antigravity`) |
| `vscode` | Visual Studio Code | `VERIFIED` | MCP, Extension, Tasks | 1.85+ | `.vscode/mcp.json` | Yes (`oc platforms connect vscode`) |
| `cursor` | Cursor AI Editor | `VERIFIED` | MCP, System Rules | 0.40+ | `.cursor/mcp.json` | Yes (`oc platforms connect cursor`) |
| `jetbrains` | JetBrains IDEs (IntelliJ, PyCharm, etc.) | `VERIFIED` | MCP, External Tools | 2024.1+ | `.idea/mcp.json` | Yes (`oc platforms connect jetbrains`) |
| `zed` | Zed Editor | `VERIFIED` | ACP, MCP Context Server | 0.160+ | `.config/zed/settings.json` | Yes (`oc platforms connect zed`) |
| `claude-code` | Anthropic Claude Code CLI | `VERIFIED` | MCP stdio | 1.0+ | `.claude/mcp.json` | Yes (`oc platforms connect claude-code`) |
| `codex` | OpenAI Codex / CLI Agents | `PARTIALLY_SUPPORTED` | MCP stdio, REST API | 1.0+ | `codex.config.json` | Manual / Guided |
| `generic` | Generic MCP Client | `EXPERIMENTAL` | MCP stdio | RFC-MCP | `.openclone/mcp.json` | Yes (`oc platforms connect generic`) |

---

## 3. Protocol Capability Breakdown

| Capability / Tool | MCP Transport | ACP Protocol | REST API | CLI Subcommand |
| :--- | :---: | :---: | :---: | :---: |
| `openclone_inspect_repository` | YES | YES | YES | `oc autonomous inspect` |
| `openclone_get_project_context` | YES | YES | YES | `oc status` |
| `openclone_analyze_requirements`| YES | YES | YES | `oc autonomous understand` |
| `openclone_generate_plan` | YES | YES | YES | `oc plan` |
| `openclone_get_agent_status` | YES | YES | YES | `oc workers` |
| `openclone_get_execution_status`| YES | YES | YES | `oc status` |
| `openclone_get_verification_results`| YES | YES | YES | `oc check list` |
| `openclone_get_delivery_report` | YES | YES | YES | `oc findings list` |
| `openclone_execute_task` (Governed) | YES (Gated) | YES (Gated) | YES (Gated) | `oc run` |

---

## 4. Platform Discovery Criteria

The `PlatformDiscoveryEngine` detects platforms through the following checks:

1. **Executable Presence:** Locates binary on system `$PATH` (e.g. `code.cmd`, `cursor.cmd`, `zed.exe`).
2. **Standard Config Directories:**
   - Antigravity: `%USERPROFILE%\.gemini\antigravity\`
   - VS Code: `%APPDATA%\Code\User\` or `%USERPROFILE%\.vscode\`
   - Cursor: `%APPDATA%\Cursor\User\` or `%USERPROFILE%\.cursor\`
   - JetBrains: `%APPDATA%\JetBrains\` or active `.idea\` in workspace root
   - Zed: `%APPDATA%\Zed\` or `%USERPROFILE%\.config\zed\`
3. **Workspace Markers:** Detects workspace-level configuration folders in project roots.
