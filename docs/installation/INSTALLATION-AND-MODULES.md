# OpenClone Installation and Capability Modules Guide

**Version:** 1.0.0  
**Standard:** AISDF Standard 1.0.0 / OpenClone Platform 1.0.0  
**Status:** `USER & OPERATIONAL GUIDE`

---

## 1. Zero-Clone Installation Routes

OpenClone is packaged to allow application developers to install and use the framework without manually cloning the source repository:

### Route A: Direct Host Plugin Installation (No Python Setup Required)
- **Google Antigravity:**
  ```bash
  agy plugin install https://github.com/MK-1603/OpenClone
  ```
- **Claude Code:**
  ```text
  /plugin marketplace add MK-1603/OpenClone
  /plugin install openclone@openclone-marketplace
  ```
- **OpenAI Codex:**
  ```bash
  codex plugin marketplace add MK-1603/OpenClone
  ```

### Route B: OpenClone Transactional CLI Installer
Developers with Python (>= 3.10) can use the built-in installer to configure any supported host in their workspace or user profile:

```bash
# 1. Verify environmental health
python -m src.openclone.cli doctor

# 2. Inspect detected AI coding environments
python -m src.openclone.cli status

# 3. Install adapter for a specific host
python -m src.openclone.cli install cursor --scope workspace
python -m src.openclone.cli install antigravity --scope user
python -m src.openclone.cli install claude_code
python -m src.openclone.cli install codex

# 4. Preview installation without writing files
python -m src.openclone.cli install cursor --dry-run
```

---

## 2. Managing On-Demand Capability Modules

OpenClone provides capability modules that can be discovered and enabled on demand:

See [`modules/modules.manifest.json`](../../modules/modules.manifest.json) for the full module catalog:

| Module ID | Description | Default Loading Mode | Path |
|---|---|:---:|---|
| `mod-specialist-workforce` | 72 specialist roles across 12 teams | On-Demand | `workforce/` |
| `mod-knowledge-catalogues` | Master engineering encyclopedias | Lazy-Loaded | `docs/knowledge-catalogues/` |
| `mod-ui-ux-design` | Taste Skill anti-slop rules and tokens | On-Demand | `domains/05-UX-UI-ENGINEERING/` |
| `mod-security-hardened` | 19-point SaaS security baseline | On-Demand | `docs/security/` |
| `mod-project-lifecycle` | 22-phase lifecycle packs and gates | On-Demand | `docs/engineering-lifecycle/` |
| `mod-taste-skill-assets` | Heavy 3D renders and photo assets (~35MB) | Lazy-Loaded | `skills/taste-skill/` |

---

## 3. Safe Updates, Rollback, and Uninstallation

### Updating Adapters
```bash
python -m src.openclone.cli update cursor
```
The updater verifies the new version, stages changes, and atomically replaces files while preserving existing user settings.

### Rolling Back
```bash
python -m src.openclone.cli rollback cursor
```
Restores the prior configuration state from `.openclone/backups/`.

### Clean Uninstallation
```bash
python -m src.openclone.cli uninstall cursor
```
- Removes **ONLY** OpenClone-owned files recorded in `.openclone/install-manifest.json`.
- Automatically restores any pre-existing user configurations from backup.
- Preserves all user source code and project data intact.
