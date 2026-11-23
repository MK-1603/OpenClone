# OpenClone Documentation Index

## Platform Architecture & Guides
- [OpenClone Architecture Specification](architecture/OPENCLONE-2.0-ARCHITECTURE.md) — Target system architecture, component boundaries, ADRs, and module dependency model.
- [Global Plugin Installation Guide](installation/GLOBAL-PLUGIN-INSTALLATION.md) — Zero-clone global installation, CLI reference, and host lifecycle management.
- [Host Compatibility Matrix](compatibility/HOST-COMPATIBILITY.md) — Multi-host conformance matrix, extension formats, and truthful maturity ratings.
- [Security Architecture & Threat Model](security/THREAT-MODEL.md) — STRIDE threat analysis, boundary containment, and cryptographic replay defense.
- [19-Point SaaS Security Baseline](security/saas-security-baseline.md) — Pre-production SaaS security controls and verification checks.
- [Release Readiness & Implementation Status](guides/RELEASE-READINESS.md) — Transparent maturity matrix and capability ledger.
- [Repository Health Assessment](guides/REPOSITORY-HEALTH.md) — Repository baseline health report.
- [Security Status Report](security/SECURITY-STATUS.md) — Comprehensive security status and scanner lock verification.

## Core Framework & Getting Started
- [Canonical Documentation Map](DOCUMENTATION-MAP.md) — Single source of authority, subject matrices, and precedence rules.
- [Repository & Distribution Architecture](architecture/REPOSITORY-AND-DISTRIBUTION-ARCHITECTURE.md) — Lean core, native adapters, and progressive disclosure model.
- [Installation & Capability Modules Guide](installation/INSTALLATION-AND-MODULES.md) — Zero-clone host installation, updates, and on-demand capability packs.
- [Quick Start Guide](../QUICK-START.md) — Portable project workflow and optional local control plane setup.
- [Mission & Scope](../OPENCLONE-MISSION-AND-SCOPE.md) — Vision, boundaries, and architectural principles.
- [Core Principles](../OPENCLONE-CORE-PRINCIPLES.md) — Instruction-first, deterministic governance, least privilege.
- [Lifecycle Overview](../OPENCLONE-LIFECYCLE-OVERVIEW.md) — The 7-phase instruction-to-deployment engineering lifecycle.
- [Governance & Rules](../GOVERNANCE.md) — Precedence hierarchy, human approval gates, audit standards.
- [Domain Map](../DOMAIN-MAP.md) — High-level map across the 31 engineering domains.

## Portable Project Workflow & Tooling
- [Workflow WF-015: Portable Specification to Build](../workflows/WF-015-PORTABLE-PROJECT-SPECIFICATION-TO-BUILD.md) — Zero-install workflow.
- [Portable Project Intelligence Master Prompt](../prompts/PORTABLE-PROJECT-INTELLIGENCE-MASTER-PROMPT.md) — Canonical prompt for ChatGPT and Claude.
- [Templates Library](../templates/README.md) — Portable templates for `PROJECT.md`, `BUILD_PROMPT.md`, `PROGRESS.md`, `HANDOFF.md`.
- [PROJECT.md and AGENTS.md Lifecycle Guide](project-lifecycle/PROJECT-AND-AGENT-FILES.md) — Structuring specification and agent files.

## Alternatives & Fallback Engineering Suite
- [Alternatives Suite Index](alternatives/README.md) — Architecture principles for replaceable components.
- [Master Alternatives Catalogue](alternatives/ALTERNATIVES_CATALOGUE.md) — Primary implementations, fallbacks, and specialist alternatives.
- [Repository Alternatives Matrix](alternatives/REPOSITORY_ALTERNATIVES_MATRIX.md) — Evaluation of the 27 external reference repositories.
- [Provider & Model Alternatives](alternatives/PROVIDER_AND_MODEL_ALTERNATIVES.md) — Direct providers, 8 router candidates, and IDE fallback matrices.
- [UI/UX & Design Alternatives](alternatives/UI_UX_AND_DESIGN_ALTERNATIVES.md) — Component primitives, tokens, typography, and motion options.
- [Security Tool Alternatives](alternatives/SECURITY_TOOL_ALTERNATIVES.md) — SAST, DAST, secret scanning, and the 19 SaaS controls.
- [Backend & Infrastructure Alternatives](alternatives/BACKEND_AND_INFRA_ALTERNATIVES.md) — Runtimes, databases, ORMs, queues, and storage.
- [Agent & Skill Alternatives](alternatives/AGENT_AND_SKILL_ALTERNATIVES.md) — Skill formats, tool protocols (MCP), and context management.
- [Decision & Fallback Policy](alternatives/DECISION_AND_FALLBACK_POLICY.md) — Explicit triggers for provider failover and migrations.
- [Deferred & Rejected Options](alternatives/DEFERRED_AND_REJECTED_OPTIONS.md) — Record of rejected routers and unmonitored agent swarms.

## Complete Knowledge Catalogues & Taxonomy
- [Knowledge Catalogues Index](knowledge-catalogues/README.md) — Canonical software engineering taxonomies and capability mapping.
- [UI Design Catalogue](knowledge-catalogues/UI_DESIGN_CATALOGUE.md) — 86 visual styles & 232 architecture taxonomy entries across 8 layers.
- [Animation & Motion Catalogue](knowledge-catalogues/ANIMATION_MOTION_CATALOGUE.md) — 365 motion concepts, timing tokens, and 60fps rules.
- [Backend & System Design Catalogue](knowledge-catalogues/BACKEND_SYSTEM_DESIGN_CATALOGUE.md) — 580 backend topics across 23 core engineering domains.
- [AI Engineering Catalogue](knowledge-catalogues/AI_ENGINEERING_CATALOGUE.md) — 1,095 topics across 18 domains with token budgeting standards.
- [Catalogue to Product Capability Map](knowledge-catalogues/CATALOGUE_TO_PRODUCT_CAPABILITY_MAP.md) — Product classification mapping.

