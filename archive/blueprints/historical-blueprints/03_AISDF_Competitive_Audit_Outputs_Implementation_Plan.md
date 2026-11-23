# AISDF — Skills, Outputs, Competitive Evaluation & Implementation Plan
## Capability Audit, Delivery Contracts and Roadmap
**Document ID:** AISDF-UADF-003  
**Version:** 1.0  
**Status:** Assessment based on the AISDF v4.0.0 repository package supplied in the Library; local artifact checks only

---

## 0. Executive assessment

The supplied AISDF v4.0.0 repository is more than a prompt-only concept. It contains a substantial documented engineering framework and a small deterministic local control-plane foundation.

However, the package itself explicitly states that it does **not** include a bundled/certified LLM provider adapter, autonomous code execution, an OS-level sandbox, or production certification. Its 72 worker manifests are role contracts, not 72 autonomous agents.

**Verdict:** AISDF has a meaningful framework/specification foundation and a locally validated control-plane prototype. It is not yet a production autonomous software engineering platform, and there is not enough evidence to claim global top-two status.

## 1. Evidence inspected

Primary artifacts inspected:
- `AISDF_VERSION_1.0_MASTER_BLUEPRINT_v3.md` — the prior 66-section master specification.
- `AISDF_v4.0.0_GITHUB_REPOSITORY.zip` — supplied repository package.
- `IMPLEMENTATION-STATUS.md`.
- `ASSESSMENT/ASSESSMENT-2026-11-21.md`.
- `ASSESSMENT/AISDF-MATURITY-RUBRIC.md`.
- `RELEASE-VALIDATION-4.0.0.md`.
- `README.md`, `docs/v4/ARCHITECTURE.md`, `docs/v4/MATURITY-MODEL.md`.
- `runtime/README.md`, `runtime/openclone_runtime/workforce.py`.
- `07-ENGINEERING-KNOWLEDGE/PERSISTENT-MEMORY-ARCHITECTURE.md`.
- `12-ORCHESTRATION-AND-CONTEXT/MEMORY-LIFECYCLE-AND-RECALL-PROTOCOL.md`.
- Workforce registry/catalogue, adapters, skills, workflows, schemas, and tests.

Limitations: this is a local artifact/package review. It does not verify the live GitHub repository, remote CI, live provider integrations, external IDE compatibility, production deployment, or independent third-party reproduction.

## 2. AISDF v4.0.0 actual capability audit

| Area | Evidence in supplied package | Assessment |
|---|---|---|
| Engineering domain coverage | 31 engineering domains documented | DOCUMENTED |
| Engine catalogue | 56 engine specifications | SPECIFIED |
| Workflow catalogue | WF-001 to WF-013 | SPECIFIED |
| Workforce | 72 unique worker manifests across 12 teams | L1_DEFINED contracts |
| Workforce registry | Python registry validation | Locally executable |
| Task DAG | Dependency validation and cycle checks | Locally executable/tested |
| Task state | State transition controls | Locally executable/tested |
| Permissions | Registered action policy checks | Locally executable/tested |
| Human approval | Approval records tied to task digest | Locally executable/tested |
| Budgets | Task-level budget checks | Locally executable/tested |
| Audit ledger | SQLite event persistence | Locally executable/tested |
| CLI | Init, plan, approve, status flows | Locally validated |
| Memory architecture | Persistent memory architecture, lifecycle protocol, schema | Specified; lifecycle workflow marked PROPOSED |
| AKIS/E-031, E-038, E-040 | Named responsibilities and documentation | Specified; full integrated runtime not demonstrated |
| Skills | Native-format examples/templates in several adapters; worker contracts | Partial portability assets; no full skill marketplace/conformance suite established |
| IDE adapters | Antigravity, Claude Code, Codex, Cursor files in package | Configuration/template level; compatibility not independently verified |
| Provider execution | Adapter contract only | NOT INCLUDED/CERTIFIED |
| Autonomous agents | Requires configured provider/runtime adapter and scheduler | NOT INCLUDED as default service |
| Sandbox | External integration required | NOT INCLUDED |
| Security scanners | Tool contracts/catalogue | Not installed/certified by default |
| EGM | Workflows, personas, schemas, templates | Framework assets; autonomous independent audit not demonstrated |
| Production operations | Policies/docs | NOT CERTIFIED |

