# OpenClone Antigravity Integration Guide
## Google Antigravity IDE Integration Specification & Plugin Package

**Version:** 1.0.0  
**Target:** Google Antigravity IDE / Antigravity Agent Runtime  
**Canonical Product:** OpenClone 2.0

---

## 1. Overview

Google Antigravity is a premier agentic development environment. The OpenClone Antigravity Integration embeds OpenClone's 31 engineering domains, 56 capability engines, and 12-stage autonomous execution engine natively into Antigravity.

---

## 2. Integration Architecture

OpenClone integrates into Antigravity across five native capability layers:

1. **Antigravity MCP Server:** Standardized tool exposure for workspace inspection, plan generation, agent status, and governed execution.
2. **OpenClone Specialized Skill (`openclone-engineering`):** A custom Antigravity skill containing procedures, domain knowledge, and execution guidelines (`SKILL.md`).
3. **Antigravity Rule Configuration (`.openclone/antigravity.rules` / `AGENTS.md`):** Deterministic governance and truthfulness rules for Antigravity agents.
4. **Subagent Delegation:** Mapping OpenClone worker contracts (architect, security auditor, tester, release engineer) to Antigravity subagent types.
5. **Lifecycle Hooks:** SessionStart and PreCommit hooks that audit repository health and verify ledger integrity.

---

## 3. Native Antigravity Plugin Package Structure

The plugin package resides at `integrations/antigravity/` and is installed automatically into `%USERPROFILE%\.gemini\antigravity\plugins\openclone\`:

```text
integrations/antigravity/
|-- plugin.json                     # Antigravity plugin manifest
|-- mcp.json                        # MCP server registration
|-- skills/
|   `-- openclone-engineering/
|       `-- SKILL.md                # Specialized engineering skill
|-- rules/
|   `-- governance.md               # Deterministic governance rules
`-- agents/
    `-- openclone-autonomous.json   # Subagent specification
```

### 3.1. Plugin Manifest (`plugin.json`)
```json
{
  "id": "openclone-engineering-suite",
  "name": "OpenClone Universal Engineering Platform",
  "version": "2.0.0",
  "description": "Autonomous engineering execution engine, workforce coordination, and governance suite for Google Antigravity.",
  "author": "OpenClone Contributors",
  "engines": {
    "antigravity": ">=1.0.0"
  },
  "mcpServers": {
    "openclone": {
      "command": "oc.exe",
      "args": ["mcp"]
    }
  },
  "skills": ["skills/openclone-engineering"]
}
```

---

## 4. Automated Installation via CLI

Install or connect Antigravity with a single command:

```bash
# Discover local Antigravity installation
oc platforms discover

# Connect OpenClone to Antigravity
oc platforms connect antigravity

# Check integration status
oc platforms status
```

The CLI:
1. Detects Antigravity configuration directory (`%USERPROFILE%\.gemini\antigravity`).
2. Creates a timestamped safety backup of any existing plugin or MCP settings.
3. Deploys the plugin manifest, skills, and MCP configuration.
4. Performs a loopback health check.
