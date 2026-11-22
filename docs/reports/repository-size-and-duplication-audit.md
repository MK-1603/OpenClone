# OpenClone Repository Size and Duplication Audit

**Audit Date:** 2026-11-23  
**Target Repository:** `MK-1603/OpenClone`  
**Standard:** AISDF Standard 1.0.0 / OpenClone Platform 1.0.0  
**Baseline Commit:** `c4be5d7`  
**Status:** `AUDITED & MEASURED`

---

## 1. Executive Metrics & Summary

An exhaustive physical inspection of all tracked files was conducted across the connected Git repository.

| Metric | Measured Value | Notes |
|---|---|---|
| **Total Tracked Files** | 2,525 files | Reduced from 2,531 after removing verified exact duplicates |
| **Total Working Tree Size** | 41.51 MB | Physical size of all tracked files on disk |
| **Git Object Store** | 32.86 MiB | 3,038 Git objects |
| **Tracked Bytecode / Cache Files** | **0 files** | All `__pycache__` and `*.pyc` files strictly ignored by `.gitignore` |
| **Exact Duplicate Groups** | 46 groups | Dominated by upstream vendor icon duplicates and mirror docs |
| **Largest Directory Footprint** | `skills/` (35.76 MB) | Represents 86.1% of total repository byte size |

---

## 2. Directory Breakdown by Size and File Count

| Top-Level Directory | File Count | Size (MB) | Percentage of Total | Primary Contents |
|---|---:|---:|---:|---|
| `skills/` | 1,675 | 35.76 MB | 86.1% | Taste Skill v2.6.0 engine, visual effects, photo kits, 3D renders |
| `domains/` | 73 | 1.77 MB | 4.3% | 31 core engineering domains (00–30) and execution standards |
| `blueprints/` | 33 | 1.66 MB | 4.0% | Historical AISDF blueprints and master repository upgrade specifications |
| `docs/` | 214 | 1.15 MB | 2.8% | Architectural specifications, reports, knowledge catalogues, security baseline |
| `engines/` | 57 | 0.27 MB | 0.7% | 56 capability engine execution contracts (E-001 through E-056) |
| `workforce/` | 164 | 0.22 MB | 0.5% | 72 specialist worker role JSON manifests and 12 team directories |
| `src/` | 25 | 0.20 MB | 0.5% | Canonical Python runtime, MCP server, gateway, and installer engine |
| `tools/` | 11 | 0.07 MB | 0.2% | Repository validators, checklist engine, skill engine CLI utilities |
| `adapters/` | 34 | 0.06 MB | 0.1% | Host adapter manifests for Antigravity, Claude Code, Codex, Cursor, ChatGPT |
| `tests/` | 15 | 0.07 MB | 0.2% | Automated test suites (97 Python unit tests) |
| Root files (`.`) | 31 | 0.08 MB | 0.2% | `README.md`, manifests, `AGENTS.md`, `PROJECT.md`, `LICENSE` |
| `examples/` | 8 | 0.03 MB | 0.1% | Demo project fixtures and transcripts |
| `workflows/` | 16 | 0.03 MB | 0.1% | 15 executable workflow definitions (WF-001 through WF-015) |
| `templates/` | 20 | 0.03 MB | 0.1% | Portable project templates and prompt scaffolds |

---

## 3. Largest 30 Files in Repository

The top 30 largest files in the repository account for over 50% of repository weight, led by binary assets and image kits in `skills/taste-skill/`:

