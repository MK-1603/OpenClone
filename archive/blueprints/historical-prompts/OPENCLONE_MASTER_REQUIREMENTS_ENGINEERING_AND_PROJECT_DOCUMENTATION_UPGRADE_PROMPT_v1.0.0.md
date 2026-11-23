# OPENCLONE — MASTER REQUIREMENTS ENGINEERING & PROJECT DOCUMENTATION UPGRADE PROMPT
## Consolidate, strengthen and operationalize OpenClone's own requirements and the project documents it generates
**Version:** 1.0.0  
**Execution environment:** Existing OpenClone repository  
**Primary executor:** Antigravity or another authorized coding agent  
**Execution mode:** Audit first, then implement in-place with reversible changes

---

# 1. MISSION

Act as OpenClone's principal product architect, requirements engineer, software architect, documentation-system designer, QA lead and repository implementation agent.

Your mission is to inspect the existing OpenClone repository and upgrade its requirements engineering system so that:

1. OpenClone itself has a clear, approved, testable product definition.
2. OpenClone can analyze a user's new or existing application and produce a complete, proportionate, traceable requirements package.
3. OpenClone generates a project-specific `PROJECT.md` and `AGENTS.md` that remain consistent with supporting specifications.
4. Requirements flow from user intent through architecture, implementation, tests, deployment and maintenance.
5. The framework distinguishes verified facts, user-approved requirements, recommendations, assumptions, unknowns and implementation evidence.
6. The system does not generate excessive documentation for small projects or omit critical analysis for complex/high-risk projects.

**Important distinction:** There are two separate requirement subjects:
- **OpenClone's own product requirements:** what the OpenClone framework is, who it serves, what it must do, its boundaries, architecture, quality goals and roadmap.
- **Generated application requirements:** what an individual application built with OpenClone must do and how its coding agents must implement it.

Do not mix these into one `PROJECT.md`. Maintain separate source-of-truth documents and separate approval states.

This is an implementation task, not merely a proposal. Inspect the actual repository, reuse existing assets, make safe changes, run tests and report evidence.

---

# 2. NON-NEGOTIABLE RULES

1. Work in the existing OpenClone repository. Do not create a second framework or duplicate requirements engine.
2. Inspect the real repository, current branch, Git status, source files, templates, schemas, registries, workflows, CLI, tests and documentation before editing.
3. Preserve user changes, Git history, stable IDs, existing functionality, licenses and attribution.
4. Reuse and consolidate existing templates and project-generation code. Do not create a competing generator.
5. Do not assume a document is authoritative because of its filename. Identify canonical, draft, deprecated, alternate and historical versions.
6. Never silently convert an AI suggestion or assumption into an approved requirement.
7. Never invent user research, market evidence, technical capabilities, provider features, costs, compliance obligations or test results.
8. Do not mark a project `READY` while critical requirements or approval decisions remain unresolved.
9. Do not implement, deploy, publish, spend money, change production data or access external accounts without the required authorization.
10. Do not create empty folders or documents simply to match a proposed tree.
11. Avoid unnecessary abstractions, duplicated registries, duplicated templates and oversized specifications.
12. Make changes in small, reversible batches. Update references and tests after each migration.
13. If blocked by missing credentials, access or owner decisions, finish safe work and record the blocker precisely.
14. Report what is actually implemented and tested. Do not claim that documentation alone makes a feature operational.

---

# 3. PHASE ZERO — REPOSITORY AND DOCUMENT AUDIT

## 3.1 Establish baseline

Record:
- Repository root, remote, branch, commit SHA and worktree state.
- Existing package/runtime and CLI entry points.
- Existing project-generation implementation.
- Existing requirement, project and agent templates.
- Existing schemas and registries.
- Existing lifecycle workflows and engines.
- Test, lint, type-check, build and validation commands.
- CI checks and known failures.
- Existing user changes and generated files.

Run safe baseline checks and record exact commands and results. Do not overwrite or clean user changes.

## 3.2 Inspect relevant existing assets

