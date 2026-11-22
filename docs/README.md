# OpenClone Documentation Index

## Core Framework & Getting Started
- [Quick Start Guide](../QUICK-START.md) — Portable project workflow and optional local control plane setup.
- [Mission & Scope](../AISDF-MISSION-AND-SCOPE.md) — Vision, boundaries, and architectural principles.
- [Core Principles](../AISDF-CORE-PRINCIPLES.md) — Instruction-first, deterministic governance, least privilege.
- [Lifecycle Overview](../AISDF-LIFECYCLE-OVERVIEW.md) — The 7-phase instruction-to-deployment engineering lifecycle.
- [Governance & Rules](../GOVERNANCE.md) — Precedence hierarchy, human approval gates, audit standards.
- [Domain Map](../DOMAIN-MAP.md) — High-level map across the 31 engineering domains.
- [Implementation Status](../IMPLEMENTATION-STATUS.md) — Transparent maturity matrix and capability ledger.

## Portable Project Workflow & Tooling
- [Workflow WF-015: Portable Specification to Build](../workflows/WF-015-PORTABLE-PROJECT-SPECIFICATION-TO-BUILD.md) — Zero-install workflow.
- [Portable Project Intelligence Master Prompt](../prompts/PORTABLE-PROJECT-INTELLIGENCE-MASTER-PROMPT.md) — Canonical prompt for ChatGPT and Claude.
- [Templates Library](../templates/README.md) — Portable templates for `PROJECT.md`, `BUILD_PROMPT.md`, `PROGRESS.md`, `HANDOFF.md`.
- [PROJECT.md and AGENTS.md Lifecycle Guide](project-lifecycle/PROJECT-AND-AGENT-FILES.md) — Structuring specification and agent files.

## Upgrade, Baseline Audit & Traceability
- [Baseline Audit](upgrade/BASELINE_AUDIT.md) — Pre-flight audit, stack discovery, and test evidence.
- [Markdown Document Inventory](upgrade/MARKDOWN_DOCUMENT_INVENTORY.md) — Complete status ledger of 52 discovered documents.
- [Requirements Traceability Matrix](upgrade/REQUIREMENTS_TRACEABILITY_MATRIX.md) — Bidirectional mapping from requirements to code and tests.
- [Conflict & Decision Register](upgrade/CONFLICT_AND_DECISION_REGISTER.md) — Trade-off records and resolved architectural contradictions.
- [Implementation Roadmap](upgrade/IMPLEMENTATION_ROADMAP.md) — Phased execution history across Phases 0–10.
- [Implementation Report](upgrade/IMPLEMENTATION_REPORT.md) — Verified deliverables, test evidence, and release readiness.

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

## Technical Architectures, Security & Integrations
- [Workflow Runtime](WORKFLOW-RUNTIME.md) — State machine, dependency DAG, and cryptographic ledger.
- [19-Point SaaS Security Baseline](security/saas-security-baseline.md) — Exhaustive pre-production SaaS security controls and verification checks.
- [27 External Repositories Intake Audit](integrations/27-repositories-audit.md) — Classification, license status, and integration models for 27 intake repos.
- [Security Toolchain Architecture](integrations/security-toolchain.md) — 12-tool classification and execution boundaries.
- [Strix Dynamic AI Pentest Integration](integrations/strix-dynamic-testing.md) — Target authorization and Docker sandboxing.
- [External LLM Router Comparison](integrations/llm-router-comparison.md) — Evaluation of 8 external router candidates.
- [Multi-Host Compatibility Matrix](integrations/compatibility-matrix.md) — Antigravity, Claude Code, Cursor, Codex verification.
- [Engineering Coverage Catalogue](engineering-coverage/CATALOGUE.md) — The 56 capability engines.
- [MK Framework Methodology](../domains/01-METHODOLOGY/MK-FRAMEWORK/README.md) — Venture-to-software execution method.
