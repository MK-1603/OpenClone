# AISDF — Complete Engine Architecture, Three-Mode Intake, Orchestration & Delivery Blueprint

**Framework:** AI Software Development Framework (AISDF)  
**Tagline:** From Problem Statement to Production Software  
**Document:** Engine Architecture and End-to-End Execution/Handoff Specification  
**Version:** 1.2.0  
**Status:** Proposed architecture for review — not yet implemented  
**Repository type:** Open-source GitHub framework repository  
**Canonical principle:** The framework defines reusable engineering methods, prompts, contracts, schemas, workflows, rules, examples and validation. Compatible AI tools execute them in the user's authorized environment.

---

# 1. Executive interpretation

AISDF is intended to guide a project from an initial problem or project document to a deployed and maintained software product. It must work across compatible tools such as ChatGPT, Claude, Gemini and other assistants for analysis and documentation; design tools such as Stitch, Figma or direct AI-assisted design workflows; and coding environments such as Antigravity, Cursor, Claude Code, Codex, Windsurf and other compatible IDE/CLI agents.

The framework must not assume that every named tool supports every action. It must inspect and record the actual capabilities of the selected tool and adapt the workflow accordingly.

The intended user journey is:

1. Give AISDF a problem statement, idea, project document or existing repository.
2. Select one of three intake modes.
3. Run predefined analysis and validation workflows using a selected AI assistant.
4. Generate and approve the project documents that become the source of truth.
5. Design UX/UI using a suitable design workflow/tool.
6. Evaluate and select technology based on requirements and constraints.
7. Hand the approved project package to a compatible AI coding IDE/agent.
8. Build incrementally with controlled branches, commits, tests and evidence.
9. Run security, quality, usability, performance and production-readiness verification.
10. Prepare and authorize deployment through configurable pipelines.
11. Verify the deployed product, record history and maintain it.

**Important:** “No errors” cannot be guaranteed. AISDF must instead require measurable quality gates, disclose residual risks, block unsafe releases and report verified, unverified, failed and blocked work honestly.

---

# 2. Scope and boundary

## 2.1 What AISDF is

An open-source engineering framework containing:

- Methodology and decision gates.
- Three project-intake modes.
- Analysis and validation engines expressed as reusable workflows.
- Project document templates and schemas.
- Product, UX/UI, technology and architecture methods.
- Knowledge and tool discovery methods.
- AI-agent roles, execution contracts and handoff protocols.
- Git and change-management rules.
- Testing, security, performance, accessibility and usability standards.
- Deployment, operations and maintenance workflows.
- Evidence, audit and project-state records.
- Tool adapters and verified compatibility profiles.
- Optional lightweight scripts that validate framework assets.

## 2.2 What AISDF is not

Unless separately proposed and approved, AISDF is not:

- A hosted AI platform or model.
- A universal agent runtime.
- An IDE or design editor.
- A Git hosting provider.
- A CI/CD hosting provider.
- A cloud provider or deployment platform.
- A load balancer implementation.
- A guarantee of error-free software.
- A replacement for human product, security or release accountability.

The framework tells compatible tools and people **what to do, how to do it, what evidence to produce, and when to stop or ask for approval**.

---

# 3. Three project-intake modes

The three modes are selected at the beginning. The framework may later transition modes only after documenting why.

## Mode 1 — Problem / Idea Discovery

**Use when:** The user has an idea, problem statement, rough notes, voice transcript or early concept, but no complete product specification.

**Goal:** Determine whether the problem is real, who experiences it, what outcome is needed, and whether a software solution is justified.

Workflow:

1. Capture the raw problem without prematurely designing a solution.
2. Identify user/customer groups and affected stakeholders.
3. Separate observed facts, user claims, assumptions and unknowns.
4. Analyze pain, frequency, severity, current alternatives and workarounds.
5. Research existing products, substitutes and comparable solutions.
6. Evaluate desirability, feasibility, viability and timing as applicable.
7. Run inversion, premortem, risk and failure analysis.
8. Define success measures and pre-commit kill/pivot criteria.
9. Decide: proceed, validate further, narrow, pivot, defer or stop.
10. If proceeding, create the approved Problem Brief and Product Discovery Record.

Required outputs:

- `problem-brief.md`
- `stakeholder-and-user-map.md`
- `evidence-and-assumptions-register.md`
- `market-and-alternatives-review.md` (where relevant)
- `risk-and-premortem.md`
- `success-and-kill-criteria.md`
- `discovery-decision-record.md`

**Exit gate:** No product build plan until the problem, intended users, desired outcome, critical assumptions and next decision are explicit. A commercial validation gate may be skipped for educational/internal projects with a recorded reason.

## Mode 2 — New Project / Product Build

**Use when:** The problem and intended outcome are sufficiently understood, or the user already has an approved project brief and wants a new application.

**Goal:** Turn the approved brief into a build-ready product and engineering package.

Workflow:

1. Validate the input package and identify missing decisions.
2. Create product requirements and scope.
3. Define user roles, journeys and workflows.
4. Define functional and non-functional requirements.
5. Produce UX structure, flows, wireframes and design system.
6. Evaluate technology and external services.
7. Design architecture, data model, APIs, integrations and deployment topology.
8. Define security and privacy requirements.
9. Decompose work into milestones, epics and dependency-aware tasks.
10. Approve the baseline and create the implementation handoff package.

Required outputs include a PRD, requirements register, acceptance criteria, UX/UI specification, architecture document, ADRs, data/API contracts, threat model, test strategy, deployment plan, task graph and project baseline.

**Exit gate:** A coding agent must not infer unresolved product-critical decisions silently. It may proceed with explicitly low-risk assumptions only when the project policy permits them.

## Mode 3 — Existing Project / Improvement / Transformation

**Use when:** A repository, application, prototype or deployed system already exists.

**Goal:** Understand the current system before changing it, preserve intended behavior and make only approved changes.

Mandatory sequence:

**Inspect → Understand → Analyze → Discover → Compare → Document → Approve → Implement → Verify.**

Workflow:

1. Inspect repository structure, branch, working tree and recent history.
2. Identify stack, architecture, modules, entry points and external services.
3. Inspect tests, CI, deployment, environment configuration and security controls.
4. Run the project where safe; record what was and was not executable.
5. Map current features and user journeys.
6. Identify defects, technical debt, security risks, performance issues and UX gaps.
7. Trace dependencies and assess impact of the requested change.
8. Compare options: preserve/improve, redesign, or transform.
9. Produce a Project X-Ray and proposed change plan.
10. Obtain approval for scope or architecture changes.
11. Implement in isolated branches/worktrees as appropriate.
12. Run regression and independent verification.

Required outputs:

- `project-xray.md`
- `current-state-architecture.md`
- `feature-inventory.md`
- `dependency-and-integration-map.md`
- `risk-and-defect-register.md`
- `change-impact-analysis.md`
- `proposed-change-plan.md`
- `baseline-and-verification-report.md`

**Exit gate:** No broad refactor, replacement, migration or product-direction change without explicit approval. Apply the Change Only Law.

---

# 4. Complete AISDF engine catalogue

An “engine” is a named capability with defined inputs, outputs, workflow, decision rules, owner, evidence and failure behavior. It is not necessarily a separate software service or autonomous agent. Keep engines as documented modules unless real execution evidence justifies runtime automation.

## A. Intake, understanding and validation

| ID | Engine | Responsibility | Main outputs |
|---|---|---|---|
| E-001 | Intake & Mode Selection | Classify input and select Mode 1, 2 or 3 | Intake record, selected mode |
| E-002 | Document Ingestion & Normalization | Parse documents, notes, repository context and source material | Normalized project brief |
| E-003 | Problem Discovery | Identify user problem, context, impact and desired outcome | Problem brief |
| E-004 | Existing Project X-Ray | Inspect existing codebase and current product behavior | X-Ray report |
| E-005 | Feature Inventory & Analysis | Identify current/proposed features, dependencies, value and gaps | Feature catalogue |
| E-006 | Problem Validation | Test evidence, assumptions, alternatives and problem severity | Validation report |
| E-007 | Product/Market Validation | Evaluate demand, alternatives, timing and viability when relevant | Validation decision |
| E-008 | Gap, Conflict & Ambiguity | Detect missing, conflicting, vague or unverifiable statements | Clarification register |
| E-009 | Risk, Inversion & Premortem | Identify failure paths, threats and pre-mortem risks | Risk register |
| E-010 | Scope & Kill-Criteria | Define boundaries, exclusions, success and stop conditions | Scope baseline |

