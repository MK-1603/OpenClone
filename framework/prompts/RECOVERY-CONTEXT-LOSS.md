# Protocol Prompt — Context Loss Recovery (Session Continuity)

You are executing the **OpenClone Context Loss Recovery Protocol** following a chat session reset, context compaction, or fresh model turn.

---

## 1. Objective
Recover complete, verified project state from repository disk artifacts without relying on ephemeral memory or hallucinating prior decisions.

## 2. Recovery Procedure (Step-by-Step)

### Step 1: Discover Ground-Truth Project Artifacts
Inspect the workspace to locate and read the persistent sources of truth:
1. `PROJECT.md` — Project mission, scope, and domain boundaries.
2. `Features-List.md` / `ACCEPTANCE_MATRIX.md` — Active requirements and acceptance gates.
3. `PROGRESS.md` & `HANDOFF.md` — Current milestone, completed work units, and last handoff note.
4. `Solution-Blueprint.md` & `Tech-Stack.md` — Architectural topology and database schema.

### Step 2: Verify Physical Codebase State
Do not trust `HANDOFF.md` blindly. Run git or directory inspection commands to verify actual files on disk:
- Inspect recent Git commits: `git log -n 5 --oneline`.
- Check git status: `git status`.
- Run existing test suites to establish current baseline: `pytest` or `npm test`.

### Step 3: State Reconstruction Report
Formulate and output a concise state summary:
- **Project Name & Version:** [e.g., ManMadhan Store v1.0.0]
- **Current Milestone:** [e.g., Phase 04 — Step 3: Backend API]
- **Verified Completed Tasks:** [List of tasks confirmed by tests on disk]
- **Immediate Next Work Unit:** [The exact next task to execute]

### Step 4: Resume Execution
Proceed strictly with the next unexecuted work unit following the approved `BUILD_PROMPT.md` and `ACCEPTANCE_MATRIX.md`.
