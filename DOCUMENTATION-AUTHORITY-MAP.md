# OpenClone Documentation Authority Map
**Version:** 2.0.0  
**Status:** CANONICAL HIERARCHY  
**Last Updated:** 2026-11-23  

---

## 1. Documentation Precedence Order
1. **Platform & Sandbox Constraints:** Tool execution boundaries, developer terminal approval allowlists.
2. **Repository Operating Contract ([`AGENTS.md`](AGENTS.md)):** Core operating contract for AI agents.
3. **Active Project Specification ([`PROJECT.md`](PROJECT.md)):** Scope and architecture of the active project.
4. **Normative Framework Standards:** Domain rules and security baselines in `domains/` and `security/`.
5. **Runtime Contracts:** Deterministic engine contracts in `src/openclone/`, `runtime/`, `engines/`, and `schemas/`.
6. **Architecture Specifications:** `docs/architecture/` and `blueprints/OPENCLONE-MASTER-BLUEPRINT.md`.
7. **Operational Assessments:** `assessments/current/` (`REPOSITORY-HEALTH.md`, `SECURITY-STATUS.md`, `RELEASE-READINESS.md`).
8. **Reference Knowledge:** `docs/knowledge-catalogues/` (master encyclopedias) and `docs/knowledge/` (MCP skill guidance).
9. **Historical Archive:** `blueprints/archive/`, `assessments/archive/`, `docs/archive/`.

---

## 2. Directory Ownership Matrix

| Directory | Scope & Responsibility | Authority Document |
|---|---|---|
| `src/openclone/` | Modular v2.0 plugin platform (CLI, MCP Server, Skills Engine, Installer) | `openclone.manifest.json` |
| `runtime/openclone_runtime/` | Deterministic execution engine, SQLite audit ledger, permission gating | `runtime/README.md` |
| `runtime/aisdf_runtime/` | Backward compatibility forwarding wrappers | `runtime/aisdf_runtime/README.md` |
| `integrations/` | Metadata registry and manifests for 28 upstream repositories | `integrations/registry/upstream_registry.json` |
| `domains/` | 31 comprehensive software engineering knowledge domains | `domains/00-GOVERNANCE/OPENCLONE-RULEBOOK.md` |
| `engines/` | 56 execution capability engine contracts (E-001..E-056) | `engines/README.md` |
| `workforce/` | 72 specialist engineering worker contracts across 12 disciplines | `workforce/README.md` |
| `concepts/` | 10 core architectural invariants and alternative paradigms | `concepts/README.md` |
| `blueprints/` | Authoritative platform and methodology blueprints | `blueprints/README.md` |
| `assessments/current/` | Active platform health, security, and release readiness | `assessments/README.md` |
| `docs/knowledge-catalogues/` | Master engineering encyclopedias (UI, backend, AI, motion) | `docs/knowledge-catalogues/README.md` |
| `docs/knowledge/` | Fast runtime MCP skill guidance profiles | `docs/knowledge/README.md` |
