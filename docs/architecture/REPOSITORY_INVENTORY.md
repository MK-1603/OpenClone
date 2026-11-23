# OpenClone — Complete Repository Inventory & Architectural Baseline

**Inventory Date:** 2026-11-23  
**Total Tracked Files:** 2,676  
**Total Repository Size:** 42.11 MB  
**Status:** Audit Complete · Evidence-Backed  

---

## 1. Classification Breakdown

| Classification | File Count | Percentage | Total Size (KB) | Avg File Size (KB) |
|---|---|---|---|---|
| **Application implementation** | 1,530 | 57.2% | 34,846.2 KB | 22.8 KB |
| **Documentation** | 500 | 18.7% | 2,259.8 KB | 4.5 KB |
| **Governance** | 212 | 7.9% | 284.9 KB | 1.3 KB |
| **Configuration** | 174 | 6.5% | 1,433.0 KB | 8.2 KB |
| **Knowledge** | 131 | 4.9% | 2,089.4 KB | 15.9 KB |
| **Historical reference** | 42 | 1.6% | 1,708.4 KB | 40.7 KB |
| **Integration** | 36 | 1.3% | 92.8 KB | 2.6 KB |
| **Testing** | 24 | 0.9% | 156.0 KB | 6.5 KB |
| **Core implementation** | 19 | 0.7% | 190.1 KB | 10.0 KB |
| **Runtime** | 8 | 0.3% | 62.7 KB | 7.8 KB |

---

## 2. Directory Top-Level Breakdown

| Directory | File Count | Size (KB) | Primary Classification | Purpose |
|---|---|---|---|---|
| `skills/` | 1,678 | 36,615.0 KB | Core Component | Managed Platform Subsystem |
| `docs/` | 281 | 1,366.4 KB | Core Component | Managed Platform Subsystem |
| `workforce/` | 164 | 226.5 KB | Core Component | Managed Platform Subsystem |
| `domains/` | 74 | 1,812.0 KB | Core Component | Managed Platform Subsystem |
| `engines/` | 57 | 277.3 KB | Core Component | Managed Platform Subsystem |
| `adapters/` | 43 | 71.2 KB | Core Component | Managed Platform Subsystem |
| `./` | 37 | 102.7 KB | Core Component | Managed Platform Subsystem |
| `integrations/` | 36 | 92.8 KB | Core Component | Managed Platform Subsystem |
| `blueprints/` | 33 | 1,697.6 KB | Core Component | Managed Platform Subsystem |
| `assessments/` | 26 | 34.8 KB | Core Component | Managed Platform Subsystem |
| `prompts/` | 25 | 26.1 KB | Core Component | Managed Platform Subsystem |
| `concepts/` | 21 | 21.0 KB | Core Component | Managed Platform Subsystem |
| `src/` | 20 | 190.5 KB | Core Component | Managed Platform Subsystem |
| `templates/` | 20 | 33.0 KB | Core Component | Managed Platform Subsystem |
| `tools/` | 20 | 245.0 KB | Core Component | Managed Platform Subsystem |
| `agents/` | 17 | 10.1 KB | Core Component | Managed Platform Subsystem |
| `workflows/` | 16 | 33.6 KB | Core Component | Managed Platform Subsystem |
| `tests/` | 15 | 71.7 KB | Core Component | Managed Platform Subsystem |
| `security-operations/` | 12 | 4.2 KB | Core Component | Managed Platform Subsystem |
| `schemas/` | 11 | 17.1 KB | Core Component | Managed Platform Subsystem |
| `EGM-WORKFLOWS/` | 8 | 8.0 KB | Core Component | Managed Platform Subsystem |
| `examples/` | 8 | 25.5 KB | Core Component | Managed Platform Subsystem |
| `registries/` | 8 | 18.9 KB | Core Component | Managed Platform Subsystem |
| `runtime/` | 8 | 62.7 KB | Core Component | Managed Platform Subsystem |
| `memory/` | 6 | 4.0 KB | Core Component | Managed Platform Subsystem |
| `.github/` | 5 | 5.8 KB | Core Component | Managed Platform Subsystem |
| `rules/` | 5 | 3.1 KB | Core Component | Managed Platform Subsystem |
| `REFERENCE-PROJECTS/` | 4 | 3.8 KB | Core Component | Managed Platform Subsystem |
| `assets/` | 4 | 17.8 KB | Core Component | Managed Platform Subsystem |
| `modes/` | 4 | 2.9 KB | Core Component | Managed Platform Subsystem |
| `security/` | 3 | 11.4 KB | Core Component | Managed Platform Subsystem |
| `modules/` | 2 | 7.0 KB | Core Component | Managed Platform Subsystem |
| `reference/` | 2 | 0.9 KB | Core Component | Managed Platform Subsystem |
| `standards/` | 2 | 2.6 KB | Core Component | Managed Platform Subsystem |
| `.agents/` | 1 | 0.3 KB | Core Component | Managed Platform Subsystem |

---

## 3. High-Value Architecture Highlights
- **Zero Runtime Dependencies:** Pure Python standard library local control plane (`pyproject.toml` dependencies: 0).
- **Dual-Tier Engineering Catalogues:** Fast Live MCP Guidance (<12 KB) in `docs/knowledge/` and Master Encyclopedias in `docs/knowledge-catalogues/`.
- **Integrated Security Engine:** 12 pinned security scanner adapters in `integrations/adapters/` and `security/scanners.lock.json`.
- **Deterministic Governance:** SQLite audit ledger with hash-chained SHA-256 state transitions in `runtime/openclone_runtime/`.
