# OpenClone — Unified Platform Integrations & Full-Stack Repository Upgrade
## Antigravity execution brief | Version 1.2.0 | In-place upgrade | Final-release objective

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
| 7 | UI/UX and developer experience | UX audit, responsive/accessibility evidence |
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
- Responsive browser tests.
- Accessibility checks.
- Visual regression for critical flows.
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
- UI/UX is coherent, responsive, accessible, and free of fake functionality (if a UI exists or is approved).
- CI, tests, security controls, deployment artifacts, operations docs, and rollback guidance are present and validated.
- Final report accurately distinguishes implemented, tested, live-connected, deployed, and production-hardened capabilities.

**Start now with Stage 0 only. Inspect the actual working repository and report the verified baseline before broad implementation. Then proceed stage by stage, updating OpenClone in place. The final result must be a coherent repository release candidate—not just another prompt, plan, or documentation-only upgrade.**