## B. Product and requirements intelligence

| ID | Engine | Responsibility | Main outputs |
|---|---|---|---|
| E-011 | User & Stakeholder Intelligence | Define users, roles, needs and stakeholders | Personas/role model |
| E-012 | Requirements Engineering | Convert needs into testable requirements | Requirements register |
| E-013 | Feature Prioritization | Prioritize by value, risk, effort and dependencies | Prioritized feature list |
| E-014 | Product Specification | Define product behavior and boundaries | PRD/product specification |
| E-015 | Acceptance Criteria | Define observable pass/fail criteria | Acceptance criteria |
| E-016 | Traceability | Link problem → requirement → design → task → test → evidence | Traceability graph |

## C. UX/UI and experience design

| ID | Engine | Responsibility | Main outputs |
|---|---|---|---|
| E-017 | UX Research & Journey | Model tasks, journeys, pain points and user context | Journey maps |
| E-018 | Information Architecture | Define navigation, content hierarchy and page structure | Sitemap/IA |
| E-019 | Interaction & Flow Design | Define states, transitions, forms and error paths | User flows |
| E-020 | UI & Design-System | Define visual system, components, tokens and responsive rules | UI specification/design system |
| E-021 | Design Tool Selection & Handoff | Select compatible design tool and produce implementation-ready handoff | Design handoff package |
| E-022 | Usability & Accessibility Review | Evaluate usability, keyboard, screen-reader and accessibility criteria | UX/accessibility findings |

Design tools may include Stitch, Figma or AI-assisted generation in a general assistant. Tool choice depends on verified export, collaboration, inspectability and code-handoff capabilities. A generated screenshot alone is not a complete implementation specification.

## D. Technology and architecture intelligence

| ID | Engine | Responsibility | Main outputs |
|---|---|---|---|
| E-023 | Technology Research | Verify current technologies, versions and support | Technology research record |
| E-024 | Stack Selection | Compare stack choices against requirements and team capability | Approved stack |
| E-025 | Architecture Design | Define components, boundaries and quality attributes | Architecture document |
| E-026 | Data & Database Design | Model data, constraints, migrations, backup and retention | Data model |
| E-027 | API & Integration Design | Define contracts, auth, errors, rate limits and integrations | API/integration contracts |
| E-028 | Infrastructure & Scaling Design | Design hosting, networking, caching, queues and scaling when justified | Infrastructure plan |
| E-029 | Cost & Capacity Analysis | Estimate operational costs and resource needs | Cost/capacity model |
| E-030 | Architecture Decision & Change Control | Record alternatives, tradeoffs and approval | ADRs |

## E. Knowledge, tools and acquisition

| ID | Engine | Responsibility | Main outputs |
|---|---|---|---|
| E-031 | AKIS Knowledge Intelligence | Organize, retrieve, rank and freshness-check knowledge | Context/knowledge pack |
| E-032 | AFIAE Feature & Tool Discovery | Discover APIs, SDKs, libraries, MCP servers, models and services | Candidate catalogue |
| E-033 | Tool/Service Evaluation | Assess security, license, compatibility, cost and lock-in | Evaluation report |
| E-034 | Compatibility Verification | Verify tool capabilities and supported actions | Compatibility profile |

## F. Execution and orchestration

| ID | Engine | Responsibility | Main outputs |
|---|---|---|---|
| E-035 | Execution Planning | Convert baseline into milestones and task graph | Execution plan |
| E-036 | Task & Dependency Orchestration | Sequence tasks and manage dependencies | Task DAG |
| E-037 | Agent Role & Delegation | Assign bounded responsibilities to compatible agents | Agent assignment |
| E-038 | Context & Handoff | Package context and transfer ownership safely | Handoff package |
| E-039 | Tool/IDE Adapter | Translate framework contracts into tool-specific instructions | Adapter execution record |
| E-040 | Project State & Continuity | Preserve canonical project state across sessions | State snapshot |
| E-041 | Git & Change Orchestration | Manage branches, commits, PRs and merges | Change records |
| E-042 | Human Approval & Escalation | Stop for material decisions and record authorization | Approval record |

## G. Quality, security and verification

| ID | Engine | Responsibility | Main outputs |
|---|---|---|---|
| E-043 | Test Strategy & Generation | Derive test layers and cases from requirements | Test plan/cases |
| E-044 | Build, Test & Debug | Execute checks, diagnose failures and repair within scope | Test/build evidence |
| E-045 | Code Review & Change Impact | Review diffs, maintainability and regressions | Review report |
| E-046 | Security & Privacy | Threat model, secure design, dependency and secret checks | Security findings |
| E-047 | Performance & Load | Define and run workload-based performance tests | Performance report |
| E-048 | Independent Verification | Verify acceptance criteria independently of implementation claims | Verification verdict |
| E-049 | UX & Accessibility Verification | Validate real user journeys and accessibility | Usability evidence |
| E-050 | Release Readiness | Aggregate quality gates and residual risks | Release decision |

## H. Delivery and lifecycle

| ID | Engine | Responsibility | Main outputs |
|---|---|---|---|
| E-051 | CI/CD Pipeline Design | Define reproducible build/test/release automation | Pipeline specification |
| E-052 | Deployment & Environment | Configure environment-based deployment and secrets | Deployment record |
| E-053 | Production Verification | Smoke tests, health checks and rollback validation | Production evidence |
| E-054 | Observability & Incident Readiness | Define logs, metrics, traces, alerts and runbooks | Operations pack |
| E-055 | Maintenance & Change Governance | Manage updates, defects, vulnerabilities and deprecation | Maintenance records |
| E-056 | Project Closeout & Learning | Capture final state, lessons and next steps | Closeout report |

---

# 5. Predefined AI prompt and document system

AISDF must not depend on a single giant prompt. The master prompt is an entry point that loads the correct mode, rules and workflow documents.

## 5.1 Prompt hierarchy

1. `MASTER-ENTRY-PROMPT.md` — identify project, mode, tool and current state.
2. `MODE-1-PROBLEM-DISCOVERY.md`
3. `MODE-2-NEW-PROJECT.md`
4. `MODE-3-EXISTING-PROJECT.md`
5. Engine prompts — one per substantial engine or grouped capability.
6. Phase prompts — product, UX, architecture, implementation, testing, release.
7. Role prompts — analyst, product engineer, UX designer, architect, implementer, reviewer, tester, security reviewer, release engineer.
8. Handoff prompts — agent-to-agent, session-to-session, phase-to-phase.
9. Recovery prompts — failed task, blocked task, context loss, rollback, incident.

## 5.2 Required prompt behavior

Every prompt must instruct the AI tool to:

- Read the project baseline and relevant framework laws first.
- Identify its role and permitted scope.
- Cite source documents/sections for decisions.
- Separate facts, approved decisions, assumptions, inferences and unknowns.
- Never invent tool execution, test results or research.
- Ask only questions that block a safe or correct decision.
- Avoid duplicating existing work.
- Respect Change Only Law and No AI Slope.
- Produce the specified output format.
- Update project state and handoff records.
- Stop and request approval when a gate requires it.
- Report what it could not verify.

## 5.3 Mandatory project documents