Search and inspect, if present:
- Root `PROJECT.md` and `AGENTS.md`.
- `templates/PROJECT.template.md`.
- `templates/AGENTS.template.md`.
- `templates/PROJECT-PROFILE.template.yaml`.
- Other project, requirements, architecture, testing, deployment and report templates.
- `tools/openclone_runtime/project.py`.
- `tools/openclone_runtime/openclone.py`.
- `src/openclone/`.
- `runtime/`.
- `workflows/WF-001-NEW-PROJECT-FROM-DOCUMENT.md`.
- `workflows/WF-013-PROJECT-DEFINITION-ASSESSMENT-AND-IMPLEMENTATION-PLANNING.md`.
- Relevant modes, engines, domains, schemas, registries and project lifecycle docs.
- `examples/demo-project/` and other valid reference projects.
- Existing generated `PROJECT.md` and `AGENTS.md` examples.

Inspect complete relevant documents, not just filenames or snippets.

## 3.3 Produce audit artifacts

Use existing assessment conventions where appropriate. Create/update:
- `assessments/requirements/REQUIREMENTS-SYSTEM-AUDIT.md`
- `assessments/requirements/DOCUMENT-INVENTORY-AND-AUTHORITY-MAP.md`
- `assessments/requirements/GAP-AND-CONFLICT-REGISTER.md`
- `assessments/requirements/REQUIREMENTS-MIGRATION-PLAN.md`

For each existing document record:
- Path and purpose.
- Intended audience.
- Authority level.
- Status and version.
- Duplicated/overlapping content.
- Missing sections.
- Consumers and references.
- Proposed action: retain, improve, merge, deprecate, archive or replace.
- Migration and compatibility risks.

**Gate:** Do not rewrite the documentation system until the audit and authority map are complete.

---

# 4. DEFINE TWO DISTINCT REQUIREMENTS SYSTEMS

## 4.1 OpenClone framework product definition

OpenClone's own root-level `PROJECT.md` must describe OpenClone itself.

It should cover:

1. Product identity, status, owner and version.
2. Product vision and positioning.
3. Problem statement and target users.
4. User needs and primary use cases.
5. Product goals, non-goals and scope boundaries.
6. Functional requirements for OpenClone capabilities.
7. Non-functional requirements with measurable targets.
8. Product workflows and lifecycle.
9. Framework architecture and component boundaries.
10. AI model, coding-agent and tool integration requirements.
11. Repository intelligence and asset discovery requirements.
12. Project generation requirements.
13. Security, privacy, permissions and trust boundaries.
14. Deployment and operations requirements.
15. Testing, evaluation and quality strategy.
16. Cost, usage and resource governance.
17. Release and maintenance lifecycle.
18. Risks, assumptions and open decisions.
19. Roadmap and milestones.
20. Acceptance criteria and definition of done.
21. Requirement traceability and approval record.

Do not copy generic generated-application requirements into OpenClone's own product definition unless they genuinely apply to the framework.

## 4.2 Generated application definition

For each application, generate a separate project workspace with:
- `PROJECT.md`: what the application is, why it exists, what it must do and how success is measured.
- `AGENTS.md`: how authorized coding agents must work in that application's repository.
- Supporting specifications only when justified by complexity and risk.

Never let an application's `PROJECT.md` overwrite or be confused with OpenClone's root-level `PROJECT.md`.

---

# 5. REQUIREMENTS ENGINEERING STANDARD

Implement a consistent requirements model.

## 5.1 Requirement record

Every requirement should support these fields where applicable:

| Field | Meaning |
|---|---|
| ID | Stable unique identifier |
| Title | Concise requirement name |
| Statement | Testable requirement |
| Category | Functional, non-functional, business, integration, data, security, operational, UX, compliance, etc. |
| Source | User, stakeholder, existing system, regulation, research or framework |
| Rationale | Why the requirement exists |
| Actor/persona | Who needs it |
| Priority | MUST, SHOULD, COULD, WON'T |
| Status | Proposed, clarified, approved, implemented, verified, rejected, deferred |
| Evidence | Source supporting the requirement |
| Dependencies | Related requirements and constraints |
| Acceptance criteria | Observable conditions for success |
| Verification method | Test, inspection, analysis, demonstration or audit |
| Owner | Decision/accountability owner |
| Change history | What changed, when and why |

Do not force every field into a single flat table if a structured schema is more suitable. Keep IDs stable.

