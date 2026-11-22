# AISDF — Master Complete Blueprint
## AI Software Development Framework
### From Problem Statement to Production Software

**Document:** Master Complete Functional, Methodology, Engine, Knowledge, Orchestration, Handoff, Verification and Repository Blueprint  
**Master version:** 2.0.0  
**Status:** Consolidated proposed architecture — implementation and compatibility validation remain pending  
**Repository type:** Open-source GitHub framework repository  
**Canonical format:** Markdown-first, with versioned YAML/JSON schemas and optional lightweight validation tools  
**Prepared:** 21 November 2026

---

# Document authority and how to use this blueprint

This is the consolidated master blueprint for AISDF. It brings together the original repository foundation (v1.0), the expanded functional architecture and Markdown file map (v1.1), and the engine/orchestration/full-handoff/predefined-rules expansion (the file named v1.3).

The source file named `AISDF_Complete_Engine_Architecture_and_Predefined_Rules_v1.3.md` contains a metadata mismatch: its internal document header still says version `1.2.0`, although its filename and added sections identify it as the v1.3 expansion. This master document records that discrepancy and uses **Master Blueprint v2.0.0** as the consolidated version. The source text is retained in the appendices so that no previously agreed material is silently lost.

## Authority rules

1. This master blueprint is the consolidated reference for AISDF architecture and repository planning.
2. Within the consolidated blueprint, the newest explicitly added requirements—knowledge freshness, alternatives evaluation, progressive disclosure, full completion, the 20-rule rulebook, preflight and phase-exit checks—are mandatory additions.
3. The original v1.0 repository-only boundary remains in force: AISDF is a framework repository, not a hosted SaaS application, IDE, model provider, universal agent runtime or deployment platform.
4. The v1.1 functional system model, missing-capability list, 48-function catalogue, project contracts, master prompt, 31-domain Markdown map, workflows, schemas and registries remain foundational.
5. The v1.3 expansion's 56-engine catalogue, three-mode intake, design-to-code handoff, coding-tool execution, Git controls, testing/security/performance, deployment, orchestration, freshness, alternatives and completion controls extend the earlier design.
6. If duplicate descriptions differ, use the more specific and stricter rule, provided it does not violate the repository-only boundary or an explicit approved project constraint.
7. A future implementation must create one canonical document per topic and use links/IDs rather than maintaining duplicated copies across the repository.

## Important status distinction

This document is a **blueprint**, not proof of implementation. It does not mean that a GitHub repository has already been created, that all 56 engines are implemented, that adapters have been tested, or that an application has been built and deployed using AISDF. All such claims require repository artifacts and reproducible evidence.

## Intended promise

> Give AISDF a problem statement, project document or existing repository, together with access to a compatible and authorized AI-assisted development environment. AISDF guides the selected tools through discovery, validation, specification, UX/UI design, technology selection, architecture, implementation, testing, security review, verification, deployment preparation and maintenance—using predefined rules, current evidence, controlled handoffs and explicit completion criteria.

AISDF does **not** promise zero bugs, zero vulnerabilities, universal tool compatibility, or unrestricted unattended production deployment. It requires honest reporting of what passed, failed, was not run, is blocked, was waived or remains unverified.

---

# Master navigation

## Part I — Framework foundation
1. Mission, scope and repository boundary
2. Core principles and mandatory engineering laws
3. Intended users and usage modes
4. Development paths: Path 0, Path A, Path B and transformation
5. Universal lifecycle
6. Functional system architecture

## Part II — Intake, analysis and product definition
7. Three intake modes
8. Project document ingestion and normalization
9. Project X-Ray and existing-system assessment
10. Problem, feature, gap, conflict and risk analysis
11. Validation and decision gates
12. Requirements engineering and traceability
13. Product engineering and prioritization

## Part III — Design and engineering intelligence
14. UX/UI and design-system workflow
15. Design tool selection and design-to-code handoff
16. Technology intelligence and alternatives
17. Architecture and architecture decision records
18. Data, API and integration engineering
19. Platform, infrastructure and scaling design
20. Security, privacy and threat modeling
21. AI/model and agent engineering
22. AKIS knowledge intelligence
23. AFIAE feature/tool/service discovery

## Part IV — Execution, agents and orchestration
24. Execution planning and task graph
25. Engine catalogue: 56 engines
26. Agent roles and task contracts
27. Tool capability profiles and adapters
28. Orchestration architecture
29. Handoff protocol and state machine
30. Project state, session continuity and checkpoints
31. Git, branches, commits, pull requests and GitHub automation
32. Full-completion protocol and progressive disclosure

## Part V — Quality and delivery
33. Testing strategy and continuous repair
34. Security verification
35. Performance, load and capacity verification
36. Usability and accessibility verification
37. Independent verification and evidence
38. Release readiness
39. CI/CD, deployment and environment configuration
40. Production verification, operations and maintenance
41. Failure handling, rollback and recovery
42. Audit, observability and history

## Part VI — Governance and implementation
43. Knowledge freshness, versioning and alternatives
44. Predefined rulebook and rule precedence
45. Repository architecture and 31 knowledge domains
46. Prompts, workflows, schemas, registries and templates
47. Framework validation and benchmarks
48. Implementation roadmap and definition of done
49. Risks, tradeoffs and unresolved decisions

## Part VII — Full source blueprints
50. Original repository foundation v1.0
51. Complete functional blueprint and Markdown file map v1.1
52. Engine architecture and predefined rules expansion (v1.3 source file)

---

# 1. Mission and definition

AISDF (AI Software Development Framework) is an open-source, tool-independent software engineering framework. It defines a structured, auditable and reusable way to move from a problem statement or existing codebase to a specified, designed, implemented, tested, secured, verified, deployed and maintained software product.

The GitHub repository is the canonical source of framework knowledge. It contains:

- Engineering methodology and lifecycle workflows.
- Project discovery and existing-codebase assessment standards.
- Requirements, product, UX/UI, architecture and technology guidance.
- Engineering knowledge documents and verified references.
- AI agent roles, task contracts, rules and verification standards.
- Security, privacy, execution and governance policies.
- Reusable schemas, checklists, templates, examples and prompts.
- Registries for documents, engines, workflows, agents, technologies, tools and standards.
- Lightweight scripts and CI checks that validate the framework repository itself.
- Contribution, versioning, release and maintenance governance.

AISDF is not itself a hosted SaaS product, AI coding IDE, model provider, universal autonomous runtime, project management application or deployment platform. It describes how compatible tools can work under the user's actual permissions and execution environment.

# 2. The eight connected functional systems

| System | Purpose | Main outputs |
|---|---|---|
| A. Project Intelligence | Understand new or existing projects | Project profile, normalized brief, Project X-Ray, state |
| B. Requirements & Product Intelligence | Convert needs into agreed scope | PRD, requirements, features, acceptance criteria, risks |
| C. Engineering Design Intelligence | Produce implementation-ready design | UX/UI, architecture, data/API contracts, ADRs |
| D. Knowledge Intelligence (AKIS) | Retrieve relevant, verified and current knowledge | Knowledge packs, source/version metadata |
| E. Feature & Tool Intelligence (AFIAE) | Discover and evaluate tools, APIs, libraries and services | Candidate catalogue, compatibility and approval records |
| F. Execution & Agent Coordination | Turn plans into controlled work | Task graph, assignments, contracts, handoffs |
| G. Quality & Verification | Prove approved requirements are satisfied | Test results, evidence, defects, verdicts |
| H. Delivery & Lifecycle Governance | Deliver, operate, maintain and evolve software | Release records, runbooks, change records |

These systems are framework capabilities expressed as Markdown specifications, schemas, prompts, workflows, checklists, templates, examples and optional repository-validation scripts.

# 3. Three intake modes

## Mode 1 — Problem / Idea Discovery

Use when the user has an idea, rough problem statement, notes or transcript, but no complete specification.

**Objective:** Establish who has the problem, what outcome is needed, what evidence supports it, what alternatives exist and whether a software solution is justified.

Required process:
1. Capture the original problem without prematurely selecting a solution.
2. Identify users, customers and stakeholders.
3. Separate evidence, user claims, assumptions, inferences and unknowns.
4. Assess pain, frequency, severity, current workarounds and alternatives.
5. Research relevant products and comparable solutions when useful.
6. Evaluate desirability, feasibility, viability and timing where applicable.
7. Apply inversion thinking, premortem and risk analysis.
8. Define success measures and pre-committed kill/pivot criteria.
9. Decide proceed, validate further, narrow, pivot, defer or stop.
10. Produce and approve the discovery baseline.

Outputs:
- Problem brief.
- Stakeholder/user map.
- Evidence and assumptions register.
- Market/alternatives review where relevant.
- Risk and premortem.
- Success and kill criteria.
- Discovery decision record.

Exit gate: the problem, target users, desired outcome, critical assumptions and next decision must be explicit. Commercial validation may be skipped for academic, internal or experimental projects with a recorded reason.

## Mode 2 — New Project / Product Build

Use when the problem is understood sufficiently or the user has an approved project brief.

Required process:
1. Validate intake and detect missing decisions.
2. Define product requirements and scope.
3. Define roles, journeys and workflows.
4. Define functional and non-functional requirements.
5. Produce UX structure, flows, wireframes and design system.
6. Evaluate technology and external services.
7. Design architecture, data, APIs, integrations and deployment.
8. Define security, privacy and operational requirements.
9. Decompose work into milestones and dependency-aware tasks.
10. Approve the baseline and create the coding handoff package.

Exit gate: no unresolved product-critical decision may be silently invented. Only low-risk, reversible assumptions may be used when the project policy permits them.

## Mode 3 — Existing Project / Improvement / Transformation

Use when a repository, prototype, application or deployed system already exists.

Mandatory sequence:

**Inspect → Understand → Analyze → Discover → Compare → Document → Approve → Implement → Verify.**

Required process:
1. Inspect repository structure, branch, working tree and history.
2. Identify stack, architecture, modules, entry points and external services.
3. Inspect tests, CI, deployment, environment configuration and security.
4. Run the project where safe and record what was executable.
5. Map existing features and user journeys.
6. Identify defects, technical debt, risks, performance and UX gaps.
7. Trace dependencies and change impact.
8. Compare preserve/improve, redesign and transform options.
9. Produce Project X-Ray and change plan.
10. Obtain required approvals.
11. Implement controlled changes in branches/worktrees.
12. Run regression and independent verification.

Required outputs:
- Project X-Ray.
- Current architecture.
- Feature inventory.
- Dependency/integration map.
- Risk/defect register.
- Change impact analysis.
- Proposed change plan.
- Baseline and verification report.

Exit gate: no broad refactor, migration, replacement or product-direction change without explicit approval. Apply Change Only Law.

# 4. Development paths and operating modes

## Path 0 — Venture and business validation (optional)

1. Starving Crowd Check.
2. Model a Proven Winner.
3. Founder-Market Fit.
4. Inversion Thinking.
5. Premortem.
6. Pre-Commit Kill Criteria.
7. Market Timing.
8. Build Offer.
9. Disciplined Execution.
10. Feedback Loops.
11. Check Kill Criteria.
12. Resource Reinvestment.
13. Defend Moat.
14. Systemize and Delegate.

Path 0 must not block educational, internal, experimental or non-commercial work.

## Path A — New product development

Problem/user check → alternatives check → product/build fit → inversion/premortem → go/kill criteria → product/MVP → scope freeze → UX/UI → architecture → implementation mapping → AI-assisted development → verification/security/QA → deployment/launch → feedback and scaling.

## Path B — Existing project development

Project X-Ray → current-state check → exact change request → impact/dependency analysis → scope/acceptance → minimum safe plan → implementation map → controlled changes → verification → regression → security/performance/UX QA → build/deployment → documentation/state update → close and monitor.

## Product transformation

- Improve existing product while preserving its concept.
- Redesign while preserving its core purpose.
- Transform direction, architecture or purpose.

Transformation requires impact analysis, reuse/replace/migrate/retire decisions and explicit approval.

## Operating modes

- Beginner Mode: guided explanations, staged decisions and explicit approvals.
- Developer Mode: detailed engineering specifications and implementation.
- Team Mode: ownership, reviews, handoffs and merge coordination.
- Enterprise Governance Mode: policies, evidence and auditability; no certification claim.
- Autonomous Controlled Mode: execute within approved scope and actual tool capability, escalating at defined gates.

# 5. Universal lifecycle

```text
PROJECT DOCUMENT / EXISTING REPOSITORY
                |
                v
       INTAKE & CLASSIFICATION
                |
                v
       PROJECT UNDERSTANDING
                |
                v
       REQUIREMENT EXTRACTION
                |
                v
       GAP / CONFLICT / RISK ANALYSIS
                |
        +-------+-------+
        |               |
     Clarify         Sufficient
        |               |
        +-------+-------+
                |
                v
       APPROVED PROJECT BASELINE
                |
                v
       PRODUCT & UX SPECIFICATION
                |
                v
       TECHNOLOGY & ARCHITECTURE
                |
                v
       IMPLEMENTATION DECOMPOSITION
                |
                v
       EXECUTION PLAN & TASK GRAPH
                |
                v
       CONTROLLED IMPLEMENTATION
                |
                v
       CONTINUOUS TEST / DEBUG / REVIEW
                |
                v
       INDEPENDENT VERIFICATION
                |
          +-----+-----+
          |           |
        Failed      Passed
          |           |
        Repair     Release gate
          |           |
          +-----------+
                |
                v
       DELIVERY / DEPLOYMENT
                |
                v
       PRODUCTION VERIFICATION
                |
                v
       MAINTENANCE & CHANGE CONTROL
```

Every lifecycle stage must define purpose, entry criteria, inputs, activities, outputs, owner, approvals, failure paths, exit criteria and evidence.

# 6. Ten critical functional capabilities

1. Project document ingestion and normalization.
2. Ambiguity, conflict and clarification.
3. Requirements traceability graph.
4. Project state and session continuity.
5. Execution protocol and task state machine.
6. Dependency-aware planning and scheduling.
7. Tool capability and execution adapter contract.
8. Continuous verification and repair loop.
9. Release and production readiness gates.
10. Human control and autonomy levels.

Autonomy levels:
- L0 Explain: analyze/recommend.
- L1 Prepare: draft files and patches for approval.
- L2 Execute bounded tasks: approved scope, review at gates.
- L3 Execute project workflow: execute approved tasks and tests, escalate material actions.
- L4 Continuous operation: narrowly pre-authorized routine operations with human governance and revocation.

No autonomy level overrides actual permissions or security policy.

# 7. Mandatory AISDF laws

1. **Change Only Law:** Change the requested item and only technically required dependencies; preserve unrelated behavior.
2. **No AI Slope:** No unnecessary features, abstractions, dependencies, services, agents, prompts, context, infrastructure or refactors.
3. **Approval First:** Material scope/product/architecture changes, migrations, sensitive permissions, purchases, destructive and production actions require appropriate approval.
4. **Evidence Over Claims:** Completion requires evidence, not an AI assertion.
5. **Least Privilege:** Use only permissions necessary for the assigned task.
6. **No Authority Escalation:** Delegation, tool switching, MCP, CLI or subagents cannot increase authority.
7. **Right-Sized Engineering:** Match complexity to actual requirements and risks.
8. **Source of Truth:** Project records and repository state—not chat memory—are canonical.
9. **Traceability:** Requirements connect to design, tasks, code changes, tests, verification and release.
10. **User Intent Preservation:** Do not silently alter the user's goals, constraints or product direction.
11. **Freshness and Provenance:** Time-sensitive facts need source/version/date and status.
12. **Full Completion:** Do not mark work done until required exit criteria pass.
13. **No Fake Execution:** Never claim research, commands, tests, pushes or deployment unless actually performed.
14. **Reversibility:** Plan rollback/recovery for risky changes.
15. **Failure Disclosure:** Report failed, blocked, partial, waived and unverified work honestly.

# 8. Project intelligence and analysis

## Project document ingestion

Accept Markdown as canonical starter format and define handling for PDF, DOCX, plain text, transcripts and repository context. Preserve the original input. Extract:
- Project identity, goals and scope.
- Users and stakeholders.
- Platforms and environments.
- Functional requirements and business rules.
- Non-functional requirements.
- Constraints and preferences.
- Dependencies and integrations.
- Security/privacy requirements.
- Budget, timing and operational constraints.
- Explicit exclusions.
- Source references and confidence.

Classify each statement as explicit requirement, business rule, constraint, preference, assumption, inference, open question or out-of-scope.

## Ambiguity and conflict handling

Severity:
- Blocker.
- Material.
- Minor.
- Informational.

Ask when uncertainty changes product behavior, security, data, cost, legal exposure, architecture, permissions or acceptance. Use safe defaults only for reversible low-risk details. Batch related questions and explain why answers matter.

Conflict precedence:
1. Explicit approved requirement.
2. Approved decision record.
3. Current project source of truth.
4. Documented assumption.
5. AI inference.

Required records: open questions, assumptions, conflicts, rationale, owner, confidence, impact and review condition.

## Project X-Ray

Inspect:
- Repository structure and ownership.
- Languages, frameworks, versions and package managers.
- Entry points and execution scripts.
- Architecture, modules and dependency boundaries.
- Data model, migrations and storage.
- API and external integrations.
- Authentication, authorization and tenant boundaries.
- UI routes, screens, states and user flows.
- Tests, CI, deployment and environments.
- Secrets handling and security controls.
- Performance, reliability and observability.
- Documentation, known defects and technical debt.
- Git status, branch and recent history.

Do not claim a system was run if it was only inspected statically. Record inaccessible or unverified areas.

## Feature analysis

For each feature record:
- Feature ID and name.
- User/problem served.
- Current/proposed status.
- Priority and value.
- Dependencies.
- Data and permissions.
- UX states.
- Risks and complexity.
- Acceptance criteria.
- Tests and verification.
- Decision: keep, improve, redesign, replace, defer or remove.

Feature removal or product scope changes require approval when they affect approved behavior.

# 9. Requirements, product and traceability

Every requirement receives a stable ID, source, description, type, priority, owner, status, rationale, dependencies, risks and acceptance criteria.

Traceability chain:

`Problem → Requirement → Design element → Task → Code/change → Test → Verification → Evidence → Release`

Rules:
- No approved requirement disappears during decomposition.
- Every feature has acceptance criteria.
- Every task references requirements or is explicitly enabling/maintenance work.
- Every acceptance criterion maps to a test or manual verification.
- Requirement changes trigger impact analysis.
- Completion requires evidence.

Product engineering defines target users, outcomes, value proposition, MVP, scope, roadmap, feature prioritization, metrics and kill criteria. Commercial validation is conditional on project type.

# 10. UX/UI and design handoff

Workflow:

```text
Approved problem + PRD
        |
User roles and journeys
        |
Information architecture
        |
Task flows + screen inventory
        |
Wireframes / prototypes
        |
Visual design + tokens
        |
Responsive and interaction states
        |
Accessibility + usability review
        |
Design approval
        |
Developer handoff package
```

The design handoff includes:
- Page/screen inventory and route map.
- User journeys and flow diagrams.
- Responsive behavior and breakpoints.
- Component inventory and variants.
- Color, typography, spacing, radius, shadow and motion tokens.
- Default, hover, focus, active, loading, empty, error, success and disabled states.
- Form validation and error messages.
- Navigation and permissions.
- Accessibility requirements.
- Asset inventory and licensing.
- Prototype/design links and exportable assets.
- Design-to-requirement traceability.
- Known limitations and open questions.

Stitch, Figma or another tool may be used after verifying current capabilities, export, inspectability, collaboration and coding handoff. General AI assistants may help with research, flows, specs and prompts. A screenshot alone is not an implementation-ready design specification.

# 11. Technology intelligence and alternatives

No universal stack is prescribed. Selection depends on product needs, platform, team capability, scale, budget, sensitivity, ecosystem maturity and operations.

For every consequential technology decision record:
- Requirement.
- Candidate and selected option.
- Official source and version.
- Support status and release date.
- Compatibility.
- Security and privacy.
- License.
- Cost and operating burden.
- Lock-in and migration.
- Team skill/learning cost.
- Alternatives and tradeoffs.
- Rejection reasons.
- Verification date and reconsideration triggers.

Compare reasonable alternatives for AI assistants/models, coding IDEs, design tools, languages/frameworks, databases/ORMs, hosting, authentication, APIs/SDKs/libraries/MCP servers, queues/caches/search, architecture, testing, observability, Git and release strategies.

Do not manufacture alternatives. If a technology is mandated or no meaningful alternative exists, record the constraint and tradeoff.

# 12. Knowledge intelligence — AKIS

AKIS is a knowledge organization and retrieval methodology, not a hosted retrieval service.

It defines:
- Knowledge taxonomy and metadata.
- Stable document IDs and versioning.
- Source quality and provenance.
- Freshness and review dates.
- Retrieval and relevance ranking.
- Permissions and trust boundaries.
- Deduplication and supersession.
- Context budgets and progressive disclosure.
- Cross-reference and version traceability.

