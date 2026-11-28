# Changelog

## 2.0.0 - 2026-11-28: Universal AI Software Engineering Platform & Brand Upgrade

- **Phase 0 Project Intelligence Architect (PIA)**: Implemented canonical Sets A, B, C, D across `PIA-NEW`, `PIA-DEFINED`, and `PIA-EVOLUTION` modes.
- **Universal Product Blueprint & Design Engine**: Complete 22-phase lifecycle specification, human-crafted design systems, and responsive wireframes.
- **Project Identity, Brand & Asset Generation System (PIAGS)**: Full branding suite with 57 official SVG/PNG brand assets, multi-DPI app icons, and social cards.
- **Universal Engineering Intelligence System**: 155 engineering disciplines organized into canonical domains with modular specialist engines.
- **Universal Development & Cloud Infrastructure Intelligence**: Automated IDE/tooling recommendations, cloud provider architectures, and deployment readiness checks.
- **Complete CLI Deprecation & Pure-Platform Migration**: Removed legacy CLI shell subsystems in favor of headless MCP servers, REST gateways, and native IDE plugins.
- **Native VS Code & Antigravity Integrations**: Native extension manifests, activity bar explorer, tree views, and Antigravity autonomous engineering skills.
- **Full Quality & Test Verification**: Expanded automated test suite to 727 verified tests with 100% pass rate and clean repository structure validation.
- **Release Documentation**: Published comprehensive [`RELEASE-NOTES.md`](RELEASE-NOTES.md).

## 2.5.0 - 2026-11-25: Native Windows Executable & Installer Packaging

