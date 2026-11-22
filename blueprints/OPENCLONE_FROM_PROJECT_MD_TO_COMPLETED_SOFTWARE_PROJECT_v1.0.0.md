# OpenClone — From PROJECT.md to a Completed Software Project
**User workflow, product behavior, and coding-agent execution contract**
**Version 1.0.0**

## 1. The intended experience

A user should be able to bring a project idea or an existing `PROJECT.md` to OpenClone and use OpenClone's knowledge, domains, standards, skills, workflows, adapters, and security toolchain to guide a coding agent from requirements through a tested, documented, release-ready project.

The workflow is:

```text
User idea / existing PROJECT.md / existing repository
                         |
                         v
                 OPENCLONE INTAKE
                         |
                         v
              DISCOVER RELEVANT KNOWLEDGE
       domains + standards + skills + workflows
       architecture + security + quality gates
                         |
                         v
              PROJECT BLUEPRINT GENERATION
                 PROJECT.md + AGENT.md
                         |
                         v
                 PREFLIGHT VALIDATION
        scope + requirements + risks + acceptance
                         |
                         v
                 EXECUTION PLAN
           milestones + tasks + dependencies
                         |
                         v
              CODING AGENT / IDE ADAPTER
      Antigravity / Claude Code / Codex / Qwen Code
                 / Kiro / Kilo / others
                         |
                         v
              IMPLEMENTATION IN PHASES
                         |
                         v
           TESTING + SECURITY + QUALITY GATES
                         |
                         v
             REVIEW + FIX + RE-VERIFY
                         |
                         v
             DOCUMENTED PROJECT HANDOFF
```

**Important:** `PROJECT.md` is the project's requirements and architecture source of truth. `AGENT.md` is the execution contract for the coding agent. OpenClone provides reusable knowledge and governance. The coding agent performs repository changes. Do not confuse these roles.

---

## 2. What each file is responsible for

| Artifact | Responsibility | Owner |
|---|---|---|
| `PROJECT.md` | Product purpose, requirements, scope, architecture, data model, constraints, acceptance criteria | User + OpenClone |
| `AGENT.md` | How the coding agent must work, repository rules, workflow, quality gates, safety boundaries | OpenClone |
| `IMPLEMENTATION_PLAN.md` | Phases, milestones, tasks, dependencies, risks, verification steps | OpenClone + coding agent |
| `TASKS.md` or issue tracker | Current task state, owner, dependencies, status | Coding agent / team |
| `DECISIONS/` or ADR files | Important architecture and product decisions with rationale | Team + coding agent |
| `CHANGELOG.md` | Meaningful project changes | Coding agent |
| Test and security reports | Evidence that requirements and quality gates were checked | Automated tools + coding agent |

Use the target repository's existing conventions. Do not create duplicate files if equivalent canonical artifacts already exist.

### Source-of-truth precedence

When instructions conflict, use this precedence unless the project explicitly defines another safe rule:

1. Applicable law, platform policies, and security boundaries.
2. User-approved product decisions and explicit constraints.
3. Target repository's existing project-specific instructions and architecture decisions.
4. Validated `PROJECT.md`.
5. `AGENT.md` execution rules.
6. OpenClone domain standards, skills, and workflows.
7. Coding-agent defaults.

OpenClone standards must not silently override a project's explicit user-approved requirement. If there is a conflict, stop the affected work, explain it, and request a decision when necessary.

---

## 3. Two ways to start a project

### Mode A — Start from an idea or rough requirements

1. Create or open the target project workspace.
2. Give OpenClone the idea, objectives, target users, constraints, and any existing assets.
3. OpenClone asks only for genuinely blocking missing information.
4. OpenClone discovers relevant domains, skills, standards, and workflows.
5. OpenClone drafts `PROJECT.md` and `AGENT.md`.
6. User reviews and approves the scope and major decisions.
7. OpenClone validates the documents and generates an implementation plan.
8. A coding agent implements the project phase by phase.

### Mode B — Start from an existing `PROJECT.md`