| Document | Purpose |
|---|---|
| `00-project-intake.md` | Original request and selected mode |
| `01-problem-brief.md` | Problem, users, outcome and evidence |
| `02-validation-report.md` | Validation, assumptions and decision |
| `03-project-profile.yaml` | Machine-readable project facts and constraints |
| `04-prd.md` | Approved product requirements |
| `05-feature-catalogue.md` | Features, priority, status and dependencies |
| `06-acceptance-criteria.md` | Testable acceptance conditions |
| `07-ux-specification.md` | Journeys, IA, flows, states and responsive behavior |
| `08-design-system.md` | Tokens, components and visual rules |
| `09-technology-evaluation.md` | Technology options and selection rationale |
| `10-architecture.md` | System boundaries and architecture |
| `11-data-api-contracts.md` | Data, API and integration specifications |
| `12-security-threat-model.md` | Threats, controls and residual risks |
| `13-test-strategy.md` | Test layers, data and quality gates |
| `14-deployment-operations.md` | Environments, deployment, rollback and operations |
| `15-execution-plan.md` | Milestones, task graph and ownership |
| `16-decision-log.md` | Approved and rejected decisions |
| `17-risk-register.md` | Risks, severity, mitigation and owner |
| `18-verification-report.md` | Test evidence and independent verdict |
| `19-release-record.md` | Version, commit, deployment and release status |
| `20-project-state.md` | Current phase, completed work, blockers and next actions |

Documents may be omitted when genuinely irrelevant, but the omission and reason must be recorded. Do not create empty files merely to satisfy a checklist.

---

# 6. UX/UI design workflow and handoff

```text
Approved problem + PRD
        |
        v
User roles and journeys
        |
        v
Information architecture
        |
        v
Task flows + screen inventory
        |
        v
Wireframes / prototypes
        |
        v
Visual design + design tokens
        |
        v
Responsive + interaction states
        |
        v
Accessibility + usability review
        |
        v
Design approval
        |
        v
Developer handoff package
```

The design handoff must include:

- Page/screen inventory and route map.
- User journeys and flow diagrams.
- Responsive behavior and breakpoints.
- Component inventory and variants.
- Design tokens: colors, type, spacing, radii, shadows and motion.
- Interaction states: default, hover, focus, active, loading, empty, error, success, disabled.
- Form validation and error messages.
- Navigation and permissions by role.
- Accessibility requirements.
- Asset inventory and licenses.
- Prototype links or exported assets where available.
- Design-to-requirement traceability.
- Known design limitations and unresolved questions.

**Tool selection:** Stitch, Figma or another design tool may be selected after checking current capabilities, export formats, inspectability, collaboration and integration with the chosen coding tool. ChatGPT/Claude or another assistant may help create flows, specifications and design prompts, but the final design must be reviewed against the actual product requirements.

---

# 7. Technology selection and architecture workflow

AISDF must not prescribe one universal stack. It must choose based on product requirements, team skills, platform, scale, budget, data sensitivity, ecosystem maturity and operational burden.

For every candidate technology, record:

- Problem it solves.
- Official documentation and source.
- Current stable version/date checked.
- License and commercial restrictions.
- Maintenance and community health.
- Security history and update process.
- Compatibility with selected stack and deployment target.
- Performance and scalability characteristics.
- Cost model and likely usage costs.
- Vendor lock-in and migration path.
- Team learning/maintenance cost.
- Alternatives considered.
- Reason for selection or rejection.

Architecture must cover applicable concerns:

- Client, application/API and background processing boundaries.
- Authentication, authorization and tenant isolation.
- Data storage, migrations, backup and recovery.
- Caching and rate limiting.
- Queues and asynchronous jobs.
- Network boundaries and secrets.
- Logging, metrics and tracing.
- Horizontal/vertical scaling strategy.
- Load balancing only when multiple instances or traffic architecture require it.
- CDN, WAF and edge controls where justified.
- Failure modes, timeouts, retries, idempotency and circuit breakers.
- Cost and capacity estimates.

**No AI Slope:** A load balancer, microservices, Kubernetes, message broker or multi-region deployment is not automatically required. The architecture must justify each component against a real requirement or risk. For a small application, a simpler deployment may be safer and cheaper.

---

# 8. Coding IDE / agent execution protocol

## 8.1 Tool capability check

Before assigning work, create a capability profile for the selected tool:

- Can it read the whole repository or selected files?
- Can it edit files?
- Can it run shell commands?
- Can it run tests and inspect results?
- Can it access the network?
- Can it use Git branches and commits?
- Can it open pull requests?
- Can it access design artifacts?
- Can it use approved MCP/API integrations?
- Can it deploy?
- What permissions and sandbox limits apply?
- What evidence can it return?

Do not infer capabilities from product marketing or tool name. Verify against current official documentation and a safe test.

## 8.2 Execution stages

1. Preflight: inspect branch, clean/dirty worktree, project instructions and baseline.
2. Plan: identify task, dependencies, affected files and acceptance criteria.
3. Branch: create task/feature branch from the approved base.
4. Implement: smallest coherent change; do not silently expand scope.
5. Test: run targeted tests, then relevant regression checks.
6. Review: inspect diff, secrets, dependencies, security and accessibility impacts.
7. Commit: create meaningful, traceable commit(s).
8. Handoff: attach evidence, changed files, unresolved issues and next action.
9. PR: open pull request when the repository workflow requires review.
10. Merge: only after required checks and approvals.
11. Release: tag/version and deploy through approved pipeline.
12. Verify: smoke tests and production health checks.

## 8.3 Git branching model

Use a simple model by default:

- `main`: protected, releasable baseline.
- `feature/<ticket-or-task>-<short-name>`: feature work.
- `fix/<ticket-or-task>-<short-name>`: bug fixes.
- `hotfix/<ticket-or-task>-<short-name>`: urgent production fixes.
- `docs/<short-name>`: documentation-only changes.
- `chore/<short-name>`: maintenance.

Rules:

- Never force-push or rewrite shared history without explicit authorization.
- Never commit secrets, `.env` files, private keys or credentials.
- Keep commits small and descriptive.
- Link commits and PRs to task IDs.
- Require CI checks before merge.
- Require human review for sensitive, destructive, security-critical or production-impacting changes.
- Preserve branch protection and repository rules.
- Use worktrees or separate branches for parallel agents; never allow uncontrolled simultaneous edits to the same files.
- Delete merged branches according to repository policy, retaining history through Git commits and PR records.

Suggested commit format: `type(scope): concise change [TASK-ID]`.

## 8.4 GitHub automation

The framework may define GitHub Actions templates for:

- Lint and formatting.
- Type checking and builds.
- Unit, integration and end-to-end tests.
- Dependency and secret scanning.
- Static analysis and license checks.
- Artifact creation and provenance.
- Preview deployment.
- Release tagging and changelog generation.
- Production deployment after the configured approval gate.

The framework must not store provider credentials in source code. Use GitHub environments, scoped secrets, OIDC where supported, least-privilege tokens and protected deployment environments.

**Auto-push policy:** An agent may push to its authorized feature branch if the user/repository policy explicitly grants that permission. It must not push directly to protected `main` or deploy to production merely because a master prompt says so. Pull requests, required checks and approvals are the safe default.

---

# 9. Testing, security, usability and performance gates

“High testing” means a risk-based test strategy, not blindly maximizing test count.

## 9.1 Test layers

- Static analysis, formatting and type checks.
- Unit tests.
- Component tests.
- Integration tests.
- API contract tests.
- Database and migration tests.
- End-to-end user journey tests.
- Regression tests.
- Accessibility tests.
- Cross-browser/device tests where applicable.
- Security tests and dependency scanning.
- Performance/load/stress/soak tests where justified.
- Backup/restore and recovery tests for critical systems.
- Production smoke tests and synthetic checks.

## 9.2 Security gates

At minimum, evaluate:

- Authentication and authorization.
- Role and tenant isolation.
- Input validation and output encoding.
- Injection, XSS, CSRF and SSRF risks where applicable.
- Secrets and credential handling.
- Dependency and supply-chain risks.
- Secure headers, TLS and cookie settings.
- Rate limits and abuse controls.
- File upload and storage controls.
- Logging without leaking sensitive data.
- Backup encryption, retention and access.
- Threat model and residual risks.

Security findings must be prioritized by severity and exploitability. Critical/high findings block release unless an accountable owner explicitly accepts a documented exception under the project's policy.

## 9.3 Performance and load

Define realistic workload assumptions first:

- Expected users and concurrent sessions.
- Request mix and peak traffic.
- Data size and growth.
- Latency targets and percentiles.
- Error-rate target.
- Resource/cost ceiling.

