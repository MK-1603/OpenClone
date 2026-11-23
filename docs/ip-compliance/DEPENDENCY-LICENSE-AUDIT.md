# OpenClone Upstream Dependency & Supply Chain License Audit

**Document ID:** `AUDIT-DEPENDENCY-LICENSES-v1.0.0`  
**Standard:** AISDF Standard 1.0.0  
**Status:** `AUDITED & COMPLIANT`  

---

## 1. Supply Chain Language & Tooling Analysis

| Category | Repositories | Runtimes / Package Managers | Supply Chain Risk | Isolation Strategy |
|---|---|---|---|---|
| **JavaScript / TypeScript** | UI-001, UI-002, UI-003, UI-004, UI-006, UI-007, SEC-006, ENG-003 | `npm`, `pnpm`, `yarn` | Node dependencies, transitive CVEs | Excluded from core plugin. Only pure tokens and Markdown guidelines extracted. |
| **Python** | SEC-001, SEC-003, SEC-009, SEC-011, SEC-012, ENG-001, ENG-004 | `pip`, `poetry`, `uv` | PyPI package compatibility | Core uses zero-dependency Python standard library. Optional tools run in venvs. |
| **Go** | SEC-002 (nuclei), SEC-007 (trivy), SEC-008 (trufflehog) | `go modules` | Binary provenance | Scanners pinned by cryptographic hash in `security/scanners.lock.json`. |
| **OCaml / C / Rust** | SEC-005 (semgrep), SEC-010 (clamav) | Native toolchains | Native compilation risks | Managed externally via pre-compiled distribution packages or Docker. |
| **Markdown / Prompts** | UI-005, UI-008, UI-009, UI-010, UI-011, SEC-004, ENG-002 | Text files | Zero runtime dependencies | Incorporated as architectural knowledge and prompt templates with attribution. |