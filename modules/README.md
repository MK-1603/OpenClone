# OpenClone Modular Capability Architecture

OpenClone organizes capabilities into a **lean, progressive-disclosure architecture** that decouples the lightweight core plugin from heavy optional modules and extended knowledge assets.

---

## 1. Three-Layer Distribution Model

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

### Layer A: Bootstrap Installer (`src/openclone/installer/`)
- Thin command-line installer (< 50 KB).
- Automated host detection across Google Antigravity, Claude Code, OpenAI Codex, Cursor, and Generic MCP.
- Transactional installation, safety backups, path containment checks, and clean uninstallation.
- Environmental diagnostics via `openclone doctor`.

### Layer B: Core Plugin (`src/openclone/`)
- Canonical OpenClone capability registry (15 capabilities).
- Shared MCP service (`src/openclone/mcp/server.py`) exposing core inspection tools over stdio/SSE.
- Deterministic policy engine and cryptographic human approval validator (`src/openclone/integrations/gateway.py`).
- Root `plugin.json` and 16 specialist agent definitions for zero-clone direct installation.

### Layer C: On-Demand Capability Packs (`modules/modules.manifest.json`)
Specialist capability modules loaded on demand only when required by specific project types or tasks:

1. **`mod-specialist-workforce` (`workforce/`):** 72 specialist roles across 12 disciplines. Loaded into context only when assigned to a specific task.
2. **`mod-knowledge-catalogues` (`docs/knowledge-catalogues/`):** Master software engineering encyclopedias (232 UI styles, 580 backend topics, 1,095 AI topics, 365 motion concepts).
3. **`mod-ui-ux-design` (`domains/05-UX-UI-ENGINEERING/`):** Taste Skill anti-slop rules, design tokens, and typography rhythm.
4. **`mod-security-hardened` (`docs/security/`):** 19-point SaaS security baseline and 12 pinned static analysis scanner locks.
5. **`mod-project-lifecycle` (`docs/engineering-lifecycle/`):** 22-phase lifecycle packs, quality gates, and V0–V5 evidence engine.
6. **`mod-taste-skill-assets` (`skills/taste-skill/`):** Heavy photo kits, 3D renders, and scene assets (~35 MB), excluded from default end-user plugin installations.

---

## 2. Progressive Disclosure in AI Coding Environments

Rather than dumping all 72 agent roles and 2,000+ catalogue topics into every AI prompt context, OpenClone enforces **progressive disclosure**:

1. **Core Context (< 4 KB):** Loads only `AGENTS.md` operating contract and active project architecture `PROJECT.md`.
2. **Task Phase Context:** When advancing to a specific phase (e.g. `PHASE_04_UI_UX_DESIGN`), loads only the matching domain guidelines.
3. **Specialist Role Context:** Invokes specific specialist agents (e.g. `product-architect-agent.md`, `security-auditor-agent.md`) only when delegated.
4. **Reference Retrieval:** Deep knowledge catalogues are queried dynamically via the MCP tool `openclone_search_knowledge` or `openclone_get_guidance`.

---

## 3. Module Manifest

See [`modules.manifest.json`](modules.manifest.json) for machine-readable schemas, version pins, dependency declarations, and size estimates for all capability modules.