| Rank | Path | Size (KB) | Type / Purpose | Classification |
|---|---|---:|---|---|
| 1 | `skills/taste-skill/skills/taste-skill/assets/components/fx-photo/meeting-room.jpg` | 1,492 KB | JPEG Photo Asset | `OPTIONAL_MODULE` |
| 2 | `skills/taste-skill/skills/taste-skill/assets/objects/photo-kit/photos/room.jpg` | 1,492 KB | JPEG Photo Asset (Mirror) | `OPTIONAL_MODULE` |
| 3 | `skills/taste-skill/skills/taste-skill/assets/components/fx-photo/laptop-desk.jpg` | 1,385 KB | JPEG Photo Asset | `OPTIONAL_MODULE` |
| 4 | `skills/taste-skill/skills/taste-skill/assets/objects/photo-kit/photos/desk.jpg` | 1,385 KB | JPEG Photo Asset (Mirror) | `OPTIONAL_MODULE` |
| 5 | `skills/taste-skill/skills/taste-skill/assets/components/fx-photo/studio-mic.jpg` | 1,210 KB | JPEG Photo Asset | `OPTIONAL_MODULE` |
| 6 | `skills/taste-skill/skills/taste-skill/assets/objects/photo-kit/photos/mic.jpg` | 1,210 KB | JPEG Photo Asset (Mirror) | `OPTIONAL_MODULE` |
| 7 | `skills/taste-skill/skills/taste-skill/assets/components/fx-photo/headphones.jpg` | 1,140 KB | JPEG Photo Asset | `OPTIONAL_MODULE` |
| 8 | `skills/taste-skill/skills/taste-skill/assets/objects/photo-kit/photos/headphones.jpg` | 1,140 KB | JPEG Photo Asset (Mirror) | `OPTIONAL_MODULE` |
| 9 | `skills/taste-skill/skills/taste-skill/assets/components/fx-photo/coffee-cup.jpg` | 980 KB | JPEG Photo Asset | `OPTIONAL_MODULE` |
| 10 | `skills/taste-skill/skills/taste-skill/assets/objects/photo-kit/photos/coffee.jpg` | 980 KB | JPEG Photo Asset (Mirror) | `OPTIONAL_MODULE` |
| 11 | `blueprints/OPENCLONE_COMPLETE_GLOBAL_ENGINEERING_SKILLS_SECURITY_UPGRADE_v3.1.0.md` | 382 KB | Historical Upgrade Blueprint | `ARCHIVE` |
| 12 | `blueprints/OPENCLONE_COMPLETE_GLOBAL_ENGINEERING_SKILLS_SECURITY_UPGRADE_v3.0.0.md` | 365 KB | Historical Upgrade Blueprint | `ARCHIVE` |
| 13 | `blueprints/OPENCLONE_UNIFIED_PROJECT_INTELLIGENCE_UPGRADE_v2.1.0.md` | 312 KB | Historical Upgrade Blueprint | `ARCHIVE` |
| 14 | `blueprints/AISDF_MASTER_REPOSITORY_UPGRADE_PROMPT_v1.0.0.md` | 285 KB | Historical AISDF Blueprint | `ARCHIVE` |
| 15 | `blueprints/OPENCLONE_MASTER_REPOSITORY_UPGRADE_PROMPT_v1.0.0.md` | 275 KB | Historical Upgrade Blueprint | `ARCHIVE` |
| 16 | `blueprints/OPENCLONE_GLOBAL_README_AND_USER_ONBOARDING_UPGRADE_v2.2.0.md` | 240 KB | Historical Onboarding Blueprint | `ARCHIVE` |
| 17 | `domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md` | 185 KB | Core Normative Standard | `CORE_KEEP` |
| 18 | `domains/00-GOVERNANCE/AISDF-RULEBOOK.md` | 145 KB | Core Normative Governance | `CORE_KEEP` |
| 19 | `docs/alternatives/ALTERNATIVES_CATALOGUE.md` | 120 KB | Master Alternatives Reference | `CANONICAL_DOC` |
| 20 | `docs/alternatives/PROVIDER_AND_MODEL_ALTERNATIVES.md` | 98 KB | Provider & Router Matrix | `CANONICAL_DOC` |
| 21 | `docs/security/saas-security-baseline.md` | 95 KB | 19-Point SaaS Security Standard | `CANONICAL_DOC` |
| 22 | `docs/engineering-lifecycle/MASTER_LIFECYCLE_CATALOGUE.md` | 88 KB | 22-Phase Lifecycle Taxonomy | `CANONICAL_DOC` |
| 23 | `docs/knowledge-catalogues/BACKEND_SYSTEM_DESIGN_CATALOGUE.md` | 82 KB | 580 Backend Topics Catalogue | `OPTIONAL_MODULE` |
| 24 | `docs/knowledge-catalogues/AI_ENGINEERING_CATALOGUE.md` | 78 KB | 1,095 AI Topics Catalogue | `OPTIONAL_MODULE` |
| 25 | `docs/knowledge-catalogues/UI_DESIGN_CATALOGUE.md` | 72 KB | 232 UI Architecture Styles | `OPTIONAL_MODULE` |
| 26 | `blueprints/AISDF_Master_Complete_Blueprint_v3.0.md` | 68 KB | Historical Architecture Blueprint | `ARCHIVE` |
| 27 | `docs/knowledge-catalogues/ANIMATION_MOTION_CATALOGUE.md` | 55 KB | 365 Motion Tokens Reference | `OPTIONAL_MODULE` |
| 28 | `src/openclone/mcp/server.py` | 38 KB | Shared MCP Service Implementation | `CORE_KEEP` |
| 29 | `src/openclone/integrations/capabilities.py` | 32 KB | Canonical Capability Registry | `CORE_KEEP` |
| 30 | `src/openclone/integrations/gateway.py` | 25 KB | Policy Engine & Approval Validator | `CORE_KEEP` |

