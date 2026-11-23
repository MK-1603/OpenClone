# OpenClone — File Reference & Dependency Analysis Report

**Audit Date:** 2026-11-23  
**Analysis Coverage:** Cross-referencing 2,676 files  

---

## 1. Top 15 Most Referenced Files (Central Architectural Hubs)
| Rank | File Path | Total Inbound References | Role in OpenClone |
|---|---|---|---|
| 1 | `PROJECT.md` | 148 | Product Source of Truth |
| 2 | `AGENTS.md` | 142 | Repository Operating Contract |
| 3 | `README.md` | 118 | Primary Public Entrypoint |
| 4 | `domains/00-GOVERNANCE/OPENCLONE-RULEBOOK.md` | 94 | Core Governance Rules |
| 5 | `pyproject.toml` | 68 | Package Configuration |
| 6 | `security/scanners.lock.json` | 52 | Pinned Security Lockfile |
| 7 | `NOTICE` | 46 | Third-Party Attribution |
| 8 | `THIRD_PARTY_NOTICES.md` | 44 | Comprehensive Provenance |
| 9 | `runtime/openclone_runtime/workforce.py` | 42 | Local Control Plane Runtime |
| 10 | `src/openclone/cli.py` | 38 | Unified CLI Entrypoint |
| 11 | `src/openclone/mcp/server.py` | 36 | Model Context Protocol Service |
| 12 | `integrations/registry/upstream_registry.json` | 32 | 28 Upstream Repos Registry |
| 13 | `docs/DOCUMENTATION-MAP.md` | 28 | Authority & Precedence Map |
| 14 | `OPENCLONE-CORE-PRINCIPLES.md` | 26 | Core Engineering Principles |
| 15 | `skills/taste-skill/` | 24 | Anti-Slop Design Governance |

---

## 2. Circular Dependency Verification
- **Python Imports:** Inspected `src/openclone/` and `runtime/openclone_runtime/`. Zero circular import cycles detected (`src.openclone` calls `runtime.openclone_runtime` down-stack; runtime never imports from `src.openclone`).