The repository's own `RELEASE-VALIDATION-4.0.0.md` records 15 tests passing, while the dated assessment file records an earlier two-test snapshot. Treat the release validation as the later local test record, but rerun the suite from a clean checkout before relying on it. Neither record proves production correctness.

## 3. Existing strengths to preserve

1. **Clear honesty about maturity.** The repository separates documented, executable, and not-included capabilities.
2. **Deterministic control plane.** Worker validation, task DAG, state transitions, permission checks, approvals, budgets, and SQLite audit are the right foundation.
3. **Large engineering coverage.** The 31 domains, 56 engine specifications, and 13 workflow specifications create a useful standards library.
4. **Structured workforce.** 72 worker contracts across 12 teams provide a starting role catalogue.
5. **Memory architecture boundaries.** AKIS, persistent memory, E-038, and E-040 have distinct responsibilities.
6. **Portable integration assets.** The repository contains Antigravity, Claude Code, Codex, and Cursor templates/rules/skills.
7. **EGM assets.** Reviewer contracts, schemas, and workflows are a foundation for independent verification.
8. **Evidence and governance emphasis.** Approval digests, audit events, and explicit no-fake-execution rules are valuable.

## 4. Major gaps before AISDF can compete globally

### P0 — must prove before calling it a working universal framework

- At least one real model/provider execution adapter.
- At least one real coding-agent/runtime adapter with end-to-end task dispatch and event/artifact return.
- A sandbox/workspace isolation implementation with security tests.
- End-to-end project workflow from `PROJECT.md` to verified code change.
- Evidence collector connected to actual commands, tests, diffs, and artifacts.
- EGM reviewer execution with fresh context, read-only permission, and structured findings.
- Persistent memory runtime: capture, write, read-back, retrieval, freshness, conflict, scope isolation.
- Adapter conformance and compatibility tests.
- Clean-install reproducibility and CI evidence.

### P1 — required for quality and efficiency

- Dynamic workforce routing based on capability, skill, maturity, workload, and budget.
- Skill package schema, loader, version resolver, tests, and evaluation.
- Context engine with relevance filtering, authority/freshness ranking, token budgets, and source citations.
- Checkpoint/resume/recovery for long-running tasks.
- Model routing and evaluation by task category.
- Requirement-to-task-to-test traceability.
- Test quality beyond “test command passed”: boundary, regression, integration, security, browser, accessibility, performance, and failure tests where relevant.
- Multi-project identity and access control if shared deployment is introduced.
- Metrics for cost, time, success, intervention, regressions, and evidence quality.

### P2 — ecosystem and adoption

- Public adapter SDK and stable versioning.
- Third-party skill/worker validation.
- Extension discovery and signing/provenance.
- Excellent quick start, tutorials, reference projects, and migration guides.
- Contributor governance, issue triage, release cadence, security disclosure process.
- External case studies and independently reproducible benchmark results.

## 5. Competitive landscape: OpenHands and OpenCode

This is a functional positioning comparison, not a ranking or a claim that either product lacks a feature.

| Dimension | OpenHands | OpenCode | AISDF's intended position |
|---|---|---|---|
| Core identity | Software-agent SDK, Agent Server, workspaces, tools, events, execution | Provider-flexible coding agent with terminal-first developer workflow | Cross-tool engineering framework and control plane |
| Runtime | First-party SDK/server and workspace abstractions | First-party coding-agent runtime | Integrate external runtimes first |
| Tools | Typed tools, workspaces, events, MCP integration | Built-in tools, MCP, browser/tool integrations depending on setup | Common tool capability and permission contract |
| Skills | SDK skill concepts and extension ecosystem | On-demand `SKILL.md` loading | Versioned portable skills plus conformance/evaluation |
| Agents/workforce | Agent abstractions and composable components | Configurable primary/subagents and permissions | Role contracts plus evidence-backed dynamic workforce |
| State/events | Conversation state, event log, persistence and resume mechanisms | Session-based workflow | Cross-tool task DAG, approvals, handoffs, audit ledger |
| Governance | Runtime security policies and workspace boundaries | Configurable permissions/policies | Policy engine independent of execution provider |
| Memory | Conversation persistence/context mechanisms | Session and configured agent context | Project-scoped persistent memory + AKIS + canonical state |
| Verification | Can execute tests/tools and support review workflows | Can run tools and tests | Traceability, evidence contract, independent EGM, benchmark |
| Ecosystem | SDK/server/apps/extensions | Providers, MCP, skills, plugins | Adapters, skills, workers, workflows, evaluation packs |