## Engineering Lifecycle & Independent Verification Suite
- [Lifecycle Suite Index](engineering-lifecycle/README.md) — 22-phase lifecycle and dynamic verification architecture.
- [Baseline Audit](engineering-lifecycle/BASELINE_AUDIT.md) — Pre-implementation audit and gap analysis.
- [Master Lifecycle Catalogue](engineering-lifecycle/MASTER_LIFECYCLE_CATALOGUE.md) — Complete 22-phase taxonomy and catalogued tasks.
- [Project-Type Packs](engineering-lifecycle/PROJECT_TYPE_PACKS.md) — 10 specialized project configurations.
- [Checklist Item Schema](engineering-lifecycle/CHECKLIST_ITEM_SCHEMA.md) — Data contracts for lifecycle tasks.
- [Status & Quality Gates](engineering-lifecycle/STATUS_AND_QUALITY_GATES.md) — Enforced state transitions and phase exit criteria.
- [Verification & Evidence](engineering-lifecycle/VERIFICATION_AND_EVIDENCE.md) — 6 verification levels (V0–V5) and truth checks.
- [IDE Handoff Contract](engineering-lifecycle/IDE_HANDOFF_CONTRACT.md) — Scoped context packaging and anti-hallucination guards.
- [Traceability & Change Impact](engineering-lifecycle/TRACEABILITY_AND_CHANGE_IMPACT.md) — Bidirectional mapping and change invalidation.
- [Security Model](engineering-lifecycle/SECURITY_MODEL.md) — Sandbox boundaries and secret redaction.
- [Test Matrix](engineering-lifecycle/TEST_MATRIX.md) — Automated verification and test cases.
- [Implementation Report](engineering-lifecycle/IMPLEMENTATION_REPORT.md) — Final delivery verification and acceptance record.

## Universal AI Tool Integrations & Global Plugin Ecosystem
- [27 Upstream Repositories Master Registry](integrations/INTEGRATION-REGISTRY.md) — Master provenance, commit hashes, and integration status.
- [Upstream Integration Decisions](integrations/INTEGRATION-DECISIONS.md) — Architectural rationale, what was reused, what was rejected.
- [Upstream License & Attribution Register](integrations/UPSTREAM-LICENSE-AND-ATTRIBUTION.md) — SPDX licenses, copyleft boundary isolation, and author attribution.
- [Upstream Update & Cadence Policy](integrations/UPSTREAM-UPDATE-POLICY.md) — 6-step update protocol, license diffs, and revocation procedures.
- [Universal Integrations Index](integrations/README.md) — Universal integration core, gateway, and multi-adapter architecture.
- [Universal Architecture](integrations/UNIVERSAL_INTEGRATION_ARCHITECTURE.md) — Single canonical core, multi-adapter design, and security layers.
- [Canonical Capability Registry](integrations/CAPABILITY_REGISTRY.md) — The 15 canonical capabilities, schemas, risk classes, and scopes.
- [MCP Server Specification](integrations/MCP_SERVER.md) — Model Context Protocol implementation (Tools, Resources, Prompts).
- [HTTP & OpenAPI Specification](integrations/HTTP_OPENAPI.md) — REST API endpoints, OpenAPI 3.1 schema, and webhook contracts.
- [Authorization & Scopes](integrations/AUTHORIZATION_AND_SCOPES.md) — OAuth 2.1/OIDC token claims, scoped permissions, and tenant boundaries.
- [Host Compatibility Matrix](integrations/HOST_COMPATIBILITY_MATRIX.md) — Verified compatibility across ChatGPT, Claude, Antigravity, Cursor.
- [Host Setup Guides](integrations/HOST_SETUP_GUIDES.md) — Copy-pasteable connection configs for all supported AI coding hosts.
- [Skill Portability](integrations/SKILL_PORTABILITY.md) — Canonical skill package export, lifecycle states, and runtime loading.
- [Security & Approvals](integrations/SECURITY_AND_APPROVALS.md) — Policy engine, risk classifications, and SHA-256 approval binding.
- [Conformance Tests](integrations/CONFORMANCE_TESTS.md) — Automated test suite verifying schemas, isolation, and gateway rules.
- [Migration Guide](integrations/MIGRATION_GUIDE.md) — Backward compatibility rules and migration paths for existing users.
- [Implementation Report](integrations/IMPLEMENTATION_REPORT.md) — Final delivery audit, test evidence, and release acceptance.

## Technical Architectures & Security
- [Workflow Runtime](WORKFLOW-RUNTIME.md) — State machine, dependency DAG, and cryptographic ledger.
- [27 External Repositories Intake Audit](integrations/27-repositories-audit.md) — Classification, license status, and integration models.
- [Security Toolchain Architecture](integrations/security-toolchain.md) — 12-tool classification and execution boundaries.
- [Strix Dynamic AI Pentest Integration](integrations/strix-dynamic-testing.md) — Target authorization and Docker sandboxing.
- [External LLM Router Comparison](integrations/llm-router-comparison.md) — Evaluation of 8 external router candidates.
- [Multi-Host Compatibility Matrix](integrations/compatibility-matrix.md) — Antigravity, Claude Code, Cursor, Codex verification.
- [Engineering Coverage Catalogue](engineering-coverage/CATALOGUE.md) — The 56 capability engines.
- [MK Framework Methodology](../domains/01-METHODOLOGY/MK-FRAMEWORK/README.md) — Venture-to-software execution method.
