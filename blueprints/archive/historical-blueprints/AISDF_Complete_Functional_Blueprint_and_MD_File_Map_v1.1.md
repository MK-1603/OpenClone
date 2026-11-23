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