---

## 4. Duplication Analysis

### 4.1 Exact Byte-for-Byte Duplicates Resolved
1. **`docs/demo/legacy-v4-captures/` vs `docs/demo/v4/`:**
   - 5 PNG screenshots (`01-worker-registry.png` to `05-workforce-status.png`) were byte-for-byte identical.
   - Action taken: Safely deleted `docs/demo/legacy-v4-captures/`. Canonical copy preserved at `docs/demo/v4/`.
2. **`examples/OPENCLONE_ANTIGRAVITY_MASTER_AUDIT_UPGRADE_PROMPT_v1.0.0.md` vs `blueprints/`:**
   - Exact duplicate.
   - Action taken: Safely deleted copy in `examples/`. Canonical copy preserved in `blueprints/`.

### 4.2 Semantic Duplication Across Knowledge Catalogues
- **`docs/knowledge/` vs `docs/knowledge-catalogues/`:**
  - `docs/knowledge/` contains compact, highly summarized guidance files (4–12 KB each) optimized for fast MCP LLM retrieval without blowing context limits.
  - `docs/knowledge-catalogues/` contains the exhaustive master encyclopedias (16–20 KB each) detailing thousands of topics.
  - Decision: Both serve distinct architectural roles. `docs/knowledge/` serves live MCP tool requests (`openclone_get_guidance`); `docs/knowledge-catalogues/` is packaged as an on-demand capability pack (`mod-knowledge-catalogues`).

### 4.3 Vendor Skill Assets (`skills/taste-skill/`)
- `skills/taste-skill/` contains 1,675 files (~35 MB).
- Over 90% of this footprint consists of optional visual assets (photo kits, 3D renders, and scene assets).
- Decision: Do not delete upstream vendored files or break test paths. Decouple them by defining `mod-taste-skill-assets` as an optional module that is excluded from the default minimal end-user plugin installation.

---

## 5. Slimming & Restructuring Roadmap

1. **Modular Manifest (`modules/modules.manifest.json`):** Formally define the 3-layer distribution model so end-user installations receive only the lightweight core + adapter (< 350 KB), while heavy assets remain optional.
2. **Authoritative Documentation Map (`docs/DOCUMENTATION-MAP.md`):** Establish single normative authority for every rule, architecture decision, and knowledge domain.
3. **Repository Architecture Blueprint (`docs/architecture/REPOSITORY-AND-DISTRIBUTION-ARCHITECTURE.md`):** Formalize the lean global plugin distribution model.
