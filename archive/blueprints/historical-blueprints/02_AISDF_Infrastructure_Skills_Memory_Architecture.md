# AISDF — Infrastructure, Skills & Memory Architecture
## Technical Architecture and Extension Contracts
**Document ID:** AISDF-UADF-002  
**Version:** 1.0  
**Status:** Proposed technical target; implementation maturity must be evidenced

---

## 0. Design objective

Define the infrastructure that turns AISDF from a documented framework into a portable, secure, extensible engineering system. Reuse the current v4.0.0 repository foundation where possible. Do not replace working deterministic controls merely to adopt a fashionable framework.

## 1. Architecture requirements

- Provider- and IDE-independent core.
- Local-first developer experience; optional self-hosted/shared service later.
- Deterministic policy and task control.
- Pluggable model and execution adapters.
- Portable Markdown and schema-based artifacts.
- Project and tenant isolation.
- Durable state, checkpoint, resume, and audit.
- Bounded cost, token, time, retries, concurrency, and delegation.
- Rebuildable search indexes.
- Explicit maturity and compatibility evidence.

## 2. Recommended logical layers

```text
Developer CLI / IDE integrations / API
                  |
         Identity & Project Resolver
                  |
        Project Intelligence Service
                  |
      Workflow + Workforce Orchestrator
                  |
    Policy / Approval / Budget Enforcement
                  |
       Context Engine + Memory Gateway
                  |
        Adapter SDK / Execution Broker
                  |
       Isolated Workspace / Agent Runtime
                  |
      Evidence Collector / Verification
                  |
       EGM Review / Release Decision
                  |
          Audit & Operations Layer
```

### Control plane
Owns identity, project scope, plans, task states, role selection, skill selection, approvals, permissions, budgets, memory authorization, and audit records.

### Data plane
Owns model calls, agent sessions, file operations, terminal execution, browser actions, and external tools.

### Trust boundary
The model must never be the final authority for permissions. The deterministic control plane validates every action before it reaches the adapter/runtime.

## 3. Technology recommendation

### 3.1 Build vs integrate

| Capability | Recommendation | Reason |
|---|---|---|
| Core control plane | Build in AISDF | This is the framework's authority and differentiation |
| Workforce registry | Keep and improve current implementation | v4 already validates worker manifests |
| Task DAG/state/approval/audit | Keep current deterministic Python/SQLite core for local mode | Existing local implementation is useful and testable |
| Agent execution runtime | Integrate OpenHands SDK/Agent Server or other engines | Avoid rebuilding mature workspace/tool/event infrastructure |
| IDE/CLI adapters | Build AISDF adapter SDK | Portability is central to the product |
| Model providers | Adapter/plugin model | Avoid vendor lock-in |
| Memory persistence | Keep portable Markdown + SQLite initially; PostgreSQL for shared deployment | Simpler local operation and clear canonical records |
| Semantic search | Add only after retrieval evaluation; pgvector or another replaceable index | Avoid vector database complexity before proof |
| Workflow orchestration | Start with explicit task DAG and durable state; evaluate LangGraph/Temporal only when requirements justify | Avoid framework lock-in and unnecessary distributed complexity |
| Observability | Structured logs, OpenTelemetry-compatible traces/metrics | Cross-adapter debugging |
| Sandbox | Integrate a hardened container/remote workspace provider | v4 does not include an OS-level sandbox |
| Secret management | OS keychain for local; managed secret store for hosted deployment | Never store secrets in project memory |

### 3.2 Suggested implementation stack

**Local reference mode**
- Python 3.10+ core, consistent with v4 baseline.
- SQLite for local task state, approvals, and audit ledger.
- Markdown/JSON for portable project artifacts and memory.
- JSON Schema for work units, memory, skills, evidence, and adapter manifests.
- CLI as the first user-facing control surface.

**Shared/self-hosted mode (later)**
- FastAPI or equivalent service boundary.
- PostgreSQL for multi-user durable state and audit records.
- PostgreSQL full-text search initially; optional pgvector after measured need.
- Redis only if queueing, distributed locks, or ephemeral coordination require it.
- Object storage for large artifacts and logs.
- Container/remote workspace execution.
- OpenTelemetry traces, metrics, and structured logs.