Run baseline, load, stress and soak tests as appropriate. Test bottlenecks in database, API, queue, cache and network. A load balancer is not proof of scalability; it must be paired with statelessness or session strategy, health checks, capacity planning and failure testing.

## 9.4 UX and accessibility

Test complete user tasks, not just visual similarity:

- Can target users complete core journeys?
- Are labels, navigation and feedback understandable?
- Are empty/loading/error/success states correct?
- Is keyboard navigation usable?
- Are focus and contrast acceptable?
- Are responsive layouts functional?
- Are destructive actions clear and recoverable?
- Are permissions and privacy understandable?

## 9.5 Honest verification verdict

Every criterion must be marked one of:

- `PASS_VERIFIED` — evidence exists and the check passed.
- `FAIL` — check ran and failed.
- `NOT_RUN` — check was not executed.
- `BLOCKED` — unable to execute due to a named blocker.
- `NOT_APPLICABLE` — reason recorded.
- `WAIVED` — accountable approver, reason, scope and expiry recorded.

Never label a feature “complete” only because code was generated or an AI agent said it was complete.

---

# 10. Deployment automation and environment configuration

## 10.1 Environment model

Define environments as required by the project, commonly:

- Local development.
- Automated test/CI.
- Preview or staging.
- Production.

Configuration must be externalized. Use environment variables or the hosting platform's secret/configuration manager. Provide `.env.example` with variable names and safe descriptions only—never real credentials.

Each variable should have:

- Name.
- Purpose.
- Required/optional.
- Environment(s).
- Secret/non-secret classification.
- Validation rule.
- Owner/source.
- Rotation guidance.

No hardcoded credentials, hostnames, tokens, private URLs or environment-specific values in application source. Infrastructure configuration may be version-controlled as code, but secrets must remain in a secret manager.

## 10.2 Deployment pipeline

```text
Approved PR
   |
   v
CI: lint + typecheck + build
   |
   v
Unit + integration + contract tests
   |
   v
Security + dependency + secret checks
   |
   v
Preview/staging deployment
   |
   v
E2E + smoke + performance checks
   |
   v
Release readiness gate
   |
   v
Approval (if required by risk/policy)
   |
   v
Production deployment
   |
   v
Health checks + smoke tests
   |
   +---- failed ---> rollback / traffic stop / incident workflow
   |
   v
Release evidence + monitoring
```

Deployment automation is provider-specific and must be represented through configurable templates/adapters. AISDF must not hardcode Vercel, AWS, Azure, GCP, Cloudflare, Render or another provider as universally required.

## 10.3 Production safeguards

- Separate preview/staging and production credentials.
- Least-privilege deployment identity.
- Protected production environment.
- Database migration plan and rollback/forward-fix strategy.
- Backup and restore plan.
- Health checks and readiness/liveness checks where applicable.
- Progressive rollout/canary/blue-green only when justified.
- Rollback trigger and accountable owner.
- Post-deployment smoke tests.
- Monitoring and incident contact/runbook.

---

# 11. Complete handoff protocol

A handoff is a formal transfer of responsibility and sufficient context—not merely “continue from here.”

## 11.1 Handoff types

- User → AISDF intake.
- AI assistant → project documents.
- Analysis engine → product/requirements engine.
- Product → UX/UI design.
- Design tool → coding IDE.
- Technology/architecture → implementation agent.
- Agent → agent.
- Agent → human reviewer.
- Coding agent → test/verification agent.
- Verification → release manager/approver.
- CI/CD → deployment environment.
- Deployment → operations/maintenance.
- Session → next session.
- Existing project → transformation team/agent.

## 11.2 Mandatory handoff package

Every handoff must contain:

1. `handoff_id` and `project_id`.
2. Sender identity/role and intended receiver role/tool.
3. Timestamp and schema/framework version.
4. Current project mode, lifecycle phase and task state.
5. Objective and explicit scope.
6. Canonical source-of-truth document paths and revision/commit.
7. Relevant requirements and acceptance criteria IDs.
8. Approved decisions and applicable ADRs.
9. Assumptions, unknowns and unresolved questions.
10. Relevant AKIS knowledge references with source/version/date.
11. Relevant AFIAE tool/service evaluation and approval state.
12. Dependencies, blockers and prerequisite task IDs.
13. Files/modules allowed to change and files/modules prohibited.
14. Tool permissions, network access and execution boundaries.
15. Work completed and work not completed.
16. Files changed and commit/branch references.
17. Tests run, exact commands, results and environment.
18. Verification evidence references.
19. Risks, defects and residual concerns.
20. Required next actions and expected outputs.
21. Approval state and approvals still required.
22. Handoff status and receiver acknowledgement.

## 11.3 Handoff state machine

```text
DRAFT
  |
  v
SUBMITTED
  |
  +----> REJECTED (reason + correction)
  |
  v
ACKNOWLEDGED
  |
  +----> NEEDS_CLARIFICATION
  |
  v
ACCEPTED
  |
  v
IN_PROGRESS
  |
  +----> BLOCKED ----> ESCALATED / RESUMED
  |
  +----> FAILED -----> RETRY / REASSIGN / CANCEL
  |
  v
READY_FOR_REVIEW
  |
  +----> CHANGES_REQUESTED ----> IN_PROGRESS
  |
  v
VERIFIED
  |
  v
CLOSED
```

A receiver must acknowledge the package and confirm that required inputs are accessible before execution. A rejected or incomplete handoff must not be treated as accepted work.

## 11.4 Handoff acceptance checklist

- Correct project and baseline?
- Correct task and scope?
- Source files and documents accessible?
- Requirements and acceptance criteria clear?
- Dependencies available?
- Permissions sufficient but not excessive?
- No unresolved blocker hidden?
- Previous test/evidence status clear?
- Expected output and definition of done explicit?
- Required approvals present?

---

# 12. Orchestration architecture

## 12.1 Framework control plane vs execution plane

**Framework control plane:** Markdown policies, schemas, workflow definitions, registries, task contracts, approval rules, state records and adapter specifications.

**Execution plane:** The user's selected assistant, design tool, IDE/CLI agent, Git provider, CI runner, hosting platform and approved integrations.

AISDF repository does not itself run a hosted orchestrator. A compatible AI tool or future separately approved runtime interprets the framework and performs authorized actions.

## 12.2 Orchestration patterns

| Pattern | Strength | Risk / tradeoff | Use |
|---|---|---|---|
| Single coordinator | Clear ownership and simpler state | Coordinator bottleneck/context overload | Small/medium projects |
| Hierarchical | Delegates by domain and phase | More handoffs and coordination | Larger projects |
| Peer-to-peer | Flexible collaboration | Harder conflict resolution and audit | Narrow expert collaboration |
| Sequential workflow | Predictable gates | Slower for independent work | Requirements, release |
| Parallel task graph | Faster independent tasks | Merge/context conflicts | Independent modules/tests |
| Event-driven | Loose coupling and traceability | More infrastructure/complexity | Mature systems or runtime |
| Shared workspace | Simple setup | Concurrent edit conflicts | One agent or small tasks |
| Isolated branches/worktrees | Safer parallel work | Merge overhead | Multi-agent code work |

Default: sequential stage gates with limited parallelism for independent tasks. Add complexity only when measured needs justify it.

## 12.3 Task state model

`DRAFT → READY → ASSIGNED → IN_PROGRESS → BLOCKED/REVIEW → VERIFIED → DONE`

Additional terminal states: `CANCELLED`, `REJECTED`, `WAIVED` (with approval). State changes must record actor, timestamp, reason and evidence.

---

# 13. Data contracts and schemas

The repository should include versioned JSON Schemas or equivalent contracts for:

- `project-profile.schema.json`
- `intake-record.schema.json`
- `problem-brief.schema.json`
- `requirement.schema.json`
- `assumption.schema.json`
- `decision-record.schema.json`
- `risk.schema.json`
- `feature.schema.json`
- `design-handoff.schema.json`
- `technology-evaluation.schema.json`
- `tool-capability-profile.schema.json`
- `task.schema.json`
- `agent-role.schema.json`
- `agent-handoff.schema.json`
- `workflow.schema.json`
- `test-case.schema.json`
- `verification-evidence.schema.json`
- `git-change-record.schema.json`
- `deployment-record.schema.json`
- `release-record.schema.json`
- `project-state.schema.json`
- `audit-event.schema.json`