Markdown in Git is canonical. Obsidian may be an optional authoring UI, not a runtime requirement. Modularity and selective retrieval help context efficiency; an editor itself does not guarantee token savings.

# 13. Feature & Tool Intelligence — AFIAE

AFIAE discovers and evaluates APIs, SDKs, libraries, plugins, MCP servers, skills, models, tools, infrastructure and external services.

Workflow:

`Requirement → Gap → Discovery → Source Verification → Evaluation → Pricing/License → Security → Compatibility → Compare → Approval → Authorized Acquisition → Integration → Verification → Monitoring`

Discovery can be automated. Installation, credentials, purchases, subscriptions and production integrations require appropriate authorization.

# 14. Complete engine catalogue — 56 engines

An engine is a named capability with purpose, inputs, outputs, rules, dependencies, owner, evidence, failure handling and exit criteria. It is not automatically a separate agent, service or microservice.

## A. Intake, understanding and validation

| ID | Engine | Responsibility |
|---|---|---|
| E-001 | Intake & Mode Selection | Classify input and choose one of three modes |
| E-002 | Document Ingestion & Normalization | Parse project docs, notes, repository context and sources |
| E-003 | Problem Discovery | Identify user problem, context, impact and outcome |
| E-004 | Existing Project X-Ray | Inspect codebase and current behavior |
| E-005 | Feature Inventory & Analysis | Identify current/proposed features, value, dependencies and gaps |
| E-006 | Problem Validation | Assess evidence, assumptions, alternatives and severity |
| E-007 | Product/Market Validation | Evaluate demand, alternatives, timing and viability where relevant |
| E-008 | Gap, Conflict & Ambiguity | Detect missing, conflicting, vague or unverifiable statements |
| E-009 | Risk, Inversion & Premortem | Identify failure paths, threats and pre-mortem risks |
| E-010 | Scope & Kill-Criteria | Define boundaries, exclusions, success and stop conditions |

## B. Product and requirements intelligence

| ID | Engine | Responsibility |
|---|---|---|
| E-011 | User & Stakeholder Intelligence | Define users, roles, needs and stakeholders |
| E-012 | Requirements Engineering | Convert needs into testable requirements |
| E-013 | Feature Prioritization | Prioritize by value, risk, effort and dependencies |
| E-014 | Product Specification | Define product behavior and boundaries |
| E-015 | Acceptance Criteria | Define observable pass/fail criteria |
| E-016 | Traceability | Link problem, requirements, design, tasks, tests and evidence |

## C. UX/UI and experience design

| ID | Engine | Responsibility |
|---|---|---|
| E-017 | UX Research & Journey | Model tasks, journeys, pain points and user context |
| E-018 | Information Architecture | Define navigation and content hierarchy |
| E-019 | Interaction & Flow Design | Define states, transitions, forms and error paths |
| E-020 | UI & Design-System | Define visual system, components, tokens and responsive rules |
| E-021 | Design Tool Selection & Handoff | Select compatible tool and prepare implementation-ready handoff |
| E-022 | Usability & Accessibility Review | Evaluate usability, keyboard, screen reader and accessibility |

## D. Technology and architecture intelligence

| ID | Engine | Responsibility |
|---|---|---|
| E-023 | Technology Research | Verify technologies, versions and support |
| E-024 | Stack Selection | Compare stack choices against requirements and team capability |
| E-025 | Architecture Design | Define components, boundaries and quality attributes |
| E-026 | Data & Database Design | Model data, constraints, migrations, backup and retention |
| E-027 | API & Integration Design | Define contracts, auth, errors, limits and integrations |
| E-028 | Infrastructure & Scaling Design | Design hosting, networking, caching, queues and scaling when justified |
| E-029 | Cost & Capacity Analysis | Estimate operational costs and resource needs |
| E-030 | Architecture Decision & Change Control | Record alternatives, tradeoffs and approvals |

## E. Knowledge, tools and acquisition

| ID | Engine | Responsibility |
|---|---|---|
| E-031 | AKIS Knowledge Intelligence | Organize, retrieve, rank and freshness-check knowledge |
| E-032 | AFIAE Feature & Tool Discovery | Discover APIs, SDKs, libraries, MCP servers, models and services |
| E-033 | Tool/Service Evaluation | Assess security, license, compatibility, cost and lock-in |
| E-034 | Compatibility Verification | Verify tool capabilities and supported actions |

## F. Execution and orchestration

| ID | Engine | Responsibility |
|---|---|---|
| E-035 | Execution Planning | Convert baseline into milestones and task graph |
| E-036 | Task & Dependency Orchestration | Sequence tasks and manage dependencies |
| E-037 | Agent Role & Delegation | Assign bounded responsibilities to compatible agents |
| E-038 | Context & Handoff | Package context and transfer ownership safely |
| E-039 | Tool/IDE Adapter | Translate framework contracts into tool-specific instructions |
| E-040 | Project State & Continuity | Preserve canonical project state across sessions |
| E-041 | Git & Change Orchestration | Manage branches, commits, PRs and merges |
| E-042 | Human Approval & Escalation | Stop for material decisions and record authorization |

## G. Quality, security and verification

| ID | Engine | Responsibility |
|---|---|---|
| E-043 | Test Strategy & Generation | Derive test layers and cases from requirements |
| E-044 | Build, Test & Debug | Execute checks, diagnose failures and repair within scope |
| E-045 | Code Review & Change Impact | Review diffs, maintainability and regressions |
| E-046 | Security & Privacy | Threat model, secure design, dependency and secret checks |
| E-047 | Performance & Load | Define and run workload-based performance tests |
| E-048 | Independent Verification | Verify acceptance criteria independently |
| E-049 | UX & Accessibility Verification | Validate real user journeys and accessibility |
| E-050 | Release Readiness | Aggregate quality gates and residual risks |

## H. Delivery and lifecycle

| ID | Engine | Responsibility |
|---|---|---|
| E-051 | CI/CD Pipeline Design | Define reproducible build/test/release automation |
| E-052 | Deployment & Environment | Configure environment-based deployment and secrets |
| E-053 | Production Verification | Smoke tests, health checks and rollback validation |
| E-054 | Observability & Incident Readiness | Define logs, metrics, traces, alerts and runbooks |
| E-055 | Maintenance & Change Governance | Manage updates, defects, vulnerabilities and deprecation |
| E-056 | Project Closeout & Learning | Capture final state, lessons and next steps |

Every engine specification must include: ID, purpose, scope, non-goals, trigger, required inputs, source documents, outputs, steps, decision rules, dependencies, responsible role, tool capabilities, permissions, freshness requirements, alternatives requirement, approvals, failure behavior, evidence, acceptance criteria, exit criteria and handoff.

# 15. Prompt and document architecture

Do not use one giant prompt as the framework. The master prompt is an entry point that loads the relevant mode, rules, engine specifications and workflow.

## Prompt hierarchy

- Master entry prompt.
- Three mode prompts.
- Engine prompts.
- Phase prompts: product, UX, architecture, implementation, testing, release.
- Role prompts: analyst, requirements engineer, product engineer, designer, architect, implementer, reviewer, tester, security reviewer, release engineer.
- Handoff prompts: agent-to-agent, session-to-session, phase-to-phase.
- Recovery prompts: blocked task, failed task, context loss, rollback and incident.

## Required project records

1. `00-project-intake.md`
2. `01-problem-brief.md`
3. `02-validation-report.md`
4. `03-project-profile.yaml`
5. `04-prd.md`
6. `05-feature-catalogue.md`
7. `06-acceptance-criteria.md`
8. `07-ux-specification.md`
9. `08-design-system.md`
10. `09-technology-evaluation.md`
11. `10-architecture.md`
12. `11-data-api-contracts.md`
13. `12-security-threat-model.md`
14. `13-test-strategy.md`
15. `14-deployment-operations.md`
16. `15-execution-plan.md`
17. `16-decision-log.md`
18. `17-risk-register.md`
19. `18-verification-report.md`
20. `19-release-record.md`
21. `20-project-state.md`

Create only relevant documents; record why an optional artifact is omitted. Do not generate empty placeholder files.

## Mandatory prompt behavior

Every prompt must instruct the AI tool to:
- Read project baseline and applicable laws first.
- Identify role, scope and permissions.
- Cite source documents/sections for decisions.
- Separate facts, approved decisions, assumptions, inferences and unknowns.
- Never invent execution, tests, research or compatibility.
- Ask only questions that block a safe/correct decision.
- Avoid duplicating existing work.
- Respect Change Only Law and No AI Slope.
- Produce specified outputs.
- Update project state and handoffs.
- Stop for required approvals.
- Report what could not be verified.

# 16. Technology, architecture and infrastructure design

Every selected technology must be evaluated for fit, support, security, licensing, cost, compatibility, maintenance, ecosystem, team capability and lock-in.

Architecture must address applicable concerns:
- Client, application/API and background-processing boundaries.
- Authentication, authorization and tenant isolation.
- Data storage, migrations, backup and recovery.
- Caching, queues and rate limiting.
- Network boundaries and secrets.
- Logs, metrics and traces.
- Scaling, failure modes, timeouts, retries and idempotency.
- Cost and capacity.

Load balancers, microservices, Kubernetes, message brokers, multi-region deployment and other complex infrastructure are conditional—not defaults. Justify each against a real requirement. A load balancer alone does not prove scalability.

# 17. AI IDE and agent execution

## Tool capability check

Before assigning work, verify whether the selected tool can:
- Read repository/files.
- Edit files.
- Run shell commands.
- Run tests and inspect results.
- Access network/browser.
- Use Git branches and commits.
- Open pull requests.
- Access design artifacts.
- Use approved MCP/API integrations.
- Deploy.
- Respect sandbox and permission controls.
- Return usable evidence.

Record supported versions, plan/account restrictions where verified, tested capabilities, limitations, source and last verification date. Capability status: `VERIFIED`, `PARTIAL`, `EXPERIMENTAL`, `NOT_VERIFIED`, `DEPRECATED`.

## Execution stages

1. Preflight repository and baseline.
2. Plan task, dependencies and affected files.
3. Create task/feature branch.
4. Implement smallest coherent approved change.
5. Run targeted and relevant regression tests.
6. Review diff, secrets, dependencies, security and accessibility.
7. Commit meaningful changes.
8. Prepare handoff and evidence.
9. Open PR when required.
10. Merge after checks and approvals.
11. Release/deploy through approved pipeline.
12. Verify production.

# 18. Git and GitHub governance

Default branch model:
- `main`: protected, releasable baseline.
- `feature/<task>-<short-name>`.
- `fix/<task>-<short-name>`.
- `hotfix/<task>-<short-name>`.
- `docs/<short-name>`.
- `chore/<short-name>`.

Rules:
- No force push or shared-history rewrite without explicit authorization.
- Never commit secrets, `.env`, private keys or credentials.
- Keep commits small and descriptive.
- Link commits and PRs to task IDs.
- Require CI before merge.
- Require review for sensitive, destructive, security-critical or production-impacting changes.
- Use separate branches/worktrees for parallel agents.
- Define file ownership and merge order.
- Preserve PR and commit history.

Suggested commit format: `type(scope): concise change [TASK-ID]`.

GitHub Actions templates may validate formatting, types, builds, tests, security, dependencies, secrets, artifacts, provenance, preview deployment and releases. Use scoped secrets, GitHub environments and OIDC where supported.

**Auto-push policy:** Feature-branch push may be enabled if explicitly authorized. Direct push to protected `main`, merge and production deployment must follow repository policy and approval gates. A master prompt cannot grant permissions that the environment has not granted.

# 19. Testing, security, performance and UX quality gates

## Testing layers

- Formatting, lint, static analysis and type checks.
- Unit and component tests.
- Integration and API contract tests.
- Database and migration tests.
- End-to-end user journeys.
- Regression.
- Accessibility.
- Cross-browser/device where applicable.
- Security and dependency scans.
- Performance/load/stress/soak where justified.
- Backup/restore and recovery for critical systems.
- Production smoke and synthetic checks.

## Security

Evaluate authentication, authorization, tenant isolation, input validation, output encoding, injection, XSS, CSRF, SSRF where relevant, secrets, supply chain, TLS, headers, rate limits, file handling, logging, backup, retention and threat model.

Critical/high findings block release unless an accountable owner accepts a documented exception under project policy. No compliance certification claim without evidence and authority.

## Performance/load

Define expected users/concurrency, request mix, peak traffic, data size/growth, latency percentiles, error-rate targets and resource/cost ceiling. Run appropriate baseline, load, stress and soak tests. Test database, API, queue, cache and network bottlenecks.

## UX/accessibility

Test real user tasks, navigation, feedback, empty/loading/error/success states, keyboard, focus, contrast, responsive behavior, destructive actions, permissions and privacy comprehension.

## Verification status

- `PASS_VERIFIED`
- `FAIL`
- `NOT_RUN`
- `BLOCKED`
- `NOT_APPLICABLE`
- `WAIVED`

A waiver requires approver, reason, scope and expiry/review condition. Never label code complete merely because it was generated.

# 20. Deployment and operations

Environment model as appropriate:
- Local development.
- CI/test.
- Preview/staging.
- Production.

Externalize configuration. Use `.env.example` with variable names and safe descriptions only. Track purpose, required/optional, environment, secret classification, validation, owner/source and rotation guidance. Never hardcode credentials.

Deployment pipeline:

```text
Approved PR
   -> lint/typecheck/build
   -> unit/integration/contract tests
   -> security/dependency/secret checks
   -> preview/staging
   -> E2E/smoke/performance checks
   -> release readiness
   -> required approval
   -> production deploy
   -> health checks/smoke tests
   -> release evidence/monitoring
```

Provider-specific deployment must be handled by configurable adapters. Do not hardcode a provider as universal. Production safeguards include separated credentials, least privilege, protected environment, migration plan, backup/restore, health checks, rollback/forward-fix plan, progressive rollout only when justified, monitoring and runbooks.

# 21. Handoff protocol

A handoff is a formal transfer of responsibility and sufficient context, not “continue from here.”

## Handoff types

- User → intake.
- Assistant → project documents.
- Analysis → requirements.
- Product → UX/UI.
- Design tool → coding IDE.
- Architecture → implementation agent.
- Agent → agent.
- Agent → human reviewer.
- Coding agent → tester/verifier.
- Verification → release approver.
- CI/CD → deployment.
- Deployment → operations.
- Session → next session.
- Existing project → transformation owner.

## Mandatory handoff package

1. Handoff and project IDs.
2. Sender and receiver roles/tools.
3. Timestamp and schema/framework version.
4. Project mode, phase and task state.
5. Objective and scope.
6. Canonical source-of-truth paths and revision/commit.
7. Requirement and acceptance-criteria IDs.
8. Approved decisions/ADRs.
9. Assumptions, unknowns and open questions.
10. AKIS sources/version/date.
11. AFIAE evaluations and approval state.
12. Dependencies and blockers.
13. Allowed/prohibited files/modules.
14. Tool permissions and execution boundaries.
15. Completed and incomplete work.
16. Changed files, branch and commits.
17. Tests, exact commands, results and environment.
18. Verification evidence.
19. Risks, defects and residual concerns.
20. Next actions and expected outputs.
21. Approval state.
22. Handoff status and receiver acknowledgement.

## Handoff state machine

`DRAFT → SUBMITTED → ACKNOWLEDGED → ACCEPTED → IN_PROGRESS → READY_FOR_REVIEW → VERIFIED → CLOSED`

Exception states: `REJECTED`, `NEEDS_CLARIFICATION`, `BLOCKED`, `FAILED`, `ESCALATED`, `CHANGES_REQUESTED`, `CANCELLED`.

Receiver must acknowledge package and access before execution. Incomplete handoff is not accepted work.

# 22. Task and project state

Suggested task states:
`DRAFT → READY → ASSIGNED → IN_PROGRESS → BLOCKED/REVIEW → VERIFIED → DONE`

Additional states: `CANCELLED`, `REJECTED`, `WAIVED`, `FAILED`, `PARTIALLY_COMPLETED`, `NEEDS_APPROVAL`.

Every transition records actor, timestamp, reason and evidence.

Canonical project control records:
- `PROJECT-STATE.md`
- `DECISIONS.md` or ADR directory
- `TASK-BOARD.yaml`
- `RISKS.md`
- `CHANGELOG.md`
- `HANDOFF.md`
- `BASELINE.md`
- `RELEASE-STATUS.md`

At session start, read canonical control records. At session end, update state and create resumable handoff. Never rely on hidden chat memory as the sole source.

# 23. Full-completion and pause/resume protocol

Once an engine, workflow, phase or task starts, it must meet its defined exit criteria before being marked complete or before dependent work begins.

Before starting define:
- Work-unit ID.
- Objective and scope.
- Inputs and baseline.
- Required activities.
- Expected outputs and paths.
- Acceptance criteria.
- Verification method.
- Dependencies.
- Permissions and approvals.
- Budget/deadline where applicable.
- Stop and escalation conditions.

Completion sequence:
1. Read instructions and rules.
2. Confirm inputs/access.
3. Confirm dependencies/approvals.
4. Execute required activities.
5. Create/update outputs.
6. Validate structure/completeness.
7. Run checks.
8. Record evidence/open issues.
9. Update state/traceability.
10. Submit handoff.
11. Obtain acknowledgement where required.
12. Mark complete only if exit criteria pass.

Pause only for missing decision/approval, unavailable access/tool/dependency, safety/security issue, budget/environment limit or unsafe failure.

Checkpoint must contain completed/incomplete steps, current state, outputs, commands/actions, test results/logs, blocker, resume requirements, exact next action and uncommitted/unpushed changes.

Resume from first incomplete step after revalidating baseline. Do not restart completed work unnecessarily.

A parent task is complete only when required child tasks are done or explicitly waived. Parallel work requires explicit dependencies, file ownership and integration plan; final integration and verification remain mandatory.

# 24. Knowledge freshness, version intelligence and provenance

Every meaningful statement used in analysis/design/execution is classified as:
- `USER_PROVIDED`
- `REPOSITORY_OBSERVED`
- `OFFICIALLY_VERIFIED`
- `INDEPENDENTLY_CORROBORATED`
- `MODEL_KNOWLEDGE`
- `INFERENCE`
- `ASSUMPTION`
- `RECOMMENDATION`
- `UNKNOWN`

Never turn an assumption or inference into verified fact by repetition.

Source hierarchy:
1. Official documentation, release notes, security advisories and API references.
2. Standards bodies, specifications and maintainers' repositories.
3. Official vendor engineering/security documentation.
4. Reputable independent research/publications.
5. Community discussions as supporting signals.
6. Model knowledge for stable background or marked preliminary guidance.

For time-sensitive knowledge record source, owner, type, product/standard, version, published/updated date where available, verification date/method, support status, confidence, next review, limitations and supersession.

Freshness defaults:
- Highly volatile: AI models/IDE features/pricing/API limits — check at each selection/use and before implementation.
- Fast changing: frameworks/SDKs/cloud features/packages — check at project start and before major upgrade/release.
- Moderate: security guidance/deployment/platform support — project start and release/security review.
- Slow: foundational concepts — scheduled maintenance or when challenged.
- Historical: review when new evidence or challenge arises.

Before using knowledge, check source authority, project version, maintenance status, newer release/migration/deprecation/security advisories, platform applicability, breaking changes and official support.

Stale sources are marked `STALE`, `SUPERSEDED`, `UNVERIFIED` or `CONFLICTED`. Do not silently reuse. Find authoritative replacement, record impact and request a decision if scope/cost/security/architecture/migration risk changes.

Technology compatibility matrix records runtime, framework, package manager, database, ORM/driver, hosting/runtime, AI tool/model and external API versions/support/evidence.

Do not always select newest. Select supported, compatible versions and define pinning/range and upgrade policy.

# 25. Progressive disclosure and advanced detail

Three information levels:
- Level 1 Essential: mandatory rules, immediate steps, inputs, outputs, decisions and checks; always loaded.
- Level 2 Practical: examples, implementation guidance, common errors and relevant tradeoffs; load when needed.
- Level 3 Advanced: internals, edge cases, scaling, specialist patterns and standards mapping; load on request or risk/complexity trigger.

Never hide security, permissions, approval, destructive-action warnings or mandatory verification in advanced material.

Advanced triggers include explicit user request, security/privacy/compliance sensitivity, multi-service/tenant/region complexity, migrations/data loss/production impact, scale/performance targets, version constraints, tool failure, unmet acceptance criteria, high cost/lock-in or difficult reversibility.

Load master prompt, mode, core laws, current workflow, relevant engine specs, relevant knowledge and alternatives only where needed. Provide minimum sufficient accurate context—not context minimization at the expense of correctness.

# 26. Predefined rulebook — 20 rules