Do not migrate local SQLite to a distributed stack until multi-user concurrency, remote execution, or service availability requirements justify it.

## 4. Core runtime services

| Service | Responsibility | Required invariants |
|---|---|---|
| Project Registry | Resolve project ID, root, repo URL, commit, workspace | No cross-project path leakage |
| Worker Registry | Validate worker IDs, contracts, skills, maturity | Unknown worker is rejected |
| Planner | Build and validate task DAG | No missing dependency or cycle |
| State Machine | Enforce legal transitions | No bypass of approval or verification |
| Policy Engine | Check actions, paths, tools, network, risk | Deny by default for ungranted actions |
| Approval Service | Record human approvals against immutable digests | Material plan change invalidates approval |
| Budget Manager | Enforce limits | No unbounded retries or spend |
| Context Engine | Assemble authorized context | No whole-vault prompt injection |
| Memory Gateway | Capture/recall memory | Scope and provenance enforced |
| Adapter Broker | Negotiate capabilities and dispatch | Unsupported capability fails closed |
| Evidence Collector | Capture real outputs and artifact references | No fabricated execution result |
| Verification Engine | Run required checks and map results to requirements | Unrun check is not passed |
| EGM Coordinator | Create independent review package | Reviewer has no write permission by default |
| Audit Ledger | Persist state/action events | Append-only semantics where practical |

## 5. Task lifecycle and state machine

Suggested states:

`DRAFT → PLANNED → APPROVAL_PENDING → APPROVED → READY → RUNNING → VERIFYING → REVIEW_PENDING → ACCEPTED`

Terminal/exception states:
`REJECTED`, `BLOCKED`, `FAILED`, `CANCELLED`, `EXPIRED`, `NEEDS_REPLAN`.

Rules:
- Only the policy/state service may transition task state.
- `RUNNING` requires a valid execution adapter and workspace grant.
- Sensitive actions require an approval record bound to the task/plan digest.
- A changed plan returns affected tasks to `APPROVAL_PENDING`.
- A failed task must preserve logs and partial artifacts.
- Retry requires a bounded policy and a new attempt record.
- Completion requires DoD evidence, not an agent statement.

## 6. Workforce and skill architecture

### 6.1 Worker vs skill

A **worker role** defines who owns a type of responsibility, capability boundaries, and expected outputs.

A **skill** defines a reusable procedure or method for performing a task.

A **tool** performs an operation.

An **adapter** connects AISDF to an external environment or execution engine.

Do not confuse these:
- Worker: Security Reviewer.
- Skill: Threat-model a web API using STRIDE and trust-boundary analysis.
- Tool: Read repository files or run a dependency scanner.
- Adapter: Invoke the configured coding agent or scanner runtime.

### 6.2 Worker contract

Required fields:
- `worker_id`, `name`, `team`, `version`.
- `purpose`, `responsibilities`, `non_responsibilities`.
- `capabilities`, `required_skills`, `supported_artifacts`.
- `allowed_actions`, `denied_actions`, `file_scope`.
- `input_schema`, `output_schema`.
- `acceptance_criteria`, `review_policy`.
- `maturity_level`, `evidence_refs`, `last_verified`.
- `model_constraints`, `budget_defaults`.

### 6.3 Skill package contract

Recommended layout:

```text
skills/
  <skill-id>/
    SKILL.md
    skill.yaml
    schemas/
      input.schema.json
      output.schema.json
    tests/
      fixtures/
      acceptance.yaml
    examples/
    CHANGELOG.md
```

Required metadata:
- Unique ID, title, version, owner, license.
- Summary and trigger conditions.
- Required inputs and expected outputs.
- Preconditions and prohibited use.
- Required worker capabilities.
- Tool/adapter dependencies.
- Procedure and decision points.
- Failure handling and escalation.
- Security classification and permissions.
- Evidence requirements.
- Test fixtures and evaluation cases.
- Compatibility and deprecation policy.

Skills should be small, composable, versioned, and loaded on demand. Do not place an entire handbook in every prompt. Use native skill packaging where available and a portable Markdown fallback elsewhere.

### 6.4 Skill maturity

- **S0 — Draft:** written, not reviewed.
- **S1 — Reviewed:** schema and safety review passed.
- **S2 — Executable:** tested through at least one supported adapter.
- **S3 — Verified:** acceptance suite passes repeatedly across supported environments.
- **S4 — Maintained:** versioned, monitored, compatibility-tested, and supported.