## 13.1 Example handoff contract

```json
{
  "schema_version": "1.0.0",
  "handoff_id": "HO-0001",
  "project_id": "PROJECT-001",
  "task_id": "TASK-014",
  "handoff_type": "design_to_implementation",
  "status": "SUBMITTED",
  "created_at": "2026-01-01T00:00:00Z",
  "sender": {
    "role": "ux_designer",
    "tool": "design_tool"
  },
  "receiver": {
    "role": "frontend_implementer",
    "tool": "coding_agent"
  },
  "baseline": {
    "document_revision": "git-sha-or-version",
    "branch": "feature/TASK-014-screen-implementation"
  },
  "objective": "Implement the approved screen and interactions.",
  "scope": {
    "in_scope": ["Approved screen and specified states"],
    "out_of_scope": ["Unapproved redesign", "Unrelated refactoring"],
    "allowed_paths": ["src/features/example/**"],
    "restricted_paths": [".github/workflows/**", "infra/production/**"]
  },
  "references": {
    "requirements": ["REQ-012"],
    "acceptance_criteria": ["AC-012-01", "AC-012-02"],
    "design_documents": ["docs/07-ux-specification.md"],
    "decisions": ["ADR-004"]
  },
  "assumptions": [],
  "open_questions": [],
  "dependencies": ["TASK-010"],
  "permissions": {
    "read_repository": true,
    "edit_allowed_paths": true,
    "run_tests": true,
    "network_access": false,
    "push_feature_branch": false,
    "merge": false,
    "deploy_production": false
  },
  "expected_outputs": [
    "Implemented screen",
    "Tests",
    "Changed-file summary",
    "Verification evidence"
  ],
  "evidence": [],
  "blockers": [],
  "next_action": "Receiver acknowledges and validates inputs.",
  "approval": {
    "required": false,
    "status": "NOT_REQUIRED",
    "approver": null
  }
}
```

The timestamp and sample values are illustrative. Real project records must use actual values and valid schema constraints.

---

# 14. Repository structure additions

Retain the existing 31-domain structure and add explicit engine and handoff navigation. Do not create duplicate knowledge silos.

```text
AISDF/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── GOVERNANCE.md
├── CHANGELOG.md
├── VERSION
├── 00-GOVERNANCE/
├── 01-METHODOLOGY/
├── 02-PROJECT-INTELLIGENCE/
├── 03-REQUIREMENTS-ENGINEERING/
├── 04-PRODUCT-ENGINEERING/
├── 05-UX-UI-ENGINEERING/
├── 06-TECHNOLOGY-INTELLIGENCE/
├── 07-ENGINEERING-KNOWLEDGE/
├── 08-SOFTWARE-ARCHITECTURE/
├── 09-PLATFORM-ENGINEERING/
├── 10-AI-AND-MODEL-ENGINEERING/
├── 11-AGENT-ENGINEERING/
├── 12-ORCHESTRATION-AND-CONTEXT/
├── 13-HARNESS-AND-EXECUTION/
├── 14-SECURITY-AND-PRIVACY/
├── 15-DATA-AND-DATABASE-ENGINEERING/
├── 16-API-AND-INTEGRATION-ENGINEERING/
├── 17-TESTING-AND-VERIFICATION/
├── 18-DEVOPS-AND-CLOUD-ENGINEERING/
├── 19-DEPLOYMENT-AND-OPERATIONS/
├── 20-RELIABILITY-AND-OBSERVABILITY/
├── 21-DISTRIBUTED-SYSTEMS-AND-SCALABILITY/
├── 22-COST-AND-RESOURCE-GOVERNANCE/
├── 23-LEGAL-AND-COMPLIANCE/
├── 24-PRODUCT-ANALYTICS-AND-SUPPORT/
├── 25-FRAMEWORK-MAINTENANCE/
├── 26-DISTRIBUTION-AND-EXTENSIONS/
├── 27-STANDARDS-AND-COMPATIBILITY/
├── 28-TEMPLATES-AND-EXAMPLES/
├── 29-BENCHMARKS-AND-EVALUATION/
├── 30-AGENT-RULES-AND-VERIFICATION/
├── engines/
│   ├── ENGINE-CATALOGUE.md
│   ├── engine-registry.yaml
│   └── engine-spec-template.md
├── modes/
│   ├── MODE-1-PROBLEM-DISCOVERY.md
│   ├── MODE-2-NEW-PROJECT.md
│   └── MODE-3-EXISTING-PROJECT.md
├── prompts/
├── workflows/
├── schemas/
├── registries/
├── templates/
├── examples/
├── adapters/
│   ├── assistant-tools/
│   ├── design-tools/
│   ├── coding-tools/
│   ├── git-providers/
│   ├── ci-cd/
│   └── deployment-providers/
├── tests/
├── tools/
└── .github/
    ├── ISSUE_TEMPLATE/
    ├── workflows/
    ├── PULL_REQUEST_TEMPLATE.md
    └── CODEOWNERS
```

Adapters are documentation/contracts first. A tool-specific adapter is marked `verified`, `partial`, `experimental` or `not-verified`, with version/date/source/evidence. Do not claim compatibility merely because a prompt can be pasted into a tool.

---

# 15. Failure handling and recovery

Every workflow must specify recovery behavior.

| Failure | Required response |
|---|---|
| Ambiguous requirement | Pause affected task; ask a focused question or record permitted assumption |
| Conflicting documents | Identify source precedence; request owner decision |
| Missing tool capability | Use an approved fallback or mark blocked |
| Tool/API unavailable | Retry with bounded policy; then stop/escalate |
| Test failure | Preserve logs, isolate cause, repair within scope, rerun |
| Unexpected code changes | Stop, inspect diff, revert only with safe authorization |
| Merge conflict | Reconcile against current baseline; never overwrite blindly |
| Security finding | Contain, classify, remediate or block release |
| Deployment failure | Stop rollout, collect evidence, rollback/forward-fix per plan |
| Context/session loss | Reconstruct from canonical project state and handoff package |
| Agent disagreement | Compare evidence and requirements; escalate unresolved decisions |
| Cost/time budget exceeded | Stop at safe boundary and report remaining work |

Retries must be bounded and idempotent where possible. Repeatedly retrying a failing operation is not a recovery strategy.

---

# 16. Audit, observability and project history

Record meaningful events:

- Intake and mode selection.
- Document creation/revision.
- Assumption and decision changes.
- Approval and rejection.
- Task assignment/state changes.
- Agent/tool invocation where available.
- Git branch, commit and PR.
- Test run and result.
- Security finding and disposition.
- Deployment and rollback.
- Release and closeout.

Every event should identify actor/tool, action, timestamp, project/task, affected artifact, result and evidence reference. Avoid logging secrets or unnecessary personal data.

Git history is the canonical source for code changes. Project decision logs and release records provide the engineering rationale and evidence links. Do not confuse chat transcript history with a reliable project audit trail.

---

# 17. Framework validation and benchmark strategy

AISDF itself must be tested as a framework.

## 17.1 Repository validation

Automate checks for:

- Required root and domain documentation.
- Unique document/engine/workflow IDs.
- Valid YAML/JSON and schema conformance.
- Required metadata and status.
- Internal links.
- Prompt references to existing documents.
- Workflow input/output/gate completeness.
- Handoff schema examples.
- Registry consistency.
- Deprecated or stale tool adapters.

## 17.2 End-to-end benchmark projects

Use representative sample projects:

1. Small CRUD web application.
2. Mobile-first PWA.
3. Existing project bug fix with regression risk.
4. Existing project redesign with preservation constraints.
5. API-backed SaaS with authentication and tenant isolation.
6. Data-intensive project with migrations.
7. AI-integrated application with prompt-injection and data-leakage risks.

Measure:

- Requirement extraction accuracy.
- Ambiguity detection.
- Unsupported assumption rate.
- Traceability coverage.
- Scope drift.
- Defect escape rate.
- Test quality and coverage relevance.
- Security findings missed.
- Usability issues missed.
- Deployment reproducibility.
- Handoff completeness.
- Human approval compliance.
- Cost and time.
- Truthfulness of completion reports.