| ID | Rule | Required check |
|---|---|---|
| RULE-001 | Source-of-truth | Locate canonical docs, repo and baseline |
| RULE-002 | Evidence over claims | Link completion claims to evidence |
| RULE-003 | Change Only Law | Check scope and unrelated diffs |
| RULE-004 | No AI Slope | Justify additions |
| RULE-005 | Approval First | Verify approval before material/destructive/production action |
| RULE-006 | Least Privilege | Minimum permission; no escalation |
| RULE-007 | Freshness & Version | Verify volatile knowledge and record source/version/date |
| RULE-008 | Alternatives | Compare meaningful options for consequential decisions |
| RULE-009 | Provenance | Separate user input, observed/verified facts, assumptions and inference |
| RULE-010 | Full Completion | Meet exit criteria before marking done |
| RULE-011 | No Fake Execution | Claim action only when actually executed |
| RULE-012 | Traceability | Link requirement, task, change, test and evidence |
| RULE-013 | Secure Secrets | Never hardcode/expose credentials |
| RULE-014 | Git Safety | Approved branches, reviews and protection |
| RULE-015 | Compatibility | Verify tools, versions and integrations |
| RULE-016 | Failure Disclosure | Report blockers, failures, waivers and residual risks |
| RULE-017 | Reversibility | Plan rollback/recovery |
| RULE-018 | Handoff Completeness | Validate package and acknowledgement |
| RULE-019 | Right-Sized Engineering | Justify complexity |
| RULE-020 | User Intent Preservation | Do not silently change user goals or constraints |

## Preflight checklist

- Correct project/mode.
- Current phase and work-unit ID.
- Canonical baseline located.
- Applicable rules/workflow version loaded.
- User requirements preserved.
- Facts/assumptions/inferences/unknowns separated.
- Knowledge freshness checked.
- Alternatives evaluated or omission justified.
- Inputs/dependencies available.
- Tool capabilities verified.
- Permissions least-privileged.
- Scope/exclusions explicit.
- Approvals identified.
- Outputs/acceptance criteria explicit.
- Verification/evidence defined.
- Failure/recovery route known.

If a critical item fails, do not begin the affected action.

## Phase exit checklist

- Required activities complete or explicitly dispositioned.
- Required outputs created and validated.
- Requirements/decisions traceable.
- Required checks actually run.
- Evidence stored/linked.
- Risks/open questions recorded.
- No unapproved scope expansion.
- No hidden partial completion.
- Project state updated.
- Handoff complete.
- Receiver acknowledgement/approval recorded where required.
- Exit criteria passed or phase honestly marked blocked/failed/partial.

## Rule precedence

1. Applicable law, safety and platform/security restrictions.
2. Explicit user-approved project constraints and organizational policy.
3. AISDF mandatory laws/rulebook.
4. Approved project baseline and ADRs.
5. Workflow/engine specification.
6. Tool-specific adapter.
7. Local task instructions.
8. Model assumptions/generic preferences.

Lower-level instructions cannot override higher-level rules. Conflicts between high-priority requirements require escalation.

# 27. Orchestration architecture

**Framework control plane:** Markdown policies, schemas, workflows, registries, task contracts, approval rules, state and adapter specifications.

**Execution plane:** User's selected assistant, design tool, IDE/CLI agent, Git provider, CI runner, hosting platform and approved integrations.

AISDF repository does not run a hosted orchestrator. A compatible tool or separately approved future runtime interprets the framework.

Patterns and tradeoffs:
- Single coordinator: simple ownership, possible bottleneck.
- Hierarchical: scalable delegation, more handoffs.
- Peer-to-peer: flexible, harder conflict/audit.
- Sequential: predictable gates, slower.
- Parallel task graph: faster independent tasks, merge conflicts.
- Event-driven: loose coupling, more infrastructure.
- Shared workspace: simple, edit conflicts.
- Isolated branches/worktrees: safer parallelism, merge overhead.

Default: sequential gates and limited parallelism for independent tasks. Add complexity only when justified.

# 28. Failure and recovery

| Failure | Required response |
|---|---|
| Ambiguous requirement | Pause affected task; ask or record permitted assumption |
| Conflicting documents | Apply source precedence; request owner decision |
| Missing tool capability | Approved fallback or blocked status |
| Tool/API unavailable | Bounded retries, then stop/escalate |
| Test failure | Preserve logs, isolate, repair in scope, rerun |
| Unexpected code changes | Stop and inspect; revert only safely authorized |
| Merge conflict | Reconcile against baseline; never overwrite blindly |
| Security finding | Contain, classify, remediate or block release |
| Deployment failure | Stop rollout; collect evidence; rollback/forward-fix |
| Context/session loss | Reconstruct from canonical state and handoff |
| Agent disagreement | Compare evidence; escalate unresolved decisions |
| Budget exceeded | Stop at safe boundary and report remaining work |

Retries must be bounded and idempotent where possible.

# 29. Audit, observability and history

Record intake/mode, document revisions, assumptions/decisions, approvals, task state changes, agent/tool invocations where available, Git branches/commits/PRs, tests, security findings, deployments/rollbacks, releases and closeout.

Each event should include actor/tool, action, timestamp, project/task, artifact, result and evidence. Do not log secrets or unnecessary personal data.

Git history is canonical for code changes. Decision logs and release records capture rationale/evidence. Chat history is not the project audit trail.

# 30. Repository architecture — 31 canonical domains

The repository must retain the original 31 numbered domains:

00-GOVERNANCE  
01-METHODOLOGY  
02-PROJECT-INTELLIGENCE  
03-REQUIREMENTS-ENGINEERING  
04-PRODUCT-ENGINEERING  
05-UX-UI-ENGINEERING  
06-TECHNOLOGY-INTELLIGENCE  
07-ENGINEERING-KNOWLEDGE  
08-SOFTWARE-ARCHITECTURE  
09-PLATFORM-ENGINEERING  
10-AI-AND-MODEL-ENGINEERING  
11-AGENT-ENGINEERING  
12-ORCHESTRATION-AND-CONTEXT  
13-HARNESS-AND-EXECUTION  
14-SECURITY-AND-PRIVACY  
15-DATA-AND-DATABASE-ENGINEERING  
16-API-AND-INTEGRATION-ENGINEERING  
17-TESTING-AND-VERIFICATION  
18-DEVOPS-AND-CLOUD-ENGINEERING  
19-DEPLOYMENT-AND-OPERATIONS  
20-RELIABILITY-AND-OBSERVABILITY  
21-DISTRIBUTED-SYSTEMS-AND-SCALABILITY  
22-COST-AND-RESOURCE-GOVERNANCE  
23-LEGAL-AND-COMPLIANCE  
24-PRODUCT-ANALYTICS-AND-SUPPORT  
25-FRAMEWORK-MAINTENANCE  
26-DISTRIBUTION-AND-EXTENSIONS  
27-STANDARDS-AND-COMPATIBILITY  
28-TEMPLATES-AND-EXAMPLES  
29-BENCHMARKS-AND-EVALUATION  
30-AGENT-RULES-AND-VERIFICATION

Each domain requires `README.md` and `INDEX.md`, domain standards and relevant alternatives documents. Alternatives documents are created when meaningful competing approaches exist; they are not compulsory filler.

Additional top-level directories:
- `engines/`: catalogue, registry, engine specification template.
- `modes/`: three mode specifications.
- `prompts/`
- `workflows/`
- `schemas/`
- `registries/`
- `templates/`
- `examples/`
- `adapters/assistant-tools/`
- `adapters/design-tools/`
- `adapters/coding-tools/`
- `adapters/git-providers/`
- `adapters/ci-cd/`
- `adapters/deployment-providers/`
- `tests/`
- `tools/`
- `.github/`

Every domain README/INDEX points to canonical documents. Avoid duplicated knowledge silos.

# 31. Root files and governance

Root files:
- `README.md`
- `AISDF-MISSION-AND-SCOPE.md`
- `AISDF-FUNCTIONAL-MAP.md`
- `AISDF-LIFECYCLE-OVERVIEW.md`
- `AISDF-CORE-PRINCIPLES.md`
- `AISDF-GLOSSARY.md`
- `AISDF-FAQ.md`
- `QUICK-START.md`
- `MASTER-ENTRY-PROMPT.md`
- `LICENSE`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `GOVERNANCE.md`
- `SECURITY.md`
- `SUPPORT.md`
- `CHANGELOG.md`
- `VERSION`
- `CITATION.cff`
- `.editorconfig`
- `.gitignore`

Apache-2.0 was suggested subject to ownership/legal review; MIT is an alternative. Do not publish a license until rights and dependencies are checked. Use SemVer, contribution review, maintainer governance, issue/PR templates, security disclosure process and deprecation policy.

# 32. Required repository document map

The detailed per-domain Markdown file map from the v1.1 source is retained in Appendix B. It defines the required files for all 31 domains, including:
- Governance and methodology.
- Project intelligence and requirements.
- Product and UX/UI.
- Technology and engineering knowledge.
- Architecture and platform.
- AI, agents and orchestration.
- Harness and security.
- Data, APIs and integrations.
- Testing and verification.
- DevOps, deployment, reliability and scaling.
- Cost, legal, analytics and support.
- Framework maintenance, distribution, standards, examples and benchmarks.

Additional v1.3 files:
- `AISDF-RULEBOOK.md`
- `RULE-PRECEDENCE-AND-CONFLICT-RESOLUTION.md`
- `KNOWLEDGE-FRESHNESS-AND-REVIEW-POLICY.md`
- `EVIDENCE-AND-PROVENANCE-POLICY.md`
- `VERSION-AND-COMPATIBILITY-MATRIX.md`
- `ALTERNATIVES-EVALUATION-STANDARD.md`
- `TECHNOLOGY-SUPPORT-AND-DEPRECATION-POLICY.md`
- `KNOWLEDGE-METADATA-STANDARD.md`
- `SOURCE-QUALITY-AND-VERIFICATION.md`
- `STALE-KNOWLEDGE-REVIEW-WORKFLOW.md`
- `WORK-UNIT-FULL-COMPLETION-PROTOCOL.md`
- `PAUSE-RESUME-AND-CHECKPOINT-PROTOCOL.md`
- `HANDOFF-ACKNOWLEDGEMENT-PROTOCOL.md`
- `PROGRESSIVE-DISCLOSURE-AND-CONTEXT-LOADING.md`
- `TOOL-CAPABILITY-VERIFICATION.md`
- `ADAPTER-FRESHNESS-REGISTER.md`
- `PRE-FLIGHT-CHECKLIST.md`
- `PHASE-EXIT-CHECKLIST.md`
- `NO-FAKE-EXECUTION-RULE.md`
- `COMPLETION-REPORT-CONTRACT.md`

# 33. Workflows

The v1.1 blueprint defines 20 canonical workflows:

1. WF-001 New project from document.
2. WF-002 Existing project X-Ray.
3. WF-003 Clarification and baseline.
4. WF-004 Requirements to tasks.
5. WF-005 UX/design to implementation.
6. WF-006 Architecture/ADR approval.
7. WF-007 Technology/tool evaluation.
8. WF-008 AFIAE.
9. WF-009 AKIS.
10. WF-010 Agent assignment/handoff.
11. WF-011 Controlled implementation.
12. WF-012 Code review/change impact.
13. WF-013 Test/debug/repair.
14. WF-014 Independent verification.
15. WF-015 Release/deployment.
16. WF-016 Production verification.
17. WF-017 Session resume/handoff.
18. WF-018 Transformation.
19. WF-019 Security incident/recovery.
20. WF-020 Closeout/maintenance.

Every workflow must define trigger, purpose, inputs, preflight, steps, outputs, roles, dependencies, approvals, failure paths, retries, evidence, exit criteria and handoff.

# 34. Schemas and registries

## Canonical schemas

Original v1.1 schemas:
- project-profile
- requirement
- assumption
- decision-record
- risk
- task
- agent-role
- agent-handoff
- workflow
- test-case
- verification-evidence
- release-record
- tool-adapter
- technology-entry
- document-metadata
- traceability-link

Additional v1.3 schemas:
- intake-record
- problem-brief
- feature
- design-handoff
- technology-evaluation
- tool-capability-profile
- git-change-record
- deployment-record
- project-state
- audit-event
- knowledge-entry
- source-evidence
- alternative-evaluation
- work-unit
- checkpoint
- completion-report
- rule-check-result

All schemas must be versioned, validated and have valid examples. Do not let examples contain fake claims of actual execution.

## Registries

1. Document registry.
2. Workflow registry.
3. Engine registry.
4. Agent registry.
5. Tool-adapter registry.
6. Technology registry.
7. Standards registry.
8. Template registry.
9. Benchmark registry.
10. Glossary registry.
11. Rule registry.
12. Knowledge/source registry.

Each registry entry must have stable ID, owner/status, version, references, lifecycle metadata and validation rules.

# 35. Agent roles and contracts

Suggested roles:
- Project Analyst.
- Requirements Engineer.
- Product/Business Analyst.
- UX Researcher.
- UX/UI Designer.
- Architect.
- Technology Researcher.
- Database Engineer.
- API/Backend Engineer.
- Frontend Engineer.
- Mobile Engineer.
- AI/ML Engineer.
- Security Reviewer.
- Test Engineer.
- DevOps/Platform Engineer.
- Documentation Engineer.
- Independent Verifier.
- Release Manager.

One tool/agent may perform several roles on a small project. Do not create agents merely to increase count.

Every agent contract defines purpose, scope, non-goals, required context, inputs/outputs, allowed/prohibited tools, security boundaries, approvals, handoff, failure handling, verification duties and limitations.

# 36. Framework validation and benchmarks

## Repository validation

CI should validate:
- Required root/domain docs.
- Unique document/engine/workflow/rule IDs.
- YAML/JSON/schema correctness.
- Required metadata/status.
- Internal links.
- Prompt references.
- Workflow input/output/gate completeness.
- Handoff examples.
- Registry consistency.
- Stale/deprecated tool adapters.
- Version and supersession relationships.

## End-to-end benchmark projects

Use representative cases:
1. Small CRUD web app.
2. Mobile-first PWA.
3. Existing project bug fix with regression risk.
4. Existing project redesign with preservation constraints.
5. API-backed SaaS with auth and tenant isolation.
6. Data-intensive project with migrations.
7. AI-integrated app with prompt-injection/data-leakage risks.

Measure requirement extraction, ambiguity detection, unsupported assumptions, traceability, scope drift, defect escape, test quality, missed security issues, missed usability issues, deployment reproducibility, handoff completeness, approval compliance, cost/time and completion-report truthfulness.

# 37. Implementation roadmap

| Release slice | Deliverable | Exit condition |
|---|---|---|
| R0 | Scope, governance, principles, glossary | Boundaries/laws approved |
| R1 | Three intake modes | Inputs, steps, outputs and gates complete |
| R2 | Engine catalogue/spec template | Every engine contract defined |
| R3 | Project templates/schemas | Sample package validates |
| R4 | Product/requirements/feature analysis | Requirements trace to acceptance |
| R5 | UX/UI and design handoff | Design package implementation-ready |
| R6 | Technology/architecture intelligence | Reproducible evaluation and ADR |
| R7 | AKIS/AFIAE | Provenance, freshness, acquisition approval |
| R8 | Agent/task/handoff orchestration | Cross-agent/session handoff passes |
| R9 | Git/coding-tool adapters | Safe branch workflow demonstrated |
| R10 | Testing/security/performance/UX | Quality gates and evidence work |
| R11 | CI/CD/deployment templates | Safe non-production pipeline works |
| R12 | End-to-end benchmark project | At least one project passes defined gates |
| R13 | Documentation/release/maintenance | Public release checklist passes |

Recommended first proof: one small bounded application through intake, specification, design, implementation, verification and staging deployment. Demonstrate a design handoff, coding-tool handoff, feature branch/PR and automated checks. Do not claim full capability before this works.

# 38. Definition of done for AISDF V1

AISDF V1 is not complete until:
1. Three intake modes are documented, tested and converge on a canonical baseline.
2. Every published engine has purpose, inputs, outputs, workflow, rules, dependencies, owner, failure handling and exit criteria.
3. Knowledge entries have provenance, version and freshness metadata.
4. Consequential decisions include alternatives or a reason for omission.
5. Tool adapters distinguish verified/partial/experimental/unverified.
6. Essential instructions always load; advanced detail is conditional.
7. Completion, pause/resume and handoff protocols exist in prompts/templates/schemas.
8. Rulebook and preflight/exit checks are referenced by workflows.
9. No fake execution or unsupported compatibility claims.
10. Git/PR/CI/deployment examples work in a test repository.
11. At least one end-to-end sample project passes acceptance/verification.
12. CI validates schemas, links, IDs, metadata and registries.
13. Public docs disclose limitations and unverified areas.

# 39. Key tradeoffs and decisions

- Three modes are entry paths, not separate frameworks.
- Engines are capability modules, not automatically agents or microservices.
- Master prompt is an entry point, not the whole framework.
- Assistant, design tool and coding IDE are different roles connected by handoffs.
- Feature-branch push may be authorized; protected merge/production deploy need policy gates.
- Automation depends on actual tool capability and authorization.
- Deployment is provider-neutral.
- Load balancing/advanced infrastructure are conditional.
- Testing is evidence-based.
- No AI Slope applies to AISDF itself.
- Alternatives must be meaningful and requirement-based.
- Freshness metadata does not replace checking official sources before consequential use.
- Independent verification must be meaningfully separated from implementation claims.
- Full completion does not mean blind continuation; stop safely when blocked and checkpoint.

# 40. Open decisions before public repository release

These must be decided by maintainers rather than silently assumed:
- License (Apache-2.0 suggested subject to rights review; MIT alternative).
- Public visibility and maintainers.
- Default branch (`main` proposed).
- Markdown/YAML/JSON conventions.
- Whether Obsidian support is documented as optional.
- Semantic versioning.
- Issue/PR contribution process.
- Governance and security contact.
- Which adapters are included in V1 and their verified status.
- Which standards are normative versus informative.
- CI requirements.
- Whether an optional docs website is approved.
- Whether any future runtime is separately proposed (not part of current repository scope).

# 41. Final capability statement

AISDF is a tool-independent, evidence-based, version-aware and completion-controlled software engineering framework. It helps compatible and authorized AI tools move from a problem statement or existing repository through discovery, product definition, design, technology selection, architecture, implementation, testing, security review, verification, deployment preparation and maintenance.

It must never promise:
- Zero errors or zero vulnerabilities.
- Universal compatibility with every AI tool.
- That a prompt grants access or permissions.
- That code generation equals completion.
- That a green test suite proves absence of defects.
- That deployment occurred without execution evidence.
- That every project needs microservices, load balancers, Kubernetes or complex infrastructure.

Its promise is disciplined process, clear handoffs, current evidence, bounded automation, traceability, safe approvals and honest completion reporting.

---

# PART VII — Full source blueprints

The following appendices preserve the complete original source documents in full. They are retained to make this master artifact self-contained and to preserve detailed domain file maps, workflow specifications, templates, examples, registries, governance and original wording. The consolidated sections above provide the integrated navigation and authority model; the appendices provide the full source detail.


# APPENDIX A — Original AISDF Open-Source GitHub Repository Blueprint v1.0 (Full Source)

# AISDF --- Open-Source GitHub Repository Blueprint

**Project:** AI Software Development Framework (AISDF)\
**Tagline:** From Problem Statement to Production Software\
**Document:** Complete Repository Blueprint\
**Version:** 1.0.0\
**Status:** Proposed open-source repository baseline\
**Scope:** GitHub repository, documentation, knowledge assets, schemas,
rules, templates, examples, validation tools, and community governance.\
**Explicit exclusion:** This blueprint does not specify building or
hosting the AISDF application/platform. AISDF is being defined here as
an open-source software engineering framework that people and AI
development tools can read, adopt, adapt, and execute within their own
environments.

------------------------------------------------------------------------

# 1. Executive Definition

AISDF is an open-source, AI-assisted software development framework that
provides a structured, auditable, and reusable way to move from a
problem statement or an existing codebase to a well-understood,
specified, designed, implemented, tested, secured, verified, deployed,
and maintained software product.

The GitHub repository is the framework's canonical source of truth. It
contains:

-   Engineering methodology and lifecycle workflows.
-   Project discovery and existing-codebase assessment standards.
-   Requirements, product, UX/UI, architecture, and technology guidance.
-   Engineering knowledge documents and verified references.
-   AI agent role definitions, task contracts, rules, and verification
    standards.
-   Security, privacy, execution, and governance policies.
-   Reusable schemas, checklists, templates, examples, and decision
    records.
-   Lightweight scripts and CI checks that validate the repository's own
    content.
-   Contribution, versioning, release, and maintenance governance.

AISDF is **not** a hosted SaaS product, AI coding IDE, model provider,
autonomous agent runtime, project management application, or deployment
platform in this repository scope.

It may describe how to use tools such as Antigravity, Cursor, Codex,
Claude Code, Windsurf, Kiro, Cline, Roo Code, OpenHands, GitHub Copilot,
and other tools. Describing or providing rules for a tool does not make
that tool a runtime dependency.

## 1.1 Core promise

> Give people and AI development tools a reliable engineering framework
> for understanding, planning, building, verifying, and maintaining
> software---without locking them into one model, IDE, cloud provider,
> or technology stack.

## 1.2 Repository principles

1.  **Human-readable first:** Markdown is the primary content format.
2.  **Tool-independent:** Core methodology must not require a particular
    AI vendor or IDE.
