# Document Inventory & Authority Map — OpenClone
## Authority Hierarchy and Canonical Ownership

- **Framework Version:** `1.0.0`
- **Scope:** Root and sub-directory documentation across OpenClone
- **Audit Date:** 2026-11-22

---

## 1. Document Authority Precedence

In accordance with Section 1 of the AISDF Operating Contract (`AGENTS.md`), documents follow strict precedence:

```
Platform Safety / Sandbox Constraints
  └── Explicit Current Human Owner Instructions
        └── AGENTS.md (Operating Contract & Safety Rules)
              └── PROJECT.md (Product Source of Truth & Approved Milestones)
                    └── Architecture Documents, ADRs, Schemas & Domain Specs
                          └── Historical Notes, Blueprints & Generated Reports
```

---

## 2. Comprehensive Document Inventory

| Document Path | Purpose | Primary Audience | Authority Level | Status | Canonical Owner |
|---|---|---|---|---|---|
| `AGENTS.md` | Operating contract, safety rules, permission profiles, git workflow | AI Agents & Human Engineers | **Tier 1 (Highest)** | Active / Canonical | OpenClone Governance |
| `PROJECT.md` | OpenClone framework definition, scope, functional requirements, roadmap | Human Lead & Core Maintainers | **Tier 2 (Source of Truth)** | Active / Canonical | Product Architecture |
| `README.md` | Public open-source landing page, quick start, architecture, integrations | External Developers & Users | Tier 3 (Public Landing) | Active / Polished | Framework Documentation |
| `VERSION` | Authoritative semver identifier (`1.0.0`) | Automated Tools & CI/CD | Tier 1 (Identifier) | Active / Pinned | Release Engineering |
| `LICENSE` | MIT Open-source license terms | Legal & General Public | Tier 1 (Legal) | Active / Pinned | Legal & Compliance |
| `blueprints/*.md` | Master architectural blueprints and prompt specifications (v1.0–v2.0.0) | Architects & System Designers | Tier 4 (Design Blueprint) | Active / Indexed | System Architecture |
| `domains/*/README.md` | 31 Engineering domain standards, specifications, and topologies | Specialist Teams & Engineers | Tier 3 (Domain Specs) | Active / Canonical | Domain Leads |
| `engines/E-*.md` | 56 Capability engine execution contracts with preconditions & outputs | Engine Execution & Workforce | Tier 3 (Contracts) | Active / Validated | Engine Architecture |
| `workflows/WF-*.md` | 14 Executable workflow definitions (WF-001 through WF-014) | Orchestration Plane & Agents | Tier 3 (Workflows) | Active / Verified | Orchestration Lead |
| `workforce/teams/*` | 72 Specialist role contracts across 12 teams | AI Agents & Task DAG | Tier 3 (Role Manifests) | Active / Validated | Workforce Registry |
| `templates/*.md` | Templates for generated user applications (`PROJECT.md`, `AGENTS.md`) | OpenClone Project Generator | Tier 4 (Generator Template)| Active / Reusable | Project Generation |
| `adapters/*/README.md`| Native platform manifests and guides (Antigravity, Claude, Codex, Cursor) | IDE / Host Integrators | Tier 3 (Adapter Specs) | Active / Integrated | Platform Engineering |
| `assessments/*` | Evidence-based audit ledgers, gap analyses, and migration records | Reviewers & Auditors | Tier 4 (Audit Ledger) | Active / Traceable | Quality Assurance |

---

## 3. Disambiguation Rules

1. **OpenClone Product vs Application**: If a document specifies OpenClone's local control plane, it belongs in `PROJECT.md` or `docs/`. If it specifies an application generated for a user, it belongs in `templates/` or target workspace.
2. **Blueprints vs Active Specifications**: Documents in `blueprints/` preserve historical genesis and master specifications. Active implementation code lives in `src/openclone/`, `runtime/`, and `tools/`.