## 5.2 Distinguish knowledge states

Use explicit labels:
- `VERIFIED_FACT`
- `USER_REQUESTED`
- `USER_APPROVED`
- `AI_RECOMMENDATION`
- `ASSUMPTION`
- `OPEN_QUESTION`
- `UNKNOWN`
- `CONFLICT`
- `NOT_APPLICABLE`
- `BLOCKED`

The system must not treat `AI_RECOMMENDATION`, `ASSUMPTION` or `UNKNOWN` as approved decisions.

## 5.3 Prioritization

Use a consistent priority model:
- `MUST`: required for the agreed release.
- `SHOULD`: important but a release may proceed with an accepted exception.
- `COULD`: useful if time/resources permit.
- `WONT`: explicitly excluded from the current scope.

Priority is not the same as implementation status or risk severity.

## 5.4 Acceptance criteria

Acceptance criteria must be testable and linked to requirements.

Prefer:
- Given / When / Then.
- Measurable thresholds.
- Explicit permission outcomes.
- Defined input/output behavior.
- Defined error and recovery behavior.

Avoid vague statements such as “fast”, “secure”, “user-friendly”, “scalable” or “production-ready” without a measurable or inspectable definition.

## 5.5 Traceability

Implement traceability:

```text
User / Stakeholder Need
        |
        v
Problem / Outcome
        |
        v
Requirement ID
        |
        v
Acceptance Criterion
        |
        v
Architecture / ADR
        |
        v
Implementation Task
        |
        v
Code / Component
        |
        v
Test Case
        |
        v
Verification Evidence
        |
        v
Release / Operational Status
```

A requirement is not complete merely because code exists. It needs the required verification evidence.

---

# 6. PRODUCT AND PROBLEM DISCOVERY

For new projects, OpenClone should establish:

- Who experiences the problem?
- What problem are they trying to solve?
- How frequently and severely does it occur?
- What do they do today?
- What alternatives exist?
- Why are current alternatives insufficient?
- What evidence supports the problem?
- What outcome would demonstrate value?
- Who is the buyer, user, administrator or beneficiary, if different?
- What is deliberately out of scope?

When external research is requested or necessary, distinguish researched evidence from user-provided information and model inference. Include source, date and confidence. Never fabricate interviews, surveys, competitor findings or market size.

For small internal tools, use a proportionate discovery process. Do not force startup market research when it is irrelevant.

---

# 7. EXISTING-PROJECT REPOSITORY ANALYSIS

For an existing application, perform repository discovery before proposing changes.

Inspect:
- Branch and commit.
- Languages, frameworks and runtime versions.
- Package manifests and lockfiles.
- Folder structure and entry points.
- Existing features and routes.
- API endpoints and contracts.
- Database schemas, migrations and data ownership.
- Authentication, authorization and tenant boundaries.
- Integrations and external services.
- Existing tests and test coverage evidence.
- CI/CD and deployment configuration.
- Logging, metrics and error handling.
- Known defects, TODOs and technical debt.
- Security-sensitive areas.
- Documentation and actual behavior.

Classify features accurately:
- `EXISTING_AND_VERIFIED`
- `EXISTING_BUT_UNVERIFIED`
- `PARTIALLY_IMPLEMENTED`
- `MISSING`
- `BROKEN`
- `PROPOSED`
- `DEPRECATED`
- `OUT_OF_SCOPE`

Do not infer that a feature works merely because a route, component, schema or test file exists. Verify behavior where possible.

Produce an existing-system baseline and gap register. Preserve working functionality unless a change is explicitly approved.

---

# 8. BUSINESS RULES, STATES AND PERMISSIONS

Create dedicated specifications when the application complexity warrants them.

## 8.1 Business rules

Each business rule should define:
- Stable rule ID.
- Trigger.
- Preconditions.
- Conditions.
- Expected behavior.
- Exceptions.
- Data affected.
- Permissions.
- Validation and invariants.
- Related requirements.
- Verification method.

Business rules must not be hidden only inside UI descriptions or implementation code.

## 8.2 State and lifecycle model

For important entities define:
- States.
- Allowed transitions.
- Transition actor.
- Preconditions.
- Side effects.
- Invalid transitions.
- Retry/recovery behavior.
- Audit requirements.

