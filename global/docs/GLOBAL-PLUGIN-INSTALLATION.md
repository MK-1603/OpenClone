# OpenClone 2.0 Global Plugin Installation & Lifecycle Guide

**Document ID:** `INSTALL-OC-2.0-GLOBAL-v2.0.0`  
**Product:** OpenClone 2.0 Universal AI Software Engineering Platform  
**Standard:** AISDF Standard 1.0.0  
**Status:** `NORMATIVE SPECIFICATION & USER MANUAL`  
**Author:** Release & Platform Engineering Team  

---

## 1. Zero-Clone Installation Principle

OpenClone 2.0 eliminates manual source repository cloning, submodules, and brittle symlinks for end users. The platform distributes as a **lightweight global plugin** (< 350 KB) that configures native AI coding assistants in seconds via a transactional installer engine.

### Quick Start (One Command)
```bash
# Automated global installation across detected IDEs
openclone install --all

# Or target a specific host
openclone install --host antigravity
openclone install --host claude
openclone install --host codex
openclone install --host cursor
```

---

## 2. Supported Host Environments & Detection Logic

The installer engine (`src/openclone/installer/engine.py`) detects installed coding environments using platform-native paths across Windows, macOS, and Linux:

| Host Environment | Detection Criteria | Global Installation Target | Scope | Status |
|---|---|---|---|---|
| **Google Antigravity** | `~/.gemini/antigravity/` | `~/.gemini/antigravity/plugins/openclone` | Global User | `VERIFIED` |
| **Claude Code** | `~/.claude.json` or `~/.claude/` | `~/.claude.json` (global mcpServers) | Global User | `VERIFIED` |
| **OpenAI Codex** | `~/.codex/` | `~/.codex/config.json` | Global User | `VERIFIED` |
| **Cursor** | `~/.cursor/` or `AppData/Cursor` | `~/.cursor/mcp.json` | Global User | `VERIFIED` |
| **Generic MCP** | Stdio command invocation | `openclone mcp` (stdio transport) | Client-defined | `VERIFIED` |

---

## 3. Comprehensive CLI Reference

The `openclone` CLI provides end-to-end lifecycle management:

### 3.1 `openclone doctor`
Audits system prerequisites, environment variables, detected hosts, write permissions, and network connectivity:
```bash
$ openclone doctor
[PASS] Python Runtime: 3.12.3 (Supported: >=3.10)
[PASS] Platform: Windows 11 (AMD64)
[PASS] Antigravity Detected: C:\Users\user\.gemini\antigravity
[PASS] Claude Code Detected: C:\Users\user\.claude.json
[PASS] Cursor Detected: C:\Users\user\.cursor
[PASS] Configuration Write Permissions: OK
[PASS] Cryptographic Engine: SHA-256 / HMAC available
Doctor Summary: 7 checks passed, 0 failed. System ready for OpenClone 2.0.
```

### 3.2 `openclone install`
Performs transactional installation into one or more detected AI environments:
```bash
# Dry run: preview file changes without writing to disk
openclone install --host antigravity --dry-run

# Interactive installation (prompts for host selection)
openclone install

# Unattended automated installation for all detected hosts
openclone install --all
```

**Installer Safety Guarantees:**
1. **Pre-modification Backup:** Automatically creates a timestamped copy (e.g. `~/.cursor/mcp.json.bak.1795372500`) before altering any existing configuration file.
2. **Atomic Writes:** Configuration writes are performed atomically to prevent partial corruption if the process is interrupted.
3. **OpenClone Ownership Isolation:** Only registers the `openclone` entry in existing configuration files; all user-defined servers and settings remain untouched.

### 3.3 `openclone status`
Reports active installations, registered host adapters, installed capability modules, and runtime health:
```bash
$ openclone status
OpenClone Version: 2.0.0
AISDF Standard: 1.0.0
Core Runtime Footprint: 348 KB

Installed Hosts:
  - Google Antigravity: ACTIVE (Global Plugin v2.0.0)
  - Claude Code: ACTIVE (MCP stdio v2.0.0)
  - Cursor: ACTIVE (MCP stdio v2.0.0)

Active Capability Packs:
  - openclone-core (348 KB) [REQUIRED]

Available Optional Modules:
  - mod-taste-skill-assets (35.76 MB) [NOT INSTALLED]
  - mod-knowledge-catalogues (0.55 MB) [NOT INSTALLED]
  - mod-workforce-extended (0.22 MB) [NOT INSTALLED]
```

### 3.4 `openclone modules`
Manages on-demand capability packs defined in [`modules/modules.manifest.json`](../../modules/modules.manifest.json):
```bash
# List available capability modules
openclone modules list

# Install an optional module
openclone modules install mod-knowledge-catalogues

# Remove an optional module
openclone modules remove mod-knowledge-catalogues
```

### 3.5 `openclone update`
Checks for updates and applies patches idempotently without overwriting custom local configuration:
```bash
openclone update
```

### 3.6 `openclone rollback`
Restores previous configuration states from the automated timestamped backups:
```bash
openclone rollback --host cursor
```

### 3.7 `openclone uninstall`
Safely removes OpenClone integration from specified hosts or all hosts:
```bash
# Uninstall from a single host
openclone uninstall --host antigravity

# Complete uninstallation from all hosts
openclone uninstall --all
```
*Note: Uninstallation completely cleans OpenClone keys and directories while restoring host configuration files to their original state.*

---

## 4. Manual Configuration Fallback

If you prefer to configure your environment manually without using the CLI, add the following JSON block to your host's MCP configuration file:

```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "openclone.mcp.server"],
      "env": {
        "OPENCLONE_ENV": "production"
      }
    }
  }
}
```
