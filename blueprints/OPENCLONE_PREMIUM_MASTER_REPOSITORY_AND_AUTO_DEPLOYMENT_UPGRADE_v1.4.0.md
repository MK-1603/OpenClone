# OPENCLONE — PREMIUM MASTER REPOSITORY, PLATFORM & APPLICATION DELIVERY UPGRADE
## Antigravity in-place execution specification | v1.4.0
**Canonical objective:** Upgrade the existing OpenClone repository and framework in place. Consolidate its architecture, integrations, UI/UX intelligence, security, repository structure, and automatic deployment of applications built through OpenClone.

> **This is the single consolidated master specification.** It supersedes the separate execution prompts v1.2.1 and v1.3.0 for this upgrade. Do not run those older prompts as independent projects. Use this document as the source of truth, while preserving any more specific existing governance rules in the repository.

## Critical clarification: what must auto-deploy

The key product requirement is that **when a user builds an application using OpenClone, OpenClone should be able to automatically deploy that user's application** through an authorized hosting provider. This is separate from deploying OpenClone itself. The application lifecycle, approval gates, CI/CD, provider adapters, verification and rollback are specified in Section 17.

## Execution contract

- Work inside the existing OpenClone repository; do not create a parallel framework or second repository.
- Verify the actual local checkout, remote, branch and commit before acting. The known remote was `MK-1603/aisdf`; verify rather than assume.
- Antigravity is the local implementation agent. It must inspect, edit, execute tests and report evidence. This document does not itself modify the repository.
- Preserve uncommitted work and existing capabilities. Never use destructive Git operations to force a clean state.
- Do not push, merge, publish, provision paid resources, connect accounts, expose applications publicly, change production configuration or deploy to production without the required owner authorization.
- Distinguish specified, implemented, tested, connected, deployed and production-hardened capabilities. A prompt, schema, mock or generated config is not proof of a working integration.
- Do not claim execution or verification without actual command output and evidence.

---

# PART A — UNIFIED PLATFORM AND FULL-STACK REPOSITORY UPGRADE (v1.2.1)

# OpenClone — Unified Platform Integrations & Full-Stack Repository Upgrade
## Antigravity execution brief | Version 1.2.1 | In-place upgrade | Full UI/UX skill orchestration | Final-release objective

**Product:** OpenClone  
**Canonical repository currently known:** `MK-1603/aisdf`  
**Product mission:** A universal, governed AI software-engineering framework that can be invoked from multiple AI platforms through one shared capability layer.  
**Target platforms:** ChatGPT, Claude, OpenAI Codex, and Google Gemini.  
**Core principle:** One OpenClone core. Four platform integrations. One source of truth.

---

# 1. Mission

Work inside the user's existing local clone of the OpenClone repository. First inspect the actual current repository and establish a verified baseline. Then upgrade the existing repository in place, integrating the platform plugin system, recommendation/connector capabilities, token and cost governance, UI/UX improvements, testing, security, documentation, and deployment/release engineering.

This is **not** a request to create a separate plugin project, a second framework, a parallel repository, or a detached `UPGRADE/` tree. Do not create `OPENCLONE-V2/`, `NEW-CORE/`, `PLUGINS-NEW/`, `UPGRADE/`, or equivalent parallel structures. Extend the current architecture and place each capability in the existing domain/engine/module that owns that responsibility. Add a new domain or package only when the audit proves that no existing location can own it cleanly; document the reason and update all maps, indexes, dependencies, and governance references.

Do not stop after producing plans or documentation. The intended outcome is a tested, reviewable, versioned repository release candidate. Implement what is safely possible in the local environment, run the available checks, document anything blocked by missing credentials/platform access, and never claim a deployment or external integration succeeded unless it was actually verified.

## Non-negotiable principles

Preserve and enforce the existing OpenClone principles:
1. Evidence over claims.
2. Approval before consequential actions.
3. Least privilege.
4. Change Only Law.
5. No AI Slope.
6. Traceability and provenance.
7. Freshness and review.
8. Full completion.
9. Independent verification.
10. Right-sized engineering.
11. User-intent preservation.
12. Honest limitations.

Maintain existing rule precedence and resolve conflicts explicitly. Do not silently weaken security, approvals, project constraints, or existing acceptance criteria to make tests pass.

---

# 2. Required execution order

Use this sequence. Do not skip stages or begin broad implementation before the baseline audit.

| Stage | Work | Exit evidence |
|---|---|---|
| 0 | Repository discovery and baseline | Inventory, current commit, commands, clean/dirty state |
| 1 | Gap and architecture audit | Capability maturity matrix and prioritized gap register |
| 2 | Target architecture and compatibility contracts | Approved-in-repo design, ADRs, schemas |
| 3 | Shared OpenClone core/tool API | Contract tests and local execution |
| 4 | Four platform integrations | Per-platform compatibility evidence |
| 5 | Recommendation and connector system | Registry, alternatives, auth/scope tests |
| 6 | Token/model/cost optimization | Budget, routing, telemetry and policy tests |
| 7 | Full UI/UX engineering and multi-skill orchestration | Style-system registry, component/button audit, skill compatibility, responsive/accessibility evidence |
| 8 | Security, reliability, testing and supply chain | Security and quality gates |
| 9 | Deployment and release engineering | Reproducible build, deployment guide, smoke tests |
| 10 | Documentation and migration | Updated canonical docs and migration notes |
| 11 | Independent final verification | Release checklist, known limitations, final version |

At the beginning, perform **Stage 0 only** and report findings. Continue through the remaining stages without waiting for additional user messages unless an action is destructive, externally consequential, paid, credential-sensitive, or requires a product decision that cannot be safely inferred. For those actions, stop and request approval. For reversible local implementation choices, select the simplest defensible option and record the rationale.

---

# 3. Stage 0 — Inspect the real repository

1. Confirm repository root, remote URL, current branch, current commit SHA, working-tree status, submodules, package managers, runtime versions, and available build/test commands.
2. Read the repository's `AGENTS.md`, README, project mission/scope, core principles, rulebook, governance, architecture maps, engine standards, workflow standards, security policy, assessment reports, and relevant nested agent instructions before editing.
3. Recursively inventory source, specs, prompts, skills, schemas, tests, examples, CI workflows, deployment manifests, infrastructure, generated files, and hidden configuration.
4. Identify actual executable entry points and runtime modules. Distinguish documentation-only assets from executable code.
5. Run baseline tests, schema validation, lint, typecheck, formatting checks, build, and repository validation where available. Capture exact commands, exit codes, and logs.
6. Record pre-existing failures separately. Do not attribute old failures to new changes.
7. Detect duplicated, orphaned, contradictory, stale, misnamed, or misplaced files. Check domain README headings and metadata against their actual folder names.
8. Identify secret leakage, unsafe defaults, missing license notices, dependency risks, generated artifacts, and overly broad permissions.
9. Map all current engines and domains to: owner, inputs, outputs, dependencies, maturity, tests, source files, evidence, and upgrade disposition.

Create or update the existing canonical assessment location (do not create a detached upgrade folder):
- Repository inventory
- Current architecture and dependency map
- Capability maturity matrix
- Existing test and validation baseline
- Gap and risk register
- Duplication/conflict/staleness report
- Integration coverage matrix
- UI/UX and accessibility audit (if a UI exists)
- Deployment/release audit
- Token/cost governance audit

Use these maturity labels consistently:
`CONCEPT`, `SPECIFIED`, `DESIGNED`, `IMPLEMENTED`, `UNIT_TESTED`, `INTEGRATION_TESTED`, `END_TO_END_VERIFIED`, `PRODUCTION_HARDENED`, `DEPRECATED`, `BLOCKED`.

A README, prompt, schema, mock, adapter interface, or passing unit test does not prove a live third-party integration. Label evidence precisely.

---

# 4. Target architecture — one core, four adapters

Implement a provider-independent architecture. The exact package and directory placement must follow the existing repository's conventions.

```text
ChatGPT adapter ─────┐
Claude adapter ──────┤
OpenAI Codex adapter ├── OpenClone MCP / Tool Gateway ── OpenClone Core
Gemini adapter ──────┘                                  │
                                                        ├─ Governance & policy
                                                        ├─ Project intelligence
                                                        ├─ Engineering engines
                                                        ├─ Recommendation engine
                                                        ├─ Connector registry
                                                        ├─ Model/router registry
                                                        ├─ Context & token optimizer
                                                        ├─ Evidence/audit ledger
                                                        ├─ Verification engine
                                                        └─ UI/UX & delivery workflows
```

## 4.1 Shared core

The shared core owns all business logic and policy:
- Project and workspace context.
- Requirement and architecture workflows.
- Engineering engine orchestration.
- Recommendation scoring and alternatives.
- Connector capability registry.
- Model selection and routing policies.
- Context retrieval and token budgets.
- Approval and permission checks.
- Evidence, provenance, audit events, and verification.
- Error taxonomy and normalized result contracts.