3.  **Evidence over claims:** A completed checklist or agent statement
    is not proof that software works.
4.  **Approval before material change:** Scope, product direction,
    architecture, sensitive access, purchases, and production actions
    require the appropriate human authorization.
5.  **Least privilege:** Agent instructions must never grant permissions
    that the execution environment has not granted.
6.  **No AI Slope:** Avoid unnecessary features, dependencies, agents,
    abstractions, context, and infrastructure.
7.  **Change Only Law:** When asked to change one thing, change that
    thing and only the dependencies technically required; preserve
    unrelated behavior.
8.  **Right-sized engineering:** Do not impose enterprise architecture
    on a small project.
9.  **Traceability:** Connect requirements to implementation tasks,
    tests, verification, and evidence.
10. **Portable ownership:** Users own their code, project documents,
    decisions, and outputs.
11. **Verified knowledge:** Time-sensitive technical guidance must
    identify authoritative sources and verification dates.
12. **Explicit uncertainty:** Mark assumptions, unknowns, unverified
    claims, and tool limitations.

------------------------------------------------------------------------

# 2. Scope and Non-Scope

## 2.1 Included in this repository

  -----------------------------------------------------------------------
  Area                                Repository deliverable
  ----------------------------------- -----------------------------------
  Methodology                         New-product, existing-project, and
                                      transformation workflows

  Project intelligence                Inspection and assessment
                                      procedures

  Requirements                        PRD, functional/non-functional
                                      requirements, acceptance criteria

  Product engineering                 Validation, MVP, prioritization,
                                      roadmap methods

  UX/UI                               Research, flows, design-system and
                                      accessibility standards

  Technology intelligence             Evaluation criteria, comparison
                                      templates, source policy

  Architecture                        Architecture methods, diagrams, ADR
                                      templates, review checklists

  Knowledge                           Modular engineering knowledge
                                      documents

  AI/agents                           Agent roles, task contracts,
                                      prompts/rules, evaluation guidance

  Orchestration                       Tool-independent workflow, handoff,
                                      conflict, and recovery standards

  Harness                             Secure execution requirements and
                                      policy guidance

  Security/privacy                    Threat modeling, secure
                                      development, privacy and governance
                                      standards

  Data/API                            Data modeling, API, event, and
                                      integration design guidance

  Testing                             Test strategy, verification,
                                      evidence and quality standards

  Delivery/operations                 CI/CD, deployment, monitoring,
                                      incident and recovery guidance

  AFIAE                               External capability
                                      discovery/evaluation/acquisition
                                      methodology

  External tool integration           IDE, CLI, MCP, Git and
                                      human-mediated integration guidance

  Templates                           Reusable project and engineering
                                      templates

  Examples                            Small illustrative examples and
                                      reference workflows

  Validation                          Scripts and CI checks for
                                      repository quality

  Governance                          Contribution, release, versioning,
                                      security reporting and maintenance
  -----------------------------------------------------------------------

## 2.2 Explicitly excluded

The repository does not build or operate:

-   A web application or dashboard.
-   A SaaS backend or API server.
-   A hosted AI agent orchestration service.
-   A model gateway or model hosting platform.
-   A database-backed project management application.
-   A sandbox execution service.
-   A cloud deployment platform.
-   A billing or subscription system.
-   An autonomous purchasing or installation service.
-   A proprietary IDE or code editor.

A future project may implement some of these capabilities, but it must
be separately proposed and approved. Do not silently turn this
repository into an application monorepo.

## 2.3 Repository automation boundary

Lightweight repository tooling is allowed when it validates or maintains
the framework itself. Examples:

-   Markdown linting.
-   YAML and JSON schema validation.
-   Broken-link checking.
-   Required metadata checks.
-   Duplicate document ID checks.
-   Knowledge freshness reports.
-   Template/example validation.
-   Documentation site generation, if later approved.

These tools must not become a hidden application runtime.

------------------------------------------------------------------------

# 3. Intended Users and Usage Modes

## 3.1 Target audiences

-   Students and beginners.
-   Individual developers.
-   Professional software engineers.
-   Product designers.
-   Technical founders.
-   Startups and small teams.
-   Engineering organizations.
-   AI-assisted development tool users.

## 3.2 Framework usage modes

### Beginner Mode

Guided explanations, plain-language questions, staged decisions, and
explicit approval points.

### Developer Mode

Technical specifications, architecture, APIs, database design,
implementation mapping, test planning, and engineering review.

### Team Mode

Task ownership, reviews, handoffs, shared decisions, and team
governance.

### Enterprise Adoption Mode

Organization policies, security controls, evidence requirements,
auditability, and compliance mapping. AISDF provides guidance and
templates; it does not certify compliance.

------------------------------------------------------------------------

# 4. Development Methodology

AISDF provides three connected paths.

## 4.1 Path 0 --- Venture and Business Validation (optional)

1.  Starving Crowd Check.
2.  Model a Proven Winner.
3.  Founder-Market Fit.
4.  Inversion Thinking.
5.  Premortem.
6.  Pre-Commit Kill Criteria.
7.  Market Timing.
8.  Build Offer.
9.  Disciplined Execution.
10. Feedback Loops.
11. Check Kill Criteria.
12. Resource Reinvestment.
13. Defend Moat.
14. Systemize and Delegate.

This path is optional. It must not block technical work when the user is
building an internal, educational, experimental, or non-commercial
project.

## 4.2 Path A --- New Product Development

1.  Problem and user check.
2.  Proven-product and alternatives check.
3.  Product/build fit.
4.  Inversion and premortem.
5.  Go/kill criteria.
6.  Product and MVP definition.
7.  Scope freeze.
8.  UX/UI and design system.
9.  Architecture and source of truth.
10. Implementation mapping.
11. AI-assisted development.
12. Verification, security, and QA.
13. Deployment, observation, and launch.
14. Feedback, iteration, and scaling.

## 4.3 Path B --- Existing Project Development

1.  Project X-Ray.
2.  Current-state check.
3.  Exact change request.
4.  Impact and dependency analysis.
5.  Scope and acceptance criteria.
6.  Minimum safe plan.
7.  AI implementation map.
8.  Controlled changes.
9.  Verification.
10. Regression testing.
11. Security, performance, and UX QA.
12. Build and deployment.
13. Documentation and source-of-truth updates.
14. Close and monitor.

## 4.4 Product transformation

-   **Direction A --- Improve:** Improve the existing product while
    preserving its concept.
-   **Direction B --- Redesign:** Redesign while preserving the core
    purpose.
-   **Direction C --- Transform:** Change the product direction,
    architecture, or purpose. Explicitly decide what to reuse, replace,
    migrate, retire, or run in parallel.

AISDF must not choose a transformation direction without approval.

## 4.5 Core existing-project workflow

**Inspect → Understand → Analyze → Discover → Compare → Document →
Approve → Implement → Verify.**

## 4.6 Universal workflow

**Discovery → Problem Definition → Validation → Requirements → Product
Definition → Technology Intelligence → UX/UI → Architecture →
Documentation → Implementation Planning → Development → Testing/Security
→ Independent Verification → Delivery → Production Verification →
Maintenance.**

------------------------------------------------------------------------

# 5. Mandatory Framework Laws

These rules apply across all methodology paths and agent instructions.

## 5.1 Change Only Law

When the request targets a specific feature or behavior:

-   Modify the requested scope.
-   Modify only technically necessary dependencies.
-   Preserve unrelated features, design, behavior, and architecture.
-   Identify unavoidable collateral changes before making them.
-   Record and explain any deviation.

## 5.2 No AI Slope

Do not add unnecessary:

-   Features.
-   Abstractions.
-   Dependencies.
-   Services.
-   Agents.
-   Prompts.
-   Context.
-   Infrastructure.
-   Refactors.
-   Configuration.
-   Automation.

Every addition must solve an identified requirement or risk.

## 5.3 Approval First

Require the appropriate approval before material changes to:

-   Product direction.
-   Scope.
-   Requirements.
-   Architecture.
-   Data migrations with material risk.
-   Security policy.
-   Sensitive permissions.
-   Paid services or purchases.
-   Production deployment.
-   Destructive operations.

## 5.4 Evidence Over Claims

"Implemented," "tested," "secure," "deployed," and "complete" are claims
that require evidence appropriate to the claim.

## 5.5 No Authority Escalation

Delegation, provider switching, task splitting, MCP use, CLI execution,
or tool chaining must not increase the authority granted to an agent.

## 5.6 Default Deny and Least Privilege

Agent instructions are not security enforcement. The operating system,
sandbox, credentials, network, and external platform must enforce
permissions.

## 5.7 Right-Sized Engineering

Select the simplest architecture that satisfies verified requirements
and foreseeable constraints.

## 5.8 Source-of-Truth Law

Project state, approved decisions, requirements, and evidence must live
in the project's authoritative records. Chat memory is not the project's
source of truth.

------------------------------------------------------------------------

# 6. Repository Information Architecture

## 6.1 Recommended root structure

``` text
AISDF/
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── GOVERNANCE.md
├── SUPPORT.md
├── CHANGELOG.md
├── VERSION
├── CITATION.cff
├── .gitignore
├── .editorconfig
├── .markdownlint.jsonc
│
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
│
├── schemas/
├── registries/
├── workflows/
├── templates/
├── examples/
├── tests/
├── tools/
├── assets/
│
└── .github/
    ├── ISSUE_TEMPLATE/
    ├── PULL_REQUEST_TEMPLATE.md
    ├── DISCUSSION_TEMPLATE/
    ├── workflows/
    ├── CODEOWNERS
    └── dependabot.yml
```

The 31 numbered domains are retained as the canonical knowledge domains.
The root-level `templates/` and `examples/` folders may contain
cross-domain starter assets; domain-specific authoritative material
belongs in its numbered domain. Avoid duplicate canonical documents.

## 6.2 Domain ownership

  -----------------------------------------------------------------------
  Domain                              Canonical responsibility
  ----------------------------------- -----------------------------------
  00 Governance                       Rules, ownership, contribution,
                                      release policy

  01 Methodology                      Path 0, Path A, Path B, lifecycle
                                      and laws

  02 Project Intelligence             Intake, X-Ray, assessment, state
                                      analysis

  03 Requirements Engineering         Requirements, scope, acceptance and
                                      traceability

  04 Product Engineering              Validation, product strategy, MVP
                                      and roadmap

  05 UX/UI Engineering                Research, flows, design systems and
                                      accessibility

  06 Technology Intelligence          Technology evaluation and
                                      official-source research

  07 Engineering Knowledge            Cross-cutting engineering
                                      fundamentals and practices

  08 Software Architecture            Architecture methods, diagrams and
                                      ADRs

  09 Platform Engineering             Developer platforms, environments
                                      and platform practices

  10 AI and Model Engineering         Models, inference, evaluation and
                                      provider concepts

  11 Agent Engineering                Agent roles, contracts, memory,
                                      tools and evaluation

  12 Orchestration and Context        Workflows, routing, retrieval and
                                      context management

  13 Harness and Execution            Sandboxes, tool execution and
                                      permission enforcement

  14 Security and Privacy             Threats, controls, privacy and
                                      incident security

  15 Data and Database Engineering    Data modeling, databases,
                                      migrations and lifecycle

  16 API and Integration Engineering  APIs, events, connectors and
                                      contracts

  17 Testing and Verification         Test design, independent
                                      verification and evidence

  18 DevOps and Cloud Engineering     CI/CD, infrastructure as code and
                                      cloud practices

  19 Deployment and Operations        Releases, deployment, rollback and
                                      operational procedures

  20 Reliability and Observability    SLOs, logs, metrics, traces and
                                      incident reliability

  21 Distributed Systems and          Concurrency, queues, scaling and
  Scalability                         distributed design

  22 Cost and Resource Governance     Budgets, quotas, cost measurement
                                      and optimization

  23 Legal and Compliance             Licenses, privacy obligations and
                                      compliance mapping

  24 Product Analytics and Support    Product metrics, support and
                                      feedback

  25 Framework Maintenance            Knowledge freshness, framework
                                      upgrades and deprecation

  26 Distribution and Extensions      Repository distribution,
                                      CLI/SDK/plugin guidance

  27 Standards and Compatibility      Standards registry, compatibility
                                      and lifecycle

  28 Templates and Examples           Reusable project and engineering
                                      assets

  29 Benchmarks and Evaluation        Framework and agent evaluation
                                      scenarios

  30 Agent Rules and Verification     Agent-specific rules, constraints
                                      and verification
  -----------------------------------------------------------------------

## 6.3 Required domain landing pages

Every domain must contain:

-   `README.md` --- domain overview and navigation.
-   `INDEX.md` --- canonical document registry for the domain.
-   `01-...md` --- primary topic documents.
-   `02-...-ALTERNATIVES.md` --- alternatives where meaningful.
-   `03-...-AGENT-RULES-AND-VERIFICATION.md` --- conditional agent
    rules.
-   `examples/` --- only where examples materially help.
-   `templates/` --- only where reusable templates are needed.

Do not create empty placeholder files merely to make every folder look
complete. A domain may be marked `Planned` until it has useful content.

------------------------------------------------------------------------

# 7. Documentation Standard

## 7.1 Document types

  Type           Purpose
  -------------- -----------------------------------------------
  Principle      Stable rule or engineering principle
  Methodology    Repeatable workflow
  Standard       Normative requirement
  Guide          Explanatory implementation guidance
  Reference      Structured technical facts or API information
  Decision       Recorded choice and alternatives
  Checklist      Review or execution aid
  Template       Reusable document structure
  Example        Illustrative application
  Benchmark      Repeatable evaluation
  Agent Rule     Agent behavior and boundaries
  Verification   Evidence and acceptance requirements

## 7.2 Standard topic document structure

``` markdown
---
id: AISDF-EXAMPLE-001
title: Example Engineering Topic
domain: 07-ENGINEERING-KNOWLEDGE
version: 1.0.0
status: Draft
document_type: guide
owner: AISDF Maintainers
last_verified: YYYY-MM-DD
next_review: YYYY-MM-DD
related_documents: []
official_sources: []
---

# Title

## 1. Purpose
## 2. Scope
## 3. Definitions
## 4. Fundamentals
## 5. Internal Working
## 6. Architecture
## 7. Workflow
## 8. Implementation Guidance
## 9. Best Practices
## 10. Security and Privacy
## 11. Testing and Verification
## 12. Production Considerations
## 13. Limitations and Trade-offs
## 14. Alternatives
## 15. Common Mistakes
## 16. AISDF Integration
## 17. Examples
## 18. Checklist
## 19. References
## 20. Change History
```

Not every heading is mandatory for every document. Authors must remove
irrelevant sections rather than fill them with meaningless text.

## 7.3 Metadata rules

Required metadata:

-   `id`
-   `title`
-   `domain`
-   `version`
-   `status`
-   `document_type`
-   `owner`
-   `last_verified`
-   `related_documents`

Recommended metadata:

-   `next_review`
-   `official_sources`
-   `tags`
-   `applicability`
-   `technology_versions`
-   `supersedes`

Allowed statuses:

-   Draft.
-   In Review.
-   Approved.
-   Deprecated.
-   Retired.

A Draft document must not be presented as an approved standard.

## 7.4 Document IDs

Use stable IDs, for example:

-   `AISDF-METH-001`
-   `AISDF-REQ-001`
-   `AISDF-ARCH-001`
-   `AISDF-AKIS-001`
-   `AISDF-AFIAE-001`
-   `AISDF-SEC-001`
-   `AISDF-AGENT-001`

Do not reuse IDs after retirement.

## 7.5 Links and references

-   Use relative Markdown links for repository portability.
-   Link to canonical documents rather than duplicating them.
-   Prefer official documentation for technical claims.
-   Record source title, URL, publisher, version/date where available,
    and last-verified date.
-   Clearly distinguish normative rules from recommendations and
    examples.
-   Do not cite a source as support for a claim it does not establish.

------------------------------------------------------------------------

# 8. Core Repository Registries

Registries are structured records that make the framework navigable and
machine-checkable. They are not a runtime database.

## 8.1 Document Registry

Tracks document ID, path, title, domain, type, status, version, owner,
review date, and relationships.

## 8.2 Technology Registry

Tracks:

-   Technology ID and name.
-   Category.
-   Official website and documentation.
-   Supported versions.
-   License.
-   Maturity and maintenance state.
-   Security advisories.
-   Compatibility.
-   Alternatives.
-   Last verified date.
-   Source references.

## 8.3 Standards Registry

Tracks:

-   Standard ID.
-   Publisher.
-   Standard name.
-   Version.
-   Official source.
-   Applicability.
-   AISDF mapping.
-   Adoption status.
-   Review date.

Standards may include OWASP, NIST SSDF, NIST CSF, NIST AI RMF, CWE/CVE,
SLSA, OpenSSF, and WCAG. AISDF must record the exact version and
applicability it discusses. Listing a standard does not establish
compliance.

## 8.4 Agent Registry

Tracks:

-   Agent ID.
-   Role.
-   Purpose.
-   Responsibilities.
-   Non-responsibilities.
-   Required inputs.
-   Expected outputs.
-   Tools.
-   Permission assumptions.
-   Prohibited actions.
-   Handoff rules.
-   Verification requirements.
-   Evaluation scenarios.

## 8.5 Tool and Connector Registry

Tracks:

-   Tool ID.
-   Provider.
-   Product.
-   Category.
-   Official documentation.
-   Integration methods.
-   Verified capabilities.
-   Authentication model.
-   Permission scopes.
-   Data handling.
-   Pricing model.
-   License/terms.
-   Limitations.
-   Compatibility.
-   Security review.
-   Last verified date.

A tool's inclusion in the registry does not mean AISDF has a working
integration with it.

## 8.6 Template Registry

Tracks template ID, purpose, file path, required fields, applicable
lifecycle phase, version, owner, and validation method.

## 8.7 Workflow Registry

Tracks workflow ID, trigger, inputs, stages, decision gates, outputs,
responsible roles, failure paths, and acceptance criteria.

------------------------------------------------------------------------

# 9. Knowledge Engineering and AKIS

AKIS is the repository's knowledge organization and retrieval
methodology. In this repository scope, it is documented and may have
lightweight indexing/validation scripts. It is not a hosted retrieval
service.

## 9.1 Authoring and source of truth

-   Obsidian may be used as a local authoring interface.
-   Markdown files in Git are the canonical content.
-   GitHub is the collaboration and version history location.
-   AISDF documentation must remain readable without Obsidian.
-   Runtime systems, if separately developed in the future, must not
    depend on the Obsidian application.

## 9.2 Knowledge document quality

Each technical knowledge document should answer, as applicable:

1.  What is it?
2.  Why does it exist?
3.  How does it work internally?
4.  What architecture does it use?
5.  When should it be used?
6.  When should it not be used?
7.  What are its alternatives?
8.  What are its limitations?
9.  What security concerns apply?
10. How is it tested?
11. How is it operated in production?
12. How does it connect to AISDF workflows?

## 9.3 Retrieval design guidance

A future AKIS implementation may use:

1.  Metadata filtering.
2.  Domain and section selection.
3.  Keyword retrieval.
4.  Semantic retrieval when justified.
5.  Dependency-aware retrieval.
6.  Permission filtering.
7.  Deduplication.
8.  Ranking.
9.  Context budgeting.
10. Source/version attachment.

Obsidian does not itself guarantee token savings. Savings come from
modular content, selective retrieval, ranking, deduplication, and
context budgets.

## 9.4 Knowledge freshness

-   Mark fast-changing documentation with a review interval.
-   Prefer official sources.
-   Track technology version applicability.
-   Re-check links and critical technical claims.
-   Retain the last known valid content if an update fails.
-   Mark unverified or stale content clearly.
-   Do not automatically promote a newly ingested document to Approved
    status.

------------------------------------------------------------------------

# 10. AFIAE --- Feature Intelligence and Acquisition Methodology

AFIAE is a framework methodology for discovering and evaluating external
capabilities. It is not an automated purchasing service in this
repository.

## 10.1 Discovery categories

-   APIs.
-   SDKs.
-   Libraries.
-   Plugins.
-   MCP servers.
-   Agent skills.
-   AI models.
-   Developer tools.
-   Infrastructure.
-   Templates.
-   Premium services.
-   Integration connectors.

## 10.2 Workflow

**Requirement → Capability Gap → Discovery → Source Verification →
Feature Evaluation → Pricing/License Review → Security Review →
Compatibility Review → Comparison → Approval → Authorized Acquisition →
Integration → Verification → Monitoring.**

## 10.3 Capability evaluation criteria

-   Relevance to the requirement.
-   Functional completeness.
-   Official source confidence.
-   Maintenance and release activity.
-   Version compatibility.
-   Security posture.
-   License and usage terms.
-   Pricing and total cost.
-   Data handling and privacy.
-   Permissions required.
-   Portability and exit cost.
-   Operational support.
-   Alternatives.
-   Failure and rollback behavior.

## 10.4 Acquisition rules

-   Discovery and comparison may be automated within policy.
-   Installation, credential access, purchases, paid subscriptions, and
    production changes require authorization.