Generate state diagrams where useful.

## 8.3 Authorization matrix

For role-based or multi-tenant systems, define:
- Roles and permissions.
- Resource ownership.
- Tenant/workspace boundaries.
- Read/write/delete/admin actions.
- Delegation and transfer rules.
- Privileged actions.
- Deny-by-default behavior.
- Authorization test cases.

Do not rely on frontend visibility to enforce access control. Authorization must be enforced server-side or at the trusted execution boundary.

---

# 9. PRODUCT EXPERIENCE AND UX/UI REQUIREMENTS

Document:
- User personas and primary tasks.
- Information architecture.
- Navigation and route map.
- Critical user journeys.
- Wireframes or design references when required.
- Visual direction and its rationale.
- Typography, colors, spacing and component tokens.
- Responsive behavior.
- Accessibility target appropriate to the product.
- Localization needs where relevant.
- Interaction states.
- Empty, loading, success, error and offline states.
- Form validation and destructive-action confirmation.
- Keyboard, screen-reader and touch behavior.
- Performance implications of animation and media.

For every interactive control, define actual behavior. Do not accept decorative controls or fake functionality as complete.

Do not force a global visual style on every generated application. Design decisions must fit the product, audience, platform and brand.

---

# 10. ARCHITECTURE AND TECHNICAL SPECIFICATION

For projects that need detailed architecture, generate:

1. System context.
2. Container/service architecture.
3. Component responsibilities.
4. Data-flow diagrams.
5. Trust boundaries.
6. Database design and relationships.
7. API and event contracts.
8. Background jobs and queue behavior.
9. Integration dependency map.
10. Deployment topology.
11. Architecture Decision Records.

For each material technology decision record:
- Decision ID.
- Status: proposed, accepted, rejected or superseded.
- Context and constraints.
- Options considered.
- Selected option and rationale.
- Trade-offs and consequences.
- Owner and date.
- Evidence/source and verification date.

Technology choices must be justified against project needs. Do not add Redis, Elasticsearch, Kafka, Kubernetes, microservices or extra databases by default. `NONE` is a valid choice when the requirement does not justify a component.

Clearly distinguish:
- Existing observed architecture.
- Proposed target architecture.
- Approved architecture.
- Implemented architecture.

---

# 11. DATA, API AND INTEGRATION REQUIREMENTS

For data:
- Entities and relationships.
- Ownership and tenant boundaries.
- Classification and sensitivity.
- Validation and constraints.
- Indexes and query needs.
- Retention and deletion.
- Export/correction requirements.
- Backup and recovery.
- Migration and compatibility.
- Audit history.

For APIs and events:
- Stable ID and version.
- Method/event type.
- Authentication and authorization.
- Request and response schema.
- Validation and error semantics.
- Idempotency and rate limits.
- Pagination/filtering where applicable.
- Audit requirements.
- Compatibility and deprecation policy.

For external integrations:
- Purpose.
- Data exchanged.
- Direction.
- Required scopes.
- Failure and retry behavior.
- Rate limits.
- Provider dependency.
- Data residency/privacy implications.
- Sandbox/test strategy.
- Status and evidence.

Never place secret values in requirements or project documents.

---

# 12. NON-FUNCTIONAL REQUIREMENTS

Select only applicable categories and define measurable targets.

Consider:
- Security.
- Privacy.
- Performance and latency.
- Reliability and availability.
- Scalability and capacity.
- Accessibility.
- Usability.
- Maintainability.
- Portability.
- Compatibility.
- Observability.
- Recovery objectives.
- Cost and resource limits.
- Compliance, where verified and applicable.

Examples of measurable specifications:
- p95 latency target for a named critical endpoint.
- Maximum expected concurrent users.
- Backup recovery point and recovery time objectives.
- Availability target and measurement window.
- Supported browser/device matrix.
- Accessibility conformance target.
- Maximum monthly infrastructure/model budget.

If the user has not supplied enough information to define a target, record an open decision or propose a target for approval. Do not present an arbitrary target as a user-approved requirement.

---

# 13. SECURITY, PRIVACY AND TRUST