No platform adapter may independently implement or override core engineering rules.

## 4.2 MCP/tool gateway

Use Model Context Protocol (MCP) as the primary interoperability layer where supported. Treat MCP as a protocol surface, not as the entire product architecture. Keep domain logic behind stable, versioned OpenClone contracts.

Provide:
- Versioned tool schemas and capability discovery.
- Resource and prompt exposure only where useful and supported.
- Transport configuration appropriate to local and remote use.
- Authentication and authorization for remote access.
- Request validation, rate limits, timeouts, cancellation, idempotency where applicable.
- Structured errors and correlation IDs.
- Health/readiness endpoints for deployed services.
- Audit logging without storing secrets or unnecessary prompt content.
- Backward-compatibility and deprecation policy.

Avoid exposing an excessively large tool catalog. Group capabilities by task and use a small, composable, discoverable tool surface.

## 4.3 Four platform adapters

Build and verify these four adapters against each platform's current official documentation and actual supported integration mechanisms:

1. **OpenClone for ChatGPT**
2. **OpenClone for Claude**
3. **OpenClone for OpenAI Codex**
4. **OpenClone for Google Gemini**

Each adapter must document:
- Supported connection mechanism and protocol/transport.
- Setup and installation steps.
- Authentication and authorization model.
- Tool discovery and invocation behavior.
- Platform-specific limitations.
- Supported features and unsupported features.
- Compatibility/version matrix.
- Local test procedure and, where credentials/access exist, live smoke-test procedure.

Do not assume that all four platforms support identical MCP transports, OAuth flows, tool annotations, resource types, prompts, or mention syntax. Verify current official docs. A universal `@OpenClone` mention cannot be promised across platforms; describe the actual invocation pattern each platform supports. Do not simulate an integration by adding only a configuration snippet.

### Adapter contract

Each adapter must translate platform-specific requests into a shared OpenClone request envelope, and translate core responses into the platform's supported result format.

Minimum normalized request fields:
- `request_id`
- `platform`
- `platform_user_id` or privacy-preserving identity reference
- `workspace_id`
- `project_id` (optional)
- `task`
- `arguments`
- `requested_capabilities`
- `approval_context`
- `budget_policy`
- `locale` (optional)

Minimum normalized response fields:
- `request_id`
- `status`
- `summary`
- `structured_result`
- `artifacts` (optional)
- `evidence_refs`
- `warnings`
- `required_approvals`
- `usage` (tokens/cost/latency where available)
- `next_actions`

Validate all inputs. Never trust platform-provided identity or project ownership without authentication and authorization checks.

---

# 5. OpenClone tool experience

Aim for a natural single integration entry point per platform, not four unrelated products. The user should be able to invoke OpenClone's capabilities from the supported platform's normal app/tool/connector interface.

Example intended experiences (illustrative only; actual syntax must match each platform):
- ChatGPT: select or mention the installed OpenClone app, then ask it to inspect or build a project.
- Claude: enable the OpenClone MCP connector, then request an engineering workflow.
- Codex: configure the OpenClone MCP server in the supported Codex environment, then invoke its tools during coding.
- Gemini: connect the supported OpenClone integration, then request project analysis or engineering assistance.

Provide a compact tool surface such as:
- `openclone_discover`
- `openclone_project_inspect`
- `openclone_recommend`
- `openclone_plan`
- `openclone_execute_approved`
- `openclone_verify`
- `openclone_status`

These are candidate names, not mandatory names. Reuse existing engines and tools where they already exist. Avoid creating multiple tools that perform the same action. Provide capability discovery so clients can learn which optional features are enabled.

Separate read/analysis actions from writes/execution actions. Default to read-only. Require explicit approval for consequential changes, external service writes, deployment, destructive actions, purchases, and permission expansion.

---

# 6. Recommendation and connector system

Upgrade the existing technology intelligence and integration engineering capabilities into a coherent recommendation and connector lifecycle. This must cover, at minimum:

## 6.1 Recommendation categories

- Frontend: web frameworks, UI libraries, styling, component systems, state, forms, accessibility.
- Backend: runtimes, frameworks, API styles, background workers.
- Data: relational/document databases, cache, search, vector storage, object storage, queues/event streaming.
- AI: model providers, hosted models, local models, embeddings, rerankers, speech, image, multimodal services.
- Developer tools: coding agents, IDEs, source control, CI, package managers, testing tools.
- Infrastructure: cloud, edge, containers, hosting, secrets, DNS, CDN.
- Quality and operations: observability, logging, tracing, metrics, error tracking, security scanning, backup, incident response.

## 6.2 Alternatives are mandatory

For every material technology recommendation:
- Recommend one primary option.
- Include at least two credible alternatives when available.
- Explain why the primary fits the requirements.
- Compare trade-offs: performance, security/privacy, reliability, maturity, ecosystem, compatibility, licensing, cost, vendor lock-in, operations, team skills, and portability.
- Cite evidence with source and retrieval date.
- State uncertainty and missing evidence.
- State when the recommendation should be reconsidered.
- Do not invent pricing, benchmarks, features, or compatibility.
- If only one credible option exists, explain why and mark alternatives unavailable rather than fabricate them.

Support user constraints such as `open_source_only`, `self_hosted`, `local_first`, `privacy_first`, `budget_limit`, `preferred_stack`, `region`, `compliance`, and `team_experience`.

## 6.3 Connector lifecycle

Implement a registry and lifecycle with explicit states:
`DISCOVERED → EVALUATED → RECOMMENDED → AWAITING_APPROVAL → CONFIGURED → AUTHENTICATED → CONNECTED → HEALTH_CHECKED → VERIFIED`
and terminal/exception states such as `REJECTED`, `DISCONNECTED`, `EXPIRED`, `DEGRADED`, `BLOCKED`.

Connector metadata:
- Provider and product identity.
- Category and supported capabilities.
- Supported protocols/APIs/SDKs.
- Authentication type and required scopes.
- Data accessed and data transmitted.
- Region/data residency where relevant.
- Pricing/billing considerations.
- Rate limits and quotas.
- Reliability and health signals.
- Version/compatibility range.
- Primary/secondary/fallback designation.
- Evidence and last verification timestamp.

**Recommend mode is the default.** It may research and propose. **Connect mode requires explicit user authorization** and only then may guide or execute a connection within granted scopes. Never create accounts, purchase plans, provision paid resources, share user data, or change external permissions without explicit approval.

Distinguish:
- MCP server connection.
- Native platform app/connector.
- Provider API/SDK integration.
- CLI/tool integration.
- Local service integration.

Do not call all of these “plugins” when their security and lifecycle differ.

## 6.4 Credential and access security

- Never store raw API keys in source control, logs, prompts, generated docs, or plaintext config.
- Use environment variables for local development and an appropriate secret manager for deployment.
- Support credential rotation, revocation, expiry, and least-privilege scopes.
- Redact secrets and sensitive headers.
- Validate callback URLs, origins, redirect URIs, and token audiences.
- Protect against SSRF, path traversal, command injection, prompt injection, tool poisoning, confused-deputy attacks, and cross-tenant data access.
- Treat tool outputs and retrieved documents as untrusted input.
- Add per-user, per-workspace, and per-project authorization tests.
- Provide an emergency connector disable/revoke path.

---

# 7. Model intelligence, routing, and fallback

Build a model capability registry rather than hard-coding a single provider.

Track:
- Provider, model identifier, version/snapshot, availability.
- Input/output modalities.
- Context window (only from verified current source).
- Tool/function calling support.
- Structured output support.
- Streaming support.
- Reasoning capability where documented.
- Embedding/reranking/speech/image capabilities.
- Region and data handling.
- Price per input/output token where published and current.
- Rate limits and quota information where available.
- Latency/quality evidence and verification date.

Provide routing policies:
- `economy`
- `balanced`
- `quality`
- `privacy_first`
- `local_first`
- `manual_only`

Selection must consider task type, capability fit, project policy, privacy, quality requirements, context size, latency, budget, provider availability, and user preference.

### Alternatives and fallback

For each enabled model capability:
- Define primary provider/model.
- Define a secondary alternative when feasible.
- Define fallback behavior and retry limits.
- Respect data residency and privacy policy; do not silently send data to a different provider.
- Do not automatically downgrade a high-risk task to a weaker model.
- Require explicit policy permission before cross-provider failover.
- Record routing decisions and reasons without retaining unnecessary sensitive prompt data.

Never claim two models are interchangeable just because both accept text. Verify required tool calling, structured output, modality, context, safety, and reliability behavior.

---

# 8. Token, context, latency, and cost optimization

Implement measurable optimization without degrading correctness or safety.