Do not advertise “zero bugs” or “fully autonomous” without reproducible evidence and clear test boundaries.

---

# 18. V1 implementation sequence

Build the framework repository in deliberate increments:

| Release slice | Deliverable | Exit condition |
|---|---|---|
| R0 | Scope, governance, principles and glossary | Boundaries and laws approved |
| R1 | Three intake modes | Each mode has inputs, steps, outputs and gates |
| R2 | Engine catalogue and engine spec template | Every engine has contract and owner |
| R3 | Project document templates and schemas | Sample project package validates |
| R4 | Product/requirements and feature analysis | Requirements trace to acceptance criteria |
| R5 | UX/UI and design handoff | Design package is implementation-ready |
| R6 | Technology and architecture intelligence | ADR and technology evaluation are reproducible |
| R7 | AKIS and AFIAE | Knowledge/tool provenance and approval defined |
| R8 | Agent, task and handoff orchestration | Cross-agent/session handoff test passes |
| R9 | Git and coding-tool adapters | Safe branch workflow demonstrated |
| R10 | Test, security, performance and UX verification | Quality gates and evidence work |
| R11 | CI/CD and deployment templates | Non-production pipeline works safely |
| R12 | End-to-end benchmark projects | At least one complete project passes defined gates |
| R13 | Documentation, release and maintenance | Public release checklist passes |

Recommended first proof: use one small, bounded application and run it through all three relevant phases (intake, design/specification, implementation and verification). Demonstrate one design handoff, one coding-tool handoff, one feature branch/PR, automated checks and a staging deployment. Do not claim full capability before this works.

---

# 19. Important architectural decisions and tradeoffs

1. **Three modes are entry paths, not three separate frameworks.** They converge on one shared project baseline and lifecycle.
2. **Engines are capability modules, not automatically microservices or agents.** Avoid turning every named engine into an autonomous AI agent.
3. **One master prompt is an entry point, not the entire framework.** It must reference modular rules, templates and workflows.
4. **AI assistant, design tool and coding IDE are different execution roles.** Use handoff contracts between them.
5. **Git branch automation is not unrestricted direct push.** Feature-branch push may be allowed; protected branch merge and production deployment need policy gates.
6. **Automation is conditional on verified tool capability and authorization.** A prompt cannot grant missing permissions.
7. **Deployment must be provider-neutral.** Provider adapters contain provider-specific instructions and configuration.
8. **Load balancing and advanced infrastructure are conditional.** Use only when workload and architecture justify them.
9. **Testing is evidence-based.** A green test suite does not prove absence of defects.
10. **No AI Slope applies to the framework itself.** Do not add engines, agents, infrastructure or tools without a demonstrated requirement.

---

# 20. Final verdict

The requested AISDF direction is coherent when treated as a **tool-independent software engineering framework with three intake modes, a documented engine catalogue, standardized project records, design/technology handoffs, controlled AI coding execution, Git governance, evidence-based verification and configurable deployment workflows**.

The existing v1.0 and v1.1 blueprints already establish the repository-only scope, Path 0/Path A/Path B methodology, Project X-Ray, AKIS, AFIAE, 31 knowledge domains, schemas, workflows, agents, verification and governance. This v1.2 proposal makes the user's requested three-mode intake, explicit engine catalogue, design-to-code handoff, GitHub automation boundaries, testing gates and deployment lifecycle more concrete.

**What is not yet true:** No GitHub repository has been created by this document; no adapters have been proven; no coding tool has been tested end-to-end; no application has been built or deployed through AISDF. These remain implementation and validation work.

**Release promise:** AISDF can guide compatible, authorized tools through a disciplined end-to-end process and report evidence honestly. It must never promise error-free software, universal tool compatibility, zero security risk or unattended production deployment.


---

# 21. Knowledge freshness, version intelligence and alternative evaluation

**Requirement:** AISDF must actively prevent outdated, unsupported or silently assumed engineering guidance from entering project decisions. Every time-sensitive recommendation must be traceable to a version, source and verification date.

## 21.1 Knowledge classification

Every meaningful statement used in analysis, design or execution must be classified as one of:

| Classification | Meaning | Required treatment |
|---|---|---|
| `USER_PROVIDED` | Explicitly supplied by the user or project document | Preserve meaning; cite document/section |
| `REPOSITORY_OBSERVED` | Directly observed in the current repository | Cite path, line, commit or command evidence |
| `OFFICIALLY_VERIFIED` | Checked against an authoritative current source | Record source, version and checked date |
| `INDEPENDENTLY_CORROBORATED` | Supported by more than one credible source | Record all material sources |
| `MODEL_KNOWLEDGE` | General model knowledge not freshly checked | Mark as unverified where freshness matters |
| `INFERENCE` | Reasoned conclusion derived from evidence | Show the basis and confidence |
| `ASSUMPTION` | Temporary premise used to proceed | Record owner, impact and validation plan |
| `RECOMMENDATION` | Suggested choice, not an established fact | Give rationale, alternatives and tradeoffs |
| `UNKNOWN` | Not established | Do not present as fact |

Never convert a recommendation, assumption or inference into a verified fact by repeating it in later documents. Preserve provenance as information moves through handoffs.

## 21.2 Source hierarchy

Use sources in this order where applicable:

1. Official product documentation, release notes, security advisories and API references.
2. Official standards bodies, specifications and maintainers' repositories.
3. Official vendor engineering/security documentation.
4. Reputable independent technical research and established engineering publications.
5. Community discussions and issue reports as supporting signals, not sole authority.
6. Model knowledge only for stable background context or clearly marked preliminary guidance.

A search result snippet is not sufficient evidence for a consequential technical decision. Open and inspect the source. For security, licensing, pricing, version support and breaking changes, prefer the primary source.

## 21.3 Freshness metadata

Every time-sensitive knowledge entry, technology recommendation and tool adapter must include:

- `source_url` or canonical source reference.
- `source_owner`.
- `source_type`.
- `product_or_standard`.
- `version_or_release`.
- `published_or_updated_at` when available.
- `verified_at`.
- `verified_by` or verification method.
- `support_status`: current, maintenance, deprecated, end-of-life, unknown.
- `confidence`.
- `next_review_due`.
- `known_limitations`.
- `supersedes` and `superseded_by`, where applicable.

Do not invent a version or publication date. Use `unknown` and explain what could not be confirmed.

## 21.4 Freshness classes and review policy

Suggested default review intervals; shorten them for high-risk projects:

| Knowledge class | Examples | Default review |
|---|---|---|
| Highly volatile | AI models, AI IDE features, pricing, SaaS plans, API limits | At each project selection/use; recheck before implementation |
| Fast changing | Framework releases, SDKs, cloud service features, package versions | At project start and before major upgrades/releases |
| Moderately changing | Security guidance, deployment patterns, platform support matrices | At project start and at release/security review |
| Slow changing | Core algorithms, architecture principles, stable protocol concepts | Review on scheduled maintenance or when a relevant change is reported |
| Stable historical | Historical background and foundational concepts | Review when challenged or when new evidence appears |

These intervals are policy defaults, not guarantees that a source remains current. A `next_review_due` date does not replace checking release notes before a consequential upgrade.

## 21.5 Outdated knowledge detection

Before using a knowledge item, the responsible engine must check:

1. Is the source authoritative for this claim?
2. Is the version relevant to the project's actual version?
3. Is the source still maintained?
4. Has a newer release, migration guide, deprecation notice or security advisory appeared?
5. Does the guidance apply to the user's operating system, language, runtime, deployment provider and selected tool?
6. Are there known breaking changes or compatibility constraints?
7. Is the recommendation still supported by the official source?

If a source is stale, superseded, unavailable or contradictory:

- Mark it `STALE`, `SUPERSEDED`, `UNVERIFIED` or `CONFLICTED`.
- Do not silently reuse it as current guidance.
- Search for an authoritative replacement when the task requires current information.
- Record the impact on existing project decisions.
- Request a decision if the replacement changes scope, cost, security, architecture or migration risk.