Include a project-appropriate threat model covering relevant threats:
- Authentication and authorization bypass.
- Tenant/workspace isolation failures.
- Injection and unsafe input handling.
- XSS, CSRF, SSRF and file-upload risks where relevant.
- Secret exposure.
- Data leakage and excessive retention.
- Insecure integrations and webhooks.
- Supply-chain and dependency risk.
- Abuse, rate-limit bypass and resource exhaustion.
- Unsafe AI/tool execution and prompt injection where AI is used.
- Privilege escalation.
- Unsafe migrations and data loss.

Specify:
- Trust boundaries.
- Data classification.
- Authentication and authorization.
- Least privilege.
- Secret storage and rotation.
- Encryption requirements.
- Audit logging.
- Rate limiting and abuse controls.
- Dependency/security scanning.
- Backup/recovery.
- Incident response.
- Security verification and accepted residual risks.

Do not claim legal or regulatory compliance without verified applicability and evidence.

---

# 14. IMPLEMENTATION AND DELIVERY PLANNING

Generate a dependency-aware plan with:
- Milestones.
- Deliverables.
- Requirement IDs.
- Dependencies.
- Owners/agents.
- Acceptance gates.
- Test evidence.
- Risks.
- Status.

Break work into independently verifiable tasks. Every task should have:
- Task ID.
- Scope.
- Related requirements.
- Expected files/components.
- Dependencies.
- Definition of done.
- Verification command or method.
- Status.

Avoid overly granular task plans for small projects. Use the smallest useful work breakdown.

Change control:
- Requirement changes update affected acceptance criteria and tests.
- Architecture changes require an ADR.
- Scope expansion requires impact analysis.
- Breaking changes require migration guidance.
- Existing functionality and data must not be silently removed.
- Production-impacting changes require configured approval.

---

# 15. TESTING AND QUALITY ENGINEERING

Create a risk-based verification strategy.

Possible test levels:
- Static analysis, format, lint and type checks.
- Unit tests.
- Schema and contract tests.
- Integration tests.
- End-to-end tests.
- Security tests.
- Accessibility tests.
- Performance/load tests.
- Migration tests.
- Backup/restore tests.
- Deployment and rollback tests.

For each test:
- Test ID.
- Requirement/acceptance IDs.
- Preconditions and test data.
- Expected result.
- Environment.
- Execution command or method.
- Result and evidence.
- Defect/reference if failed.

A test file existing is not proof of a passing test. Record exact commands, exit codes, environment and results. Preserve known failures and distinguish pre-existing from newly introduced failures.

---

# 16. DEPLOYMENT, OPERATIONS AND MAINTENANCE

Specify:
- Deployable units.
- Runtime and package manager versions.
- Build commands and artifacts.
- Environments: local, test, preview, staging, production as applicable.
- Environment variables by name and classification only.
- CI/CD triggers and gates.
- Preview policy.
- Production approval.
- Database migration strategy.
- Health/readiness checks.
- Logs, metrics, traces and alerts.
- Error tracking.
- Backup and restore.
- Rollback and recovery.
- Incident response.
- Cost monitoring.
- Ownership and support.
- Upgrade and dependency maintenance.
- Post-release feedback and roadmap review.

A deployment plan is not proof of deployment. Report the actual environment and verification evidence.

Production auto-deployment must be explicitly enabled by an authorized owner and protected by required quality, security, approval, health and rollback gates.

---

# 17. DOCUMENT PACKAGE GENERATED FOR EACH APPLICATION

Use one canonical project root and one source of truth. Generate supporting documents only when needed.

Recommended structure:

```text
application/
├── PROJECT.md
├── AGENTS.md
├── requirements/
│   ├── FUNCTIONAL-REQUIREMENTS.md
│   ├── NON-FUNCTIONAL-REQUIREMENTS.md
│   ├── BUSINESS-RULES.md
│   ├── ACCEPTANCE-CRITERIA.md
│   └── EXISTING-SYSTEM-ANALYSIS.md
├── architecture/
│   ├── SYSTEM-ARCHITECTURE.md
│   ├── DATABASE-DESIGN.md
│   ├── API-DESIGN.md
│   ├── SECURITY-ARCHITECTURE.md
│   └── ADR/
├── design/
│   ├── UX-SPECIFICATION.md
│   └── DESIGN-SYSTEM.md
├── execution/
│   ├── IMPLEMENTATION-ROADMAP.md
│   ├── TASK-BREAKDOWN.md
│   └── TRACEABILITY-MATRIX.md
├── quality/
│   ├── TEST-STRATEGY.md
│   └── QUALITY-GATES.md
└── operations/
    ├── DEPLOYMENT-PLAN.md
    ├── ENVIRONMENT-STRATEGY.md
    └── MONITORING-AND-RECOVERY.md
```