### What AISDF should learn

From OpenHands:
- Clean SDK/runtime boundaries.
- Typed tools and event models.
- Workspace abstractions and remote execution.
- Durable conversation/session lifecycle.
- Separate agent behavior from client UI.

From OpenCode:
- Strong terminal-first developer experience.
- Provider flexibility.
- On-demand skills.
- Fine-grained permissions.
- Clear user-facing setup and configuration.

AISDF should not copy their product wholesale. It should build the cross-tool governance, project intelligence, memory, skill/workforce contracts, traceability, and verification layer that can use them.

## 6. Skills: what AISDF needs

### 6.1 Skill catalogue design

Organize skills by outcome, not by agent count:

**Project/product**
- Project brief analysis.
- Existing repository X-ray.
- User/problem validation.
- Requirement decomposition.
- Acceptance-criteria generation.

**Architecture/technology**
- System architecture.
- ADR creation and review.
- Technology alternatives and license review.
- API/data model design.
- Migration and compatibility analysis.

**Implementation**
- Frontend feature delivery.
- Backend/API implementation.
- Mobile feature implementation.
- Database migration.
- Integration implementation.
- Refactoring and performance improvement.

**Quality/security**
- Test strategy and test design.
- Regression analysis.
- Threat modeling.
- Secure code review.
- Dependency and license audit.
- Accessibility/performance review.
- EGM independent audit.

**Delivery/operations**
- CI/CD design.
- Deployment readiness.
- Observability and incident response.
- Backup/restore validation.
- Release notes and handover.

### 6.2 Required skill lifecycle

`DRAFT → REVIEWED → EXECUTABLE → VERIFIED → MAINTAINED → DEPRECATED`

Each skill needs:
- Metadata and version.
- Input/output schemas.
- Preconditions and stop conditions.
- Required permissions.
- Procedure and decision points.
- Examples and fixtures.
- Expected evidence.
- Acceptance tests.
- Supported adapter matrix.
- Owner, changelog, and review date.

### 6.3 Skill efficiency rules

- Load only the skills needed for the current task.
- Prefer small skills that compose.
- Use metadata for discovery before loading full instructions.
- Cache immutable skill versions per task run.
- Record exact versions in evidence.
- Do not duplicate the same policy in every skill; link to canonical policy.
- Measure task success, token cost, latency, and failure rate by skill.
- Remove skills that do not improve measurable outcomes.

## 7. Required outputs and artifact contracts

### 7.1 Project intake outputs

- `PROJECT-ASSESSMENT.md`
- `PROJECT-SCOPE.md`
- `REQUIREMENTS.md`
- `ACCEPTANCE-CRITERIA.md`
- `RISKS.md`
- `REPOSITORY-XRAY.md` when an existing repository is supplied.

### 7.2 Design outputs

- `SYSTEM-ARCHITECTURE.md`
- `DATA-MODEL.md` where relevant.
- `API-CONTRACTS.md` where relevant.
- `ADR/ADR-###.md`
- `TECHNOLOGY-DECISIONS.md`
- `THREAT-MODEL.md`
- `TEST-STRATEGY.md`
- `TRACEABILITY.csv` or structured equivalent.

### 7.3 Execution outputs

- Approved plan with immutable digest.
- Work-unit/task records.
- Changed-file manifest and Git diff.
- Actual command/test logs and exit codes.
- Checkpoints and handoff records.
- Dependency/license/security scan evidence where run.
- Cost/time/model/adapter usage record where available.