### 6.5 Skill selection pipeline

1. Parse task intent and required artifacts.
2. Resolve project and risk scope.
3. Match worker capability requirements.
4. Retrieve candidate skills by metadata and relevance.
5. Filter by permissions, compatibility, freshness, and maturity.
6. Select minimum sufficient skill set.
7. Attach only selected skill content to the context package.
8. Record skill IDs/versions in the task run.
9. Evaluate output against skill acceptance criteria.
10. Capture outcome and propose a skill improvement only after review.

## 7. AKIS, persistent memory, E-038, E-040

### 7.1 Responsibilities

| Component | Owns | Must not own |
|---|---|---|
| AKIS / E-031 | Knowledge indexing, retrieval, ranking, freshness | Canonical project requirements |
| Persistent Memory | Durable scoped memory lifecycle | Uncontrolled global user-data store |
| E-038 | Context packaging and handoff | Silent project-state mutation |
| E-040 | Authoritative project state | Unverified semantic summaries |
| Context Engine | Bounded context assembly | Permission decisions delegated to LLM |

### 7.2 Memory categories

- Project facts and constraints.
- Approved decisions and rationale.
- Session/task checkpoints.
- Verified lessons and recurring failures.
- Reusable engineering knowledge.
- Agent/work-unit continuity notes.
- Explicitly approved preferences, separately scoped.

### 7.3 Memory record

```json
{
  "memory_id": "mem_<stable-id>",
  "type": "decision|fact|lesson|checkpoint|knowledge|preference",
  "scope": {
    "tenant_id": null,
    "project_id": "project-id",
    "agent_id": null
  },
  "title": "Short descriptive title",
  "content": "Compact memory content",
  "source_refs": ["docs/decisions/ADR-004.md"],
  "authority": "canonical|approved|verified|provisional",
  "confidence": 0.0,
  "status": "active|stale|disputed|superseded|archived",
  "created_at": "ISO-8601",
  "validated_at": null,
  "expires_at": null,
  "supersedes": [],
  "sensitivity": "public|internal|confidential|restricted",
  "allowed_scopes": ["project:project-id"],
  "schema_version": "1.0"
}
```

This is an illustrative contract; final schema must be versioned and validated.

### 7.4 Memory lifecycle

`CAPTURE → CLASSIFY → PROVENANCE CHECK → DEDUPLICATE → VALIDATE → APPROVE IF REQUIRED → PERSIST → READ-BACK VERIFY → INDEX → RECALL → FRESHNESS CHECK → USE → RECONCILE → ARCHIVE/EXPIRE`

Rules:
- Do not store every conversation turn.
- Never store secrets, credentials, or prohibited sensitive data.
- Preserve source references and revision history.
- Mark conflicting or stale memories; do not silently overwrite.
- Indexes/embeddings are derived and rebuildable.
- Retrieval filters by project, user, tenant, permission, and status before ranking.
- Return citations/source paths and confidence.
- Abstain when evidence is missing or conflicting.
- Verify every memory write by reading it back.
- Keep personal and project/organization memory isolated.

### 7.5 Retrieval ranking

Use a staged retrieval strategy:
1. Scope and access filter.
2. Exact ID/path/keyword lookup.
3. Full-text retrieval.
4. Optional semantic retrieval.
5. Rank by authority, freshness, relevance, confidence, and task match.
6. Deduplicate and resolve superseded records.
7. Build a bounded context package.
8. Include source references and omissions.

Evaluate retrieval precision, recall, stale-memory rate, conflict detection, and cross-project leakage. Do not optimize for maximum token volume.

## 8. Universal Adapter SDK

### 8.1 Adapter types

- Coding agent/CLI adapter.
- IDE rule/skill adapter.
- Model provider adapter.
- Tool/MCP adapter.
- Workspace/sandbox adapter.
- Source-control adapter.
- Testing/security scanner adapter.
- Knowledge/memory storage adapter.

### 8.2 Adapter contract

Every adapter must implement or explicitly mark unsupported:
- `discover_capabilities()`
- `validate_environment()`
- `authenticate()` / secret reference handling
- `prepare_workspace()`
- `start_task()`
- `stream_events()`
- `collect_artifacts()`
- `request_approval()` or delegate to AISDF policy
- `pause()` / `resume()` / `cancel()`
- `recover()` / `close()`
- `health_check()`