This is a conditional structure, not a mandatory file checklist. For a small application, a concise `PROJECT.md`, `AGENTS.md` and a small task/test plan may be sufficient.

## 17.1 `PROJECT.md` responsibilities

`PROJECT.md` is the canonical project overview and source-of-truth index. It should contain:
1. Project identity and lifecycle status.
2. Problem, vision and intended users.
3. Goals, non-goals and scope.
4. Key functional and non-functional requirements.
5. Main user journeys.
6. Business rules summary.
7. UX/product direction.
8. Architecture and stack summary.
9. Data/API/integration summary.
10. Security/privacy summary.
11. Milestones and quality strategy.
12. Deployment/operations summary.
13. Risks, assumptions and open decisions.
14. Acceptance criteria and definition of done.
15. Approval and change history.
16. Links to supporting documents.
17. OpenClone traceability.

Do not duplicate entire detailed specifications inside `PROJECT.md`.

## 17.2 `AGENTS.md` responsibilities

`AGENTS.md` is the project-specific coding-agent execution contract. It should define:
1. Mission and project context.
2. Instruction precedence and source-of-truth documents.
3. Repository structure and setup commands.
4. Architecture and module ownership.
5. Coding conventions and implementation boundaries.
6. Testing and verification commands.
7. Security, privacy and secret handling.
8. UX/accessibility expectations.
9. Data/API/integration constraints.
10. Deployment/environment restrictions.
11. Tool permissions and human approval gates.
12. Git and change-management rules.
13. Context/token/cost efficiency.
14. Progress reporting and evidence requirements.
15. Definition of done.

Do not copy all OpenClone framework rules into every application. Include the project-specific subset and references. Generate platform-specific agent instruction files only when required by a verified adapter; keep them synchronized from a canonical policy.

---

# 18. PROJECT COMPLEXITY AND DOCUMENTATION SCALING

Implement a project profile that helps select documentation depth.

Possible profiles:
- `SMALL`: simple utility, prototype or low-risk internal tool.
- `STANDARD`: typical production application.
- `COMPLEX`: multi-module, multi-role, integrated or data-sensitive system.
- `CRITICAL`: high-impact, regulated, safety-sensitive or mission-critical system.

Do not classify solely by number of features. Consider:
- User and business impact.
- Security/privacy sensitivity.
- Data complexity.
- Integration count.
- Deployment topology.
- Availability/recovery needs.
- Compliance obligations.
- Team size and maintenance horizon.

For each profile define:
- Required discovery depth.
- Required requirement fields.
- Architecture artifacts.
- Security review depth.
- Test coverage expectations.
- Approval gates.
- Deployment evidence.
- Required supporting documents.

The user can override the suggested profile. Record the reason. A high-risk project must not bypass necessary controls because it is small.

---

# 19. VALIDATION AND APPROVAL GATES

Before a generated project is marked `READY_FOR_APPROVAL`:
- Required fields are present.
- User intent is represented faithfully.
- Facts, assumptions, recommendations and unknowns are separated.
- Functional requirements have stable IDs.
- Critical requirements have testable acceptance criteria.
- Scope and non-goals are explicit.
- Existing features are not misrepresented.
- Architecture matches requirements and constraints.
- Data/API/security implications are addressed.
- Milestones and verification are defined.
- `PROJECT.md` and `AGENTS.md` are consistent.
- Supporting documents resolve and do not conflict.
- No secret values are present.
- OpenClone traceability points to real assets actually inspected.

