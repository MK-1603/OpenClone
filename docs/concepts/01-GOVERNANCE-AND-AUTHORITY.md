# Concept 01: Governance & Authority Boundary (Primary Specification)

## 1. Core Principle
Humans remain the ultimate authority for software requirements, architectural decisions, destructive commands, security waivers, and release sign-offs. Artificial intelligence models propose plans and synthesize artifacts, but deterministic control planes and authorized humans decide.

## 2. Invariants
1. **Deny-by-Default:** An agent possesses zero write, execute, or network permissions until explicitly authorized in its validated worker manifest and active task contract.
2. **No Model Self-Approval:** Model output or conversational assertions cannot grant permissions, waive security checks, or transition task states.
3. **Cryptographic Revocation:** Any alteration to a task specification revokes previous human approvals immediately.

## 3. Implementation
Enforced by the OpenClone deterministic runtime (`runtime/openclone_runtime/workforce.py`) via the human approver allow-list and SHA-256 task digest matching.

---

## 4. Architectural Alternatives & Operational Trade-Offs

## 1. Alternate Paradigm: Agile Self-Sovereign Developer Mode
For solo developers, internal developer spikes, hackathons, and research exploration, requiring interactive human terminal approvals for every sensitive task introduces friction. The alternate governance model provides **Optimistic Execution with Bounded Undo**.

## 2. How the Alternate Operates
1. **Automatic Non-Interactive Stamping:** When run with `--non-interactive`, the runtime logs the actor as a local developer with optimistic execution permissions.
2. **Git Checkpoint Isolation:** Before executing tasks with `write` or `execute` actions, the runtime creates an automatic git branch checkpoint (`openclone-checkpoint/<task-id>`).
3. **Automated Rollback on Failure:** If an execution fails, triggers unhandled exceptions, or fails validation tests, the runtime rolls back the working tree to the checkpoint automatically.
4. **Post-Hoc Review:** The human reviews the consolidated diff at release time rather than gating each discrete work unit.

## 3. Trade-Off Analysis
* **Strengths:** Maximum development speed, seamless unattended automated workflows.
* **Risks:** Higher exposure during command execution; not suitable for production deployment or multi-tenant codebases.
