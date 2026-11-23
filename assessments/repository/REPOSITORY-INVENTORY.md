# OpenClone Master Repository Inventory Assessment

**Document ID:** `INV-MASTER-REPO-v2.0.0`  
**Product:** OpenClone 2.0 Universal AI Software Engineering Platform  
**Standard:** AISDF Standard 1.0.0 (Independently Versioned)  
**Date:** 2026-11-23  
**Status:** `AUDITED AND VERIFIED`  

---

## 1. Physical Footprint Summary
- **Total Non-Ignored Files:** `2,648` files
- **Total Working Tree Size:** `42.43` MB
- **Core Runtime Package Footprint:** `< 350 KB` (99.1% smaller than full mono-repo)
- **Automated Tests:** 118 passing automated tests (105 Python + 13 Node.js)

## 2. Directory Footprint Breakdown

| Directory | File Count | Size (MB) | Architectural Responsibility | Classification |
|---|---:|---:|---|---|
| `skills/` | 1,673 | 35.75 MB | Taste Skill Visual Assets & Media Renders | `IMPROVE / MODULARIZE` |
| `domains/` | 73 | 1.77 MB | 31 Engineering Domain Specifications | `KEEP` |
| `blueprints/` | 33 | 1.66 MB | Historical Architecture Provenance | `ARCHIVE` |
| `docs/` | 274 | 1.32 MB | Specifications, Guides, Reports, Compliance | `KEEP` |
| `src/` | 39 | 0.40 MB | Core Runtime / Architecture | `KEEP` |
| `engines/` | 57 | 0.27 MB | 56 Capability Engine Contracts | `KEEP` |
| `workforce/` | 164 | 0.22 MB | 72 Worker Manifests & 12 Teams | `KEEP` |
| `tests/` | 27 | 0.19 MB | Core Runtime / Architecture | `KEEP` |
| `tools/` | 15 | 0.19 MB | Core Runtime / Architecture | `KEEP` |
| `runtime/` | 9 | 0.16 MB | Core Runtime / Architecture | `KEEP` |
| `integrations/` | 41 | 0.10 MB | Upstream Registry, Manifests & Adapters | `KEEP` |
| `./` | 31 | 0.08 MB | Core Runtime / Architecture | `KEEP` |
| `adapters/` | 26 | 0.05 MB | Core Runtime / Architecture | `KEEP` |
| `workflows/` | 16 | 0.03 MB | Core Runtime / Architecture | `KEEP` |
| `templates/` | 20 | 0.03 MB | Core Runtime / Architecture | `KEEP` |
| `prompts/` | 25 | 0.03 MB | Core Runtime / Architecture | `KEEP` |
| `examples/` | 8 | 0.02 MB | Core Runtime / Architecture | `KEEP` |
| `concepts/` | 21 | 0.02 MB | Core Runtime / Architecture | `KEEP` |
| `registries/` | 8 | 0.02 MB | Core Runtime / Architecture | `KEEP` |
| `assets/` | 4 | 0.02 MB | Core Runtime / Architecture | `KEEP` |
| `schemas/` | 11 | 0.02 MB | Core Runtime / Architecture | `KEEP` |
| `assessments/` | 5 | 0.01 MB | Core Runtime / Architecture | `KEEP` |
| `security/` | 3 | 0.01 MB | Core Runtime / Architecture | `KEEP` |
| `agents/` | 17 | 0.01 MB | Core Runtime / Architecture | `KEEP` |
| `EGM-WORKFLOWS/` | 8 | 0.01 MB | Core Runtime / Architecture | `KEEP` |
| `modules/` | 2 | 0.01 MB | Core Runtime / Architecture | `KEEP` |
| `security-operations/` | 12 | 0.00 MB | Core Runtime / Architecture | `KEEP` |
| `memory/` | 6 | 0.00 MB | Core Runtime / Architecture | `KEEP` |
| `REFERENCE-PROJECTS/` | 4 | 0.00 MB | Core Runtime / Architecture | `KEEP` |
| `rules/` | 5 | 0.00 MB | Core Runtime / Architecture | `KEEP` |
| `modes/` | 4 | 0.00 MB | Core Runtime / Architecture | `KEEP` |
| `standards/` | 2 | 0.00 MB | Core Runtime / Architecture | `KEEP` |
| `ASSESSMENT/` | 3 | 0.00 MB | Core Runtime / Architecture | `KEEP` |
| `reference/` | 2 | 0.00 MB | Core Runtime / Architecture | `KEEP` |