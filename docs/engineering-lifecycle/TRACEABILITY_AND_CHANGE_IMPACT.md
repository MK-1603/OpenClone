# OpenClone Traceability & Change-Impact Management
**Version:** 1.0.0  
**Scope:** Bidirectional requirement-to-task-to-test mapping and change impact propagation.

---

## 1. Traceability Architecture

```text
PRD Requirement (REQ-001)
      |
      v
Checklist Task (PHASE_01_DISCOVERY_TASK_01)
      |
      v
Implementation Code (README.md, src/...)
      |
      v
Automated Test (tests/test_discovery.py)
      |
      v
Verification Evidence (EV_01)
      |
      v
Quality Gate (PHASE_01_DISCOVERY)
```

---

## 2. Change-Impact Propagation Rules

When an approved requirement (`PROJECT.md` or PRD) changes:
1. **Identify Linked Tasks:** Find all tasks referencing the changed requirement ID.
2. **Revert Status:** Tasks in `VERIFIED` with stale evidence revert to `VERIFICATION_PENDING` or `NEEDS_REWORK`.
3. **Reopen Quality Gates:** Any previously passed phase gate containing affected tasks reverts to `BLOCKED`.
4. **Notify Reviewers:** Scope change and impact analysis are recorded in the audit log.