Approval states:
- `DRAFT`
- `DISCOVERY`
- `READY_FOR_APPROVAL`
- `APPROVED`
- `IN_IMPLEMENTATION`
- `IN_VERIFICATION`
- `RELEASE_READY`
- `RELEASED`
- `MAINTENANCE`
- `BLOCKED`
- `ARCHIVED`

Do not skip approval states silently. A document does not grant permission for privileged actions.

---

# 20. CHANGE MANAGEMENT AND DOCUMENT CONSISTENCY

When requirements change:
1. Record the change request and source.
2. Identify affected requirements and acceptance criteria.
3. Analyze architecture, data, API, security, cost and schedule impact.
4. Update affected ADRs and supporting specifications.
5. Update implementation tasks and tests.
6. Obtain required approval.
7. Update version and change history.
8. Validate cross-document consistency.

Add automated checks for:
- Duplicate requirement IDs.
- Broken internal links.
- Invalid statuses and priority values.
- Missing acceptance criteria for MUST requirements.
- Orphaned tests/tasks.
- Unresolved placeholders in approved documents.
- Contradictory project profile and project documents.
- Missing approval for protected lifecycle transitions.
- Unsupported or stale OpenClone asset references.

---

# 21. IMPLEMENTATION IN OPENCLONE

Integrate this system into the existing architecture.

## 21.1 Reuse before creating

Inspect and reuse the existing:
- Project templates.
- Agent templates.
- Project profile schema.
- Project generator.
- Project lifecycle workflow.
- Requirements/assessment engines.
- Domain and standards assets.
- Registries.
- CLI and runtime.
- Tests and example projects.

Refactor existing components rather than creating parallel `requirements_v2`, `project_generator_v2` or duplicate template directories.

## 21.2 Canonical ownership

Define and document:
- Which component owns requirement data and status transitions.
- Which schema validates requirement records.
- Which workflow handles discovery and approval.
- Which engine performs repository analysis.
- Which component generates project documents.
- Which component validates consistency and traceability.
- Which component stores approval and change history.
- Which adapter hands off to coding agents.

Use a single authoritative source for each type of data. Derived views and generated indexes are acceptable.

## 21.3 CLI and user workflow

Inspect the current CLI and implement commands consistent with its existing conventions. Possible capabilities:
- Initialize OpenClone's own product requirements.
- Start a new application discovery.
- Analyze an existing repository.
- Validate requirements.
- Generate project documentation.
- Check document consistency.
- Show requirement traceability.
- Record an approved change.
- Produce an implementation handoff.

Do not add commands without a working implementation, help text and tests. Do not break existing CLI commands.

---

# 22. REQUIRED TEST SCENARIOS

Implement automated tests for at least these scenarios:

1. A small greenfield utility generates a concise valid package.
2. A standard SaaS application generates detailed requirements and architecture.
3. An existing repository is analyzed without claiming unverified features work.
4. Conflicting user requirements are identified and surfaced.
5. Missing critical decisions block readiness.
6. AI recommendations remain unapproved until the owner approves them.
7. A MUST requirement without acceptance criteria fails validation.
8. Duplicate requirement IDs fail validation.
9. Broken supporting-document links fail validation.
10. A requirement traces to a task and test.
11. A changed requirement identifies affected documents and tests.
12. A high-risk project receives the required security and approval gates.
13. A small project does not receive unnecessary documents.
14. Secrets are not copied into generated documents.
15. Generated `PROJECT.md` and `AGENTS.md` remain consistent.
16. An existing project preserves its verified baseline and does not rebuild working features without justification.
17. OpenClone's own product requirements remain separate from generated application requirements.

Use deterministic fixtures and test the real generation/validation path. Mocks may be used for external providers, but label those tests accurately.

---

# 23. IMPLEMENTATION PHASES

## Phase 1 — Audit
Inventory existing documents, code, schemas, workflows, registries and tests. Produce the authority map and gap register.

**Gate:** Evidence-backed baseline and migration plan.

## Phase 2 — Canonical document model
Define requirement records, statuses, IDs, priority, evidence, approval and traceability. Reuse existing schemas where suitable.

**Gate:** Schema and governance decisions reviewed.

## Phase 3 — OpenClone product requirements
Create or improve the root OpenClone product definition. Separate framework requirements from generated application requirements.

