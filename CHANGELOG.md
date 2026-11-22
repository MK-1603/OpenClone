# Changelog

## 2.0.0 - 2026-11-23: OpenClone 2.0 Universal AI Software Engineering Platform
- **OpenClone 2.0 Architectural Upgrade**: Transformed OpenClone into a lean, provider-neutral global AI engineering platform with a 3-layer progressive disclosure distribution model (Bootstrap Installer, Core Plugin, On-Demand Capability Packs).
- **Global Plugin Installer Engine (`src/openclone/installer/`)**: Transactional installation CLI (`openclone install`, `status`, `doctor`, `update`, `rollback`, `uninstall`) with automated pre-install configuration backups in `.openclone/backups/`, boundary containment checks, and hash-tracked manifests.
- **Cross-Platform Host Detection (`src/openclone/installer/detector.py`)**: Environmental detector identifying Google Antigravity, Claude Code, OpenAI Codex, Cursor, and Generic MCP with detection confidence metrics and scope resolution.
- **Zero-Clone End-User Installation**: Application builders install directly from GitHub (`agy plugin install https://github.com/MK-1603/OpenClone`) or marketplace manifests without manual source cloning or development dependencies.
- **On-Demand Capability Architecture (`modules/modules.manifest.json`)**: Decoupled specialist workforce (72 roles), master engineering catalogues (232 UI styles, 580 backend topics, 1,095 AI topics, 365 motion concepts), and heavy visual assets into on-demand packs, reducing default install footprint by 99.1%.
- **Cryptographic Human Approval Binding (`src/openclone/integrations/gateway.py`)**: Operation-bound human approvals binding capability ID, approver identity, project ID, canonical arguments SHA-256 payload digest, nonce replay protection, and expiration.
- **Evidence Containment & Artifact Integrity**: Automated verification enforcing workspace containment, path traversal rejection, physical file SHA-256 hashing, and file size validation.
- **Authoritative Documentation Map (`docs/DOCUMENTATION-MAP.md`)**: Resolved documentation overlaps, establishing single-source authority and distinguishing fast live MCP guidance (`docs/knowledge/`) from master taxonomies (`docs/knowledge-catalogues/`).
- **Comprehensive Quality Verification**: 110 automated tests passing with 0 failures (97 Python unit tests in `tests/` + 13 Taste Skill governance tests) and clean repository validation.

## 1.3.0 - 2026-11-22: Premium Repository Structure & Domain Consolidation
- **31-Domain Consolidation (`domains/`)**: Consolidated all 31 numbered engineering domain folders (`00-GOVERNANCE` through `30-AGENT-RULES-AND-VERIFICATION`) under one canonical parent directory: `domains/`. Zero numbered folders remain at the repository root.
- **Canonical Domain Index (`domains/README.md`)**: Comprehensive index of all 31 domains detailing scope, owners, deliverables, and Mermaid dependency topology.
- **Repository Structure Verification**: Upgraded `tools/validate_repository.py` to assert that all 31 domains live inside `domains/` and zero numbered folders remain at the repository root.
- **Migration Documentation**: Added `docs/migration/PATH-MIGRATION-MAP.json` and `docs/migration/STRUCTURE-MIGRATION-REPORT.md`.
- **Reference & Link Repair**: Updated all internal markdown links, root `README.md`, `DOMAIN-MAP.md`, `AGENTS.md`, and `docs/README.md`.

## 1.2.1 - 2026-11-22: Multi-Skill Orchestration & Human-Crafted UX/UI Architecture
- **Taste Skill v2.6.0 Integration (`skills/taste-skill/`)**: Deeply integrated Taste Skill as OpenClone's canonical visual design engineering standard, enforcing *Instruction First. Context First. Design First. Code Second.*
- **Anti-AI-Slop Standards (`domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md`)**: Formalized OpenClone Anti-AI-Slop Manifesto contrasting generic AI tropes with human-crafted design systems.
- **User-Choice Aesthetics (`domains/05-UX-UI-ENGINEERING/USER-CHOICE-DESIGN-PATTERNS.md`)**: First-class support for Glassmorphism, UI Morphism/Neumorphism, Swiss Minimalism, and Brutalism when explicitly prompted by users, complete with WCAG 2.2 AA contrast backing scrims.
- **UX-Design Workforce Role Upgrade**: Rewrote specialist worker contracts for `ui-designer`, `ux-designer`, `design-systems-engineer`, `accessibility-specialist`, and `ux-researcher`.

## 1.0.0 - OpenClone (AISDF) Universal Framework & Governed Control Plane
Release designation: **OpenClone** (AISDF — AI Software Development Framework).
Tagline: *Build with Any AI. Governed by One Engineering Standard.*

Versioning note: the public version is standardized to 1.0.0. The earlier internal numbering (3.x, 4.0.0) is preserved in `docs/release-history/`. 1.0.0 stabilizes the OpenClone CLI (`aisdf.py`), ledger schema v2, the 31 engineering domains, 56 engine specs, 13 workflows, 72 specialist roles, and task/evidence/finding/check contracts. Provider adapters are structured via `runtime/adapters/WORKER-ADAPTER-CONTRACT.md`.

### Fixed (gaps found by testing 4.0.0)
- Approvals accepted any string, including AI names. Now only registered humans, with recorded assurance.
- Tasks could become READY before their dependencies succeeded. Now enforced.
- Approval digest was stored but never re-checked. Now re-verified at READY and RUN; changing a task revokes approval; completed tasks cannot be silently re-planned.
- Success could be asserted without evidence. Now only `run` or `complete --evidence` can record it.
- Audit events could be edited undetected. Now hash-chained; `verify-ledger` detects tampering.
- README quick start pointed at a non-existent `tools/aisdf_runtime/workforce.py`. Now `python aisdf.py`.
- `MASTER-ENTRY-PROMPT.md` contradicted the README about being a runtime. Reconciled.
- Test roles could not request `execute`; "independent" reviewers could request `write`. Permission profiles corrected and role docs generated from manifests.
- CI used a floating action tag. Now pinned by commit SHA.

### Added
- Governed local command executor (`run`, `check run`), release gate, findings workflow, independent-review package, memory checker and Obsidian-compatible vault template, `security/scanners.lock.json`, `security/policies/release-gate.json`, `adapters/COMPATIBILITY.md` and `CONFORMANCE.md`, `docs/framework/RULES-AND-ENFORCEMENT.md`, `docs/framework/POSITIONING-AND-ROADMAP.md`.

### Changed
- `docs/v4` -> `docs/framework`; old demo screenshots moved to `docs/demo/legacy-v4-captures/` (they predate the hardening); old release validations moved to `docs/release-history/`.

### Known limits
No sandbox, no model adapter, no bundled scanner execution, no multi-tool conformance results yet. See `IMPLEMENTATION-STATUS.md`.

## 4.0.0 (legacy numbering) - Workforce foundation
- Introduced specialist workforce catalogue with machine-readable worker manifests and role contracts.
- Added provider-neutral task, worker, capability and permission contracts.
- Added local Python control-plane runtime with registry, DAG validation, task lifecycle, policy checks, approval records, budgets and SQLite audit ledger.
- Added dedicated security operations architecture and authorized testing controls.
- Preserved prior AISDF domains, engines, workflows, EGM-inspired specifications, project lifecycle tools and MK Framework.
- Clarified maturity boundaries: no bundled LLM, no production sandbox, no certified security scanner integrations, and no claim of fully autonomous operation.