## 21.6 Version and compatibility matrix

For every selected technology stack, record a compatibility matrix where relevant:

| Layer | Selected item | Version/range | Support status | Compatibility evidence |
|---|---|---|---|---|
| Language/runtime | To be selected | Exact or supported range | Verified/unknown | Official source |
| Framework | To be selected | Exact or supported range | Verified/unknown | Official source |
| Package manager | To be selected | Version | Verified/unknown | Official source |
| Database | To be selected | Version/service tier | Verified/unknown | Official source |
| ORM/driver | To be selected | Version | Verified/unknown | Compatibility docs |
| Hosting/runtime | To be selected | Runtime/build limits | Verified/unknown | Provider docs |
| AI model/tool | To be selected | Model/tool version or plan | Verified/unknown | Official source |
| External API | To be selected | API version | Verified/unknown | API docs |

Do not automatically choose the newest release. Choose a supported version compatible with the project, dependencies and deployment environment. Pin versions or define controlled ranges according to ecosystem best practices; document upgrade policy.

## 21.7 Alternatives requirement

For consequential choices, AISDF must identify and compare reasonable alternatives before recommending one. This includes, where applicable:

- AI assistant/model and coding IDE.
- Design tool and design-to-code workflow.
- Programming language and framework.
- Database, ORM and data storage.
- Hosting/cloud/deployment provider.
- Authentication and identity provider.
- API, SDK, library, MCP server or plugin.
- Queue, cache, search and storage service.
- Architecture and scaling pattern.
- Testing and observability tools.
- Git branching and release strategy.

An alternatives record must include:

1. The requirement being solved.
2. The selected option and why it fits.
3. At least one credible alternative when one exists.
4. Benefits and disadvantages.
5. Compatibility and maturity.
6. Security, privacy and license implications.
7. Cost and operational burden.
8. Lock-in and migration effort.
9. Team skill/learning cost.
10. Evidence sources and verification date.
11. Rejected options and rejection reasons.
12. Conditions that would trigger reconsideration.

**Do not manufacture alternatives.** If no meaningful alternative exists, or the user mandates a technology, record that constraint and explain the resulting tradeoff. Do not waste effort comparing irrelevant options.

## 21.8 Tool capability freshness

Tool adapters for ChatGPT, Claude, Gemini, Stitch, Figma, coding IDEs, Git providers, CI/CD systems and deployment providers must not be treated as permanently compatible.

Each adapter must state:

- Tool name and official product URL.
- Supported workflow capabilities.
- Required plan/account/permissions if known.
- Input and output formats.
- Repository, terminal, browser, network and Git access capability.
- Integration/MCP/API support where verified.
- Known restrictions and unsupported operations.
- Last verified date and tested version/plan.
- Verification method and evidence.
- Compatibility status: `VERIFIED`, `PARTIAL`, `EXPERIMENTAL`, `NOT_VERIFIED`, `DEPRECATED`.

Recheck the adapter when a workflow depends on a capability, and before public claims of compatibility. If not checked, say so.

---

# 22. Progressive disclosure: essential instructions first, advanced detail when needed

AISDF must provide enough instruction to complete the current task correctly without overwhelming every user or AI context with the entire knowledge base.

## 22.1 Three information levels

| Level | Content | When to provide |
|---|---|---|
| Level 1 — Essential | Required rules, immediate steps, inputs, outputs, decisions and completion checks | Always, before execution |
| Level 2 — Practical detail | Examples, implementation guidance, common errors, tradeoffs and relevant alternatives | When needed to perform the task or resolve a decision |
| Level 3 — Advanced reference | Deep internals, edge cases, scaling, specialist patterns, standards mapping and extended alternatives | On user request or when risk/complexity makes it necessary |

Do not hide safety-critical information in advanced material. Security boundaries, permissions, approval requirements, destructive-action warnings and required verification belong in Level 1 whenever relevant.

## 22.2 Advanced-detail triggers

The responsible engine should load advanced guidance when one or more conditions apply:

- The user explicitly asks for advanced or comprehensive detail.
- The task is security-, privacy-, safety- or compliance-sensitive.
- The architecture has multiple services, tenants, regions or critical dependencies.
- A migration, data-loss or production-impact risk exists.
- Performance or scale targets require specialist design.
- The selected technology has important compatibility or version constraints.
- A tool limitation or failure requires a fallback.
- The basic workflow cannot satisfy acceptance criteria.
- A decision has high cost, lock-in or difficult reversibility.

Do not load unrelated advanced material merely because it exists.

## 22.3 Context and document retrieval rules

- Start from the master prompt and selected mode.
- Load the core laws and current workflow.
- Retrieve only the engine specifications needed for the current phase.
- Retrieve relevant standards and knowledge with freshness metadata.
- Load alternatives only for decisions that actually need comparison.
- Keep references to the canonical documents instead of copying large sections into every prompt.
- Preserve enough context in the handoff to continue without relying on chat memory.

The framework's goal is not to minimize context at all costs. It is to provide the **minimum sufficient, accurate context** for safe and correct work.

---

# 23. Full-completion rule: finish the assigned work unit before moving on

**Requirement:** Once an engine, workflow, phase or task is started, it must be completed to its defined exit criteria before the framework marks it complete or begins dependent work.

This does not mean an AI tool should continue blindly when blocked. It means it must not silently abandon, partially complete or mislabel work.

## 23.1 Work-unit contract

Before starting a work unit, define:

- Unique work-unit ID.
- Objective and scope.
- Required inputs and baseline.
- Required activities and sequence.
- Expected outputs and file locations.
- Acceptance criteria.
- Verification method.
- Dependencies.
- Permission and approval boundaries.
- Time/token/tool budget if applicable.
- Stop conditions and escalation route.

## 23.2 Completion sequence

For each work unit:

1. Read its instructions and applicable rules.
2. Confirm required inputs and access.
3. Confirm dependencies and approval state.
4. Execute every required activity.
5. Create or update every required output.
6. Validate output structure and completeness.
7. Run the specified checks.
8. Record evidence and unresolved issues.
9. Update project state and traceability.
10. Prepare and submit the handoff.
11. Obtain receiver acknowledgement where the workflow requires it.
12. Mark the work unit complete only after exit criteria pass.

## 23.3 No silent partial completion

A work unit cannot be marked `DONE` when:

- Required outputs are missing.
- Required checks were not run.
- Acceptance criteria remain unverified.
- A blocking question is unresolved.
- A required approval is absent.
- Evidence is missing.
- The next owner has not received a required handoff.

Use explicit states:

- `NOT_STARTED`
- `IN_PROGRESS`
- `BLOCKED`
- `NEEDS_APPROVAL`
- `FAILED`
- `PARTIALLY_COMPLETED`
- `READY_FOR_REVIEW`
- `VERIFIED`
- `DONE`
- `CANCELLED`
- `WAIVED`

`PARTIALLY_COMPLETED` is an honest checkpoint, not a success state. A `WAIVED` item requires an authorized owner, reason, impact and expiry/review condition.

## 23.4 When the workflow may pause

Pause only when one of these applies:

- A necessary user decision is missing.
- An approval gate is reached.
- Required access, source, tool capability or dependency is unavailable.
- A safety/security issue requires containment.
- The execution budget or environment limit is reached.
- A failure makes continued execution unsafe or wasteful.

When pausing, the agent must produce a checkpoint containing:

- Completed steps.
- Incomplete steps.
- Exact current state.
- Outputs already created.
- Commands/actions already performed.
- Test results and logs.
- Blocker and why it prevents progress.
- What is needed to resume.
- Next exact action.
- Whether any changes are uncommitted or unpushed.

Do not restart from the beginning if the canonical checkpoint proves which steps are complete. Resume from the first incomplete step after revalidating the baseline.

## 23.5 Sequential and parallel execution

- A dependent phase cannot start until its prerequisites meet their exit criteria.
- Independent tasks may run in parallel only when dependencies, file ownership and integration points are explicit.
- Parallel agents must not claim the same exclusive file ownership without a conflict-resolution plan.
- A parent task is complete only when all required child tasks are complete or explicitly waived.
- Final integration and verification are mandatory after parallel work.