-   No paywall or license bypass.
-   No untrusted installation.
-   No automatic privilege expansion.
-   No credential publication.
-   No silent dependency replacement.

------------------------------------------------------------------------

# 11. AI, Agent, and External Tool Standards

## 11.1 Tool-independent design

AISDF defines common task and verification standards. It must not assume
all AI tools expose the same features or APIs.

Candidate tools to document and evaluate include:

-   Google Antigravity.
-   Cursor.
-   Windsurf.
-   Kiro.
-   Trae.
-   Codex.
-   Claude Code.
-   GitHub Copilot.
-   Cline.
-   Roo Code.
-   Aider.
-   OpenHands.
-   Devin.
-   Replit.
-   Lovable.
-   Bolt.new.
-   v0.

The repository must separate:

-   **Knowledge compatibility:** Can the tool read and follow AISDF
    documents?
-   **Execution compatibility:** Can it perform the required operations
    in its own environment?
-   **Integration compatibility:** Can AISDF or another controller
    interact with it through a verified interface?

These are different claims.

## 11.2 Standard agent task contract

A task contract should include:

-   Task ID.
-   Project ID.
-   Agent role.
-   Objective.
-   Input references.
-   Requirements.
-   Dependencies.
-   Allowed files.
-   Allowed tools.
-   Permission assumptions.
-   Expected output.
-   Acceptance criteria.
-   Budget/deadline where applicable.
-   Verification requirements.
-   Status.
-   Evidence references.

## 11.3 Agent rules

Agent instructions must define:

-   Role and scope.
-   Required context.
-   Expected output format.
-   Allowed tools.
-   Prohibited actions.
-   Approval gates.
-   Security constraints.
-   Handoff requirements.
-   Failure behavior.
-   Verification expectations.

Never present prompt instructions as a substitute for technical access
control.

## 11.4 Collaboration and conflict rules

-   One explicit owner per task.
-   Explicit file ownership for parallel work.
-   Separate branches/worktrees for concurrent edits.
-   No uncontrolled simultaneous edits to the same working directory.
-   Review diffs before merging.
-   Run relevant tests after merging.
-   Escalate conflicting architectural decisions.
-   Record the final decision.

## 11.5 Independent verification

The implementing agent should not be the sole source of acceptance for
critical changes. Use a separate reviewer, test process, or verification
context where practical. Different agents using the same model and
identical context are not automatically independent.

------------------------------------------------------------------------

# 12. Security, Privacy, and Safe Use

## 12.1 Security principles

-   Default deny.
-   Least privilege.
-   Explicit trust boundaries.
-   Project and tenant isolation.
-   Scoped credentials.
-   Secure secret handling.
-   Sandboxed execution.
-   Network restrictions.
-   Dependency verification.
-   Auditability.
-   Human approval for high-impact actions.
-   Emergency stop and recovery.

## 12.2 Threat categories to document

-   Prompt injection.
-   Malicious repository content.
-   Malicious tool output.
-   Credential theft.
-   Secret leakage.
-   Unauthorized file access.
-   Command abuse.
-   Sandbox escape.
-   SSRF.
-   Network exfiltration.
-   Dependency/supply-chain compromise.
-   Tenant boundary violation.
-   Privilege escalation.
-   Destructive migration.
-   Unauthorized deployment.
-   Denial of service.
-   Data retention/deletion failure.

## 12.3 Security documentation requirements

Each security guide should include:

-   Threat.
-   Assets.
-   Trust boundaries.
-   Attack surface.
-   Preconditions.
-   Preventive controls.
-   Detection.
-   Response.
-   Recovery.
-   Verification tests.
-   Residual risk.

## 12.4 Privacy

Guidance must address:

-   Purpose limitation.
-   Data minimization.
-   Consent where required.
-   Retention.
-   Export.
-   Deletion propagation.
-   Derived data and indexes.
-   Backups.
-   Third-party processors.
-   Cross-border transfers.
-   Incident handling.
-   Legal holds.

## 12.5 Responsible disclosure

`SECURITY.md` must state how maintainers receive vulnerability reports,
expected response process, supported versions, and what information
reporters should provide. Do not publish exploitable details before
coordinated disclosure.

------------------------------------------------------------------------

# 13. Data, API, and Integration Engineering Guidance

These are knowledge and design standards for projects using AISDF, not
services built by this repository.

## 13.1 Data modeling

Every project data model should define:

-   Entity identity.
-   Ownership.
-   Attributes.
-   Relationships.
-   Constraints.
-   Validation.
-   Lifecycle.
-   Versioning.
-   Access rules.
-   Retention.
-   Audit requirements.
-   Migration behavior.

## 13.2 API design

Document:

-   API purpose and consumers.
-   Authentication and authorization.
-   Request/response schemas.
-   Validation.
-   Versioning.
-   Error format.
-   Pagination.
-   Rate limits.
-   Timeouts.
-   Idempotency.
-   Deprecation.
-   Observability.
-   Contract tests.

## 13.3 Event design

Document:

-   Event name and owner.
-   Schema and version.
-   Producer and consumers.
-   Delivery guarantees.
-   Ordering requirements.
-   Duplicate handling.
-   Retry policy.
-   Dead-letter handling.
-   Replay.
-   Retention.
-   Privacy classification.

## 13.4 External integration lifecycle

**Register → Authenticate → Discover → Evaluate → Approve → Connect →
Verify → Monitor → Upgrade → Revoke.**

------------------------------------------------------------------------

# 14. Testing, Verification, and Evidence Standards

## 14.1 Test categories

-   Unit.
-   Integration.
-   Contract.
-   End-to-end.
-   Regression.
-   Acceptance.
-   Performance.
-   Load.
-   Stress.
-   Spike.
-   Endurance.
-   Accessibility.
-   Visual.
-   Browser/device compatibility.
-   Recovery.
-   Security.
-   Dependency.
-   Secret scanning.
-   Infrastructure.
-   AI behavior.
-   Retrieval quality.
-   Agent workflow.

Select tests based on project risk and requirements. Not every project
needs every test category.

## 14.2 Traceability chain

**Requirement → Task → Code Change → Test → Verification → Evidence →
Release.**

## 14.3 Evidence record

An evidence record should identify:

-   Evidence ID.
-   Project.
-   Requirement.
-   Task.
-   Source revision.
-   Environment.
-   Test or verification procedure.
-   Runner/tool.
-   Timestamp.
-   Result.
-   Logs and artifacts.
-   Status.
-   Reviewer where applicable.

Evidence for an older revision must not be used to claim a newer
revision is verified.

## 14.4 Quality gates

Critical failures cannot be hidden by averaging a quality score. Define
blockers for security, data integrity, authorization, requirement
failures, and release safety.

------------------------------------------------------------------------

# 15. Delivery, Operations, and Maintenance Guidance

The repository documents how projects should approach:

-   Source control.
-   Branching and code review.
-   CI/CD.
-   Build reproducibility.
-   Artifact provenance.
-   SBOM and dependency scanning where appropriate.
-   Environment configuration.
-   Secrets management.
-   Release versioning.
-   Feature flags.
-   Canary, rolling, and blue-green deployments where appropriate.
-   Deployment authorization.
-   Post-deployment verification.
-   Monitoring.
-   SLOs/SLIs.
-   Incident response.
-   Backup and restore.
-   Disaster recovery.
-   Rollback.
-   Maintenance windows.
-   Deprecation and end-of-life.

AISDF must not prescribe universal SLO numbers without project
requirements and measurements.

------------------------------------------------------------------------

# 16. Technology and Tool Evaluation Policy

## 16.1 Technology selection criteria

Evaluate:

-   Requirement fit.
-   Compatibility.
-   Security.
-   Performance.
-   Scalability.
-   Reliability.
-   Maintainability.
-   Maturity.
-   Community and support.
-   License.
-   Pricing and total cost.
-   Data portability.
-   Vendor lock-in.
-   Upgrade path.
-   End-of-life risk.

## 16.2 Tool catalog policy

The repository may include a catalog of tools such as Antigravity,
Cursor, Codex, Claude Code, Windsurf, Kiro, Figma, GitHub, Obsidian,
Postman, and others.

Every entry must state:

-   What it is.
-   What problem it solves.
-   Relevant capabilities.
-   Limitations.
-   Supported integration method, if verified.
-   Pricing model with verification date.
-   License/terms reference.
-   Data and privacy considerations.
-   Alternatives.
-   Last checked date.

Do not hard-code pricing in stable methodology documents. Keep dynamic
pricing in a separately reviewed catalog.

Do not imply endorsement, partnership, sponsorship, or official
integration without evidence.

------------------------------------------------------------------------

# 17. Templates and Examples

The repository should provide reusable templates.

## 17.1 Project templates

-   Project Intake.
-   Problem and Solution Specification.
-   Project X-Ray.
-   Existing Project Assessment.
-   Product Requirements Document.
-   Functional Requirements.
-   Non-Functional Requirements.
-   MVP Scope.
-   Feature Inventory.
-   User Stories.
-   Acceptance Criteria.
-   Risk Register.
-   Product Roadmap.
-   Project State Summary.

## 17.2 Engineering templates

-   UX Research.
-   User Journey.
-   User Flow.
-   Design System Specification.
-   Technology Evaluation.
-   Architecture Specification.
-   Architecture Decision Record.
-   Component Specification.
-   Database Design.
-   API Specification.
-   Event Contract.
-   Integration Specification.
-   Threat Model.
-   Test Plan.
-   Verification Report.
-   Deployment Plan.
-   Incident Report.
-   Recovery Plan.

## 17.3 AI and agent templates

-   Agent Definition.
-   Agent Task Contract.
-   Prompt Specification.
-   Provider Evaluation.
-   Tool/Connector Evaluation.
-   Agent Handoff.
-   Agent Conflict Report.
-   Execution Report.
-   AI Evaluation Report.
-   Independent Verification Report.

## 17.4 Example projects

Start with small, illustrative examples:

1.  Static website.
2.  CRUD web application.
3.  SaaS application with tenant boundaries.
4.  Backend API.
5.  Mobile application.
6.  AI/RAG application.
7.  Existing project improvement.
8.  Product transformation.
9.  Security-sensitive workflow.
10. Multi-agent controlled implementation.

Examples must be labeled illustrative, not production-certified
reference implementations.

------------------------------------------------------------------------

# 18. Repository Validation Tooling

This repository may include lightweight scripts under `tools/` and
validation cases under `tests/`.

## 18.1 Required validation checks

  Check                     Purpose
  ------------------------- -----------------------------------------
  Markdown lint             Consistent Markdown
  YAML parse                Valid front matter
  JSON validation           Valid structured registries
  Schema validation         Registry records match schemas
  Document ID check         No duplicate IDs
  Required metadata check   Required fields exist
  Link check                Internal links resolve
  Registry/path check       Registry paths exist
  Status check              Drafts not presented as approved
  Source metadata check     Technical claims have source metadata
  Template validation       Required fields are present
  Navigation check          Domain indexes point to valid documents

## 18.2 Suggested tooling

Use simple, maintainable tools. Candidate tools include:

-   Markdownlint.
-   Prettier for supported formatting.
-   A YAML parser.
-   JSON Schema validator.
-   Link checker.
-   Small scripts in Python or Node.js.

Choose one implementation language for repository validation scripts
unless a clear reason requires more than one. Pin tool versions and
document how to run checks locally.

## 18.3 CI workflow

A pull request should run:

1.  Markdown lint.
2.  YAML/JSON parse.
3.  Schema validation.
4.  Duplicate ID detection.
5.  Internal link validation.
6.  Registry consistency.
7.  Required metadata checks.
8.  Template validation.
9.  Example validation where automated.
10. Documentation build, if a documentation site is introduced.

CI validates repository quality. It does not prove that the engineering
advice is universally correct.

------------------------------------------------------------------------

# 19. GitHub Collaboration and Governance

## 19.1 Required repository files

### README.md

Must explain:

-   What AISDF is.
-   What it is not.
-   Who should use it.
-   Core principles.
-   Development paths.
-   Repository navigation.
-   Quick-start adoption path.
-   Contribution links.
-   License.
-   Current maturity and limitations.

### CONTRIBUTING.md

Must explain:

-   Issue-first contribution for significant changes.
-   Branch naming.
-   Document ID rules.
-   Metadata requirements.
-   Writing style.
-   Source requirements.
-   Testing requirements.
-   Pull request requirements.
-   Review and approval process.

### CODE_OF_CONDUCT.md

Defines respectful participation and enforcement.

### GOVERNANCE.md

Defines maintainer roles, decision-making, standards approval, release
authority, and dispute resolution.

### SECURITY.md

Defines vulnerability reporting and response.

### SUPPORT.md

Explains where users ask questions, report documentation problems, or
request changes.

### CHANGELOG.md

Records user-visible framework changes by release.

### CITATION.cff

Provides citation metadata for academic and research use.

## 19.2 GitHub issue types

Recommended issue categories:

-   Bug in documentation.
-   Incorrect or stale technical guidance.
-   New engineering topic.
-   Methodology improvement.
-   Template request.
-   Agent rule proposal.
-   Tool compatibility report.
-   Security issue.
-   Benchmark proposal.
-   Governance proposal.

## 19.3 Pull request requirements

Every PR should state:

-   Purpose.
-   Scope.
-   Related issue.
-   Affected domains.
-   Documents added/changed/retired.
-   Source verification.
-   Security/privacy impact.
-   Compatibility impact.
-   Validation performed.
-   Migration or deprecation notes.
-   Required reviewer approval.

## 19.4 CODEOWNERS

Assign maintainers by domain when the project has enough maintainers.
Until then, use a small maintainer group and avoid fictitious ownership
assignments.

## 19.5 Decision authority

-   Contributors propose changes.
-   Domain maintainers review technical content.
-   Security maintainers review security-sensitive guidance.
-   Project maintainers approve cross-domain or framework-level changes.
-   Release maintainers publish versions.

The exact people and team names must be filled in by repository owners.

------------------------------------------------------------------------

# 20. Open-Source Licensing and Intellectual Property

## 20.1 Recommended default

Evaluate **Apache License 2.0** as the preferred initial license because
it is permissive and includes an express patent grant. MIT is a simpler
permissive alternative.

This is a project recommendation, not legal advice. The repository owner
should confirm ownership of all contributed material and review
third-party content before publishing.

## 20.2 Licensing rules

-   Put the selected license in the root `LICENSE`.
-   Add copyright/attribution notices where required.
-   Preserve third-party license obligations.
-   Do not copy proprietary documentation or large copyrighted passages.
-   Prefer original explanations and links to official sources.
-   Record third-party assets and licenses.
-   Define a contribution policy.
-   Consider a Developer Certificate of Origin (DCO) or Contributor
    License Agreement only after an explicit governance decision.

## 20.3 Trademarks

AISDF may refer to third-party product names for compatibility and
descriptive purposes. Do not use third-party logos or imply endorsement
without permission.

------------------------------------------------------------------------

# 21. Versioning and Release Policy

## 21.1 Framework version

Use Semantic Versioning:

-   **MAJOR:** Breaking methodology, schema, or normative-rule changes.
-   **MINOR:** Backward-compatible additions.
-   **PATCH:** Corrections and non-breaking clarifications.

For a documentation framework, define what counts as a breaking change
in `GOVERNANCE.md`.

## 21.2 Document versions

Individual documents may have their own version and status. The
repository release records a coherent snapshot of all approved
documents.

## 21.3 Release channels

-   Draft/pre-release.
-   Stable.
-   Long-term-support (only if maintainers commit to supporting it).

Do not promise LTS until maintenance capacity exists.

## 21.4 Deprecation

A deprecated document must state:

-   Why it is deprecated.
-   Replacement document, if any.
-   Effective version/date.
-   Migration guidance.
-   Retirement conditions.

Never silently delete an important normative standard without recording
the change.

------------------------------------------------------------------------

# 22. Open-Source Adoption Workflow

A new user should be able to adopt AISDF without installing a
proprietary AISDF application.

## 22.1 Quick adoption

1.  Read the root README.
2.  Select Beginner, Developer, Team, or Enterprise Governance guidance.
3.  Choose Path A for a new product or Path B for an existing project.
4.  Copy the relevant templates into the user's own project repository.
5.  Complete the project intake.
6.  Record assumptions and constraints.
7.  Follow the relevant workflow.
8.  Select compatible AI tools if desired.
9.  Give the AI tool the relevant AISDF rules and knowledge.
10. Review all plans and approvals.
11. Implement in the user's own development environment.
12. Run tests and collect evidence.
13. Maintain the project's own source of truth.

## 22.2 AI tool adoption

AISDF should provide a tool-independent core instruction file and
optional tool-specific adapters/rules.

Do not make the core framework dependent on one IDE's configuration
format.

Suggested structure:

``` text
30-AGENT-RULES-AND-VERIFICATION/
├── CORE/
│   ├── AISDF-CORE-RULES.md
│   ├── CHANGE-ONLY-LAW.md
│   ├── NO-AI-SLOPE.md
│   ├── APPROVAL-FIRST.md
│   ├── EVIDENCE-OVER-CLAIMS.md
│   └── SECURITY-BOUNDARIES.md
│
└── ADAPTERS/
    ├── ANTIGRAVITY/
    ├── CURSOR/
    ├── CLAUDE-CODE/
    ├── CODEX/
    ├── WINDSURF/
    ├── KIRO/
    ├── CLINE/
    └── GENERIC/
```

Each adapter must identify its supported features, version assumptions,
limitations, and last verification date. A generic adapter remains
available for tools not listed.

------------------------------------------------------------------------

# 23. Repository Maintenance

## 23.1 Maintenance responsibilities

-   Review technical sources.
-   Update version-specific guidance.
-   Check broken links.
-   Review security guidance.
-   Validate schemas and templates.
-   Retire obsolete material.
-   Resolve duplicate documents.
-   Review tool compatibility.
-   Maintain benchmark scenarios.
-   Publish release notes.

## 23.2 Review frequency

Use risk-based review intervals rather than one universal schedule.

  -----------------------------------------------------------------------
  Content                             Suggested review
  ----------------------------------- -----------------------------------
  Security and vulnerability guidance Frequent and event-driven

  AI tools and provider capabilities  Frequent

  Framework methodology               Periodic

  Stable engineering fundamentals     Less frequent

  Version-specific technology guides  Around supported-version changes

  Legal and compliance guidance       When laws/standards change and on
                                      scheduled review
  -----------------------------------------------------------------------

Every document must show its last verification date when it makes
time-sensitive claims.

## 23.3 Knowledge change workflow

**Propose → Source Check → Review → Validate → Approve → Merge → Release
→ Monitor.**

------------------------------------------------------------------------

# 24. Repository Maturity and Acceptance Criteria

The repository is ready for its first public release when all mandatory
criteria below are satisfied.

## 24.1 V1.0 release gates

### Governance

-   [ ] License selected and added.
-   [ ] Contribution policy published.
-   [ ] Code of conduct published.
-   [ ] Governance policy published.
-   [ ] Security reporting instructions published.
-   [ ] Maintainer ownership assigned.

### Structure

-   [ ] Root README complete.
-   [ ] All 31 domain landing pages created or explicitly marked
    planned.
-   [ ] Domain indexes exist.
-   [ ] Document IDs are unique.
-   [ ] Metadata conventions documented.

### Core framework

-   [ ] Path 0 documented.
-   [ ] Path A documented.
-   [ ] Path B documented.
-   [ ] Product transformation documented.
-   [ ] Mandatory framework laws documented.
-   [ ] Project X-Ray workflow documented.
-   [ ] Requirements and approval workflow documented.

### Engineering knowledge

-   [ ] Core architecture guidance published.
-   [ ] Core security guidance published.
-   [ ] Core testing and verification guidance published.
-   [ ] Core data/API guidance published.
-   [ ] Deployment and operations guidance published.
-   [ ] Sources and verification dates included where needed.

### AI and tools

-   [ ] Core agent rules published.
-   [ ] Task contract schema published.
-   [ ] External tool evaluation policy published.
-   [ ] Tool-specific adapters labeled by verification status.
-   [ ] No unsupported integration claims.

### Templates and examples

-   [ ] Project intake template published.
-   [ ] PRD template published.
-   [ ] Architecture template published.
-   [ ] ADR template published.
-   [ ] Test plan and verification templates published.
-   [ ] At least one complete example workflow published.

### Repository quality

-   [ ] Markdown lint passes.
-   [ ] YAML/JSON validation passes.
-   [ ] Internal links pass.
-   [ ] Duplicate IDs check passes.
-   [ ] Registry validation passes.
-   [ ] License and attribution review completed.
-   [ ] Pull request checks are enabled.

## 24.2 What V1.0 does not require

-   Building an AISDF SaaS application.
-   Implementing a hosted AI orchestrator.
-   Creating a database server.
-   Building an IDE.
-   Integrating every AI coding tool.
-   Providing an automated sandbox service.
-   Guaranteeing production outcomes.
-   Claiming compliance certification.

------------------------------------------------------------------------

# 25. Recommended Build Order for the GitHub Repository