**Gate:** Root product definition has clear scope, measurable outcomes, requirement IDs and approval status.

## Phase 4 — Generated project documentation
Consolidate the application `PROJECT.md` and `AGENTS.md` templates. Add conditional supporting-document generation.

**Gate:** Small and standard project fixtures generate proportionate, consistent packages.

## Phase 5 — Repository analysis and discovery
Integrate existing-project analysis and OpenClone asset discovery. Track provenance and verification state.

**Gate:** Existing-project fixture accurately distinguishes implemented, partial, missing and unverified capabilities.

## Phase 6 — Traceability and change management
Connect requirements, acceptance criteria, architecture, tasks, tests and evidence. Add consistency validation.

**Gate:** Traceability and change-impact tests pass.

## Phase 7 — Workflow, CLI and integration
Connect the canonical workflow to the actual runtime, CLI, project generator, registries and coding-agent handoff.

**Gate:** End-to-end project generation works using the real repository assets.

## Phase 8 — Hardening and documentation
Run regression, security, schema, link, CLI and end-to-end tests. Update contributor and user docs.

**Gate:** Final evidence-backed readiness report.

---

# 24. ACCEPTANCE CRITERIA

The upgrade is accepted only when:

## Requirements system
- [ ] OpenClone's own product requirements are separate from application requirements.
- [ ] One canonical requirement model and schema exist.
- [ ] Requirement IDs are stable and unique.
- [ ] User requests, recommendations, assumptions, unknowns and approvals are distinct.
- [ ] Priority, status and risk are not conflated.
- [ ] Critical requirements have testable acceptance criteria.
- [ ] Requirement-to-test traceability exists.
- [ ] Change impact and document consistency can be validated.

## Project generation
- [ ] Existing project generator is reused or deliberately refactored.
- [ ] `PROJECT.md` and `AGENTS.md` are generated from canonical templates.
- [ ] Supporting documents are conditional and proportionate.
- [ ] Small, standard, complex and high-risk project profiles are handled.
- [ ] Existing repository analysis distinguishes verified from unverified features.
- [ ] No unresolved critical placeholder is allowed in approved documents.
- [ ] Human approval gates work.
- [ ] OpenClone traceability identifies real assets actually used.

## Quality
- [ ] Unit, schema, integration and end-to-end tests run.
- [ ] Existing functionality and CLI compatibility are preserved.
- [ ] Documentation links and registries validate.
- [ ] Security/privacy requirements are represented.
- [ ] Final report lists exact test commands and outcomes.
- [ ] Known limitations and blockers are explicit.

---

# 25. FINAL REPORT

At completion, report:

1. Repository identity, branch, commit and worktree state.
2. Existing documents inspected and their authority status.
3. Problems and duplication discovered.
4. Canonical requirements model and schemas created/updated.
5. Changes to OpenClone's own product requirements.
6. Changes to generated application `PROJECT.md` and `AGENTS.md`.
7. Existing-project analysis capability and evidence.
8. Traceability and change-management implementation.
9. CLI/workflow/runtime integration.
10. Files created, updated, moved, deprecated or archived.
11. Tests executed with exact commands, results and evidence.
12. Security/privacy findings.
13. Remaining decisions, limitations and blockers.

Use accurate capability statuses:
- `DOCUMENTED`
- `SPECIFIED`
- `IMPLEMENTED`
- `UNIT_TESTED`
- `INTEGRATION_TESTED`
- `E2E_TESTED`
- `VERIFIED`

Do not claim stronger evidence than actually exists.

---

# 26. START EXECUTION

Begin with the actual OpenClone repository. Inspect Git state and all relevant existing documents and implementation before making changes.

Do not ask the user to repeat information already present in the repository. Ask only one focused question when a decision cannot be resolved safely from evidence and materially affects product scope, architecture, security, cost or approval.

Complete safe work autonomously in reversible phases. Pause for authorization before destructive changes, production operations, public releases, paid resources or external account actions.

**Final objective:** OpenClone must have a trustworthy requirements engineering system for itself and for every application it helps create. Its generated project documents must be accurate, proportionate, traceable, approval-aware and directly useful to coding agents from discovery through implementation, testing, deployment and maintenance.