## 23.6 User-facing completion report

Every completed phase or major task must report:

1. What was requested.
2. What was completed.
3. Which artifacts/files changed.
4. Which checks were executed.
5. Results and evidence.
6. What remains incomplete or unverified.
7. Decisions or approvals obtained.
8. Risks and limitations.
9. Next phase or handoff destination.

Never say “fully completed” if any mandatory acceptance criterion is failed, blocked, not run or unverified.

---

# 24. Predefined rulebook and mandatory preflight checks

Rules must be stored in canonical files, versioned, referenced by prompts and validated through workflow checklists. They must not exist only as informal instructions in a conversation.

## 24.1 Core rulebook

| Rule ID | Rule | Mandatory check |
|---|---|---|
| RULE-001 | Source-of-truth | Identify canonical project documents, repository and baseline |
| RULE-002 | Evidence over claims | Every completion claim links to evidence or is marked unverified |
| RULE-003 | Change Only Law | Check scope and unrelated changes before implementation |
| RULE-004 | No AI Slope | Justify every feature, dependency, agent and infrastructure addition |
| RULE-005 | Approval First | Verify approval before material, destructive or production action |
| RULE-006 | Least Privilege | Confirm minimum permissions and no privilege escalation |
| RULE-007 | Freshness & Version | Verify volatile knowledge and record version/date/source |
| RULE-008 | Alternatives | Compare meaningful alternatives for consequential decisions |
| RULE-009 | Provenance | Distinguish user input, observed facts, verified facts, assumptions and inference |
| RULE-010 | Full Completion | Meet work-unit exit criteria before marking complete |
| RULE-011 | No Fake Execution | Never claim a command, test, push or deployment occurred unless it did |
| RULE-012 | Traceability | Link requirements to tasks, changes, tests and evidence |
| RULE-013 | Secure Secrets | Never hardcode or expose credentials |
| RULE-014 | Git Safety | Use approved branches, review and protected-branch rules |
| RULE-015 | Compatibility | Verify selected tools, versions and integration capabilities |
| RULE-016 | Failure Disclosure | Report blockers, failures, waivers and residual risks |
| RULE-017 | Reversibility | Plan rollback/recovery for risky changes |
| RULE-018 | Handoff Completeness | Validate handoff package and receiver acknowledgement |
| RULE-019 | Right-Sized Engineering | Justify architecture and operational complexity |
| RULE-020 | User Intent Preservation | Do not silently change the user's goal, constraints or product direction |

## 24.2 Mandatory preflight checklist

Before any workflow begins, check:

- [ ] Correct project and mode identified.
- [ ] Current phase and work-unit ID identified.
- [ ] Canonical project baseline located.
- [ ] Applicable AISDF rules and workflow version loaded.
- [ ] User-provided requirements preserved.
- [ ] Facts, assumptions, inferences and unknowns separated.
- [ ] Required knowledge freshness checked.
- [ ] Relevant alternatives evaluated or reason for omission recorded.
- [ ] Inputs and dependencies available.
- [ ] Tool capabilities verified for required actions.
- [ ] Permissions are sufficient and least-privileged.
- [ ] Scope and exclusions explicit.
- [ ] Approval requirements identified.
- [ ] Outputs and acceptance criteria explicit.
- [ ] Verification method and evidence requirements defined.
- [ ] Failure and recovery route known.

If a critical preflight item fails, do not begin the affected action. Resolve it, ask for approval, or mark the work blocked.

## 24.3 Phase exit checklist

Before closing any phase:

- [ ] Every mandatory activity completed or explicitly dispositioned.
- [ ] Required documents/artifacts created and validated.
- [ ] Requirements and decisions traceable.
- [ ] Tests/reviews/checks actually executed where required.
- [ ] Evidence stored or linked.
- [ ] Risks and open questions recorded.
- [ ] No unapproved scope expansion.
- [ ] No hidden partial completion.
- [ ] Project state updated.
- [ ] Handoff package complete.
- [ ] Receiver acknowledgement or approval recorded where required.
- [ ] Exit criteria passed, or phase honestly marked blocked/failed/partial.

## 24.4 Rule precedence

When instructions conflict, apply this order:

1. Applicable law, safety and platform/security restrictions.
2. Explicit user-approved project constraints and organizational policy.
3. AISDF mandatory laws and rulebook.
4. Approved project baseline and architecture decisions.
5. Current workflow and engine specification.
6. Tool-specific adapter instructions.
7. Local task instructions.
8. Model assumptions or generic preferences.

A lower-level instruction cannot override a higher-level rule. If two high-priority requirements conflict, stop and request an authorized decision rather than choosing silently.

---

# 25. Additional repository files required by this update

Add these canonical documents:

```text
00-GOVERNANCE/
  AISDF-RULEBOOK.md
  RULE-PRECEDENCE-AND-CONFLICT-RESOLUTION.md
  KNOWLEDGE-FRESHNESS-AND-REVIEW-POLICY.md
  EVIDENCE-AND-PROVENANCE-POLICY.md

06-TECHNOLOGY-INTELLIGENCE/
  VERSION-AND-COMPATIBILITY-MATRIX.md
  ALTERNATIVES-EVALUATION-STANDARD.md
  TECHNOLOGY-SUPPORT-AND-DEPRECATION-POLICY.md

07-ENGINEERING-KNOWLEDGE/
  KNOWLEDGE-METADATA-STANDARD.md
  SOURCE-QUALITY-AND-VERIFICATION.md
  STALE-KNOWLEDGE-REVIEW-WORKFLOW.md

12-ORCHESTRATION-AND-CONTEXT/
  WORK-UNIT-FULL-COMPLETION-PROTOCOL.md
  PAUSE-RESUME-AND-CHECKPOINT-PROTOCOL.md
  HANDOFF-ACKNOWLEDGEMENT-PROTOCOL.md
  PROGRESSIVE-DISCLOSURE-AND-CONTEXT-LOADING.md

27-STANDARDS-AND-COMPATIBILITY/
  TOOL-CAPABILITY-VERIFICATION.md
  ADAPTER-FRESHNESS-REGISTER.md

30-AGENT-RULES-AND-VERIFICATION/
  PRE-FLIGHT-CHECKLIST.md
  PHASE-EXIT-CHECKLIST.md
  NO-FAKE-EXECUTION-RULE.md
  COMPLETION-REPORT-CONTRACT.md

schemas/
  knowledge-entry.schema.json
  source-evidence.schema.json
  alternative-evaluation.schema.json
  tool-capability-profile.schema.json
  work-unit.schema.json
  checkpoint.schema.json
  completion-report.schema.json
  rule-check-result.schema.json
```

These are additions to the existing repository map, not a replacement for its 31 domains.

---

# 26. Updated definition of done for AISDF

AISDF V1 must not be called complete until:

1. The three intake modes are documented, tested and converge on a canonical project baseline.
2. Every published engine has a complete specification: purpose, inputs, outputs, workflow, rules, dependencies, owner, failure handling and exit criteria.
3. Knowledge entries carry provenance, version and freshness metadata.
4. Consequential technology/tool decisions include alternatives or a recorded reason why alternatives are not applicable.
5. Tool adapters distinguish verified, partial, experimental and unverified capabilities.
6. Essential instructions are always loaded; advanced detail is retrieved when requested or triggered by risk/complexity.
7. Work-unit completion, pause/resume and handoff protocols are implemented in prompts/templates/schemas.
8. Rulebook and preflight/exit checks are referenced by all applicable workflows.
9. No fake execution or unsupported compatibility claims appear in documentation.
10. Git branch, PR, CI and deployment examples work in at least one representative test repository.
11. At least one end-to-end sample project has passed documented acceptance and verification gates.
12. Framework CI validates schemas, links, IDs, metadata and registry consistency.
13. Public documentation clearly states limitations, unverified areas and supported versions.

**Updated promise:** AISDF provides version-aware, evidence-based, alternative-conscious and completion-controlled guidance to compatible AI tools. It does not promise that all knowledge is permanently current; it defines how freshness is checked, stale guidance is detected and decisions are revalidated before use.