Required capabilities:
1. Per-request, per-session, per-project, and per-workspace token/cost budgets where provider usage is available.
2. Usage telemetry: input/output tokens, cached tokens if reported, model, latency, retries, tool calls, estimated/actual cost, and source of estimate.
3. Progressive disclosure: load only relevant instructions, engine specs, project files, and tool schemas.
4. Targeted retrieval instead of sending the entire repository or all 56 engine specifications to every request.
5. Context compaction and summaries with provenance and links to original evidence.
6. Reuse stable results only when freshness, project scope, permissions, and cache policy allow.
7. Prefer deterministic code, schemas, scripts, and local tools over LLM calls for mechanical work.
8. Batch compatible read operations where safe; parallelize only independent work.
9. Avoid repeated repository scans, duplicate tool calls, and verbose tool output.
10. Budget-aware model routing with explicit policy constraints.
11. Stop and request approval when a budget or spend threshold is reached; never silently incur paid usage.
12. Report measured savings only when a baseline and measurement support the claim.

Do not optimize tokens by dropping security instructions, acceptance criteria, source evidence, user requirements, or necessary verification. Token optimization is subordinate to correctness and policy.

---

# 9. UI/UX and product experience upgrade

First determine whether the current repository contains an actual user-facing application, a documentation-only framework, or both. Do not invent an existing UI. If a UI exists, audit and improve it. If no UI exists, propose the smallest useful control surface consistent with the existing mission and architecture; do not build a large dashboard merely for appearance.

## 9.1 Design governance

Use the existing design rules and integrate useful Taste Skill principles without blindly copying its files or assets. Inspect license and attribution requirements before vendoring any third-party material.

Lifecycle:
`DISCOVER → INSTRUCTION AUDIT → PRODUCT UNDERSTANDING → CURRENT UI AUDIT → VISUAL/UX GAP ANALYSIS → DESIGN STRATEGY → PRE-IMPLEMENTATION GATE → IMPLEMENTATION → VISUAL VERIFICATION → ACCESSIBILITY/PERFORMANCE REVIEW`.

