# OpenClone AI IDE Task Handoff Contract
**Version:** 1.0.0  
**Scope:** Scoped task package generation, completion report schemas, and anti-slop boundaries.

---

## 1. Focused Task Scoping

OpenClone never dumps the entire framework into an IDE prompt. Instead, `tools/checklist_engine.py handoff --task-id <ID>` emits a focused package containing:
1. **Task Context & Rationale:** Exact objectives, why it matters, and phase title.
2. **Observable Acceptance Criteria:** Checkbox list of Given/When/Then conditions.
3. **Execution Boundaries:** Explicit allowlist of files to touch; prohibition of unrelated changes.
4. **Anti-Slop Directives:** Strict prohibition of unrequested gradients, decorative blur blobs, and placeholder cards.
5. **Required Completion Report Schema:** Machine-readable JSON contract.

---

## 2. IDE Completion Report Schema

External IDE agents (Antigravity, Cursor, Claude Code, Codex) must report completion in this exact schema:

```json
{
  "task_id": "PHASE_09_BACKEND_TASK_01",
  "status": "IMPLEMENTED",
  "changed_files": [
    "src/routes/api.py",
    "tests/test_api.py"
  ],
  "test_command": "python -m unittest tests/test_api.py",
  "test_result": "PASS (8 tests ok)",
  "evidence_description": "Added input validation schema and parameterized queries."
}
```

---

## 3. Ingestion & Verification Rules

- **Submission $\neq$ Verification:** Ingesting an IDE completion report transitions the task to `VERIFICATION_PENDING` (never directly `VERIFIED`).
- **Dishonest Report Detection:** Reports with empty `changed_files` or non-existent file paths on disk are rejected with an error.
- **Independent Audit:** The independent verification engine verifies that files exist on disk, tests pass, and evidence satisfies criteria before advancing to `VERIFIED`.
