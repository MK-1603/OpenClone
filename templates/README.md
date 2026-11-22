# OpenClone Templates Library

Reusable, portable template documents for project specification, engineering governance, and AI coding agent execution.

## Portable Project Package Templates

Use these templates to bootstrap or normalize any software project. They are designed to be completely independent of OpenClone runtime dependencies:

| Template | Target Output File | Purpose |
|---|---|---|
| [`PROJECT.template.md`](PROJECT.template.md) | `PROJECT.md` | Canonical product, technical, and architectural requirements specification. |
| [`BUILD_PROMPT.template.md`](BUILD_PROMPT.template.md) | `BUILD_PROMPT.md` | Master execution prompt provided to your AI coding IDE agent. |
| [`AGENTS.template.md`](AGENTS.template.md) | `AGENTS.md` | Operating rules, safety boundaries, and evidence standards for AI agents. |
| [`IMPLEMENTATION_PLAN.template.md`](IMPLEMENTATION_PLAN.template.md) | `IMPLEMENTATION_PLAN.md` | Phased milestone roadmap with dependency ordering. |
| [`SECURITY_PLAN.template.md`](SECURITY_PLAN.template.md) | `SECURITY_PLAN.md` | Threat model, static analysis checkpoints, and dynamic test authorization. |
| [`ACCEPTANCE_MATRIX.template.md`](ACCEPTANCE_MATRIX.template.md) | `ACCEPTANCE_MATRIX.md` | Traceable requirement-to-test mapping and verification ledger. |
| [`PROGRESS.template.md`](PROGRESS.template.md) | `PROGRESS.md` | Real-time milestone tracker, active task log, and blocker register. |
| [`HANDOFF.template.md`](HANDOFF.template.md) | `HANDOFF.md` | Durable context continuation protocol across LLM context window resets. |

## Runtime & Control Plane Templates

Templates used by the optional local deterministic control plane (`openclone.py`):

| Template | Target | Purpose |
|---|---|---|
| [`PROJECT-PROFILE.template.yaml`](PROJECT-PROFILE.template.yaml) | `.aisdf/project.yaml` | Machine-readable project metadata and approver register. |
| [`WORK-UNIT.template.yaml`](WORK-UNIT.template.yaml) | `.aisdf/tasks/` | Work unit specification with input/output contracts and allowed files. |
| [`CHECKPOINT.template.yaml`](CHECKPOINT.template.yaml) | `.aisdf/checkpoints/` | State checkpoint for rollbacks and branch baselines. |
| [`SECURITY-ASSESSMENT-REPORT.template.md`](SECURITY-ASSESSMENT-REPORT.template.md) | `security-report.md` | Standardized audit and findings report. |
| [`SESSION-CONTEXT-PACK.template.yaml`](SESSION-CONTEXT-PACK.template.yaml) | `.aisdf/context/` | Serialized session context pack for multi-agent delegation. |
