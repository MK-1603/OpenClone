# OpenClone Repository and Distribution Architecture
## Lean Core, Native Host Adapters, and Progressive Disclosure

**Version:** 1.0.0  
**Standard:** AISDF Standard 1.0.0 / OpenClone Platform 1.0.0  
**Status:** `ARCHITECTURAL STANDARD`

---

## 1. Architectural Philosophy

OpenClone decouples the **source repository** from the **installed plugin artifact**:

- **The Source Repository (`MK-1603/OpenClone`):** Contains the complete framework development suite, test harnesses, maintainer validators, historical archives, and full reference encyclopedias (~41.5 MB).
- **The End-User Plugin Artifact (< 350 KB):** Contains strictly the minimal canonical core runtime, essential schemas, and the native adapter package required by the user's specific AI coding environment.
- **The Optional Capability Packs:** Specialized engineering workforce, deep catalogues, and extended UI/UX assets that are fetched or loaded only on demand.

```text
                 OPENCLONE RELEASE
                       |
             +---------+---------+
             |                   |
        INSTALLER             RELEASE INDEX
             |                   |
       Small host adapter        |
             |                   |
       Minimal core runtime      |
             |                   |
       Optional module manifest -+
             |
       Install selected host
             |
       Load optional modules only when needed
```

---

## 2. Three-Layer Distribution Model

### Layer A: Bootstrap Installer (`src/openclone/installer/`)
A lightweight, zero-dependency installation engine:
- **Footprint:** < 50 KB.
- **Capabilities:**
  - Automated detection of installed AI hosts (`detect_hosts`).
  - Preflight environment diagnostics (`openclone doctor`).
  - Transactional installation with automated configuration backups (`.openclone/backups/`).
  - Security containment checks rejecting path traversal escapes.
  - Manifest-backed uninstallation restoring original user configurations.

### Layer B: Core Plugin (`src/openclone/`)
The single canonical foundation shared across all AI coding environments:
- **Footprint:** ~300 KB.
- **Components:**
  - 15 canonical capabilities (`src/openclone/integrations/capabilities.py`).
  - Shared MCP JSON-RPC 2.0 service (`src/openclone/mcp/server.py`).
  - Cryptographic human approval gateway (`src/openclone/integrations/gateway.py`).
  - 22-phase lifecycle engine contracts (`src/openclone/lifecycle/`).
  - Root `plugin.json` and 16 specialist agent markdown definitions.

### Layer C: On-Demand Capability Packs (`modules/`)
Decoupled modules defined in [`modules/modules.manifest.json`](../../modules/modules.manifest.json):
- **`mod-specialist-workforce`:** 72 specialist roles across 12 disciplines (`workforce/`).
- **`mod-knowledge-catalogues`:** Master engineering encyclopedias (`docs/knowledge-catalogues/`).
- **`mod-ui-ux-design`:** Taste Skill anti-slop rules, tokens, and contrast checks (`domains/05-UX-UI-ENGINEERING/`).
- **`mod-security-hardened`:** 19-point SaaS security baseline and pinned scanner locks (`docs/security/`).
- **`mod-project-lifecycle`:** 10 project-type lifecycle packs and quality gate schemas (`docs/engineering-lifecycle/`).
- **`mod-taste-skill-assets`:** Heavy visual renders, photo kits, and scene assets (~35 MB), excluded from default installs.

---

## 3. Progressive Disclosure & Context Budgeting

Dumping thousands of catalogue topics and 72 agent roles into every AI model prompt causes context pollution, memory degradation, and high token costs. OpenClone enforces a strict **progressive disclosure hierarchy**:

1. **Base Session Context (< 4 KB):**
   - Ingests `AGENTS.md` (operating contract) and active `PROJECT.md` (project requirements).
   - Core prompt overhead is minimized.
2. **Phase-Specific Context (< 10 KB):**
   - Ingests guidelines for the active phase only (e.g. `domains/05-UX-UI-ENGINEERING/` during UI design).
3. **Specialist Role Context:**
   - Ingests specific specialist agent definitions only when delegated by the orchestrator.
4. **Dynamic Reference Ingestion:**
   - Deep topics are queried on-the-fly via MCP tool calls (`openclone_get_guidance` or `openclone_search_knowledge`) rather than pre-loaded into prompt memory.