1. Place the supplied `PROJECT.md` in the target repository or provide it to OpenClone.
2. Ask OpenClone to inspect it without changing the code.
3. OpenClone extracts product requirements, constraints, architecture, integrations, data, security, UX, and acceptance criteria.
4. OpenClone checks for missing, ambiguous, conflicting, risky, or untestable requirements.
5. It preserves the author's intent and marks assumptions instead of silently inventing requirements.
6. It maps relevant OpenClone domains, standards, skills, and workflows to the project.
7. It proposes only necessary clarifications and improvements.
8. After approval, it generates or updates the project-specific `PROJECT.md`, `AGENT.md`, and implementation plan.
9. The coding agent follows the approved plan.

Do not overwrite the user's original `PROJECT.md` without preserving its content and making changes reviewable.

---

## 4. The OpenClone project intake and preparation workflow

### Step 1 — Inspect the target repository

Before generating instructions or editing code:
- inspect the complete repository tree and Git status;
- identify existing code, framework, package manager, runtime, database, tests, CI, deployment, and documentation;
- identify uncommitted user changes;
- read existing `README`, `PROJECT.md`, `AGENT.md`, `AGENTS.md`, and architecture decisions;
- identify what is already implemented, partially implemented, broken, or missing.

Never assume a greenfield project when a repository already contains code.

### Step 2 — Parse and normalize requirements

Classify requirements into:
- product vision and outcomes;
- users, roles, and permissions;
- functional requirements;
- non-functional requirements;
- UX and accessibility;
- architecture and technology constraints;
- data model and lifecycle;
- integrations and external services;
- security, privacy, and compliance;
- deployment and operations;
- testing and acceptance criteria;
- exclusions and out-of-scope items.

Give requirements stable IDs, for example `FR-001`, `NFR-001`, `SEC-001`, and `UX-001`. Link implementation tasks and tests back to these IDs.

### Step 3 — Discover relevant OpenClone knowledge

Do not load every OpenClone domain and skill into every project. Select only the relevant material.

For each selected source, record:
- source path and version/revision;
- why it applies;
- which requirement or decision it supports;
- whether it is mandatory, recommended, or optional.

Prioritize:
- relevant domain standards;
- architecture and system design;
- language/framework standards;
- UI/UX and accessibility;
- security and privacy;
- database and API design;
- testing and verification;
- DevOps and deployment;
- AI/agent standards when the product uses AI;
- global anti-AI-slop governance and Taste Skill where applicable.

Avoid loading unrelated content into the coding agent's context. Use concise project-specific summaries and link to full references.

### Step 4 — Produce the project package

Generate or update:
- `PROJECT.md` — approved product and technical specification;
- `AGENT.md` — project-specific coding-agent execution contract;
- `IMPLEMENTATION_PLAN.md` — sequenced phases and tasks;
- `TRACEABILITY.md` — requirement-to-task-to-test mapping, if project complexity justifies it;
- ADRs for consequential decisions;
- security and deployment plans where applicable.

Do not generate empty boilerplate. Every file must contain project-specific information.

### Step 5 — Validate before coding

Run a preflight review:
- Are all critical user journeys represented?
- Are roles and permissions explicit?
- Are data entities and ownership rules clear?
- Are APIs and integrations defined sufficiently?
- Are security boundaries and secrets handling covered?
- Are error, empty, loading, offline, and failure states considered where relevant?
- Are acceptance criteria measurable and testable?
- Are assumptions identified?
- Are dependencies and milestones sequenced?
- Is the scope feasible?
- Are there contradictions between project and agent instructions?

Produce a readiness state:
- `READY`: no blocking ambiguity.
- `READY_WITH_ASSUMPTIONS`: can proceed with explicitly listed low-risk assumptions.
- `BLOCKED`: a critical decision or requirement is missing or contradictory.

Do not start implementation while `BLOCKED`.

---

## 5. How the coding agent should build the project

### Execution loop

For each milestone:

1. **Read:** Read `PROJECT.md`, `AGENT.md`, the current implementation plan, relevant ADRs, and only the applicable OpenClone references.
2. **Inspect:** Examine the actual files and dependencies related to the task.
3. **Plan:** Define the smallest safe implementation and list affected files.
4. **Confirm:** Ask for approval only when the change is destructive, externally visible, paid, security-sensitive, or requires a product decision not already approved.
5. **Implement:** Make a focused change; avoid unrelated refactors.
6. **Test:** Run relevant unit, integration, type, lint, build, accessibility, and security checks.
7. **Review:** Inspect the diff, edge cases, data migration impact, and regressions.
8. **Update:** Update task status, docs, and traceability.
9. **Report:** State what changed, what was tested, results, known limitations, and next task.