Discover all applicable instructions (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules`, Copilot instructions, design system docs, component conventions) and resolve conflicts using repository governance.

## 9.2 Anti-generic / anti-slop rules

Do not rely on a universal visual recipe. Avoid defaulting to generic AI gradients, neon accents, random glassmorphism, excessive rounded cards, decorative icons, oversized hero text, meaningless metrics, repetitive layouts, or animations without purpose.

Classify each design pattern as:
- `REQUIRED`
- `JUSTIFIED`
- `OPTIONAL`
- `UNNECESSARY`
- `PROHIBITED`

Choose visual language from the product's audience, task, brand, content density, accessibility needs, and usage context. Preserve existing approved design tokens and user brand decisions unless a documented audit justifies change.

## 9.3 Removal-first audit

Classify existing UI elements:
- `PRESERVE`
- `MODIFY`
- `REMOVE`
- `ADD`

Remove visual noise before adding features. Never remove business logic, user data, accessibility behavior, security controls, or important workflows without explicit approval.

## 9.4 Quality requirements

- Clear information architecture and navigation.
- Strong hierarchy and readable typography.
- Consistent design tokens and component variants.
- Responsive behavior across mobile, tablet, desktop.
- Keyboard navigation and visible focus.
- Semantic HTML and accessible labels.
- WCAG 2.2 AA target where applicable; document exceptions.
- Loading, empty, error, success, offline, and permission-denied states.
- Useful onboarding and actionable error messages.
- Avoid unnecessary motion; respect reduced-motion preferences.
- Performance budgets and image/font optimization.
- Visual regression or screenshot evidence for critical flows.
- No fake buttons, fake integrations, or placeholder success states.

If a UI is implemented, include at least:
- Project/workspace overview.
- Integration catalog and connection state.
- Technology/model recommendations with alternatives and rationale.
- Approval and permissions view.
- Usage/cost overview with clear estimate-vs-actual distinction.
- Verification/status view.
Only implement surfaces justified by the actual product scope.

---

# 10. Security, privacy, and trust architecture

Perform threat modeling for the shared core, MCP gateway, adapters, connectors, model routing, project files, and deployment.

Cover:
- Authentication, authorization, session management.
- Tenant/workspace/project isolation.
- RBAC/ABAC as appropriate.
- Least-privilege scopes and tool allowlists.
- Prompt injection and untrusted tool output.
- Secret handling and redaction.
- SSRF, CSRF, XSS, SQL injection, command injection, path traversal.
- Supply-chain and dependency security.
- Rate limiting, abuse controls, replay protection.
- Audit integrity and retention.
- Data minimization, deletion, export, retention policies.
- Secure defaults and safe error handling.
- Backup/restore and incident response.
- Model provider data handling and cross-provider failover.
- MCP transport security and origin validation.

Use threat modeling appropriate to the system (for example STRIDE) and produce a risk register with severity, likelihood, mitigation, owner, and residual risk. Do not claim compliance certification. Map relevant controls to standards only when evidence supports the mapping.

---

# 11. Testing and verification strategy

Build a test pyramid and execute what is possible:

## 11.1 Static and unit
- Formatting, lint, type checks.
- Schema validation.
- Unit tests for policies, scoring, routing, budgets, lifecycle state machines, permission checks, redaction, error mapping.
- Deterministic tests with mocked providers.

## 11.2 Contract and integration
- MCP tool schema and protocol conformance.
- Adapter contract tests for all four platforms.
- Provider adapter tests.
- Connector lifecycle and OAuth callback tests where applicable.
- Database migration and persistence tests.
- Cache/queue/search integration tests if those services are part of the actual implementation.
- Tenant isolation and authorization tests.

## 11.3 End-to-end
- Install/configure adapter.
- Discover OpenClone tools.
- Authenticate.
- Inspect a test project.
- Request recommendation with alternatives.
- Execute a harmless approved workflow.
- Verify output and evidence.
- Test provider failure and permitted fallback.
- Test token budget exhaustion.
- Test disconnect/revoke.
- Test unauthorized access is denied.

Use sandbox/test accounts and fake credentials for tests. Never run destructive tests against production. For platform live tests, record whether credentials and access were available; do not label mocked tests as live tests.

## 11.4 UI and deployment
- Responsive browser tests across representative mobile, tablet, and desktop viewports.
- Accessibility checks including keyboard-only navigation, focus visibility, semantic roles/names, contrast, zoom, reduced motion, and automated WCAG checks.
- Button/action and component-state interaction tests, including disabled/loading/error/destructive states.
- Visual regression for critical flows and selected style/morphism direction.
- Multi-skill orchestration tests for discovery, permission boundaries, instruction precedence, handoffs, and evidence collection.
- Build and production-mode smoke tests.
- Health/readiness checks.
- Deployment configuration validation.
- Rollback and backup/restore rehearsal where environment permits.

Every test report must contain exact command, environment, date, result, and limitations. Separate `PASS`, `FAIL`, `SKIPPED`, and `BLOCKED`.

---

# 12. Deployment and release engineering

Inspect the actual stack and hosting choices before prescribing a deployment topology. Prefer the smallest secure, maintainable architecture that meets measured requirements. Provide alternatives and trade-offs for material hosting choices.

Required deployment work:
1. Reproducible development setup and one-command local start where practical.
2. Environment variable inventory with safe `.env.example` values only.
3. Separate development, staging, and production configurations.
4. Containerization only if justified; secure non-root images, pinned base images, multi-stage builds, health checks, minimal runtime image.
5. CI pipeline for lint, typecheck, unit/contract tests, schema validation, build, dependency/security checks.
6. Staging deployment workflow and smoke tests.
7. Production deployment guide with approvals and rollback.
8. Database migration strategy, backups, restore procedure, and connection security.
9. TLS, secure headers, CORS, CSRF strategy, rate limiting, secrets management.
10. Logs, metrics, traces, alerts, uptime and readiness checks.
11. Release tags, changelog, semantic versioning, artifact provenance/SBOM where feasible.
12. Rollback and incident response instructions.
13. Cost estimates must identify assumptions and date; no invented pricing.

Do not deploy to a live account, provision paid services, alter DNS, rotate production secrets, run production migrations, or publish a release without explicit owner approval. Prepare and validate deployment artifacts locally. Clearly distinguish:
- `LOCAL_BUILD_VERIFIED`
- `STAGING_DEPLOYED`
- `STAGING_SMOKE_TESTED`
- `PRODUCTION_DEPLOYED`
- `PRODUCTION_SMOKE_TESTED`

A successful local build is not a deployment.

---

# 13. Documentation, organization, and maintainability

Update the canonical existing docs and indexes in place. Ensure there is one source of truth for:
- Mission and scope.
- Architecture and domain ownership.
- Engine/tool catalog.
- Platform compatibility.
- Connector registry.
- Model capability registry.
- Security and permissions.
- Token/cost policies.
- UI/UX governance.
- Testing and release gates.
- Deployment and operations.

Every new or modified engine/spec must include:
- Purpose and non-goals.
- Inputs/outputs.
- Dependencies.
- Permissions and risk classification.
- Failure modes.
- Evidence/provenance requirements.
- Acceptance criteria.
- Unit/contract/integration test mapping.
- Version and compatibility.
- Alternatives and reconsideration triggers where relevant.

Remove stale duplication only after checking references and preserving history. Fix incorrect headings, broken links, inconsistent identifiers, mismatched metadata, and orphaned files. Keep examples runnable and clearly label mock/example credentials.

---

# 14. Implementation quality and change control

- Make small, reviewable, coherent changes.
- Preserve backward compatibility where possible.
- Add migrations for breaking schema changes.
- Use feature flags for risky optional capabilities.
- Keep adapters thin; core owns policy and business logic.
- Avoid hard-coded provider names in core decision logic.
- Avoid giant generic abstractions and unnecessary microservices.
- Do not add a dependency without a reason and license/security review.
- Do not generate placeholder files to make a checklist look complete.
- Do not silently change public tool names or schemas.
- Keep changelog and migration notes current.
- Record Architecture Decision Records for significant decisions.
- Maintain a traceability map: requirement → implementation → tests → evidence.
- Preserve a clean git diff and do not overwrite user work.

Before edits, inspect `git status`. Never discard or reset user changes. Work on a dedicated branch if possible, named clearly (for example `feat/openclone-platform-integrations`). Do not push, merge, publish, or alter the remote repository without explicit authorization.

---

# 15. Final repository release candidate

The final deliverable must be the **existing OpenClone repository upgraded in place**, not a separate archive of proposals.

Before declaring completion:
1. Re-run every baseline check.
2. Run all new tests.
3. Validate schemas and documentation links.
4. Build all packages/apps.
5. Run adapter contract tests for ChatGPT, Claude, Codex, Gemini.
6. Run security and authorization tests.
7. Run UI/accessibility checks if UI exists.
8. Run deployment configuration checks and local production smoke tests.
9. Review the full git diff for unintended changes, secrets, generated junk, duplicate files, and incomplete TODOs.
10. Have an independent reviewer/verification pass inspect critical claims and test evidence.
11. Update canonical assessment and release docs with truthful status.
12. Create a release candidate tag only if local Git policy permits and user authorization is present. Otherwise provide the recommended tag and exact command without tagging.

## Required final report

Provide:
- Product/repository version and commit SHA.
- Summary of what changed.
- Existing capabilities preserved.
- New/updated capabilities.
- Four-platform integration matrix with exact maturity state.
- Recommendation and connector coverage.
- Model routing/fallback coverage.
- Token/cost optimization coverage and measured evidence.
- UI/UX and accessibility results.
- Security findings and residual risks.
- Test matrix with exact results.
- Build/package status.
- Deployment status (never overstate).
- Files added/modified/deprecated.
- Migration and configuration instructions.
- Known limitations and blocked items.
- Exact commands to reproduce validation.
- Next steps required from the owner.

Use the following final status labels:
- `COMPLETE`
- `PARTIALLY COMPLETE`
- `BLOCKED`
- `NOT IMPLEMENTED`
- `NOT VERIFIED`

Do not mark the overall release `COMPLETE` if any required release gate fails or any critical platform integration is only specified or mocked. A release candidate can be labeled `PARTIALLY COMPLETE` with a clear blocker list.

---

# 16. Definition of done

OpenClone is ready for owner review when:
- Existing repository has been audited rather than replaced.
- Existing domains, engines, governance, and working capabilities are preserved or intentionally migrated with traceability.
- Four platform adapters share one OpenClone core and one set of business rules.
- Platform-specific setup and limitations are documented and tested to the level available.
- Recommendation engine supplies evidence-backed primary and alternative options.
- Connector lifecycle uses least privilege, approval gates, and revocation.
- Model routing/fallback respects privacy and task capability.
- Token/cost controls are measurable and do not weaken safety or verification.
- UI/UX style intelligence evaluates relevant morphism and visual-style families and records a context-appropriate direction rather than applying one style everywhere.
- Buttons, controls, components, and interaction states have been audited and tested; no fake or dead actions remain in accepted critical flows.
- Multi-skill UI/UX orchestration discovers and uses only verified, compatible skills with bounded permissions and traceable handoffs.
- UI/UX is coherent, responsive, accessible, and free of fake functionality (if a UI exists or is approved).
- CI, tests, security controls, deployment artifacts, operations docs, and rollback guidance are present and validated.
- Final report accurately distinguishes implemented, tested, live-connected, deployed, and production-hardened capabilities.

**Start now with Stage 0 only. Inspect the actual working repository and report the verified baseline before broad implementation. Then proceed stage by stage, updating OpenClone in place. The final result must be a coherent repository release candidate—not just another prompt, plan, or documentation-only upgrade.**


---

# PART B — PREMIUM REPOSITORY STRUCTURE AND DOMAIN CONSOLIDATION (v1.3.0)

# OpenClone — Premium Repository Structure & Domain Consolidation Upgrade
## Antigravity in-place execution specification | v1.3.0

**Product:** OpenClone  
**Repository currently known:** `MK-1603/aisdf` (verify the actual remote and local workspace before acting)  
**Objective:** Restructure the existing OpenClone repository into a clean, premium, scalable architecture, with all 31 numbered domains (`00`–`30`) grouped under one canonical parent folder.

> This is a repository restructuring and quality upgrade—not a new project, not a second framework, and not a documentation-only exercise. Perform the work in the existing OpenClone repository and preserve its working capabilities.

---

# 1. What the user wants

The current repository has numbered domain folders such as `00-GOVERNANCE`, `01-METHODOLOGY`, through `30-AGENT-RULES-AND-VERIFICATION` at the repository root. The supplied project tree also shows separate top-level areas for adapters, assessment, blueprints, concepts, docs, engines, examples, memory, modes, prompts, registries, runtime, schemas, security, security-operations, skills, source, standards, templates, tests, tools, workflows, and workforce. fileciteturn153file0L4-L18 fileciteturn153file0L97-L138 fileciteturn153file0L353-L410 fileciteturn153file0L895-L924

The requested structural change is:

- Put **all 31 numbered domains (`00`–`30`) inside one parent folder**, recommended name: `domains/`.
- Keep their numbering, identity, scope, and internal content intact unless a verified audit justifies a correction.
- Reorganize the rest of the repository into a small number of clearly owned top-level areas.
- Make the structure understandable to developers, AI coding agents, contributors, and future maintainers.
- Upgrade root documentation, navigation, naming, consistency, and developer experience to a premium open-source project standard.
- Do not delete useful material merely to make the tree look smaller.

The `domains/` parent is the canonical home of the 31 domains. Do not leave duplicate numbered-domain folders at the root after migration.

---

# 2. Non-negotiable safety and change-control rules

1. Inspect the real local repository, current branch, current commit, and `git status` before editing.
2. Read `AGENTS.md`, root README, project/mission documents, governance rules, manifests, version file, architecture maps, and nested instructions.
3. Preserve uncommitted user work. Never run destructive reset/clean commands.
4. Create a dedicated local branch for the restructuring if Git is available and the working tree permits it. Do not push or merge without explicit authorization.
5. Do not delete, truncate, rewrite from memory, or replace existing specifications with generic placeholders.
6. Move files with Git-aware operations where possible so history can be followed.
7. Preserve stable IDs, engine IDs, schema identifiers, public CLI commands, workflow IDs, and compatibility contracts unless a migration is explicitly designed and tested.
8. Every move must have a traceable old-path → new-path mapping.
9. Update every affected link, import, test fixture, script, manifest, CI workflow, package configuration, adapter instruction, and example.
10. Do not leave two competing canonical copies of a document.
11. Do not create a new `UPGRADE/`, `V2/`, `NEW-OPENCLONE/`, or parallel repository.
12. If an operation is destructive, externally consequential, paid, or requires production credentials, stop and ask for approval.
13. Keep a rollback path until all validation passes.
14. Do not claim tests, integrations, or deployments passed unless executed and evidenced.

---

# 3. Target premium repository structure

Use this as the target organizational model. Adapt names only when the existing project conventions or executable dependencies require it. Keep the structure shallow, predictable, and easy to navigate.

```text
OpenClone/
│
├── domains/                         # THE single home for all numbered domains
│   ├── 00-governance/
│   ├── 01-methodology/
│   ├── 02-project-intelligence/
│   ├── 03-requirements-engineering/
│   ├── 04-product-engineering/
│   ├── 05-ux-ui-engineering/
│   ├── 06-technology-intelligence/
│   ├── 07-engineering-knowledge/
│   ├── 08-software-architecture/
│   ├── 09-platform-engineering/
│   ├── 10-ai-and-model-engineering/
│   ├── 11-agent-engineering/
│   ├── 12-orchestration-and-context/
│   ├── 13-harness-and-execution/
│   ├── 14-security-and-privacy/
│   ├── 15-data-and-database-engineering/
│   ├── 16-api-and-integration-engineering/
│   ├── 17-testing-and-verification/
│   ├── 18-devops-and-cloud-engineering/
│   ├── 19-deployment-and-operations/
│   ├── 20-reliability-and-observability/
│   ├── 21-distributed-systems-and-scalability/
│   ├── 22-cost-and-resource-governance/
│   ├── 23-legal-and-compliance/
│   ├── 24-product-analytics-and-support/
│   ├── 25-framework-maintenance/
│   ├── 26-distribution-and-extensions/
│   ├── 27-standards-and-compatibility/
│   ├── 28-templates-and-examples/
│   ├── 29-benchmarks-and-evaluation/
│   ├── 30-agent-rules-and-verification/
│   └── README.md
│
├── core/                            # Shared OpenClone runtime and contracts
│   ├── src/                         # Move existing src/ here only after import audit
│   ├── runtime/                     # Move existing runtime/ here only after import audit
│   ├── schemas/                     # Canonical machine-readable contracts
│   └── README.md
│
├── integrations/                    # External AI platforms and provider adapters
│   ├── mcp/
│   ├── platforms/
│   │   ├── chatgpt/
│   │   ├── claude/
│   │   ├── codex/
│   │   └── gemini/
│   ├── providers/
│   ├── connectors/
│   ├── registries/
│   └── README.md
│
├── workforce/                       # Existing specialist/agent workforce
│   ├── contracts/
│   ├── registry/
│   ├── teams/
│   └── README.md
│
├── engineering/                     # Execution workflows and engineering assets
│   ├── engines/
│   ├── workflows/
│   ├── modes/
│   ├── prompts/
│   ├── skills/
│   ├── tools/
│   ├── standards/
│   └── README.md
│
├── knowledge/                       # Reference and durable knowledge
│   ├── concepts/
│   ├── blueprints/
│   ├── memory/
│   ├── reference/
│   └── README.md
│
├── quality/                         # Tests, assessments, benchmarks, assurance
│   ├── tests/
│   ├── assessment/
│   ├── benchmarks/
│   ├── security/
│   └── README.md
│
├── delivery/                        # Build, release, deployment and operations
│   ├── ci/
│   ├── deployment/
│   ├── operations/
│   ├── release/
│   └── README.md
│
├── docs/                            # User-facing docs and project guides
│   ├── getting-started/
│   ├── architecture/
│   ├── guides/
│   ├── examples/
│   ├── migration/
│   ├── release-history/
│   └── README.md
│
├── templates/                       # Reusable project and report templates
├── examples/                        # Runnable end-to-end examples
├── adapters/                        # Keep only if these are distinct IDE/agent packaging adapters
├── .github/                          # CI, issue templates, PR templates, workflows
│
├── AGENTS.md
├── README.md
├── QUICK-START.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── SUPPORT.md
├── LICENSE
├── VERSION
├── CHANGELOG.md
├── pyproject.toml
├── requirements-dev.txt
└── manifests/                        # Canonical product/package manifests if supported
```

## Important architecture note

This is a target organization, not permission to move every folder mechanically. Some existing folders may already be referenced by Python imports, CLI entry points, skill installers, agent clients, GitHub workflows, documentation URLs, or external users. Inspect dependencies first.

If a proposed move would create more risk than value, keep the folder where it is for this release and record the reason. The mandatory requirement is that all numbered domains live under one `domains/` parent. Other top-level grouping can be staged safely.

Avoid needless nesting. Do not move root project configuration files into arbitrary folders. Keep conventional root entry points (`README.md`, `pyproject.toml`, `AGENTS.md`, `LICENSE`, `VERSION`, etc.) at the root unless a tool requires otherwise.

---

# 4. Domain consolidation requirements

## 4.1 All 31 domains

Move the existing numbered directories `00` through `30` into `domains/`. Preserve the numeric prefixes and domain names. Normalize case and hyphenation only if every reference is updated and the change is documented.

The domain list must be checked against the actual repository, not just this proposed tree. Verify:
- No number is missing.
- No duplicate domain number exists.
- No two domains claim the same ownership without an explicit boundary.
- Every domain has a useful README with purpose, scope, non-goals, owner, dependencies, key documents, and links.
- README headings match the actual domain name.
- Domain map, functional map, manifests, indexes, and engine references resolve.
- Cross-domain dependencies are explicit rather than circular or hidden.

## 4.2 Domain landing page

Create `domains/README.md` as the canonical domain index:
- Purpose of the domain system.
- All 31 domains in numeric order.
- One-sentence scope for each.
- Primary inputs/outputs and ownership.
- Links to each domain README.
- Cross-domain dependency overview.
- Guidance on where new capabilities belong.
- Rule that new domains require an ADR and governance approval.

## 4.3 No duplicate domain homes

After migration:
- No `00-*` through `30-*` numbered domain directories should remain at repository root.
- Do not copy the domains and leave the originals as stale duplicates.
- If compatibility shims are required for one release, make them explicit, minimal, tested, and scheduled for removal. Prefer redirects/links or import compatibility modules over duplicated documents.

---

# 5. Reorganize the remaining repository areas

Map every existing top-level folder to one canonical destination. The following mapping is a starting proposal, not a blind command:

| Current area | Preferred destination | Notes |
|---|---|---|
| `engines/` | `engineering/engines/` | Preserve E-001…E-056 IDs and registry |
| `workflows/` | `engineering/workflows/` | Update workflow references |
| `modes/` | `engineering/modes/` | Keep stable mode identifiers |
| `prompts/` | `engineering/prompts/` | Preserve role prompts and entry prompts |
| `skills/` | `engineering/skills/` | Preserve skill metadata, license, assets, tests |
| `tools/` | `engineering/tools/` | Update executable paths and docs |
| `standards/` | `engineering/standards/` or relevant domain | Avoid duplicated standards |
| `concepts/` | `knowledge/concepts/` | Preserve primary/alternate distinction |
| `blueprints/` | `knowledge/blueprints/` | Mark historical vs canonical clearly |
| `memory/` | `knowledge/memory/` | Preserve vault template and governance |
| `reference/` | `knowledge/reference/` | Keep source provenance |
| `ASSESSMENT/` | `quality/assessment/` | Preserve historical assessment reports |
| `tests/` | `quality/tests/` | Update test discovery/configuration |
| `security/` | `quality/security/` or security domain | Keep machine policy paths consistent |
| `security-operations/` | `quality/security/operations/` or domain 14 | Choose one canonical owner |
| `runtime/` | `core/runtime/` | Check Python imports and entry points |
| `src/` | `core/src/` only if packaging supports it | Do not break package discovery |
| `schemas/` | `core/schemas/` | Keep schema IDs and references stable |
| `registries/` | Split by ownership into `integrations/registries/`, `engineering/`, or `core/` | Avoid a generic registry dump |
| `adapters/` | `integrations/platforms/` only for actual AI platform adapters; keep IDE-specific adapters distinct if needed | Do not conflate IDE and AI chat platform adapters |
| `EGM-WORKFLOWS/` | `engineering/workflows/egm/` or domain 17/30 ownership | Preserve schemas and templates |
| `docs/` | `docs/` | Reorganize internal docs, preserve demo assets and release history |
| `REFERENCE-PROJECTS/` | `examples/reference-projects/` | Preserve runnable project examples |
| `templates/` | `templates/` | Keep reusable templates easy to find |
| `examples/` | `examples/` | Keep runnable examples and fixtures distinct |
| `workforce/` | `workforce/` | Existing clear top-level bounded context |
| `adapters/` | `integrations/` or retain for IDE adapters | Decide after inventory |
| root manifests | `manifests/` only if tooling supports it | Keep compatibility entry points if required |

Where a folder has multiple responsibilities, split by ownership only after dependency mapping. Do not move an entire folder into one destination if its contents belong to different domains.

---

# 6. Premium repository quality standard

“Premium” means professional, coherent, navigable, consistent, maintainable, and easy to contribute to—not merely more folders or decorative README badges.

## 6.1 Naming and consistency

- Use one consistent directory naming convention.
- Use stable, predictable file names.
- Fix spelling errors, mismatched README headings, inconsistent capitalization, and broken relative links.
- Avoid vague names such as `misc`, `stuff`, `new`, `old2`, `final-final`.
- Separate canonical/current documents from historical/archived records.
- Add owner and status metadata only where it improves traceability.
- Keep stable IDs such as `E-001` through `E-056`; do not renumber for aesthetics.

## 6.2 Root README and navigation

Upgrade the root README into a premium project landing page with:
1. OpenClone identity and concise value proposition.
2. What OpenClone does and does not do.
3. Key capabilities.
4. Architecture overview.
5. Four AI platform integrations: ChatGPT, Claude, Codex, Gemini (label actual maturity honestly).
6. Quick start.
7. Repository map.
8. Documentation navigation.
9. Security and privacy summary.
10. Testing and verification commands.
11. Contribution guide.
12. License and project status.

Use accurate badges only. Do not add fake stars, downloads, coverage, build status, certification, or compatibility badges.

## 6.3 Contributor experience

Provide:
- A clear quick-start for a new contributor.
- Supported language/runtime/tool versions.
- Reproducible install and test commands.
- Code style and formatting rules.
- How to add a domain document, engine, skill, adapter, connector, schema, or test.
- Pull request checklist.
- Release process and version policy.
- Troubleshooting guide.
- Architecture decision record template.
- Changelog convention.

## 6.4 Documentation design

- Consistent headings, tables, callouts, diagrams, and metadata.
- Short landing pages with links to detailed specs.
- No duplicated full specifications across multiple files.
- A clear status label: `DRAFT`, `PROPOSED`, `APPROVED`, `IMPLEMENTED`, `VERIFIED`, `DEPRECATED`.
- Every cross-reference must resolve.
- Diagrams must match actual implementation and be labeled conceptual when not implemented.
- Use Mermaid where it improves understanding; do not add diagrams for decoration.

---

# 7. Integrations and platform adapters

During the restructuring, preserve and prepare a clean integration architecture for:
- ChatGPT
- Claude
- OpenAI Codex
- Google Gemini

These must use one shared OpenClone core and stable tool contracts. Do not duplicate core logic in each platform adapter. Keep MCP/tool gateway contracts, authentication, authorization, connector registry, and platform-specific setup clearly separated.

Do not mark a platform integration as complete merely because a folder or config file exists. Record the maturity state and evidence:
`SPECIFIED`, `IMPLEMENTED`, `UNIT_TESTED`, `CONTRACT_TESTED`, `LIVE_CONNECTED`, `END_TO_END_VERIFIED`.

Do not move existing Antigravity, Cursor, Claude Code, or Codex IDE instructions into the wrong category. Distinguish:
- AI chat platform integration,
- coding-agent/IDE adapter,
- MCP server,
- provider API adapter,
- local CLI integration.

---

# 8. Migration engineering — do not break the repository

Before moving files:
1. Generate a complete file inventory and path reference map.
2. Search for references to every old path in Markdown, Python, JSON, YAML, TOML, shell, JavaScript, TypeScript, CI, package files, and test fixtures.
3. Inspect dynamic path construction and runtime path assumptions.
4. Identify public URLs or external consumers that may depend on paths.
5. Design a move manifest with old path, new path, reason, references to update, and verification test.
6. Check packaging and import discovery before moving `src/`, `runtime/`, `schemas/`, or `tools/`.
7. Check skill installation scripts and relative asset paths before moving `skills/`.
8. Check adapter discovery and instruction paths before moving `adapters/`.
9. Check CI and GitHub workflows before moving tests or configuration.
10. Plan a reversible migration.

Implement in small batches:
- Batch A: numbered domains → `domains/`.
- Batch B: documentation and knowledge organization.
- Batch C: engineering engines/workflows/prompts/skills/tools.
- Batch D: core source/runtime/schemas only if packaging and tests support it.
- Batch E: quality/security/assessment.
- Batch F: integration adapters and registries.
- Batch G: docs, links, root navigation, manifests and release metadata.

After each batch, run the relevant validation. Do not proceed to the next batch if the previous batch breaks tests or critical references.

Create a machine-readable path migration map (JSON or YAML) and a human-readable migration report. Do not retain the map as an alternative source of truth; it is a migration record.

---

# 9. Required automated validation

Add or upgrade repository validation so it checks:

### Structure
- Exactly one canonical `domains/` directory.
- All 31 numbered domains exist under `domains/`.
- No numbered domain directories remain at root.
- No duplicate domain IDs.
- Every domain has a README.
- Every domain index entry resolves.
- No accidental empty or abandoned directories.
- No stale duplicate documents.

### References and configuration
- Markdown relative links.
- Internal file references.
- Python imports and package discovery.
- CLI entry points.
- JSON/YAML/TOML validity.
- Schema references and fixtures.
- Skill asset references and install scripts.
- Adapter discovery paths.
- CI workflow paths.
- Manifest file paths.
- Documentation examples and commands.

### Quality and security
- Formatting and lint.
- Type checks where relevant.
- Unit and integration tests.
- Secret scanning.
- Dependency/security checks where tools are available.
- License/attribution inventory for third-party skills and assets.
- No generated bytecode/cache files committed unless intentionally required.

### Build and release
- Reproducible local install.
- Build/package checks.
- CLI smoke test.
- Example workflow smoke test.
- Release manifest/version consistency.
- Clean final diff.

For every command, record exact invocation, environment, exit code, and result. Distinguish `PASS`, `FAIL`, `SKIPPED`, and `BLOCKED`. Do not convert skipped tests into passes.

---

# 10. Required deliverables inside the existing repository

Update existing canonical locations. Do not create a detached upgrade folder.

1. `domains/README.md` — complete 31-domain index.
2. Updated root `README.md`.
3. Updated `AGENTS.md` with the new canonical paths and repository navigation rules.
4. Updated `DOMAIN-MAP.md`, `AISDF-FUNCTIONAL-MAP.md`, lifecycle overview, mission/scope docs, and relevant governance docs.
5. Updated engine, adapter, skill, workflow, and technology registries.
6. Machine-readable path migration map.
7. Human-readable structure migration report.
8. Updated contributor and quick-start documentation.
9. Updated CI/test/validation configuration.
10. Updated manifests and package metadata.
11. Updated changelog and migration notes.
12. Final repository assessment and release readiness report.

If a named document does not exist in the actual repository, do not invent a historical claim; create it only if it is genuinely needed and approved by the existing governance.

---

# 11. Versioning and release

- Inspect the existing `VERSION`, manifests, changelog, tags, and release policy first.
- Propose a semantic version bump based on actual compatibility impact.
- A folder-only move may be breaking if users, tools, scripts, or external links consume old paths.
- Preserve compatibility shims for a documented transition period when needed.
- Update migration instructions and deprecation schedule.
- Do not tag, push, publish, deploy, or merge without explicit authorization.
- Produce a local release candidate and clear owner instructions.

---

# 12. Final completion report

The final report must state:

1. Starting commit SHA and branch.
2. Final commit SHA (if locally committed) and branch.
3. Whether the working tree is clean.
4. Final version proposal.
5. Final top-level directory tree.
6. Confirmation that all 31 domains are under `domains/`.
7. Count and identity of the 31 domains.
8. Complete old-path → new-path migration summary.
9. Files moved, modified, added, deprecated, or retained with reasons.
10. Link/import/configuration repair results.
11. Test commands and exact results.
12. Packaging/build/CLI smoke-test results.
13. Security and license review results.
14. Compatibility risks and migration steps.
15. Blocked or unverified items.
16. Exact commands for the owner to reproduce checks.

Use honest statuses: `COMPLETE`, `PARTIALLY COMPLETE`, `BLOCKED`, `NOT IMPLEMENTED`, `NOT VERIFIED`.

**Do not call the work complete if any domain is missing, references are broken, core tests fail, or the migration has not been independently reviewed.**

---

# 13. Start instruction

Start by auditing the current repository and producing the proposed final tree plus path-migration manifest. Confirm the exact 31 domain directories and map every current top-level folder. Then implement the migration in small reversible batches, validate each batch, and finish with a tested local release candidate.

**The required outcome is a premium, clean, maintainable OpenClone repository where all 31 numbered domains live under one `domains/` folder, the rest of the structure has clear ownership, and the existing framework still works.**


---


# 17. Application Build-to-Deployment Automation — Core Product Requirement

## 17.1 Correct product intent

OpenClone is an AI-assisted software-building framework. A user should be able to describe an application, let OpenClone plan and build it using approved coding agents and tools, and then have that **application** tested, packaged, deployed, verified, monitored, and—when configured—redeployed after later changes.

This requirement is primarily about deploying applications created or managed through OpenClone. It is not limited to deploying the OpenClone framework itself.

Two distinct deployment targets must exist and must never be confused:

1. **OpenClone self-deployment:** release the OpenClone framework/runtime.
2. **User project deployment:** deploy an application that OpenClone has helped build or maintain. This is the primary requirement in this section.

The user project must remain owned by the user. OpenClone orchestrates deployment through explicitly connected providers and repositories; it does not silently create paid accounts, purchase services, register domains, provision billable infrastructure, or publish private source code.

## 17.2 User experience: Build → Test → Preview → Approve → Production

The desired experience is:

```text
User describes application
          |
          v
OpenClone project analysis
          |
          v
Plan + architecture + stack selection
          |
          v
AI coding agent builds the application
          |
          v
Local/isolated build and automated tests
          |
          v
Deployment readiness and security checks
          |
          v
Provider recommendation (with alternatives)
          |
          v
User connects repository + hosting provider
          |
          v
Preview deployment
          |
          v
Smoke tests + health checks + preview review
          |
          v
Production approval (policy controlled)
          |
          v
Production deployment
          |
          v
Post-deploy verification + release record
          |
          v
Monitoring, diagnostics, rollback, future redeploys
```

The user should not need to manually copy source files, invent deployment configuration, or learn each provider's entire workflow for every project. OpenClone should generate and validate the required configuration, guide the minimum one-time provider connection, and automate repeat deployments.

Do not promise “one-click deployment” until the provider connection, repository permissions, environment variables, build, deployment and verification path has been proven end-to-end.

## 17.3 Deployment lifecycle and project state machine

Implement a durable, auditable deployment lifecycle. Reuse existing workflow/runtime/state machinery if it already provides these guarantees; do not create a second orchestration runtime.

Suggested states:

- `NOT_ANALYZED`
- `ANALYZED`
- `DEPLOYMENT_PLAN_READY`
- `AWAITING_PROVIDER_CONNECTION`
- `AWAITING_CONFIGURATION`
- `READY_FOR_PREVIEW`
- `PREVIEW_QUEUED`
- `PREVIEW_DEPLOYING`
- `PREVIEW_DEPLOYED`
- `PREVIEW_VERIFICATION`
- `AWAITING_PRODUCTION_APPROVAL`
- `PRODUCTION_QUEUED`
- `PRODUCTION_DEPLOYING`
- `PRODUCTION_DEPLOYED`
- `POST_DEPLOY_VERIFICATION`
- `HEALTHY`
- `DEGRADED`
- `FAILED`
- `ROLLBACK_QUEUED`
- `ROLLED_BACK`
- `CANCELLED`

Every transition must have an actor, timestamp, triggering event, previous state, new state, correlation ID, project ID, environment, commit SHA, provider deployment ID (when available), and evidence. Enforce legal transitions server-side. Retries must be idempotent and must not create duplicate production releases.

## 17.4 Deployment intelligence agent

Create a bounded deployment-planning and troubleshooting agent that uses the shared OpenClone model router and tool gateway. It must not be a privileged shell agent with unrestricted production access.

Responsibilities:

1. Inspect the project manifest, source tree, lockfiles, build scripts, runtime versions, framework configuration, Dockerfiles, monorepo layout, and existing CI/CD.
2. Detect application type and deployable units: frontend, API, worker, scheduled job, static site, container service, mobile backend, or multi-service application.
3. Detect required runtime/build commands and output artifacts from actual repository evidence.
4. Detect required environment-variable *names* and configuration dependencies without reading or exposing secret values.
5. Identify persistent storage, database migrations, queues, cache, search, object storage, domains, webhooks, and external services.
6. Produce a deployment readiness report and provider-neutral deployment plan.
7. Compare suitable hosting providers using current verified capabilities, region availability, runtime limits, pricing evidence, portability, lock-in, operational burden, and project requirements.
8. Generate provider configuration and CI workflows only after reviewing existing files and preserving user customizations.
9. Run preflight checks and request approval for consequential actions.
10. Read deployment/build logs, classify failures, suggest a minimal repair, and create a patch or branch for review.
11. Re-run affected checks after a repair; enforce bounded repair attempts and time/cost budgets.
12. Verify deployment health and summarize exact evidence and remaining risks.

The agent may recommend and prepare. Execution must occur through narrowly scoped deployment tools and policy gates. It must not bypass failed tests, disable security checks, change production secrets, or weaken access controls to force a successful release.

## 17.5 Provider-neutral deployment engine and adapters

Implement one shared deployment contract and provider-specific adapters. Do not place provider-specific business logic in the AI planner or duplicate deployment workflows across providers.

Shared operations should include, where supported:

- `inspect_project`
- `validate_configuration`
- `connect_provider`
- `list_projects`
- `create_preview`
- `get_deployment_status`
- `get_deployment_logs`
- `promote_to_production`
- `cancel_deployment`
- `check_health`
- `list_domains`
- `rollback`
- `disconnect_provider`

Each adapter must publish a capability manifest indicating supported operations, authentication method, required scopes, regions, runtime/build constraints, preview support, production promotion semantics, rollback semantics, webhook support, pricing/billing caveats, rate limits, and known limitations. Do not expose unsupported operations as if they work.

Evaluate providers based on actual project requirements. Initial candidates to assess—not mandatory defaults—include:

- Vercel for supported frontend and serverless/web workloads.
- Cloudflare Workers/Pages for supported edge, static and worker workloads.
- Render for supported web services, workers, static sites and managed infrastructure.
- Railway for supported application/container and service workloads.
- Fly.io for supported containerized/global application workloads.
- AWS, Google Cloud or Azure when requirements justify their broader infrastructure and operational complexity.
- Self-hosted Docker/Compose or Kubernetes only when the user's scale, control, compliance or portability needs justify the operational burden.

Do not assume any provider is universally best. Verify current product support, limits, pricing, regions, and API behavior from official provider documentation before implementing or recommending. Keep provider adapters replaceable.

## 17.6 CI/CD execution model

Use the repository's existing Git provider and CI system when possible. For GitHub repositories, evaluate GitHub Actions as the default CI/CD execution substrate, with provider adapters performing the actual deployment. Do not introduce another pipeline engine without a documented reason.

Expected pipeline stages:

1. Checkout an exact commit SHA.
2. Install dependencies using the committed lockfile and a pinned runtime/toolchain.
3. Run formatting/lint, type checks, unit tests, schema checks and required integration tests.
4. Run secret scanning, dependency/security checks, license policy checks and artifact scanning appropriate to the project.
5. Build reproducibly and record artifact metadata/checksum.
6. Create an isolated preview deployment for pull requests or explicit preview requests.
7. Run smoke tests, route checks and health checks against the preview.
8. Require the configured approval before production promotion.
9. Deploy the exact tested artifact/commit to production; do not silently rebuild from a different revision.
10. Run post-deployment verification and publish a deployment report.
11. Trigger configured rollback or halt/alert behavior when critical health gates fail.

Use concurrency groups to prevent conflicting production releases. Protect production environments and secrets. Pin third-party actions to immutable commit SHAs where practical and maintain a controlled update process. Use least-privilege workflow permissions, short-lived OIDC federation where supported, and environment-scoped credentials. Never store provider secrets in repository source files.

## 17.7 Automatic deployment policies

Provide explicit per-project deployment modes:

- `MANUAL`: OpenClone prepares the plan; user executes deployment.
- `PREVIEW_AUTO`: approved changes can create preview deployments automatically.
- `PRODUCTION_APPROVAL`: preview and checks run automatically; production requires human approval. This should be the default.
- `PRODUCTION_AUTO`: production deploys automatically only after the owner explicitly enables it and configures branch, test, security, health, budget, and rollback policies.

A project may set separate policies for development, staging and production. Do not infer production permission from a user's request to build an application.

For `PRODUCTION_AUTO`, require:
- Explicit opt-in by a project owner/admin.
- Protected production branch or equivalent immutable release trigger.
- Required CI checks and security gates.
- Verified provider connection and scoped credentials.
- Environment-specific secret configuration.
- Successful preview or staging validation where applicable.
- Health-check definition and failure thresholds.
- Rollback or safe halt strategy.
- Spend/usage limits and alerts.
- Audit log and notification destination.
- A tested disable/revoke mechanism.

Any change to deployment target, domain, production secrets, database destruction/migration strategy, public exposure, billing, or permissions must trigger an approval gate unless a narrowly scoped policy explicitly authorizes it.

## 17.8 Environment variables, secrets and configuration

Build a secure environment configuration workflow:

- Detect variable names from source and deployment manifests.
- Classify each variable as public build-time config, server-only secret, provider token, database credential, signing key, or optional setting.
- Explain the purpose and expected format without asking users to paste secrets into an AI chat.
- Collect secrets through provider-native secret managers or an approved encrypted secret vault.
- Never write secret values to generated `.env` examples, logs, prompts, telemetry, test reports, Git history, or deployment artifacts.
- Generate `.env.example` with names and safe descriptions only.
- Validate required variables by presence and format without printing values.
- Separate local, preview, staging and production configuration.
- Support rotation, revocation and access audit.
- Prevent client-side exposure of server-only variables.

If the project uses databases, detect migrations and require backup/approval policy before production schema changes. Never automatically drop data or run destructive migrations as a deployment repair.

## 17.9 Build failure diagnosis and AI repair loop

When a build or deployment fails:

1. Capture bounded logs and structured provider error details.
2. Redact secrets, tokens, personal data and sensitive environment values before sending context to a model.
3. Classify the failure: dependency, runtime, build, configuration, permissions, provider outage, quota/billing, network, database migration, health check, or application defect.
4. Identify the smallest relevant files and log excerpts; do not send the entire repository by default.
5. Ask the model to propose a minimal, testable patch with evidence and confidence.
6. Apply changes only in an isolated worktree/branch or patch review flow.
7. Run targeted tests, then the full required pipeline.
8. Require human review for production-sensitive changes.
9. Limit automatic repair attempts, model spend, runtime and deployment retries.
10. Stop and report when confidence is low, errors repeat, or the issue needs credentials/owner decisions.

The agent must never “fix” a deployment by disabling tests, weakening CSP/authentication, exposing secrets, granting broad permissions, removing validation, or silently changing data architecture.

## 17.10 Health verification, observability and rollback

Every deployable service should define an appropriate health contract. Depending on application type, verify:

- Deployment status from provider API.
- HTTP status and response for configured health endpoints.
- Critical public routes and static assets.
- Authentication-safe synthetic checks.
- API readiness and dependency connectivity.
- Database migration status without exposing data.
- Error rates, latency and resource limits when observability is connected.
- Correct commit/version identity in the running application.

Do not assume a single HTTP 200 proves an application is healthy.

Rollback must be provider-capability-aware. Prefer promoting the last known healthy immutable release/artifact. For database schema changes, use backward-compatible expand/contract migrations; application rollback alone may not reverse a schema change safely. If automatic rollback is unsupported or unsafe, halt traffic promotion and alert the owner rather than claiming rollback succeeded.

Record deployment history, commit, artifact, provider, environment, actor, approvals, checks, logs references, health outcome, rollback relationship, and cost evidence.

## 17.11 Deployment dashboard and project UX

Integrate deployment into the existing project workspace. Do not create a detached deployment product.

Required views/components:

- Project deployment readiness summary.
- Detected application services and architecture.
- Recommended provider with alternatives and rationale.
- Provider connection state and granted scopes.
- Environment configuration checklist (never display secret values).
- Build and CI status timeline.
- Preview deployment URL and verification status.
- Production approval control with exact commit and change summary.
- Current production URL, release and health status.
- Deployment logs with redaction.
- Deployment history and comparison.
- Rollback action with impact preview and confirmation.
- Usage/cost indicators when provider data is available.
- Clear states for unsupported, disconnected, blocked, failed and unverified features.

All controls must have loading, success, error, disabled, focus, keyboard and accessible states. Never render a fake “Deploy” button if no functioning provider adapter or credential connection exists.

## 17.12 Deployment security threat model

Threats to address include:

- Prompt injection in repository files, README instructions, issue text, build logs or dependency output.
- Malicious pull requests attempting to exfiltrate secrets.
- Compromised third-party GitHub Actions or dependencies.
- Overprivileged provider tokens.
- Secret leakage through model context, logs, artifacts or client bundles.
- Unauthorized production promotion.
- Build artifact substitution between test and production.
- Dependency confusion and malicious packages.
- Supply-chain compromise.
- Untrusted code execution during build/test.
- Cross-project credential or artifact access.
- Deployment replay, duplicate webhook events and race conditions.
- Resource exhaustion, runaway AI repair loops and unexpected provider spend.

Controls:
- Treat repository content and logs as untrusted input, not authority.
- Separate planning/model tools from privileged deployment execution.
- Use isolated build runners/sandboxes and restricted network access where feasible.
- Use short-lived, environment-scoped credentials and OIDC federation where supported.
- Pin dependencies/actions and generate SBOM/provenance where appropriate.
- Verify webhook signatures and make event processing idempotent.
- Enforce project/tenant isolation and authorization server-side.
- Redact sensitive logs before model use.
- Require approval for privileged production operations.
- Maintain auditable access, deployment and secret-rotation records.
- Add rate limits, retry ceilings and budget guards.

## 17.13 Deployment data contracts and APIs

Reuse existing schemas and naming conventions. Define or extend versioned contracts for:

- `ProjectDeploymentProfile`
- `DeploymentProviderManifest`
- `DeploymentPlan`
- `DeploymentEnvironment`
- `DeploymentJob`
- `DeploymentEvent`
- `DeploymentApproval`
- `DeploymentArtifact`
- `DeploymentVerification`
- `DeploymentHealthReport`
- `DeploymentRollback`
- `DeploymentCostSnapshot`

Each schema must define identity, version, required fields, validation, ownership/tenant boundary, timestamps, idempotency key, secret-redaction rules, and compatibility behavior. Store references to secret manager entries, never raw secret values.

Expose authenticated APIs/CLI operations only if consistent with the existing OpenClone runtime. Enforce authorization on the server; never rely on frontend-only checks.

## 17.14 Deployment tests and proof requirements

Required tests:

- Provider adapter contract tests with mocks.
- Authentication and permission-scope tests.
- Secret redaction tests across prompts, logs, artifacts and errors.
- State-machine transition and idempotency tests.
- Webhook signature and replay tests.
- Preview deployment integration test.
- Production approval gate test.
- Production deployment test in an isolated test project/account.
- Health-check success/failure tests.
- Rollback test where provider semantics support it.
- Concurrent deployment and cancellation tests.
- AI repair-loop attempt/cost ceiling tests.
- Cross-project isolation tests.
- End-to-end test from a sample application commit to preview and approved production release.

A mocked adapter is not a live integration. Mark each provider accurately as `SPECIFIED`, `IMPLEMENTED`, `CONTRACT_TESTED`, `SANDBOX_INTEGRATION_TESTED`, or `LIVE_E2E_VERIFIED`. Do not claim real deployments unless a real authorized test deployment was executed and verified.

## 17.15 Recommended implementation sequence

Phase A — Discover and design:
- Audit existing deployment domain, engines, runtime, workflows, adapters, schemas and CI.
- Map current capability and reuse it.
- Define project deployment profile and provider capability manifest.
- Produce threat model and approval policy.

Phase B — Minimum viable automated deployment:
- GitHub repository integration and CI workflow generation.
- One initial provider adapter selected from actual project requirements.
- Preview deployment and health verification.
- Production approval gate.
- Deployment history and actionable failure report.

Phase C — AI-assisted operations:
- Log summarization and failure classification.
- Bounded repair proposals in isolated branches.
- Cost and quota reporting.
- Notifications and deployment dashboard.

Phase D — Provider expansion:
- Add further adapters only after the shared contract and first adapter are proven.
- Add provider conformance tests and documented feature parity.
- Add policy-controlled production auto-deploy.

Do not build all providers simultaneously. Prove one complete vertical slice first, then expand.

## 17.16 Deployment definition of done

The application deployment requirement is complete only when a sample user application can be built by the normal OpenClone workflow, tested, connected to an authorized repository/provider, deployed to preview, independently health-verified, approved and promoted to production, and later redeployed from a subsequent approved commit—with auditable evidence and a tested failure/rollback path.

If credentials, provider accounts, domains, paid resources or owner approval are unavailable, implement and test the safe portions and mark live deployment `BLOCKED` or `NOT VERIFIED`. Never fabricate a deployed URL or claim production readiness from generated configuration alone.

---

# 18. Unified final execution order and precedence

This master specification consolidates the platform, repository, and deployment requirements. Execute in this order:

1. Audit repository, Git state, governance, current architecture and baseline tests.
2. Produce capability maturity and gap reports; map all existing assets.
3. Propose one coherent target architecture and migration plan.
4. Reorganize all 31 numbered domains under the single `domains/` parent, preserving identity and references.
5. Reconcile the shared core, four AI platform adapters, MCP/tool gateway and connector lifecycle.
6. Upgrade model/provider intelligence, recommendations, alternatives and token/cost governance.
7. Integrate UI/UX design intelligence, Taste Skill and compatible specialist skills.
8. Implement deployment profile, deployment provider contract, CI/CD and one verified provider vertical slice.
9. Add security, tests, observability, operations, rollback and documentation.
10. Run independent review, full validation and release-readiness assessment.

When requirements overlap, apply this precedence:
- Existing governance and safety policies remain authoritative unless the owner approves a change.
- Existing working implementations and public contracts are preserved unless a tested migration is necessary.
- The repository structure specification governs domain consolidation.
- The shared-core specification governs AI platform and connector integration.
- Section 17 governs user-application build-to-deployment automation.
- Provider documentation governs actual provider capabilities and limitations.
- No section authorizes paid provisioning, public release, production changes, remote pushes or account permission changes without explicit owner approval.

If a conflict cannot be resolved from repository evidence and these rules, record it and request owner input. Do not silently choose a destructive interpretation.


## Final instruction to Antigravity

Start with the repository audit and baseline verification. Then present the final architecture and migration plan. Proceed in small reversible batches, using the execution order in Section 18. Do not stop at writing documentation: implement the approved changes in the existing repository, run the relevant checks, and produce a truthful final report. If an action requires credentials, billing, public exposure, production access or owner approval, pause at that gate and state exactly what is needed.

**The required outcome is one coherent, premium OpenClone system that can build applications and, through authorized provider connections, automatically test, preview, deploy, verify, monitor and safely redeploy those applications.**