- **Standalone Windows Executable (`dist/oc.exe`)**: Compiled full console application binary via PyInstaller bundling all dependencies, schemas, worker contracts, and templates (14.61 MB standalone).
- **One-Folder Distribution (`dist/openclone/`)**: Packaged full runtime directory for maximum deployment reliability.
- **Native Windows Setup Installer (`packaging/windows/openclone_installer.iss`)**: Authored Inno Setup compiler configuration producing `installer/OpenClone-Setup.exe` with dual-mode privilege support (`{autopf}` or `%LOCALAPPDATA%\Programs\OpenClone`), defensive PATH registration (prevents duplicates and preserves existing paths), Start Menu integration, and clean uninstallation.
- **Directory & Data Separation**: Strictly separated immutable program files from `%APPDATA%\OpenClone\config.json`, `%LOCALAPPDATA%\OpenClone\`, and `<project>\.openclone\audit.db`, guaranteeing zero data loss on upgrade or uninstall.
- **Automated PowerShell Build Script (`packaging/windows/build.ps1`)**: Complete 8-stage automated build workflow checking Python versions, verifying dependencies, running tests, cleaning artifacts, compiling `oc.exe`, validating binaries, generating SHA-256 checksums, and building `OpenClone-Setup.exe`.
- **Frozen Runtime Asset Resolution**: Enhanced `RuntimeManager`, `Doctor`, and `InstallationManager` with `sys._MEIPASS` inspection for 100% health validation inside frozen binary environments.
- **Release Automation (`.github/workflows/release.yml`)**: Added `build-windows-package` job on `windows-latest` compiling and publishing `oc.exe` and `OpenClone-Setup.exe` to GitHub Releases.
- **Automated Verification**: Added 6 tests in `tests/test_windows_packaging.py`; verified full test suite at **469/469 tests passing (100% pass rate)**.

## 2.4.0 - 2026-11-25: Conversational AI Terminal Assistant & Natural Language Engine

- **Conversational AI Engineering Assistant (`src/openclone/cli_oc/chat/`)**: Transformed the interactive terminal into a real conversational AI engineering assistant with streaming response pacing, multi-turn session history, and full context awareness.
- **Model Intelligence Engine (MIE) Provider Integration**: Connected assistant directly to configured zero-dependency LLM providers (`GeminiProvider`, `OpenAIProvider`, `AnthropicProvider`, `OllamaProvider`), supporting online inference and local AI daemons.
- **Truthful Maturity Invariant**: Implemented honest offline fallback when no AI provider API keys are configured, displaying clear setup instructions for environment variables (`GEMINI_API_KEY`, `OPENAI_API_KEY`, etc.) and directing users to local deterministic tools without pretending an AI model is connected.
- **Conversational Tool Orchestration**: Natural-language engineering queries dynamically classify intent and dispatch directly to real OpenClone inspection, planning, workforce, verification, and diagnostics engines.
- **15 Integrated Slash Commands**: Supported `/help`, `/inspect`, `/plan`, `/run`, `/agents`, `/models`, `/providers`, `/workflows`, `/verify`, `/status`, `/history`, `/new`, `/clear`, `/doctor`, `/exit`.
- **Bounded Project Context Intelligence (`src/openclone/cli_oc/chat/context.py`)**: Gathers real Git metrics, detected tech stack, and bounded documentation excerpts (max 3KB with secret redaction) injected as system prompt context.
- **Automated Verification**: Added 17 tests in `tests/test_conversational_terminal.py`; verified full test suite at **463/463 tests passing (100% pass rate)**.

## 2.3.0 - 2026-11-25: Professional Command-Driven Developer Terminal

- **Interactive Command Shell (`oc>`)**: Eliminated numbered-menu navigation in favor of a professional, non-redrawing interactive command shell resembling Git, Docker, and GitHub CLI (`gh`). Handles command history, quoted arguments, paths with spaces, and clean exit semantics.
- **Modular Command Registry (`src/openclone/cli_oc/registry.py`)**: Centralized typed registry organizing commands into 11 categories (Core, Project, Planning, Execution, Workforce, Intelligence, Workflows, Verification, Integrations, Runtime, Platform) with standardized error codes and fuzzy typo suggestions (e.g. `modles` $\rightarrow$ `Did you mean: oc models?`).
- **Accurate Git Intelligence Engine**: Resolved "Active Branch: unknown" and "Tracked Files: 0" defects in `AutonomousExecutionEngine._inspect()` by integrating `git rev-parse`, active branch detection (including detached HEAD states), accurate `git ls-files` tracking count, and detailed modified/untracked delta breakdown.
- **Terminal Input Isolation**: Resolved input bleeding between commands and shell loops by implementing input buffer flushing and isolated process stdin management.
- **Positional Command Arguments**: Added first-class support for positional targets and list verbs across all CLI commands (`oc inspect [path]`, `oc verify [path]`, `oc plan "<requirement>"`, `oc agents [list]`, `oc models [list]`, `oc workflows [list]`).
- **Comprehensive Terminal Test Suite (`tests/test_oc_terminal_shell.py`)**: Added 20 automated tests validating command registry, shlex parsing, Git accuracy, typo suggestions, empty line resilience, and interactive shell lifecycle (446 total tests passing).

## 2.2.0 - 2026-11-25: Universal IDE & Platform Extension Ecosystem

- **Official Google Antigravity Marketplace Plugin (`plugins/openclone-antigravity/`)**: Packaged native Antigravity plugin manifest (`plugin.json`), MCP server stdio definition (`mcp_config.json`), vector logo asset (`assets/logo.svg`), subagent specification (`agents/openclone-engineer.md`), deterministic rules (`rules/AGENTS.md`), autonomous engineering skill (`skills/openclone-engineering/SKILL.md`), and repository audit lifecycle hook (`hooks.json`).
- **Native Visual Studio Code & Cursor Extension (`extensions/vscode/`)**: Built complete VS Code extension manifest (`package.json`), Activity Bar navigation (`openclone-explorer`), tree views (`openclone-status`, `openclone-plan`, `openclone-workers`, `openclone-ledger`), command palette actions, vector icon (`resources/icon.svg`), and runtime entrypoint (`src/extension.js`).
- **Dual Installation Model (Workspace & Global)**: Extended `AntigravityAdapter` and `IntegrationManager` with `--global` / `-g` support, routing to `~/.gemini/config/plugins/openclone/` globally or `<workspace>/.gemini/plugins/openclone/` locally, complete with automated configuration backup and rollback.
- **Architectural Audits & Governance Documentation**: Published comprehensive Extension Architecture Audit ([`docs/audits/OPENCLONE_EXTENSION_ARCHITECTURE_AUDIT.md`](docs/audits/OPENCLONE_EXTENSION_ARCHITECTURE_AUDIT.md)), Architecture Specification ([`docs/architecture/OPENCLONE_EXTENSION_ARCHITECTURE.md`](docs/architecture/OPENCLONE_EXTENSION_ARCHITECTURE.md)), Test Report ([`docs/reports/OPENCLONE_EXTENSION_TEST_REPORT.md`](docs/reports/OPENCLONE_EXTENSION_TEST_REPORT.md)), Deployment Readiness Assessment ([`docs/reports/OPENCLONE_EXTENSION_DEPLOYMENT_READINESS.md`](docs/reports/OPENCLONE_EXTENSION_DEPLOYMENT_READINESS.md)), and Compatibility Matrix ([`docs/reference/OPENCLONE_IDE_COMPATIBILITY_MATRIX.md`](docs/reference/OPENCLONE_IDE_COMPATIBILITY_MATRIX.md)).
- **Extension CI/CD Pipeline (`.github/workflows/extension-ci.yml`)**: Automated GitHub Actions workflow validating manifest schemas, packaging zip artifacts, and running automated extension tests.
- **Automated Verification**: Added 16 tests in `tests/test_extension_ecosystem.py`; verified full test suite at **426/426 tests passing (100% pass rate)**.

## 2.1.0 - 2026-11-25: Autonomous Engineering Execution Engine & Brand Restoration

- **Complete OpenClone Brand Restoration**: Restored official product identity as **OpenClone — Universal AI Engineering Platform** across all core modules, CLI entry points, documentation, packaging scripts, and schema definitions.
- **Autonomous Engineering Execution Engine (`src/openclone/autonomous/`)**: Implemented the unified 12-stage controlled execution lifecycle (`REQUEST` $\rightarrow$ `UNDERSTAND` $\rightarrow$ `INSPECT` $\rightarrow$ `PLAN` $\rightarrow$ `VALIDATE PLAN` $\rightarrow$ `APPROVE` $\rightarrow$ `ROUTE MODEL` $\rightarrow$ `ASSIGN AGENTS` $\rightarrow$ `EXECUTE` $\rightarrow$ `TEST` $\rightarrow$ `VERIFY` $\rightarrow$ `DELIVER`).
- **5 Programmatic Execution Modes**: Formalized deterministic policies for `Instant`, `Fast`, `Standard`, `Deep`, and `Autonomous` modes governing task limits, reasoning tiers, token budgets, and verification depths.
- **Model Intelligence Integration**: Dynamic routing mapping task requirements to appropriate AI model provider tiers (local/fast, balanced, reasoning, frontier).
- **Bounded Repair Loop**: Automated failure classification (`SYNTAX_ERROR`, `TEST_ASSERTION`, `DEPENDENCY_MISSING`, `TIMEOUT`) with deterministic retry limits preventing infinite execution loops.
- **Unified CLI Command**: Added `openclone autonomous "<prompt>" [--mode <mode>]` generating structured markdown delivery reports with cryptographic audit ledger references.

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

Versioning note: the public version is standardized to 1.0.0. The earlier internal numbering (3.x, 4.0.0) is preserved in `docs/release-history/`. 1.0.0 stabilizes the OpenClone CLI (`openclone.py`), ledger schema v2, the 31 engineering domains, 56 engine specs, 13 workflows, 72 specialist roles, and task/evidence/finding/check contracts. Provider adapters are structured via `runtime/adapters/WORKER-ADAPTER-CONTRACT.md`.

### Fixed (gaps found by testing 4.0.0)

- Approvals accepted any string, including AI names. Now only registered humans, with recorded assurance.
- Tasks could become READY before their dependencies succeeded. Now enforced.
- Approval digest was stored but never re-checked. Now re-verified at READY and RUN; changing a task revokes approval; completed tasks cannot be silently re-planned.
- Success could be asserted without evidence. Now only `run` or `complete --evidence` can record it.
- Audit events could be edited undetected. Now hash-chained; `verify-ledger` detects tampering.
- README quick start pointed at a non-existent `tools/openclone_runtime/workforce.py`. Now `python openclone.py`.
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
