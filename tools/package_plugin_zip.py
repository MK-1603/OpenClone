#!/usr/bin/env python3
"""Build OpenClone Universal Plugin Redistributable ZIP Package.

Packages the complete OpenClone AI plugin bundle conforming to Antigravity,
Claude Code, Cursor, ChatGPT, and VS Code specifications into a clean,
production-ready ZIP archive.
"""
from __future__ import annotations

import io
import json
import os
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / "dist" / "plugin-staging"
OUTPUT_ZIP = ROOT / "openclone-plugin-v2.0.0.zip"
DIST_ZIP = ROOT / "dist" / "openclone-plugin-v2.0.0.zip"


def create_plugin_readme() -> str:
    return """# OpenClone v2.0.0 — Universal AI Engineering Plugin

**Official Production Plugin Package for Google Antigravity, Claude, ChatGPT, Cursor, and VS Code**  
*Version: 2.0.0 | Standard: AISDF Universal AI Software Development Framework*

---

## What Is Included in This Plugin

This self-contained plugin package equips any AI coding assistant or IDE with the complete OpenClone engineering standard:

- **18 Specialized Engineering Skills:** Anti-AI-slop design governance (Taste Skill v2.6.0), Universal Project Intelligence, Product Discovery, Architecture Design, Requirements Engineering, Security Baselines, and Testing/Verification.
- **16 Specialist Workforce Agents:** Orchestrator, Product Architect, Requirements Agent, Frontend Engineer, Backend Engineer, Database Engineer, Security Reviewer, Test Automation Engineer, and Independent Verifier.
- **4 Deterministic Operating Rules:** AGENTS.md, Anti-Slop, Cryptographic Evidence, and SaaS Security Baseline.
- **Universal Master Prompt Template:** `OPENCLONE-UNIVERSAL-MASTER-PROMPT-TEMPLATE.md` enforcing Phase 0 Sets A, B, C, D and human approval gates.
- **22 Model Context Protocol (MCP) Tools:** Exposing project classification, architecture blueprinting, brand engineering, model routing, and workforce governance.

---

## Installation Guide for All AI Tools

### 1. Google Antigravity
You can install this plugin directly via the Antigravity CLI or UI:

**Via CLI (Direct URL or Path):**
```bash
# Direct from GitHub:
agy plugin install https://github.com/MK-1603/OpenClone

# Or from this unzipped folder:
agy plugin install ./openclone-plugin
```

**Via Antigravity UI:**
1. Open Antigravity Settings ➔ **Plugins**.
2. Click **Install Plugin from Directory** or **Install from Archive**.
3. Select this folder (or `openclone-plugin-v2.0.0.zip`).
4. All 18 skills, 16 agents, and MCP tools are immediately activated.

---

### 2. Claude Desktop & Claude Code

#### A. Claude Code (CLI)
Run a single command to add OpenClone as a background MCP plugin:
```bash
pip install git+https://github.com/MK-1603/OpenClone.git
claude mcp add openclone python -m openclone.mcp.server
```

#### B. Claude Desktop (GUI App)
1. Open Claude Desktop Settings ➔ **Developer** ➔ **Edit Config**.
2. Add the following to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "openclone.mcp.server"]
    }
  }
}
```
*(Ensure `pip install git+https://github.com/MK-1603/OpenClone.git` has been run).*

---

### 3. ChatGPT (Custom GPT & Actions)

Connect OpenClone tools to any ChatGPT Custom GPT:

1. Open ChatGPT ➔ **Explore GPTs** ➔ **Create a GPT** ➔ **Configure**.
2. **Name:** `OpenClone Software Architect`
3. **Instructions:** Copy the content from `prompts/custom-gpt-instructions.md`.
4. **Actions (API Tools):**
   * Click **Create new action**.
   * Under **Schema**, paste the content from `adapters/chatgpt_openapi.json` (or import URL: `https://raw.githubusercontent.com/MK-1603/OpenClone/main/global/hosts/chatgpt/openapi.json`).
5. Save and publish. ChatGPT now has access to all OpenClone tools.

---

### 4. Cursor & Windsurf

1. Install the OpenClone package globally:
   ```bash
   pip install git+https://github.com/MK-1603/OpenClone.git
   ```
2. In Cursor, open **Settings** ➔ **Features** ➔ **MCP Servers** (or edit `~/.cursor/mcp.json`):
   ```json
   {
     "mcpServers": {
       "openclone": {
         "command": "python",
         "args": ["-m", "openclone.mcp.server"]
       }
     }
   }
   ```
3. Copy `rules/openclone.mdc` into your project's `.cursor/rules/` directory to enforce anti-slop and evidence rules in editor chats.

---

### 5. VS Code (Via MCP or Extension)

1. Ensure the Python environment has `openclone` installed (`pip install git+https://github.com/MK-1603/OpenClone.git`).
2. Add `adapters/vscode_mcp.json` settings to your `.vscode/settings.json` or MCP manager.
3. Open any workspace and call OpenClone tools from your AI assistant.

---

## Verification Quick Check
Verify that the OpenClone engine is active:
```bash
python -c "import openclone; print('OpenClone v' + openclone.__version__ + ' active')"
```

---
*License: MIT | Copyright (c) 2026 OpenClone Contributors*
"""