This is the order for creating repository content---not an application
development roadmap.

  -----------------------------------------------------------------------
  Phase                   Repository work         Completion output
  ----------------------- ----------------------- -----------------------
  R0                      Repository governance   License, README,
                                                  contribution and
                                                  security files

  R1                      Repository skeleton     Root structure, domain
                                                  READMEs and indexes

  R2                      Core methodology        Path 0, A, B,
                                                  transformation and
                                                  framework laws

  R3                      Project and             Intake, X-Ray,
                          requirements knowledge  requirements and
                                                  approval standards

  R4                      Product and design      Product, UX/UI and
                          knowledge               design standards

  R5                      Engineering knowledge   Technology,
                                                  architecture, data,
                                                  APIs and platform
                                                  guidance

  R6                      AKIS knowledge base     Metadata, document
                                                  standards, retrieval
                                                  methodology

  R7                      AFIAE methodology       Discovery, evaluation,
                                                  licensing, security and
                                                  acquisition

  R8                      AI and agent standards  Provider-neutral agent
                                                  rules, task contracts
                                                  and evaluation

  R9                      Execution and security  Harness requirements,
                                                  threat models and
                                                  permission standards

  R10                     Quality and operations  Testing, evidence,
                                                  deployment, reliability
                                                  and maintenance

  R11                     Templates and examples  Reusable templates and
                                                  complete sample
                                                  workflows

  R12                     Repository validation   Schemas, scripts, tests
                                                  and GitHub Actions

  R13                     Public release          Review, attribution,
                          preparation             release notes and V1.0
                                                  tag
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 26. Final Repository Architecture

The repository is the deliverable. Its contents should be organized
around these six outcomes:

``` text
                    AISDF OPEN-SOURCE REPOSITORY
                                  |
       +--------------------------+--------------------------+
       |                          |                          |
       v                          v                          v
  METHODOLOGY                KNOWLEDGE BASE             AI RULES
  Path 0 / A / B             Engineering topics         Agent contracts
  Project lifecycle          Standards and sources      Tool adapters
       |                          |                          |
       +--------------------------+--------------------------+
                                  |
       +--------------------------+--------------------------+
       |                          |                          |
       v                          v                          v
   TEMPLATES                  REGISTRIES                EXAMPLES
   PRD / ADR / Tests          Tools / Tech / Docs       Reference workflows
       |                          |                          |
       +--------------------------+--------------------------+
                                  |
                                  v
                       REPOSITORY VALIDATION
                                  |
                                  v
                       GITHUB GOVERNANCE
                                  |
                                  v
                       OPEN-SOURCE RELEASES
```

------------------------------------------------------------------------

# 27. Final Decisions and Items Requiring Owner Approval

The blueprint is detailed, but the following project-owner decisions
must be made before public release:

  -----------------------------------------------------------------------
  ID                      Decision                Recommendation
  ----------------------- ----------------------- -----------------------
  OPEN-001                License                 Apache-2.0, subject to
                                                  ownership review

  OPEN-002                Repository visibility   Public

  OPEN-003                Default branch          `main`

  OPEN-004                Documentation format    Markdown + YAML front
                                                  matter

  OPEN-005                Knowledge authoring     Obsidian optional; Git
                                                  Markdown canonical

  OPEN-006                Versioning              Semantic Versioning

  OPEN-007                Contribution model      Issue + pull request

  OPEN-008                Governance              Maintainer-led,
                                                  transparent decisions

  OPEN-009                Tool independence       Mandatory

  OPEN-010                Application             Explicitly out of scope
                          implementation          

  OPEN-011                Documentation website   Optional future
                                                  distribution, not
                                                  required for V1

  OPEN-012                Automated repository    Required for V1
                          checks                  

  OPEN-013                Tool-specific rules     Optional adapters;
                                                  generic core is
                                                  mandatory

  OPEN-014                Compliance claims       Prohibited without
                                                  independent evidence
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 28. Final Definition

**AISDF is an open-source, tool-independent AI-assisted software
engineering framework distributed through a GitHub repository.**

It provides the methodology, engineering knowledge, standards, agent
instructions, templates, schemas, examples, validation rules, and
governance required to guide software development from problem
definition through production maintenance.

Its core deliverable is not an application.

Its core deliverable is a **reusable engineering framework that people
and compatible AI development tools can adopt inside their own software
projects.**

## Final scope statement

> AISDF Repository V1.0 will publish a complete, modular, versioned, and
> maintainable open-source software engineering framework. It will not
> build or host the AISDF application. It will provide the knowledge,
> rules, workflows, templates, schemas, examples, and repository
> validation required for developers and AI tools to apply AISDF
> independently.

**Recommended next action:** Create the GitHub repository skeleton and
governance files first, then publish the core methodology before filling
all 31 knowledge domains. Do not create empty documentation simply to
claim that every domain is complete.


# APPENDIX B — AISDF Complete Functional Blueprint & Repository Document Map v1.1 (Full Source)

# AISDF — Complete Functional Blueprint & Repository Document Map

**Project:** AI Software Development Framework (AISDF)  
**Tagline:** From Problem Statement to Production Software  
**Document:** Complete Functional Blueprint and Required Markdown File Map  
**Version:** 1.1.0  
**Status:** Proposed architecture for review  
**Repository type:** Open-source GitHub repository containing methodology, knowledge, workflows, schemas, prompts, templates, examples, validation and governance.  
**Important boundary:** AISDF is not itself an application, IDE, hosted agent runtime, model provider, project-management SaaS or deployment platform. It guides compatible AI development tools operating in a user's authorized environment.

---

# 1. Executive verdict

The existing AISDF v1.0 repository blueprint is a strong repository concept. It already establishes:

- Path 0 business/venture validation, Path A new-product development, Path B existing-project improvement, and product transformation.
- Project X-Ray and project-state/source-of-truth principles.
- Requirements, product, UX/UI, architecture, engineering knowledge, AI/agent engineering, security, testing, delivery and maintenance domains.
- AKIS (knowledge organization/retrieval methodology) and AFIAE (feature discovery/evaluation/acquisition methodology).
- Tool-independent agent rules, task contracts, approval gates, traceability and evidence.
- A 31-domain repository structure, templates, examples, schemas, registries, CI and open-source governance.

**The biggest gap is not another engineering topic. It is the executable bridge between a user's project document and a completed, verified application.**

The current blueprint describes the framework and many standards, but it does not yet fully specify the operational protocol that makes a compatible coding agent reliably:
1. ingest one project document;
2. understand and normalize it;
3. distinguish facts, requirements, assumptions and unknowns;
4. ask only necessary questions;
5. produce a complete project specification;
6. plan and sequence work;
7. execute in the user's tool/environment;
8. preserve state across sessions and agents;
9. test, repair and independently verify;
10. prove what is complete, incomplete or blocked.

This document adds that missing functional layer while retaining the original repository-only scope.

## 1.1 Realistic promise

> Give AISDF one project document and access to a compatible, authorized development environment. AISDF guides the selected AI development tool through project understanding, specification, planning, implementation, testing, verification and delivery, while maintaining traceability, approval boundaries and evidence.

A single document and a master prompt can initiate the process. They cannot guarantee that every AI tool can autonomously complete every project. Tool capabilities, permissions, execution environment, project ambiguity, external services and human approvals remain real constraints.

---

# 2. AISDF full functional model

AISDF should be organized into eight connected functional systems.

| System | Purpose | Primary outputs |
|---|---|---|
| A. Project Intelligence | Understand new or existing projects | Project profile, X-Ray, state summary |
| B. Requirements & Product Intelligence | Convert needs into agreed product scope | PRD, requirements, acceptance criteria, risks |
| C. Engineering Design Intelligence | Derive implementation-ready technical design | UX/UI specs, architecture, data/API contracts, ADRs |
| D. Knowledge Intelligence (AKIS) | Find the right verified knowledge at the right time | Relevant knowledge pack, sources, version metadata |
| E. Feature & Tool Intelligence (AFIAE) | Discover and evaluate tools, APIs, libraries and services | Evaluation records, compatibility and approval recommendations |
| F. Execution & Agent Coordination | Convert plans into controlled work | Task graph, task contracts, agent assignments, handoffs |
| G. Quality & Verification | Prove the implementation satisfies approved requirements | Test results, evidence, defects, verification verdict |
| H. Delivery & Lifecycle Governance | Deliver, operate, maintain and evolve software | Release records, runbooks, change records, maintenance plan |

These are framework capabilities. They are expressed as Markdown specifications, schemas, workflows, checklists, reusable prompts and optional lightweight repository-validation scripts—not as a hosted AISDF service.

## 2.1 The end-to-end lifecycle

```text
PROJECT DOCUMENT / EXISTING REPOSITORY
                 |
                 v
       01. INTAKE & CLASSIFICATION
                 |
                 v
       02. PROJECT UNDERSTANDING
                 |
                 v
       03. REQUIREMENT EXTRACTION
                 |
                 v
       04. GAP / CONFLICT / RISK ANALYSIS
                 |
          +------+------+
          |             |
       Clarify       Sufficient
          |             |
          +------+------+
                 |
                 v
       05. APPROVED PROJECT BASELINE
                 |
                 v
       06. PRODUCT & UX SPECIFICATION
                 |
                 v
       07. TECHNICAL ARCHITECTURE
                 |
                 v
       08. IMPLEMENTATION DECOMPOSITION
                 |
                 v
       09. EXECUTION PLAN & TASK GRAPH
                 |
                 v
       10. CONTROLLED IMPLEMENTATION
                 |
                 v
       11. CONTINUOUS TEST / DEBUG / REVIEW
                 |
                 v
       12. INDEPENDENT VERIFICATION
                 |
          +------+------+
          |             |
        Failed        Passed
          |             |
       Repair       Release gate
          |             |
          +-------------+
                 |
                 v
       13. DELIVERY / DEPLOYMENT
                 |
                 v
       14. PRODUCTION VERIFICATION
                 |
                 v
       15. MAINTENANCE & CHANGE CONTROL
```

Every stage must specify: purpose, entry criteria, inputs, activities, outputs, responsible role, approval gate, failure paths, exit criteria and evidence.

---

# 3. Major missing capabilities to add

## 3.1 Project Document Ingestion and Normalization — P0

The framework must define how to accept a project document without assuming it is complete or well structured.

Required capabilities:
- Accept Markdown as the canonical starter format; explain how users can convert or attach PDF/DOCX/plain text in their chosen tool.
- Identify document version, project name, scope, intended users, platforms, constraints and source references.
- Preserve the original document; never silently rewrite the user's source.
- Extract atomic requirements with stable IDs.
- Classify each statement as: explicit requirement, business rule, constraint, preference, assumption, inferred engineering decision, open question or out-of-scope item.
- Identify duplicates, contradictions, vague terms, missing acceptance criteria and dependencies.
- Record confidence and source location for extracted information.
- Produce a normalized Project Understanding Report.

Required output: `PROJECT-UNDERSTANDING.md` and machine-readable `project-profile.yaml`.

## 3.2 Ambiguity, Conflict and Clarification Engine — P0

A framework must not ask the user hundreds of questions or silently invent answers.

Define:
- Severity levels: blocker, material, minor, informational.
- Clarification threshold: ask when an unresolved issue changes product behavior, security, data, cost, legal exposure, architecture, permissions or acceptance.
- Safe defaults: only for reversible, low-risk engineering details.
- Assumption register with owner, rationale, confidence, impact and expiry/review condition.
- Conflict resolution order: explicit approved requirement > approved decision record > current project source of truth > documented assumption > AI inference.
- Question batching: group related questions and explain why each answer matters.
- A no-blocker path: proceed with clearly labeled assumptions only when safe.

Required outputs: `OPEN-QUESTIONS.md`, `ASSUMPTIONS.md`, `CONFLICTS.md`.

## 3.3 Requirements Traceability Graph — P0

This is one of the most important missing pieces.

Every approved requirement must connect to:
`Requirement → Design element → Task → Code/change → Test → Verification → Evidence → Release`.

Rules:
- Stable IDs for requirements, tasks, tests, decisions and evidence.
- No approved requirement may disappear during decomposition.
- Every feature must have acceptance criteria.
- Every task must reference one or more requirements or be explicitly marked as enabling/maintenance work.
- Every acceptance criterion must map to a test or a documented manual verification method.
- Changed requirements trigger impact analysis.
- A requirement cannot be marked complete merely because an agent says it is complete.

Required files: `TRACEABILITY-MATRIX.md`, `requirements.yaml`, `task.schema.json`, `test-case.schema.json`, `evidence.schema.json`.

## 3.4 Project State and Session Continuity — P0

The framework currently states that project records—not chat memory—are the source of truth. It needs a concrete protocol.

Define a compact project control set:
- `PROJECT-STATE.md`: current phase, milestone, completed work, active work, blockers, next action.
- `DECISIONS.md` or ADR directory: approved decisions and superseded decisions.
- `TASK-BOARD.yaml`: task IDs, status, owner, dependencies, evidence.
- `RISKS.md`: active risks and mitigation.
- `CHANGELOG.md`: meaningful project changes.
- `HANDOFF.md`: exact context for another agent/session.
- `BASELINE.md`: approved scope and revision.
- `RELEASE-STATUS.md`: release gate status.

At every session end, update state and provide a resumable handoff. At session start, read the control files before acting. Never rely on hidden conversation history as the only record.

## 3.5 Execution Protocol and Task State Machine — P0

The existing task-contract fields are useful but need a normative lifecycle.

Suggested task states:
`PROPOSED → READY → APPROVED → IN_PROGRESS → IMPLEMENTED → TESTED → REVIEWED → VERIFIED → DONE`

Additional terminal or exception states:
`BLOCKED`, `REJECTED`, `CANCELLED`, `DEFERRED`, `NEEDS_REWORK`.

Define allowed transitions, transition owner, required evidence, retry limits, timeout handling, failure reporting and reopening rules. A task cannot jump to `DONE` without its required verification evidence.

## 3.6 Dependency-Aware Planning and Scheduling — P0

The framework should derive:
- Work breakdown structure.
- Dependency graph (DAG where appropriate).
- Critical path and parallelizable tasks.
- Milestones and release slices.
- File/module ownership for parallel agents.
- Integration points and merge order.
- Resource, token, time and budget estimates where the tool exposes them.
- Risk-weighted sequencing.

Do not parallelize tightly coupled work simply to use more agents. Avoid uncontrolled shared-worktree edits.

## 3.7 Tool Capability and Execution Adapter Contract — P0

The existing blueprint correctly distinguishes knowledge, execution and integration compatibility. Turn that into a formal adapter specification.

For every adapter, record:
- Tool name and supported versions.
- Rule-file format and discovery behavior.
- Context/file access.
- Terminal and command execution capability.
- Browser/network capability.
- Test execution capability.
- Git/branch/worktree support.
- Agent/subagent support.
- MCP or connector support, if verified.
- Approval/permission controls.
- Sandbox and isolation model.
- Limitations, known failure modes and last verified date.
- Evidence/source used to verify each claim.

Provide a generic manual adapter even if no tool-specific adapter exists. Never claim an integration merely because a tool can read Markdown.

## 3.8 Continuous Verification and Repair Loop — P0

Define a bounded loop:
1. Run the smallest relevant test after a change.
2. Run integration/regression tests at defined milestones.
3. Classify failure: code defect, test defect, environment issue, requirement ambiguity, dependency issue or infrastructure issue.
4. Capture logs and reproducible steps.
5. Repair within task scope.
6. Re-run failed test and relevant regression suite.
7. Escalate after a defined retry/impact threshold.
8. Do not weaken tests or remove acceptance criteria just to obtain a pass.

The verifier should have a distinct review context or reviewer for critical changes. Separate agents are not automatically independent if they share the same assumptions and evidence.

## 3.9 Release and Production Readiness Gates — P0

A project is not “complete” merely because it runs locally.

Define gates for:
- Requirements coverage.
- Functional acceptance.
- Security and privacy.
- Data migration and backup.
- Accessibility where applicable.
- Performance and reliability targets.
- Observability and operational readiness.
- Deployment/rollback.
- Documentation and user support.
- Production smoke tests.
- Known defects and accepted residual risks.

Production deployment, destructive migrations, credential changes and external spending remain subject to explicit authorization.

## 3.10 Human Control and Autonomy Levels — P0

Define autonomy levels consistently:

| Level | Agent may do | Human involvement |
|---|---|---|
| L0 — Explain | Analyze and recommend | Human performs changes |
| L1 — Prepare | Draft plans, files and patches | Human approves each change |
| L2 — Execute bounded tasks | Make approved changes in defined scope | Review at task/milestone gates |
| L3 — Execute project workflow | Work across approved tasks and tests | Approval for material/high-risk actions |
| L4 — Continuous operation | Monitor and propose/perform narrowly pre-authorized routine actions | Human governance, escalation and revocation |

No autonomy level overrides tool permissions, security policy or approval gates. L4 should be described as a policy model, not a promise that every coding tool supports it.

---

# 4. AISDF operating modes and development paths

## 4.1 Operating modes

- **Beginner Mode:** explain decisions, teach concepts, use smaller milestones, require explicit approvals.
- **Developer Mode:** detailed technical specs, contracts, architecture, implementation and tests.
- **Team Mode:** ownership, review, handoff, branch and merge coordination.
- **Enterprise Governance Mode:** policy mapping, auditability, risk controls and evidence; no certification claim.
- **Autonomous Controlled Mode:** execute within an approved scope and capability boundary, with escalation on defined gates.

## 4.2 Development paths

### Path 0 — Venture / problem validation
Starving Crowd Check; Model a Proven Winner; Founder-Market Fit; Inversion Thinking; Premortem; Pre-Commit Kill Criteria; Market Timing; Build Offer; Disciplined Execution; Feedback Loops; Check Kill Criteria; Resource Reinvestment; Defend Moat; Systemize and Delegate.

Path 0 is optional. Do not force business validation onto an internal tool, academic assignment or technical experiment.

### Path A — New application
Discover → validate → define product → freeze initial scope → UX/UI → architecture → implementation plan → build → verify → release → maintain.

### Path B — Existing application
Inspect → understand → analyze → discover → compare → document → approve → implement → verify.

Path B must begin with Project X-Ray. Do not overwrite or redesign existing architecture before understanding it.

### Product transformation
- Improve while preserving product concept.
- Redesign while preserving core purpose.
- Transform product direction, architecture or purpose.
Require impact analysis, migration/reuse decisions and explicit approval.

---

# 5. Full functional catalogue

This is the recommended functional inventory. A function is not complete until its input, output, workflow, owner, controls, failure behavior and acceptance criteria are documented.

| ID | Function | Required behavior/output |
|---|---|---|
| F-001 | Project intake | Accept project document, repository context and constraints |
| F-002 | Project classification | New build, existing project, transformation, research, prototype |
| F-003 | Document parsing | Extract sections, facts, requirements and source locations |
| F-004 | Requirement normalization | Atomic IDs, types, priority, acceptance criteria |
| F-005 | Gap detection | Missing, vague, contradictory and dependent requirements |
| F-006 | Clarification | Ask prioritized questions; record answers |
| F-007 | Assumption management | Register, approve, expire and revisit assumptions |
| F-008 | Project X-Ray | Inspect stack, structure, dependencies, flows, risks and tests |
| F-009 | Product definition | Users, problems, value, scope, MVP and roadmap |
| F-010 | UX research | Personas only when justified, journeys, tasks and usability needs |
| F-011 | UX/UI specification | Screens, states, flows, responsiveness, accessibility |
| F-012 | Design system | Tokens, components, typography, spacing and interaction rules |
| F-013 | Technology evaluation | Fit, compatibility, security, cost, support and lock-in |
| F-014 | AFIAE discovery | Discover relevant tools, APIs, libraries, services and extensions |
| F-015 | Architecture design | Context, containers, components, boundaries and quality attributes |
| F-016 | ADR management | Record decisions, alternatives, consequences and approval |
| F-017 | Data design | Entities, relationships, constraints, retention and migrations |
| F-018 | API/event design | Contracts, auth, errors, versioning, idempotency and events |
| F-019 | Security design | Threat model, trust boundaries, controls and residual risk |
| F-020 | Implementation decomposition | Break design/requirements into deliverable tasks |
| F-021 | Dependency planning | DAG, critical path, sequencing and parallel work |
| F-022 | Agent selection | Assign role based on verified tool capability |
| F-023 | Task contract creation | Inputs, outputs, permissions, scope and acceptance |
| F-024 | Context packaging | Supply only relevant project and knowledge context |
| F-025 | Controlled execution | Work within approved files, tools and permissions |
| F-026 | Change impact analysis | Identify affected requirements, modules, tests and docs |
| F-027 | Code review | Correctness, maintainability, security and scope compliance |
| F-028 | Test planning | Unit, integration, contract, E2E, regression and nonfunctional |
| F-029 | Test execution | Run appropriate tests and capture results |
| F-030 | Defect triage | Reproduce, classify, prioritize and assign defects |
| F-031 | Repair loop | Correct defect and re-run required tests |
| F-032 | Independent verification | Validate acceptance criteria using evidence |
| F-033 | Traceability | Requirement-to-release mapping |
| F-034 | State continuity | Persist project state, tasks, decisions and handoffs |
| F-035 | Release readiness | Evaluate release gates and residual risks |
| F-036 | Deployment planning | Environments, secrets, migration, rollout and rollback |
| F-037 | Production verification | Smoke tests, telemetry and operational checks |
| F-038 | Observability | Logs, metrics, traces, alerts and SLO guidance |
| F-039 | Incident/recovery | Incident classification, response, restore and postmortem |
| F-040 | Maintenance | Upgrades, vulnerabilities, deprecation and technical debt |
| F-041 | Cost governance | Budget, model/tool spend, infra cost and optimization |
| F-042 | Documentation generation | Keep technical and user documentation aligned |
| F-043 | Knowledge retrieval (AKIS) | Select authoritative, relevant, fresh context |
| F-044 | Knowledge lifecycle | Review, approve, version, deprecate and retire content |
| F-045 | Tool compatibility | Verify tool adapters and capability claims |
| F-046 | Benchmarking | Measure framework effectiveness on repeatable scenarios |
| F-047 | Governance | Contributions, ownership, releases and security reports |
| F-048 | Project closeout | Handover, known limitations, evidence and next steps |