No adapter may bypass the AISDF policy engine. The exact interface should be frozen only after a prototype against two materially different execution engines.

### 8.3 Adapter conformance suite

- Capability declaration matches actual behavior.
- Read-only mode cannot write.
- Denied commands are blocked.
- Workspace paths remain isolated.
- Secrets are masked.
- Task cancellation works.
- Timeout and crash recovery work.
- Events and artifacts map to canonical schemas.
- Approval digest is enforced.
- Version compatibility is recorded.
- Prompt injection and malicious tool output do not alter policy.

## 9. External tool strategy

Initial integrations should be limited to three representative paths:
1. **OpenHands SDK/Agent Server** — execution-runtime integration.
2. **OpenCode** — coding-agent/CLI integration.
3. **One IDE-native integration already present in AISDF v4** — start with Antigravity or Claude Code based on access and testability.

Do not claim support for Cursor, Windsurf, Codex, Gemini CLI, or any other product until exact versions and conformance tests are recorded.

MCP is a tool/context integration protocol, not a replacement for the AISDF task, approval, or evidence contracts. Use MCP where it fits; keep the AISDF control plane authoritative.

## 10. Context engine

The context engine assembles a task-specific package from:
- Current task contract.
- Canonical project state.
- Relevant requirements and ADRs.
- Authorized memory records.
- Selected worker contract.
- Selected skill versions.
- Relevant source files and test evidence.
- Tool/adapter capability profile.
- Security and permission constraints.
- Prior checkpoint/handoff.

It must exclude unrelated project files, stale memory, secrets, unauthorized content, and irrelevant agent histories.

Context budget must be dynamic. Measure task success and token/cost consumption rather than hardcoding one universal percentage split.

## 11. EGM independent verification

**Elephant:** context-rich implementer/continuity role.  
**Goldfish:** fresh-context auditor with independent instructions and read-only access to requirements, diffs, tests, and evidence.

Goldfish must not rely solely on Elephant's summary. It should:
- Re-read acceptance criteria.
- Inspect actual changed files.
- Inspect test evidence and reproduce critical tests.
- Search for regressions and missing cases.
- Challenge assumptions and unsupported completion claims.
- Produce structured findings with severity, evidence, and remediation.
- Avoid editing the implementation by default.

Fresh context alone is not enough: reviewer separation, permissions, inputs, and audit trail matter.

## 12. Data and persistence

**Local mode**
- SQLite: tasks, transitions, approvals, audit metadata.
- Markdown/JSON: human-readable project state, decisions, memories, skills.
- Filesystem: logs and artifacts, with path restrictions.
- Optional FTS: local text search.

**Shared mode**
- PostgreSQL: tenant/project/task/approval/memory metadata and audit.
- Object storage: larger artifacts and logs.
- Optional Redis: queue/lock/cache only when required.
- Optional vector index: after retrieval evaluation proves value.

All derived indexes must be rebuildable from canonical records.

## 13. Observability and reliability

Every task run should emit:
- Correlation ID and task ID.
- Project ID and commit SHA.
- Worker/skill/adapter/model versions.
- Approval and policy decisions.
- Start/end times and state transitions.
- Token/cost usage where available.
- Tool invocations and exit codes.
- Artifact references and test results.
- Retry/recovery events.
- EGM findings and human disposition.

Operational controls:
- Deadlines and timeouts.
- Bounded retries and backoff.
- Idempotency keys for repeatable actions.
- Checkpoints and resume.
- Crash recovery.
- Backups and restore drills.
- Dependency and adapter compatibility monitoring.
- Incident response and vulnerability disclosure.

## 14. Build order for infrastructure

1. Stabilize current local deterministic runtime.
2. Freeze task, worker, memory, evidence, and adapter schemas.
3. Add context/memory gateway with SQLite/Markdown backend.
4. Prototype OpenHands and OpenCode adapters.
5. Add workspace isolation and command policy.
6. Add evidence collector and EGM flow.
7. Add conformance suite.
8. Add shared PostgreSQL service only when multi-user requirements are real.
9. Add marketplace/discovery only after third-party extension quality can be governed.