Repeat until all approved milestones are complete.

### Build in vertical slices

Prefer working user journeys over building every database table, then every API, then every UI screen in isolation.

Example:

```text
User action
   -> UI
   -> API validation and authorization
   -> business logic
   -> database
   -> response
   -> UI state
   -> automated test
```

Complete one thin end-to-end feature, verify it, then expand.

### Suggested project phases

Adapt to the project; do not force every phase when it is irrelevant.

- **P0 — Discovery:** repository audit, requirements, assumptions, risks.
- **P1 — Specification:** approved `PROJECT.md`, `AGENT.md`, ADRs, implementation plan.
- **P2 — Foundation:** repository setup, configuration, environments, lint/type/test, CI.
- **P3 — Architecture:** data model, auth, permissions, API contracts, core services.
- **P4 — Core user journeys:** implement the highest-value end-to-end features.
- **P5 — Remaining features:** secondary flows, integrations, administration.
- **P6 — UX hardening:** responsive behavior, accessibility, loading/error/empty states.
- **P7 — Security and reliability:** threat review, validation, rate limits, data isolation, observability.
- **P8 — Verification:** automated tests, manual scenarios, regression, performance.
- **P9 — Release readiness:** deployment configuration, migrations, backups, monitoring, documentation.
- **P10 — Handoff:** final report, known limitations, runbook, next steps.

---

## 6. Completion means verified, not merely implemented

A project is not complete because the agent created files or says “done.”

Use a completion matrix:

| Dimension | Evidence required |
|---|---|
| Requirements | Every in-scope requirement has an implementation or an explicitly accepted exclusion |
| Functionality | Critical user journeys work end to end |
| Data | Schema, migrations, validation, ownership, and lifecycle are verified |
| Security | Auth, authorization, secrets, input validation, data isolation, and threat-specific controls are reviewed |
| UX | Responsive behavior, accessibility, and loading/error/empty states are checked |
| Quality | Formatting, lint, type checking, tests, and build pass where applicable |
| Integrations | External APIs and adapters are tested or clearly marked unverified |
| Operations | Environment variables, migrations, deployment, logs, backups, and rollback are documented as applicable |
| Documentation | Setup, usage, architecture, and troubleshooting match the implementation |
| Traceability | Requirement IDs link to tasks and verification evidence |

Statuses:
- `PASS`: evidence confirms the criterion.
- `FAIL`: criterion was checked and did not pass.
- `BLOCKED`: cannot be checked because a prerequisite is missing.
- `NOT RUN`: not executed.
- `ACCEPTED RISK`: user explicitly accepted a documented limitation.

Never report `NOT RUN` or `BLOCKED` as `PASS`. Do not claim production readiness without deployment and operational verification.

---

## 7. Multi-agent and multi-IDE usage

OpenClone should keep the same project package portable across supported coding environments.

Example usage:

```text
Target repository/
├── PROJECT.md
├── AGENT.md
├── IMPLEMENTATION_PLAN.md
├── docs/
│   └── architecture/
├── src/
├── tests/
└── ...
```

A supported adapter may generate or reference native files such as an environment-specific rules file. Those files must point back to the canonical project instructions and must not create conflicting copies.

The user can continue the same project in Antigravity, Claude Code, Codex, Qwen Code, Kiro, Kilo Code, Cursor, or another verified adapter, provided that:
- the adapter is verified for the current product version;
- the project files are available to that environment;
- the agent has the required permissions;
- the agent reads the latest task status and decisions;
- no two agents concurrently modify the same files without coordination.

---

## 8. Security and approval boundaries

The coding agent may perform routine local development actions within the approved repository scope.

Require explicit user approval before:
- deploying or publishing;
- spending money or calling paid services beyond configured limits;
- creating or changing external cloud resources;
- modifying global IDE/system configuration;
- deleting or overwriting user data;
- running dynamic security scans against external targets;
- using production credentials;
- changing authentication, authorization, encryption, or tenant isolation in a way that materially changes security posture;
- committing or pushing if the user has not authorized it.

Keep secrets in secure environment/secret management. Never put real API keys in `PROJECT.md`, `AGENT.md`, source code, screenshots, or logs.
