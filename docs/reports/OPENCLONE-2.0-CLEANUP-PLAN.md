# OpenClone 2.0 Repository Cleanup & Canonicalization Plan

**Document ID:** `PLAN-OC-2.0-CLEANUP-v2.0.0`  
**Product:** OpenClone 2.0 Universal AI Software Engineering Platform  
**Target Repository:** `MK-1603/OpenClone`  
**Standard:** AISDF Standard 1.0.0  
**Status:** `IMPLEMENTED AND VERIFIED`  
**Author:** Principal Platform Architect & Release Engineering Team  

---

## 1. Executive Summary & Objectives

OpenClone 2.0 transforms a large mono-repository of 2,525 files and 41.51 MB into a streamlined, modular engineering platform. The objectives of this cleanup plan are:

1. **Establish Single Source of Authority:** Eliminate competing specifications and contradictory rules across the repository by mapping every engineering domain to a canonical authority document in [`docs/DOCUMENTATION-MAP.md`](../DOCUMENTATION-MAP.md).
2. **Safe Redundancy Elimination:** Eliminate verified exact byte-for-byte duplicates while preserving historical provenance and zero broken links.
3. **Decouple Heavy Assets into Optional Modules:** Separate 35.76 MB of visual renders and photos into on-demand capability packs (`modules/modules.manifest.json`), achieving a lean core installation (< 350 KB, 99.1% smaller).
4. **Preserve Historical Provenance Safely:** Categorize historical blueprints and transition documents under `ARCHIVE` in `blueprints/` rather than deleting them, ensuring immutable audit history while excluding them from end-user plugin packages.
5. **Enforce Change Control & Approvals:** Mandate explicit human approval before any destructive deletion or production release.

---

## 2. Classification Taxonomy & Decision Rules

Every file in the repository is classified in [`docs/reports/OPENCLONE-2.0-FILE-CLASSIFICATION.csv`](OPENCLONE-2.0-FILE-CLASSIFICATION.csv) under one of ten standard governance categories:

| Category | Meaning | Repository Action | Distribution Action |
|---|---|---|---|
| `CORE_KEEP` | Essential runtime code, manifests, tools, engines, core domain rules | Kept in active repository | Packaged in core plugin |
| `ADAPTER_KEEP` | Host integration packages for IDEs and coding agents | Kept in `adapters/` | Deployed during host installation |
| `OPTIONAL_MODULE` | High-value assets, deep catalogues, specialist roles | Kept in repository | On-demand installation via `openclone modules` |
| `CANONICAL_DOC` | Current normative specification or architecture reference | Kept in `docs/` | Excluded from core runtime package |
| `MERGE_SOURCE` | Contains unique requirements to be consolidated | Merged into canonical doc | Retired after link verification |
| `ARCHIVE` | Historical specifications, older blueprints, upgrade prompts | Kept in `blueprints/` | Excluded from plugin distribution |
| `REMOVE_GENERATED`| Cache files, bytecode (`.pyc`), build artifacts | Removed from Git tracking | Added to `.gitignore` |
| `REMOVE_DUPLICATE`| Verified byte-for-byte or exact semantic redundancy | Safely deleted | N/A |
| `REMOVE_OBSOLETE` | Deprecated, superseded, or broken files | Requires human approval | N/A |
| `INVESTIGATE` | Provenance or dependency unclear | Retained untouched | N/A |

---

## 3. Detailed Audit of Repository Areas & Actions Taken

### 3.1 Heavy Visual Assets: `skills/` (35.76 MB, 1,675 files)
- **Content:** The `taste-skill` directory contains the complete visual design system, token definitions, governance tests, and an extensive library of photographic scenes and 3D renders across 14 aesthetic styles (editorial, brutalist, minimal, kinetic, bauhaus, etc.).
- **Decision:** Classified as `OPTIONAL_MODULE` (`mod-taste-skill-assets`).
- **Implementation:** The core design tokens and governance test suite (`skills/taste-skill/tests/test-governance.mjs`) remain active in the repository for CI verification, while heavy media assets are excluded from default global plugin distribution, reducing default install size by 99.1%.

### 3.2 Knowledge Repositories: Dual-Tier Architecture
- **Problem:** Exhaustive catalogues (such as 580 backend topics and 1,095 AI topics) exceed token limits if injected directly into LLM agent contexts.
- **Resolution:**
  - **Tier 1 (Live MCP Guidance):** Five compact guidance files (< 12 KB each) placed in `docs/knowledge/` for instant context injection via `openclone_get_guidance`. Classified as `CORE_KEEP`.
  - **Tier 2 (Master Knowledge Encyclopedias):** Full encyclopedias retained in `docs/knowledge-catalogues/`. Classified as `OPTIONAL_MODULE` (`mod-knowledge-catalogues`).

### 3.3 Historical Blueprints: `blueprints/` (1.66 MB, 33 files)
- **Content:** Historical architecture blueprints (v1.0.0 through v4.0.0) and upgrade specification prompts.
- **Decision:** Classified as `ARCHIVE`.
- **Implementation:** Retained in `blueprints/` to preserve complete evolutionary provenance. Excluded from all runtime packages. No files in this directory are deleted without human consent.

### 3.4 Redundant Artifacts Safely Removed
1. **`docs/demo/legacy-v4-captures/`:**
   - 5 PNG files (`architecture-overview.png`, `mcp-tools-list.png`, `approval-flow.png`, `task-lifecycle.png`, `quality-gates.png`).
   - Verified exact SHA-256 byte-for-byte duplicates of corresponding files in `docs/demo/v4/`.
   - Action: Safely removed. All markdown documentation points to `docs/demo/v4/`.
2. **`examples/OPENCLONE_ANTIGRAVITY_MASTER_AUDIT_UPGRADE_PROMPT_v1.0.0.md`:**
   - Exact duplicate of `blueprints/OPENCLONE_ANTIGRAVITY_MASTER_AUDIT_UPGRADE_PROMPT_v1.0.0.md`.
   - Action: Safely removed from `examples/`. Canonical copy preserved in `blueprints/`.

---

## 4. Governance & Human Approval Boundaries

Under AISDF Operating Contract Rule 6, the following actions **strictly require explicit human authorization**:
- Permanent deletion of any file classified under `ARCHIVE`, `INVESTIGATE`, or `MERGE_SOURCE`.
- Modification of core security policies or human approval thresholds in `src/openclone/integrations/gateway.py`.
- Pushing feature branches to `main` or publishing packages to npm or PyPI.
- Any destructive Git command (`git reset --hard`, `git push --force`).

---

## 5. Summary of Cleanup Achievements

| Metric | Pre-Cleanup Baseline | Post-Cleanup State | Improvement |
|---|---:|---:|---:|
| Tracked File Count | 2,531 files | 2,525 files | -6 verified duplicate files |
| Duplicate File Groups | 2 groups (6 files) | 0 active duplicates | 100% resolved |
| Core Plugin Install Size | ~41.51 MB | < 350 KB | 99.1% payload reduction |
| Documentation Precedence | Undocumented | Explicit in `DOCUMENTATION-MAP.md` | Single source of truth |
| Automated Test Pass Rate | 100% (110/110) | 100% (110/110) | Zero regressions |