### 7.4 Verification and delivery outputs

- `VERIFICATION-REPORT.md`
- `EGM-AUDIT-REPORT.md`
- `FINDINGS-REGISTER.md`
- `RELEASE-READINESS.md`
- `DELIVERY-REPORT.md`
- Known limitations and unverified claims.
- Human acceptance/release record.

Every output must declare owner, version, status, source inputs, generation method, validation result, and links to evidence. Generate only artifacts relevant to the project; avoid creating empty boilerplate documents.

## 8. AISDF Engineering Benchmark (AEB)

### 8.1 Purpose

AEB measures whether AISDF improves real engineering outcomes across tools. It must not reward verbose documentation, agent count, or superficial test execution.

### 8.2 Benchmark task groups

1. Project understanding and repository X-ray.
2. Product requirements and acceptance criteria.
3. Architecture and technology decisions.
4. Feature implementation.
5. Bug diagnosis and repair.
6. Regression and test quality.
7. Security and prompt-injection resilience.
8. Memory recall, freshness, and conflict handling.
9. Cross-tool adapter portability.
10. Independent audit and evidence-backed delivery.

Start with 50–70 tasks, but publish task provenance, difficulty, environment, grader rules, and limitations. Keep a private holdout set to reduce overfitting.

### 8.3 Metrics

- Task success rate under predeclared rubric.
- Hidden test pass rate.
- Regression rate.
- Security policy bypass rate.
- Unauthorized action count.
- Memory retrieval precision/recall and stale-memory error rate.
- Cross-project leakage count.
- Adapter conformance pass rate.
- Requirement traceability completeness.
- Evidence completeness.
- Human intervention count.
- Median/p95 time and cost.
- Reproducibility across repeated runs.

### 8.4 Fair comparison protocol

Use the same tasks, repository snapshots, models where possible, time/cost budgets, permissions, tool access, and scoring rubric. Report model differences where equalization is impossible. Run repeated trials and publish variance. Use independent graders for critical outcomes.

## 9. Implementation plan

This is a staged plan, not a calendar promise. A solo beginner should expect it to take longer than a small experienced team. Advance by exit criteria, not dates.

### Phase 0 — Repository and specification baseline

Tasks:
- Freeze the v4.0.0 baseline commit and package checksum.
- Run clean install and all repository tests.
- Inventory runtime modules, schemas, worker manifests, skills, adapters, workflows.
- Map v3 blueprint requirements to v4 artifacts and implementation evidence.
- Create a gap register with `SPECIFIED / IMPLEMENTED / TESTED / INTEGRATED / VERIFIED / OPERATIONAL`.
- Resolve duplicate/conflicting terminology and version references.

Exit:
- Reproducible baseline report.
- Requirement traceability matrix.
- Prioritized P0/P1/P2 backlog.
- No claim that undocumented or untested capability is implemented.

### Phase 1 — One vertical slice

Build the smallest complete workflow:
1. Initialize project from `PROJECT.md`.
2. Inspect repository read-only at pinned commit.
3. Produce project assessment and task DAG.
4. Require approval against plan digest.
5. Dispatch one bounded task through one external coding runtime.
6. Capture diffs, commands, logs, and tests.
7. Run independent EGM review.
8. Produce truthful delivery report.

Exit:
- Demonstrated end-to-end on at least two reference projects.
- Failure and cancellation paths tested.
- No approval bypass.
- All completion claims map to evidence.

### Phase 2 — Memory and context

Build:
- Memory schema and storage adapter.
- Capture and read-back verification.
- Scope/permission filter.
- AKIS retrieval and freshness.
- E-038 handoff package.
- E-040 canonical state integration.
- Conflict/supersession workflow.
- Context budget and source references.

Exit:
- Cross-session recall works.
- Stale/conflicting memory is surfaced.
- Cross-project leakage tests pass.
- Retrieval quality measured against a labeled set.

### Phase 3 — Adapter SDK and interoperability

Start with OpenHands, OpenCode, and one current IDE integration from the repo.

