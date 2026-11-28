# Acceptance Matrix: {{PROJECT_NAME}}
**Traceable Requirement-to-Test Verification Matrix**  
*Specification:* v2.1.0 | *Status:* LIVING DOCUMENT

---

## 1. Verification Summary

| Metric | Count |
|---|---|
| **Total In-Scope Requirements** | {{TOTAL_COUNT}} |
| **Verified (`PASS`)** | {{PASS_COUNT}} |
| **Failed (`FAIL`)** | 0 |
| **Blocked / In Progress (`BLOCKED`)** | {{BLOCKED_COUNT}} |
| **Not Yet Executed (`NOT_RUN`)** | {{NOT_RUN_COUNT}} |
| **Not Applicable (`NOT_APPLICABLE`)** | 0 |
| **Accepted Risk (`ACCEPTED_RISK`)** | 0 |

> ⚠️ **Enforcement Rule:** Status values are strictly restricted to `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`, `NOT_APPLICABLE`, or `ACCEPTED_RISK`. Never treat `NOT_RUN`, `BLOCKED`, or `ACCEPTED_RISK` as `PASS`.

---

## 2. Requirement Traceability Matrix

| Requirement ID | Requirement Summary | Priority / Risk | Design / Decision | Implementation Task | Code Location | Verification Method | Evidence Reference | Status | Notes |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| `FR-001` | User authentication & session | High / Medium | `ADR-001` | M1 / `TASK-001` | `src/auth/service.py` | Automated Integration Test | `pytest tests/test_auth.py` (Exit 0) | `PASS` | Password hash & JWT verified |
| `FR-002` | Data persistence & query API | High / Low | `ADR-002` | M2 / `TASK-002` | `src/db/repository.py` | Integration Test | `pytest tests/test_db.py` (Exit 0) | `PASS` | Transaction isolation verified |
| `NFR-001` | API latency under 200ms p95 | Medium / Low | `ARCHITECTURE.md` | M3 / `TASK-003` | `src/api/routes.py` | Benchmark Harness | Benchmark log (p95: 42ms) | `PASS` | Verified under 500 req/s |
| `SEC-001` | Zero secrets in source or logs | Critical / High | `SECURITY_PLAN.md` | M1 / `TASK-004` | Repository root | Static Secret Scanner | TruffleHog / Git pre-commit | `PASS` | 0 secrets found |
| `SEC-002` | Zero high/critical SAST findings | High / High | `SECURITY_PLAN.md` | M4 / `TASK-005` | `src/` | SAST Scanner | Semgrep ruleset exit 0 | `PASS` | 0 findings |
| `UX-001` | Accessible keyboard navigation | Medium / Low | `PROJECT.md` | M4 / `TASK-006` | `src/ui/components/` | Automated a11y test | Playwright / Axe-core | `PASS` | WCAG 2.2 AA compliant |
| `UX-002` | Taste Skill anti-slop compliance | Medium / Low | `domains/05/` | M4 / `TASK-007` | `src/ui/` | Static Slop Audit | `audit-slop.mjs` pass | `PASS` | Zero generic gradients/blobs |