def build_plugin_bundle():
    print("Building OpenClone Universal Plugin Bundle...")
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Root plugin.json
    plugin_manifest = {
        "$schema": "https://antigravity.google/schemas/v1/plugin.json",
        "name": "openclone",
        "displayName": "OpenClone Universal Engineering",
        "version": "2.0.0",
        "description": "Universal AI software engineering framework: 18 specialist skills, 16 autonomous workforce agents, Taste Skill anti-slop governance, 19-point SaaS security baseline, and 22 MCP tools.",
        "author": "OpenClone Contributors",
        "license": "MIT",
        "homepage": "https://github.com/MK-1603/OpenClone",
        "logo": "assets/logo.png",
        "icon": "assets/icon.png",
        "skills": [
            "skills/taste-skill",
            "skills/universal-project-intelligence",
            "skills/frontend-engineering",
            "skills/design-system-engineering",
            "skills/responsive-engineering",
            "skills/accessibility-engineering",
            "skills/backend-architecture",
            "skills/database-engineering",
            "skills/api-engineering",
            "skills/system-design-engineering",
            "skills/product-discovery",
            "skills/requirements-engineering",
            "skills/architecture-design",
            "skills/ui-ux-engineering",
            "skills/secure-engineering",
            "skills/testing-verification",
            "skills/typography-standards",
            "skills/ux-pro"
        ],
        "agents": [
            "agents/orchestrator.md",
            "agents/product-requirements-agent.md",
            "agents/product-architect-agent.md",
            "agents/frontend-agent.md",
            "agents/backend-agent.md",
            "agents/database-agent.md",
            "agents/security-agent.md",
            "agents/test-qa-agent.md",
            "agents/independent-verifier-agent.md",
            "agents/ai-engineering-agent.md",
            "agents/devops-release-agent.md",
            "agents/documentation-agent.md",
            "agents/integration-agent.md",
            "agents/performance-reliability-agent.md",
            "agents/ui-design-agent.md",
            "agents/ux-research-agent.md"
        ],
        "rules": [
            "rules/AGENTS.md",
            "rules/anti-slop.md",
            "rules/evidence.md",
            "rules/security.md"
        ],
        "suggestedPrompts": [
            "Initialize Phase 0 discovery and author Sets A, B, C, D for this idea.",
            "Audit this interface against Taste Skill v2.6.0 anti-slop typography and contrast standards.",
            "Assemble a specialist engineering team with topological handoff dependencies.",
            "Run automated verification gate and check audit ledger integrity."
        ],
        "mcpServers": {
            "openclone": {
                "command": "python",
                "args": ["-m", "src.openclone.mcp.server"]
            }
        }
    }
    (BUILD_DIR / "plugin.json").write_text(json.dumps(plugin_manifest, indent=2), encoding="utf-8")

    # 2. Assets (logo & icons)
    assets_dir = BUILD_DIR / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    src_logo_png = ROOT / "assets" / "branding" / "openclone-logo.png"
    src_logo_svg = ROOT / "assets" / "branding" / "openclone-logo.svg"
    src_icon_png = ROOT / "assets" / "branding" / "app-icons" / "icon-256.png"
    if not src_icon_png.exists():
        src_icon_png = ROOT / "assets" / "branding" / "openclone-logo.png"

    if src_logo_png.exists():
        shutil.copy2(src_logo_png, assets_dir / "logo.png")
    if src_logo_svg.exists():
        shutil.copy2(src_logo_svg, assets_dir / "logo.svg")
    if src_icon_png.exists():
        shutil.copy2(src_icon_png, assets_dir / "icon.png")

    # 3. Copy Skills
    dest_skills = BUILD_DIR / "skills"
    src_skills = ROOT / "skills"
    if src_skills.exists():
        shutil.copytree(src_skills, dest_skills, dirs_exist_ok=True)

    # 4. Copy Agents
    dest_agents = BUILD_DIR / "agents"
    src_agents = ROOT / "agents"
    if src_agents.exists():
        shutil.copytree(src_agents, dest_agents, dirs_exist_ok=True)

    # 5. Copy Rules
    dest_rules = BUILD_DIR / "rules"
    src_rules = ROOT / "rules"
    if src_rules.exists():
        shutil.copytree(src_rules, dest_rules, dirs_exist_ok=True)

    # 6. Copy Prompts
    dest_prompts = BUILD_DIR / "prompts"
    src_prompts = ROOT / "framework" / "prompts"
    if src_prompts.exists():
        shutil.copytree(src_prompts, dest_prompts, dirs_exist_ok=True)

    # Copy Custom GPT instructions
    gpt_inst = ROOT / "global" / "hosts" / "chatgpt" / "custom-gpt-instructions.md"
    if gpt_inst.exists():
        shutil.copy2(gpt_inst, dest_prompts / "custom-gpt-instructions.md")

    # 7. Copy Adapters & MCP configs
    dest_adapters = BUILD_DIR / "adapters"
    dest_adapters.mkdir(parents=True, exist_ok=True)

    chatgpt_openapi = ROOT / "global" / "hosts" / "chatgpt" / "openapi.json"
    if chatgpt_openapi.exists():
        shutil.copy2(chatgpt_openapi, dest_adapters / "chatgpt_openapi.json")

    claude_mcp = {
        "mcpServers": {
            "openclone": {
                "command": "python",
                "args": ["-m", "openclone.mcp.server"]
            }
        }
    }
    (dest_adapters / "claude_desktop_config.json").write_text(json.dumps(claude_mcp, indent=2), encoding="utf-8")
    (dest_adapters / "cursor_mcp.json").write_text(json.dumps(claude_mcp, indent=2), encoding="utf-8")
    (dest_adapters / "vscode_mcp.json").write_text(json.dumps(claude_mcp, indent=2), encoding="utf-8")

    cursor_rule = ROOT / "adapters" / "cursor" / ".cursor" / "rules" / "openclone-project-rule.template.mdc"
    if cursor_rule.exists():
        dest_rules.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cursor_rule, dest_rules / "openclone.mdc")

    # 8. README.md, LICENSE, VERSION
    (BUILD_DIR / "README.md").write_text(create_plugin_readme(), encoding="utf-8")
    shutil.copy2(ROOT / "LICENSE", BUILD_DIR / "LICENSE")
    (BUILD_DIR / "VERSION").write_text("2.0.0\n", encoding="utf-8")

    # 9. Create ZIP
    DIST_ZIP.parent.mkdir(parents=True, exist_ok=True)
    for zip_path in [OUTPUT_ZIP, DIST_ZIP]:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root_path, dirs, files in os.walk(BUILD_DIR):
                for f in files:
                    full_p = Path(root_path) / f
                    rel_p = full_p.relative_to(BUILD_DIR)
                    zf.write(full_p, arcname=str(rel_p))
        print(f"Created: {zip_path} ({zip_path.stat().st_size:,} bytes)")

    # 10. Clean up staging
    shutil.rmtree(BUILD_DIR)
    print("Build complete! Clean redistributable plugin ZIP generated.")


if __name__ == "__main__":
    build_plugin_bundle()