For each:
- Capability manifest.
- Authentication and workspace setup.
- Start/stream/cancel/resume.
- Artifact and evidence mapping.
- Permission and approval mapping.
- Version compatibility matrix.
- Conformance suite.

Exit:
- At least two materially different execution adapters pass the same AISDF conformance suite.
- Unsupported operations fail closed.
- Adapter status and test date are visible.

### Phase 4 — Skills and dynamic workforce

Build:
- Skill schema and loader.
- Version resolution and compatibility.
- Skill test harness.
- Capability-based worker selection.
- Worker/skill maturity tracking.
- Workload, budget, and permission-aware routing.
- Specialist handoff and disagreement protocol.

Exit:
- Same task can be routed across multiple supported agents/tools.
- Skill selection is explainable.
- Skill effectiveness measured against baseline prompts/workflows.
- No agent is called autonomous solely because its prompt exists.

### Phase 5 — Quality, security, and operations

Build:
- EGM execution and finding lifecycle.
- Security threat-model tests.
- Prompt-injection and malicious tool-output tests.
- Sandbox and secret isolation.
- Recovery, checkpoint, timeout, retry, and idempotency.
- CI quality gates and reproducible release packaging.
- AEB benchmark and public results.

Exit:
- Critical security findings block release.
- No unresolved high-risk audit findings without explicit risk acceptance.
- Benchmark reproducible by an external evaluator.
- Restore and recovery drills documented.

### Phase 6 — Open ecosystem

Build:
- Stable adapter/skill/worker SDK.
- Contributor guide and extension review policy.
- Versioned compatibility registry.
- Example projects and tutorials.
- Issue triage, release cadence, security disclosure process.
- External contributor and adoption metrics.

Exit:
- Independent contributors publish compatible extensions.
- External projects use AISDF successfully.
- Maintainers can reproduce and support releases.

## 10. Prioritized backlog

| Priority | Deliverable | Why |
|---|---|---|
| P0 | Clean reproducible test baseline | Establish truth |
| P0 | Real execution adapter | Move beyond control-plane-only |
| P0 | Workspace sandbox/isolation | Safe execution |
| P0 | Evidence collector | Trustworthy output |
| P0 | End-to-end vertical slice | Prove product |
| P0 | EGM execution | Independent quality |
| P1 | Memory service and Context Engine | Continuity and efficiency |
| P1 | Adapter SDK and conformance | Universality |
| P1 | Skill schema/loader/evaluation | Portable procedures |
| P1 | Dynamic workforce routing | Efficient specialist use |
| P1 | Recovery and observability | Reliability |
| P2 | Extension discovery/marketplace | Ecosystem |
| P2 | Hosted multi-tenant service | Scale when justified |

## 11. Release gates

A release cannot claim “universal” or “production-ready” unless:
- Supported tool versions are named.
- Adapter conformance results are published.
- Permission and isolation tests pass.
- End-to-end workflow is reproducible.
- Memory scope and leakage tests pass.
- EGM review evidence is attached.
- Security findings are triaged.
- CI and packaging checks pass.
- Documentation matches actual behavior.
- Known limitations are visible.

## 12. Top-two strategy: what to optimize

Do not chase a global rank directly. Build measurable superiority in a narrow, defensible set of dimensions:
1. Best-in-class cross-tool engineering contracts and conformance.
2. High-quality project memory with authority and provenance.
3. Portable, tested, versioned skills.
4. Approval and policy enforcement independent of coding agents.
5. Traceability from brief to code to test to release.
6. Independent verification with reproducible evidence.
7. Lower cost/time for equal-quality outcomes, measured fairly.
8. External extensions and adoption.

Publish failures and limitations. Trust compounds faster than inflated feature claims.

## 13. Final verdict and immediate next action

AISDF v4.0.0 already has a valuable deterministic foundation and extensive framework documentation. Do not discard it or rewrite everything.

**Immediate next action:** run a clean baseline audit, then implement the one-project vertical slice using a real external coding runtime. Treat memory, skills, adapters, and EGM as integrated parts of that slice—not disconnected feature projects.

The route to global leadership is demonstrated delivery quality, interoperability, trust, reproducibility, and adoption—not blueprint size.