---

# 6. Required execution contracts

## 6.1 Project profile

`project-profile.yaml` should capture:
- Project ID, name, description and document revision.
- Project type and chosen path.
- Target users and platforms.
- Explicit constraints and preferences.
- Approved stack (if any).
- Security/privacy classification.
- Critical integrations.
- Delivery target and budget constraints.
- Current lifecycle phase.
- Source document references.

## 6.2 Requirement record

Each requirement needs:
- Stable ID.
- Statement.
- Type: functional, nonfunctional, business rule, constraint, interface, security, privacy, operational.
- Source and location.
- Priority and rationale.
- Status: proposed, clarified, approved, deferred, rejected, implemented, verified.
- Acceptance criteria.
- Dependencies.
- Risk/impact.
- Owner/approver.
- Linked design, task, test and evidence IDs.

## 6.3 Task contract

Every task needs:
- Task ID and project ID.
- Objective and role.
- Requirement/decision references.
- Inputs and dependencies.
- Allowed files and prohibited files.
- Allowed tools and permission boundary.
- Expected output.
- Acceptance criteria.
- Test and verification requirements.
- Budget/deadline if applicable.
- Status and owner.
- Evidence and handoff references.
- Failure and escalation behavior.

## 6.4 Agent contract

Every agent role needs:
- Purpose, scope and non-goals.
- Required context.
- Input/output contract.
- Allowed tools and operations.
- Prohibited operations.
- Security boundary.
- Approval requirements.
- Handoff format.
- Failure handling.
- Verification responsibilities.
- Capability limitations.

Suggested core roles:
- Project Analyst
- Requirements Engineer
- Product/Business Analyst
- UX Researcher
- UX/UI Designer
- Architect
- Technology Researcher
- Database Engineer
- API/Backend Engineer
- Frontend Engineer
- Mobile Engineer
- AI/ML Engineer
- Security Reviewer
- Test Engineer
- DevOps/Platform Engineer
- Documentation Engineer
- Independent Verifier
- Release Manager

One tool/agent may perform several roles on a small project. Do not create agents merely to increase agent count.

## 6.5 Evidence contract

Evidence should include:
- Evidence ID.
- Requirement/task/test IDs.
- Code revision or commit.
- Environment and tool versions.
- Procedure and timestamp.
- Result and reviewer.
- Logs, screenshots, reports or artifact references.
- Known limitations.
- Validity status.

Evidence from an older revision must not be treated as proof for a newer, materially changed revision.

---

# 7. Master prompt architecture

Do not put the entire framework into one enormous prompt. Provide one short entry-point prompt that loads a modular instruction set.

## 7.1 Recommended prompt files

1. `MASTER-ENTRY-PROMPT.md` — universal starting prompt.
2. `PROJECT-INTAKE-PROMPT.md` — document ingestion.
3. `PROJECT-ANALYSIS-PROMPT.md` — understanding and gap analysis.
4. `REQUIREMENTS-PROMPT.md` — requirements normalization.
5. `ARCHITECTURE-PROMPT.md` — engineering design.
6. `IMPLEMENTATION-PLANNING-PROMPT.md` — tasks and dependencies.
7. `IMPLEMENTATION-EXECUTION-PROMPT.md` — controlled coding.
8. `CODE-REVIEW-PROMPT.md` — review against scope and standards.
9. `TESTING-AND-DEBUGGING-PROMPT.md` — testing and repair.
10. `INDEPENDENT-VERIFICATION-PROMPT.md` — evidence-based acceptance.
11. `RELEASE-READINESS-PROMPT.md` — release gates.
12. `SESSION-HANDOFF-PROMPT.md` — resume across sessions/tools.
13. `EXISTING-PROJECT-XRAY-PROMPT.md` — Path B.
14. `TRANSFORMATION-ANALYSIS-PROMPT.md` — product transformation.
15. `SECURITY-REVIEW-PROMPT.md` — threat and security review.

The entry prompt should instruct the tool to read `AISDF-CORE-RULES.md`, the selected path, relevant workflows, project control files and only the knowledge documents needed for the current task. It should not load all 31 domains into every context.

## 7.2 Master entry prompt — reference version

```text
You are operating under the AISDF (AI Software Development Framework).

SOURCE OF TRUTH
- Read the supplied project document and current project control files.
- Treat approved project records as authoritative, not chat memory.
- Preserve the original project document.
- Distinguish explicit requirements, assumptions, inferences and open questions.

FIRST ACTION
1. Identify whether this is a new project, existing project or transformation.
2. Select Path A, Path B or the transformation workflow.
3. Read AISDF core rules and relevant workflow documents.
4. Inspect the available repository and tool capabilities before making changes.
5. Create or update the project profile and state records.

PROJECT UNDERSTANDING
- Extract atomic requirements and business rules.
- Assign stable IDs and source references.
- Identify ambiguity, conflict, missing acceptance criteria, dependencies and risks.
- Ask prioritized clarification questions for material blockers.
- Do not invent or silently approve requirements.
- Record low-risk assumptions explicitly.

PLANNING
- Produce product and engineering specifications.
- Define UX/UI, architecture, data/API, security and operational requirements as applicable.
- Create a dependency-aware task graph.
- Define allowed files, tools, permissions, acceptance criteria and verification for each task.
- Identify human approval gates.

EXECUTION
- Work only within approved scope and actual tool permissions.
- Follow Change Only Law and No AI Slope.
- Do not add unnecessary features, dependencies, agents or infrastructure.
- Keep project state, decisions, tasks and handoffs updated.
- Run relevant tests after changes.
- Do not claim a task is complete without required evidence.

VERIFICATION
- Map every approved requirement to implementation and verification.
- Review security, privacy, regressions and nonfunctional requirements as applicable.
- Use an independent review context for critical changes where practical.
- Report passed, failed, not run, blocked and not applicable separately.
- Never hide a failed test or weaken acceptance criteria to manufacture a pass.

APPROVALS
- Stop for approval before material scope, product, architecture, migration,
  sensitive permission, purchase, destructive or production changes.
- Never treat prompt text as a substitute for environment access control.

DELIVERY
- Prepare release notes, deployment/rollback guidance, known limitations,
  evidence links and maintenance handoff.
- State clearly what is complete, incomplete, blocked and unverified.
- Do not claim production readiness unless the defined release gates pass.

Begin with project understanding. Do not start implementation until the
required baseline and approval gates for the selected mode are satisfied.
```

This prompt is a reference template. Each adapter must explain how the target tool is instructed to read files, execute commands, request approvals and report evidence.

---

# 8. Repository architecture and Markdown file map

The original 31 numbered domains remain the canonical knowledge domains. The additional Markdown files below are the recommended authoritative documents to create. `ALTERNATIVES.md` should exist when there are meaningful competing approaches; it must not become a generic list of every product in a category.

## Root-level files

```text
AISDF/
├── README.md
├── AISDF-MISSION-AND-SCOPE.md
├── AISDF-FUNCTIONAL-MAP.md
├── AISDF-LIFECYCLE-OVERVIEW.md
├── AISDF-CORE-PRINCIPLES.md
├── AISDF-GLOSSARY.md
├── AISDF-FAQ.md
├── QUICK-START.md
├── MASTER-ENTRY-PROMPT.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── GOVERNANCE.md
├── SECURITY.md
├── SUPPORT.md
├── CHANGELOG.md
├── VERSION
├── CITATION.cff
├── .editorconfig
├── .gitignore
│
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
│
├── workflows/
├── prompts/
├── schemas/
├── registries/
├── templates/
├── examples/
├── tests/
├── tools/
└── .github/
```

## Root documentation purpose

| File | Why it is needed |
|---|---|
| `README.md` | First landing page, value, quick start and navigation |
| `AISDF-MISSION-AND-SCOPE.md` | What AISDF is and is not |
| `AISDF-FUNCTIONAL-MAP.md` | Complete capability inventory and relationships |
| `AISDF-LIFECYCLE-OVERVIEW.md` | End-to-end lifecycle and stage gates |
| `AISDF-CORE-PRINCIPLES.md` | Laws and non-negotiable principles |
| `AISDF-GLOSSARY.md` | Consistent terminology and acronym definitions |
| `AISDF-FAQ.md` | Adoption, tool, scope and limitation questions |
| `QUICK-START.md` | First successful use in a real project |
| `MASTER-ENTRY-PROMPT.md` | Single entry point into the framework |

## Domain-specific required Markdown documents

### 00 — Governance
- `README.md`
- `INDEX.md`
- `PROJECT-GOVERNANCE.md`
- `ROLES-AND-RESPONSIBILITIES.md`
- `CONTRIBUTION-AND-REVIEW-POLICY.md`
- `DOCUMENT-STATUS-AND-APPROVAL.md`
- `VERSIONING-AND-RELEASE-POLICY.md`
- `DEPRECATION-AND-RETIREMENT-POLICY.md`
- `ALTERNATIVES-AND-TRADEOFFS.md` — governance models and contribution models, when relevant.

### 01 — Methodology
- `README.md`
- `INDEX.md`
- `AISDF-MASTER-LIFECYCLE.md`
- `PATH-0-VENTURE-VALIDATION.md`
- `PATH-A-NEW-PRODUCT.md`
- `PATH-B-EXISTING-PROJECT.md`
- `PRODUCT-TRANSFORMATION-WORKFLOW.md`
- `CHANGE-ONLY-LAW.md`
- `NO-AI-SLOPE.md`
- `APPROVAL-FIRST.md`
- `EVIDENCE-OVER-CLAIMS.md`
- `RIGHT-SIZED-ENGINEERING.md`
- `PROJECT-COMPLETION-DEFINITION.md`
- `ALTERNATIVE-DEVELOPMENT-METHODS.md` — compare relevant lifecycle approaches; explain when AISDF should adapt rather than replace them.

### 02 — Project Intelligence
- `README.md`
- `INDEX.md`
- `PROJECT-INTAKE.md`
- `PROJECT-DOCUMENT-INGESTION.md`
- `PROJECT-CLASSIFICATION.md`
- `PROJECT-UNDERSTANDING-AND-NORMALIZATION.md`
- `PROJECT-XRAY.md`
- `EXISTING-CODEBASE-ASSESSMENT.md`
- `GAP-CONFLICT-AND-ASSUMPTION-ANALYSIS.md`
- `PROJECT-STATE-AND-SESSION-CONTINUITY.md`
- `PROJECT-HANDOFF-PROTOCOL.md`
- `ALTERNATIVE-INTAKE-APPROACHES.md` — single document, interview, existing repository and mixed-source intake.

### 03 — Requirements Engineering
- `README.md`
- `INDEX.md`
- `REQUIREMENTS-ENGINEERING-STANDARD.md`
- `FUNCTIONAL-REQUIREMENTS.md`
- `NONFUNCTIONAL-REQUIREMENTS.md`
- `BUSINESS-RULES-AND-CONSTRAINTS.md`
- `USER-STORIES-AND-USE-CASES.md`
- `ACCEPTANCE-CRITERIA.md`
- `REQUIREMENT-PRIORITIZATION.md`
- `REQUIREMENT-TRACEABILITY.md`
- `CHANGE-AND-IMPACT-ANALYSIS.md`
- `AMBIGUITY-AND-CLARIFICATION-PROTOCOL.md`
- `ALTERNATIVE-REQUIREMENTS-APPROACHES.md` — compare use cases, user stories, jobs-to-be-done and specification-by-example.

### 04 — Product Engineering
- `README.md`
- `INDEX.md`
- `PRODUCT-DISCOVERY.md`
- `PROBLEM-SOLUTION-VALIDATION.md`
- `TARGET-USER-AND-JOBS.md`
- `VALUE-PROPOSITION.md`
- `PRODUCT-SCOPE-AND-MVP.md`
- `FEATURE-PRIORITIZATION.md`
- `PRODUCT-ROADMAP.md`
- `PRODUCT-METRICS-AND-OUTCOMES.md`
- `PRODUCT-CHANGE-AND-TRANSFORMATION.md`
- `ALTERNATIVE-PRIORITIZATION-METHODS.md` — compare methods and their trade-offs.

### 05 — UX/UI Engineering
- `README.md`
- `INDEX.md`
- `UX-RESEARCH.md`
- `USER-JOURNEYS-AND-FLOWS.md`
- `INFORMATION-ARCHITECTURE.md`
- `INTERACTION-DESIGN.md`
- `UI-SPECIFICATION.md`
- `DESIGN-SYSTEM-ENGINEERING.md`
- `RESPONSIVE-AND-ADAPTIVE-DESIGN.md`
- `ACCESSIBILITY-STANDARD.md`
- `USABILITY-TESTING.md`
- `DESIGN-HANDOFF-AND-IMPLEMENTATION-VERIFICATION.md`
- `ALTERNATIVE-DESIGN-APPROACHES.md` — design-system, component-library and styling strategy alternatives.

### 06 — Technology Intelligence
- `README.md`
- `INDEX.md`
- `TECHNOLOGY-SELECTION-METHOD.md`
- `TECHNOLOGY-COMPATIBILITY.md`
- `TECHNOLOGY-LIFECYCLE-AND-SUPPORT.md`
- `TECHNOLOGY-RISK-AND-LOCK-IN.md`
- `TOTAL-COST-OF-OWNERSHIP.md`
- `OFFICIAL-SOURCE-VERIFICATION.md`
- `TECHNOLOGY-ALTERNATIVES.md` — compare alternatives only against a stated requirement and evaluation date.

### 07 — Engineering Knowledge
- `README.md`
- `INDEX.md`
- `SOFTWARE-ENGINEERING-FOUNDATIONS.md`
- `CLEAN-CODE-AND-MAINTAINABILITY.md`
- `DESIGN-PRINCIPLES-AND-PATTERNS.md`
- `ERROR-HANDLING-AND-VALIDATION.md`
- `LOGGING-AND-DIAGNOSTICS.md`
- `DEPENDENCY-MANAGEMENT.md`
- `CODE-REVIEW-STANDARD.md`
- `ENGINEERING-TRADEOFFS.md`
- `ALTERNATIVE-PATTERNS-AND-TRADEOFFS.md`

### 08 — Software Architecture
- `README.md`
- `INDEX.md`
- `ARCHITECTURE-DESIGN-PROCESS.md`
- `SYSTEM-CONTEXT-AND-BOUNDARIES.md`
- `COMPONENT-AND-MODULE-DESIGN.md`
- `QUALITY-ATTRIBUTES.md`
- `ARCHITECTURE-DECISION-RECORDS.md`
- `MODULARITY-AND-COUPLING.md`
- `MIGRATION-AND-REFACTORING.md`
- `ARCHITECTURE-REVIEW.md`
- `ALTERNATIVE-ARCHITECTURE-STYLES.md` — monolith, modular monolith, services, event-driven and serverless; selection criteria, not fashion.

### 09 — Platform Engineering
- `README.md`
- `INDEX.md`
- `DEVELOPER-ENVIRONMENT-STANDARD.md`
- `LOCAL-DEVELOPMENT-AND-ENVIRONMENTS.md`
- `INTERNAL-DEVELOPER-PLATFORM-CONCEPTS.md`
- `BUILD-AND-ARTIFACT-STANDARD.md`
- `ENVIRONMENT-PARITY.md`
- `PLATFORM-SECURITY-AND-ACCESS.md`
- `ALTERNATIVE-PLATFORM-APPROACHES.md`

### 10 — AI and Model Engineering
- `README.md`
- `INDEX.md`
- `MODEL-SELECTION-AND-EVALUATION.md`
- `INFERENCE-AND-CONTEXT-BUDGETING.md`
- `PROMPT-ENGINEERING-STANDARD.md`
- `MODEL-ROUTING-AND-FALLBACK.md`
- `AI-EVALUATION-AND-REGRESSION.md`
- `RAG-AND-RETRIEVAL-ENGINEERING.md`
- `MULTIMODAL-SYSTEMS.md`
- `AI-SAFETY-AND-LIMITATIONS.md`
- `ALTERNATIVE-MODEL-AND-DEPLOYMENT-APPROACHES.md`

### 11 — Agent Engineering
- `README.md`
- `INDEX.md`
- `AGENT-ROLE-AND-SCOPE.md`
- `AGENT-TASK-CONTRACT.md`
- `AGENT-LIFECYCLE-AND-STATE.md`
- `AGENT-MEMORY-AND-CONTEXT.md`
- `TOOL-USE-AND-PERMISSIONS.md`
- `AGENT-HANDOFF-AND-COLLABORATION.md`
- `MULTI-AGENT-COORDINATION.md`
- `AGENT-EVALUATION-AND-FAILURE-MODES.md`
- `ALTERNATIVE-AGENT-ARCHITECTURES.md`

### 12 — Orchestration and Context
- `README.md`
- `INDEX.md`
- `WORKFLOW-ORCHESTRATION.md`
- `TASK-GRAPH-AND-DEPENDENCIES.md`
- `CONTEXT-PACKAGING-AND-BUDGET.md`
- `KNOWLEDGE-RETRIEVAL-PROTOCOL.md`
- `ROUTING-AND-DELEGATION.md`
- `RETRY-TIMEOUT-AND-RECOVERY.md`
- `STATEFUL-AND-STATELESS-WORKFLOWS.md`
- `ALTERNATIVE-ORCHESTRATION-PATTERNS.md`

### 13 — Harness and Execution
- `README.md`
- `INDEX.md`
- `EXECUTION-ENVIRONMENT-REQUIREMENTS.md`
- `COMMAND-AND-FILE-ACCESS-CONTROLS.md`
- `SANDBOX-AND-ISOLATION.md`
- `NETWORK-AND-SECRET-BOUNDARIES.md`
- `APPROVAL-AND-INTERRUPTION-PROTOCOL.md`
- `EXECUTION-LOGGING-AND-EVIDENCE.md`
- `TOOL-CAPABILITY-ADAPTER-SPECIFICATION.md`
- `ALTERNATIVE-EXECUTION-ENVIRONMENTS.md`

### 14 — Security and Privacy
- `README.md`
- `INDEX.md`
- `SECURE-SOFTWARE-LIFECYCLE.md`
- `THREAT-MODELING.md`
- `SECURITY-REQUIREMENTS.md`
- `IDENTITY-AUTHENTICATION-AND-AUTHORIZATION.md`
- `SECRETS-AND-CREDENTIALS.md`
- `PROMPT-INJECTION-AND-UNTRUSTED-CONTENT.md`
- `SUPPLY-CHAIN-SECURITY.md`
- `PRIVACY-AND-DATA-GOVERNANCE.md`
- `SECURITY-TESTING-AND-INCIDENT-RESPONSE.md`
- `ALTERNATIVE-SECURITY-CONTROLS.md` — compare controls in context; no one-size-fits-all security recipe.

### 15 — Data and Database Engineering
- `README.md`
- `INDEX.md`
- `DATA-MODELING.md`
- `DATABASE-SELECTION.md`
- `SCHEMA-AND-CONSTRAINT-DESIGN.md`
- `MIGRATION-AND-ROLLBACK.md`
- `TRANSACTIONS-AND-CONSISTENCY.md`
- `BACKUP-RESTORE-AND-RETENTION.md`
- `DATA-PRIVACY-AND-LIFECYCLE.md`
- `ALTERNATIVE-DATABASE-APPROACHES.md`

### 16 — API and Integration Engineering
- `README.md`
- `INDEX.md`
- `API-DESIGN-STANDARD.md`
- `API-AUTHENTICATION-AND-AUTHORIZATION.md`
- `API-VERSIONING-AND-DEPRECATION.md`
- `ERRORS-PAGINATION-AND-RATE-LIMITS.md`
- `WEBHOOKS-AND-EVENT-CONTRACTS.md`
- `IDEMPOTENCY-AND-RETRIES.md`
- `INTEGRATION-LIFECYCLE.md`
- `CONTRACT-TESTING.md`
- `ALTERNATIVE-API-AND-INTEGRATION-PATTERNS.md`

