# OpenClone Universal Multi-Host AI Coding-Tool Installation Guide
## Antigravity · Claude Code · OpenAI Codex · Cursor · VS Code · Generic MCP

**Version:** 2.0.0  
**Repository:** `https://github.com/MK-1603/OpenClone`  
**Distribution Policy:** Zero-Clone End-User Installation

---

# 1. Zero-Clone End-User Policy

End users installing OpenClone into their daily AI coding environment **DO NOT** need to:
- ❌ Manually clone `https://github.com/MK-1603/OpenClone`
- ❌ Enter an OpenClone source directory
- ❌ Run `pip install -e ".[dev]"`
- ❌ Install maintainer Python build dependencies
- ❌ Run OpenClone test suites just to activate the plugin
- ❌ Manually copy individual skill files

Each supported AI coding tool retrieves, stages, and loads OpenClone natively through its official plugin or marketplace installation mechanism.

---

# 2. Host-Specific End-User Installation

### 2.1 Google Antigravity

Antigravity installs plugins directly from the GitHub repository URL using the `agy` CLI:

```bash
# Install directly from GitHub
agy plugin install https://github.com/MK-1603/OpenClone

# Verify installation
agy plugin list
```

**What is loaded:**
- Portable Agent Skills (`skills/`)
- Specialist subagents (`agents/`)
- Governance rules (`rules/`)
- Local OpenClone MCP service (`mcpServers.openclone`)

---

### 2.2 Claude Code

Claude Code installs plugins via Git-backed marketplaces:

In your Claude Code terminal session:

```text
# 1. Add OpenClone marketplace
/plugin marketplace add MK-1603/OpenClone

# 2. Install OpenClone plugin
/plugin install openclone@openclone-marketplace

# 3. Reload active plugins
/reload-plugins

# 4. Verify installed plugins
/plugin
```

**What is loaded:**
- Canonical portable skills (`skills/`)
- Specialist role workflows & commands
- Native subagent delegation
- OpenClone MCP tools via `.mcp.json`

---

### 2.3 OpenAI Codex (CLI & ChatGPT Desktop)

Codex supports OpenAI Agent Plugins and repository marketplace sources:

In your Codex terminal:

```bash
# 1. Add OpenClone Git-backed marketplace
codex plugin marketplace add MK-1603/OpenClone

# 2. List or upgrade marketplace catalog
codex plugin marketplace list
codex plugin marketplace upgrade
```

Then in Codex (or Codex in ChatGPT desktop):
1. Open the **Plugins Directory**.
2. Select **OpenClone Engineering**.
3. Click **Install / Enable**.

#### Skills-Only Fallback
If running in an environment without full plugin marketplace UI, install portable skills to your user or project directory:
- User-level skills: `~/.agents/skills/`
- Project-level skills: `.agents/skills/`

---

### 2.4 Cursor

Cursor connects via native MCP server and project rules:

1. In Cursor, open **Settings > Features > MCP**.
2. Add a new MCP server:
   - **Name:** `openclone`
   - **Type:** `command`
   - **Command:** `python -m src.openclone.cli mcp` (or hosted Streamable HTTP endpoint)
3. For project-level rules, add [openclone.mdc](file:///d:/New%20folder/OpenClone/adapters/cursor/.cursor/rules/openclone.mdc) to `.cursor/rules/openclone.mdc`.

---

### 2.5 VS Code / GitHub Copilot / Continue / Generic MCP

For any MCP-compatible environment (VS Code MCP extension, Continue, Windsurf, Zed):

Add to your MCP configuration file:

```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "src.openclone.cli", "mcp"]
    }
  }
}
```

---

# 3. Global Capability & Conformance Matrix

| Host Environment | Native Package | Install from GitHub | Skills | Agents | Rules | MCP Tools | Verified Status |
|---|---|---|---|---|---|---|---|
| **Google Antigravity** | `plugin.json` | Yes, via `agy` CLI | ✅ VERIFIED | ✅ VERIFIED | ✅ VERIFIED | ✅ VERIFIED | `VERIFIED` |
| **Claude Code** | `.claude-plugin/` | Yes, marketplace add | ✅ VERIFIED | ✅ Native Subagents | ✅ Host-specific | ✅ VERIFIED | `VERIFIED` |
| **OpenAI Codex** | `.agents/plugins/` | Yes, `codex plugin` | ✅ VERIFIED | ✅ Host-dependent | ✅ AGENTS.md | ✅ VERIFIED | `VERIFIED` |
| **Cursor** | `.cursor/` rules + MCP | Manual config | ✅ VERIFIED | ✅ Prompted role | ✅ .cursorrules | ✅ VERIFIED | `VERIFIED` |
| **Gemini CLI** | Extension adapter | Host-dependent | ✅ VERIFIED | ✅ Prompted role | ✅ GEMINI.md | ✅ VERIFIED | `VERIFIED` |
| **VS Code / Copilot** | Extension MCP | Host-dependent | ✅ VERIFIED | ✅ Host-dependent | ✅ Workspace | ✅ VERIFIED | `VERIFIED` |
| **Generic MCP Client** | MCP Server (stdio) | MCP connect | N/A | N/A | N/A | ✅ VERIFIED | `VERIFIED` |

---

# 4. Maintainer & Contributor Development Workflow

*(Only for developers actively developing OpenClone itself)*

```bash
# Clone the repository
git clone https://github.com/MK-1603/OpenClone.git
cd OpenClone

# Install development dependencies
pip install -e ".[dev]"

# Run secret scanning audit
python tools/scan_secrets.py

# Run repository validation
python tools/validate_repository.py

# Run test suites
python -m pytest tests/
```