### 17 — Testing and Verification
- `README.md`
- `INDEX.md`
- `TEST-STRATEGY.md`
- `TEST-LEVELS-AND-TEST-PYRAMID.md`
- `TEST-DATA-AND-ENVIRONMENT.md`
- `ACCEPTANCE-AND-REQUIREMENT-TESTING.md`
- `REGRESSION-AND-CHANGE-IMPACT-TESTING.md`
- `PERFORMANCE-AND-RESILIENCE-TESTING.md`
- `SECURITY-AND-ACCESSIBILITY-TESTING.md`
- `AI-AND-AGENT-EVALUATION.md`
- `INDEPENDENT-VERIFICATION.md`
- `EVIDENCE-AND-TRACEABILITY.md`
- `DEFECT-TRIAGE-AND-REPAIR-LOOP.md`
- `ALTERNATIVE-TESTING-STRATEGIES.md`

### 18 — DevOps and Cloud Engineering
- `README.md`
- `INDEX.md`
- `CI-CD-ENGINEERING.md`
- `INFRASTRUCTURE-AS-CODE.md`
- `CONTAINER-AND-IMAGE-ENGINEERING.md`
- `CLOUD-ARCHITECTURE-AND-SECURITY.md`
- `ENVIRONMENT-AND-SECRET-MANAGEMENT.md`
- `BUILD-PROVENANCE-AND-SBOM.md`
- `ALTERNATIVE-DEVOPS-AND-CLOUD-APPROACHES.md`

### 19 — Deployment and Operations
- `README.md`
- `INDEX.md`
- `RELEASE-ENGINEERING.md`
- `DEPLOYMENT-STRATEGIES.md`
- `DATABASE-RELEASE-AND-MIGRATION.md`
- `ROLLBACK-AND-ROLL-FORWARD.md`
- `PRODUCTION-READINESS-CHECKLIST.md`
- `POST-DEPLOYMENT-VERIFICATION.md`
- `OPERATIONS-RUNBOOK.md`
- `ALTERNATIVE-DEPLOYMENT-STRATEGIES.md`

### 20 — Reliability and Observability
- `README.md`
- `INDEX.md`
- `RELIABILITY-ENGINEERING.md`
- `LOGS-METRICS-AND-TRACES.md`
- `SLO-SLI-AND-ERROR-BUDGETS.md`
- `ALERTING-AND-ON-CALL.md`
- `INCIDENT-MANAGEMENT.md`
- `DISASTER-RECOVERY.md`
- `ALTERNATIVE-OBSERVABILITY-STACKS.md`

### 21 — Distributed Systems and Scalability
- `README.md`
- `INDEX.md`
- `DISTRIBUTED-SYSTEMS-FOUNDATIONS.md`
- `SCALING-AND-CAPACITY-PLANNING.md`
- `CACHING-AND-INVALIDATION.md`
- `QUEUES-AND-ASYNC-PROCESSING.md`
- `CONSISTENCY-AND-CONCURRENCY.md`
- `RESILIENCE-AND-BACKPRESSURE.md`
- `ALTERNATIVE-SCALING-STRATEGIES.md`

### 22 — Cost and Resource Governance
- `README.md`
- `INDEX.md`
- `PROJECT-BUDGET-AND-COST-MODEL.md`
- `AI-MODEL-AND-TOKEN-COSTS.md`
- `CLOUD-AND-INFRASTRUCTURE-COSTS.md`
- `QUOTAS-AND-RATE-CONTROLS.md`
- `COST-OBSERVABILITY-AND-OPTIMIZATION.md`
- `ALTERNATIVE-COST-OPTIMIZATION-APPROACHES.md`

### 23 — Legal and Compliance
- `README.md`
- `INDEX.md`
- `OPEN-SOURCE-LICENSES.md`
- `THIRD-PARTY-LICENSE-AND-NOTICES.md`
- `PRIVACY-LEGAL-REVIEW-CHECKLIST.md`
- `DATA-RESIDENCY-AND-TRANSFER-CONSIDERATIONS.md`
- `COMPLIANCE-MAPPING-NOT-CERTIFICATION.md`
- `ALTERNATIVE-LICENSE-AND-GOVERNANCE-MODELS.md`

### 24 — Product Analytics and Support
- `README.md`
- `INDEX.md`
- `PRODUCT-ANALYTICS-PLAN.md`
- `EVENT-AND-METRIC-DEFINITION.md`
- `FEEDBACK-AND-SUPPORT-WORKFLOW.md`
- `BUG-REPORT-AND-TRIAGE.md`
- `PRODUCT-HEALTH-REVIEW.md`
- `ALTERNATIVE-ANALYTICS-APPROACHES.md`

### 25 — Framework Maintenance
- `README.md`
- `INDEX.md`
- `KNOWLEDGE-LIFECYCLE.md`
- `SOURCE-VERIFICATION-AND-FRESHNESS.md`
- `FRAMEWORK-CHANGE-CONTROL.md`
- `COMPATIBILITY-REVIEW.md`
- `DEPRECATION-AND-MIGRATION.md`
- `MAINTENANCE-CADENCE.md`
- `ALTERNATIVE-KNOWLEDGE-MAINTENANCE-MODELS.md`

### 26 — Distribution and Extensions
- `README.md`
- `INDEX.md`
- `REPOSITORY-ADOPTION.md`
- `FRAMEWORK-PACKAGING-AND-DISTRIBUTION.md`
- `EXTENSION-CONTRACT.md`
- `PLUGIN-AND-ADAPTER-GUIDELINES.md`
- `OFFLINE-AND-LOCAL-ADOPTION.md`
- `ALTERNATIVE-DISTRIBUTION-MODELS.md`

### 27 — Standards and Compatibility
- `README.md`
- `INDEX.md`
- `STANDARDS-REGISTRY-GUIDE.md`
- `TOOL-COMPATIBILITY-MODEL.md`
- `VERSION-COMPATIBILITY-POLICY.md`
- `OFFICIAL-SOURCE-AND-CLAIM-POLICY.md`
- `INTEROPERABILITY-AND-PORTABILITY.md`
- `ALTERNATIVE-STANDARDS-AND-COMPATIBILITY-MODELS.md`

### 28 — Templates and Examples
- `README.md`
- `INDEX.md`
- `PROJECT-INTAKE-TEMPLATE.md`
- `PROJECT-DOCUMENT-TEMPLATE.md`
- `PRD-TEMPLATE.md`
- `REQUIREMENTS-TEMPLATE.md`
- `UX-SPECIFICATION-TEMPLATE.md`
- `ARCHITECTURE-TEMPLATE.md`
- `ADR-TEMPLATE.md`
- `DATABASE-DESIGN-TEMPLATE.md`
- `API-SPECIFICATION-TEMPLATE.md`
- `THREAT-MODEL-TEMPLATE.md`
- `TASK-PLAN-TEMPLATE.md`
- `TEST-PLAN-TEMPLATE.md`
- `VERIFICATION-REPORT-TEMPLATE.md`
- `DEPLOYMENT-PLAN-TEMPLATE.md`
- `PROJECT-STATE-TEMPLATE.md`
- `HANDOFF-TEMPLATE.md`
- `INCIDENT-REPORT-TEMPLATE.md`
- `ALTERNATIVE-TEMPLATE-AND-EXAMPLE-PATTERNS.md`
- `examples/` — complete worked projects, not disconnected snippets only.

### 29 — Benchmarks and Evaluation
- `README.md`
- `INDEX.md`
- `AISDF-EVALUATION-FRAMEWORK.md`
- `BENCHMARK-DESIGN-AND-METHODOLOGY.md`
- `PROJECT-COMPLETION-BENCHMARK.md`
- `REQUIREMENT-COVERAGE-BENCHMARK.md`
- `REGRESSION-AND-CHANGE-SAFETY-BENCHMARK.md`
- `SECURITY-AND-VERIFICATION-BENCHMARK.md`
- `AGENT-COORDINATION-BENCHMARK.md`
- `COST-AND-EFFICIENCY-BENCHMARK.md`
- `BENCHMARK-REPORT-TEMPLATE.md`
- `ALTERNATIVE-EVALUATION-METHODS.md`

### 30 — Agent Rules and Verification
- `README.md`
- `INDEX.md`
- `AISDF-CORE-RULES.md`
- `MASTER-ENTRY-PROMPT.md`
- `CHANGE-ONLY-LAW.md`
- `NO-AI-SLOPE.md`
- `APPROVAL-FIRST.md`
- `EVIDENCE-OVER-CLAIMS.md`
- `SECURITY-BOUNDARIES.md`
- `PROJECT-DOCUMENT-INTERPRETER-RULES.md`
- `REQUIREMENT-TRACEABILITY-RULES.md`
- `TASK-STATE-MACHINE.md`
- `AGENT-ROLE-CATALOG.md`
- `AGENT-TASK-CONTRACT.md`
- `INDEPENDENT-VERIFICATION-RULES.md`
- `SESSION-START-AND-HANDOFF-RULES.md`
- `GENERIC-TOOL-ADAPTER.md`
- `ALTERNATIVE-AGENT-COORDINATION-PATTERNS.md`
- `adapters/` — tool-specific rules only after compatibility is verified.

---

# 9. Cross-domain workflows — required files

The 31 domains are knowledge areas. They must be connected by canonical workflow documents.

Create these under `workflows/`:

1. `WF-001-NEW-PROJECT-FROM-DOCUMENT.md`
2. `WF-002-EXISTING-PROJECT-XRAY.md`
3. `WF-003-PROJECT-CLARIFICATION-AND-BASELINE.md`
4. `WF-004-REQUIREMENTS-TO-TASK-DECOMPOSITION.md`
5. `WF-005-UX-AND-DESIGN-TO-IMPLEMENTATION.md`
6. `WF-006-ARCHITECTURE-AND-ADR-APPROVAL.md`
7. `WF-007-TECHNOLOGY-AND-TOOL-EVALUATION.md`
8. `WF-008-AFIAE-DISCOVERY-AND-ACQUISITION.md`
9. `WF-009-AKIS-KNOWLEDGE-RETRIEVAL.md`
10. `WF-010-AGENT-ASSIGNMENT-AND-HANDOFF.md`
11. `WF-011-CONTROLLED-IMPLEMENTATION.md`
12. `WF-012-CODE-REVIEW-AND-CHANGE-IMPACT.md`
13. `WF-013-TEST-DEBUG-AND-REPAIR.md`
14. `WF-014-INDEPENDENT-VERIFICATION.md`
15. `WF-015-RELEASE-AND-DEPLOYMENT.md`
16. `WF-016-PRODUCTION-VERIFICATION.md`
17. `WF-017-SESSION-RESUME-AND-PROJECT-HANDOFF.md`
18. `WF-018-PRODUCT-TRANSFORMATION.md`
19. `WF-019-SECURITY-INCIDENT-AND-RECOVERY.md`
20. `WF-020-PROJECT-CLOSEOUT-AND-MAINTENANCE.md`

Every workflow must define entry criteria, inputs, numbered steps, decisions, outputs, role ownership, approval gates, failure paths, exit criteria and evidence.

---

# 10. Schemas and registries — machine-readable layer

Markdown explains the framework. Schemas make records consistent and validateable.

## Required schemas

- `project-profile.schema.json`
- `requirement.schema.json`
- `assumption.schema.json`
- `decision-record.schema.json`
- `risk.schema.json`
- `task.schema.json`
- `agent-role.schema.json`
- `agent-handoff.schema.json`
- `workflow.schema.json`
- `test-case.schema.json`
- `verification-evidence.schema.json`
- `release-record.schema.json`
- `tool-adapter.schema.json`
- `technology-entry.schema.json`
- `document-metadata.schema.json`
- `traceability-link.schema.json`

Use JSON Schema with a declared draft/version. YAML records may be validated against these schemas. Do not invent a custom schema dialect without need.

## Required registries

- `document-registry.yaml`
- `workflow-registry.yaml`
- `agent-registry.yaml`
- `tool-adapter-registry.yaml`
- `technology-registry.yaml`
- `standards-registry.yaml`
- `template-registry.yaml`
- `benchmark-registry.yaml`
- `glossary.yaml`

Each registry entry needs a stable ID, canonical path, status, owner, version and review metadata as appropriate.

---

# 11. AKIS and AFIAE — clarify their boundaries

## AKIS

AKIS is the knowledge organization and retrieval methodology, not a hosted vector database or application.

It must define:
- Knowledge taxonomy and metadata.
- Canonical source and duplicate handling.
- Retrieval by domain, task, keyword, dependency and semantic relevance where available.
- Source authority and freshness.
- Version compatibility.
- Context selection and token budget.
- Citation/source traceability.
- Permission-aware retrieval.
- Knowledge conflict and supersession.
- Human review and approval before content becomes normative.

Important: Obsidian is an optional authoring interface. Git-tracked Markdown is the canonical repository source. Merely using Obsidian does not reduce context or token usage; modular retrieval and context selection do.

## AFIAE

AFIAE is a discovery and evaluation methodology, not an automatic purchasing or installation service.

It must define:
- Requirement-to-capability gap.
- Discovery sources.
- Source authenticity.
- Feature fit and completeness.
- Maintenance and support.
- License and pricing.
- Security and data handling.
- Compatibility and integration proof.
- Lock-in and portability.
- Alternatives and exit plan.
- Approval before installation, credentials, paid subscriptions or production integration.
- Verification and rollback after adoption.

---

# 12. Alternatives documents — how to write them correctly

An alternatives document is not a list of popular tools. It is a decision aid.

Every `*-ALTERNATIVES.md` should contain:
1. Decision/problem being evaluated.
2. Contexts in which the choice matters.
3. Evaluation criteria and weights (if weighting is justified).
4. Viable options.
5. Advantages and disadvantages.
6. Security, privacy and operational implications.
7. Cost and lock-in considerations.
8. Compatibility and migration implications.
9. When each option is appropriate.
10. When an option should be rejected.
11. Recommended default only when evidence supports it.
12. Official sources, version/date checked and review date.
13. Example ADR showing a real decision.

Do not create alternatives documents for every tiny topic. Use them where a real engineering decision has meaningful competing options. Keep time-sensitive vendor comparisons in registries or dated evaluation records, not in stable conceptual documents.

---

# 13. Testing the framework itself

AISDF needs two separate test targets:

## A. Repository quality tests
- Markdown lint.
- YAML/JSON parse and schema validation.
- Unique IDs.
- Required front matter.
- Internal link checks.
- Registry path consistency.
- Template completeness.
- Stale-source warnings.
- Duplicate/conflicting normative document checks.
- Prompt/agent-rule consistency checks.

## B. Framework effectiveness benchmarks
Run repeatable projects through AISDF using documented tool/model versions and comparable conditions.

Measure:
- Requirement extraction precision/recall.
- Unresolved ambiguity detection.
- Requirement-to-test coverage.
- Scope creep and unauthorized change rate.
- Defect escape rate.
- Regression rate.
- Verification accuracy.
- Rework and human correction effort.
- Completion time.
- Model/tool cost.
- Security-policy violations.
- Handoff/resume success.
- Tool portability.

Benchmark reports must state environment, model/tool version, project difficulty, evaluator method, limitations and raw evidence. Do not claim “1000/10,” guaranteed completion or superiority without repeatable evidence.

---

# 14. Critical edge cases the framework must handle

1. Project document is incomplete or contradictory.
2. Project document conflicts with the existing repository.
3. User changes scope midway.
4. Existing code is undocumented or partially broken.
5. Dependency or provider becomes unavailable.
6. Tool cannot execute commands or access required files.
7. AI produces code that passes superficial tests but violates requirements.
8. Tests are flaky or environment-dependent.
9. Multiple agents edit overlapping files.
10. Database migration is destructive or irreversible.
11. Secret or personal data appears in prompts, logs or repository.
12. Third-party tool output contains prompt injection.
13. Budget/token/time limit is reached.
14. Session ends halfway through a task.
15. Agent claims completion without evidence.
16. Deployment succeeds but production smoke tests fail.
17. Requirement is impossible or unsafe.
18. External service pricing, license or API behavior changes.
19. User asks for a change that breaks another approved requirement.
20. No compatible tool has the required capability.

For every edge case, define detection, containment, user communication, recovery and evidence.

---

# 15. Recommended implementation order for the GitHub repository

Do not write all 31 domains at once. Build the operational spine first.

| Phase | Build | Exit condition |
|---|---|---|
| R0 | Mission, scope, README, governance, license decision | Public contribution and ownership rules clear |
| R1 | Repository skeleton, metadata, registries | Navigation and document conventions validate |
| R2 | Core laws and Path A/B/Path 0 | Methodology is coherent and usable |
| R3 | Single-document intake, normalization, clarification | One sample document becomes an approved project baseline |
| R4 | Requirements IDs, traceability and project state | Every requirement can be tracked across sessions |
| R5 | Architecture, UX, data/API and security templates | Implementation-ready specification can be produced |
| R6 | Task graph, task state machine, agent contracts | Work can be decomposed and assigned safely |
| R7 | Master prompt and generic adapter | A compatible tool can follow the workflow |
| R8 | Testing, repair, evidence and independent verification | A sample build can be verified against requirements |
| R9 | Release, deployment and maintenance workflows | Delivery gates and post-deploy checks are defined |
| R10 | AKIS and AFIAE | Knowledge/tool selection is governed and traceable |
| R11 | Domain knowledge expansion | High-value engineering guidance is populated |
| R12 | Repository CI and benchmark suite | Repository and framework checks are repeatable |
| R13 | Tool adapters and public V1 release | Compatibility claims verified; release criteria passed |

**First end-to-end proof:** Take one realistic but small application project document, run it through AISDF using one supported AI coding tool, and publish the input, generated baseline, task graph, implementation revision, test evidence, verification report and limitations. This proves the workflow better than hundreds of disconnected Markdown files.

---

# 16. Definition of done for AISDF V1

AISDF V1 should not be declared complete merely because all folders exist.

V1 must demonstrate:

- A user can start with one project document.
- The framework extracts traceable requirements and records source locations.
- Ambiguities and conflicts are identified and handled.
- A human-approved project baseline can be produced.
- Product and engineering specifications can be generated.
- Tasks and dependencies can be derived.
- A generic AI tool adapter can guide a compatible coding tool.
- Work is constrained by permissions and approval gates.
- Project state can survive a session/tool handoff.
- Implementation is tested against acceptance criteria.
- Verification evidence is recorded.
- Release readiness and known limitations are reported.
- A complete example proves the end-to-end workflow.
- Schemas, links, metadata and registries pass repository CI.
- Tool capability claims are dated and evidenced.
- Governance, licensing, security reporting and contribution processes exist.

A small complete proof is more valuable than a large empty framework.

---

# 17. What not to add

To preserve the original No AI Slope principle, do not add these to the GitHub framework unless a demonstrated requirement justifies them:

- A mandatory AISDF SaaS application.
- A proprietary agent runtime.
- A mandatory vector database.
- A mandatory Obsidian vault.
- One fixed technology stack for all projects.
- One mandatory AI model or coding tool.
- A large number of agents for every project.
- Automatic installation or purchases without approval.
- Universal architecture prescriptions.
- Compliance certification claims.
- “Fully autonomous” or “guaranteed production-ready” promises.
- Duplicate documents that compete as sources of truth.

Optional future tools may be documented separately, but the framework must remain useful as plain Markdown in a Git repository.

---

# 18. Final recommendation

The AISDF concept is strongest when treated as a **portable engineering operating framework for humans and AI development tools**.

Its most important differentiator should not be the number of domains, prompts or agents. It should be the disciplined chain:

**One project source → verified understanding → approved baseline → traceable engineering plan → controlled execution → evidence-based verification → responsible delivery.**

The most important additions to the existing blueprint are:

1. Single-document ingestion and normalization.
2. Ambiguity/conflict/assumption management.
3. Requirement-to-release traceability.
4. Persistent project state and handoff.
5. Task state machine and dependency graph.
6. Tool capability adapter contract.
7. Bounded implementation/test/repair loop.
8. Independent verification and release gates.
9. Human autonomy/approval model.
10. A complete end-to-end benchmark project.

Build these first. Then populate the 31 domains around them.

**Final caution:** This is a proposed complete functional architecture, not proof that the current GitHub repository already contains these files or that any AI tool can execute every function. The actual repository must be built, validated and benchmarked before claiming those capabilities.


# APPENDIX C — AISDF Engine Architecture, Orchestration & Predefined Rules Expansion (Full Source File Named v1.3)

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


---

# Master maintenance protocol

This master blueprint is a living specification. Maintainers must:
- Version every normative change.
- Record rationale and affected sections.
- Keep registries, schemas, prompts and workflows consistent.
- Mark superseded content rather than silently deleting history.
- Revalidate time-sensitive sources and tool adapters.
- Run repository CI before release.
- Publish known limitations and compatibility status.
- Preserve a changelog and migration notes for breaking changes.

**Master document status:** Consolidated blueprint complete as a planning artifact. Repository implementation, adapter verification, benchmark execution and public release remain separate work items.
