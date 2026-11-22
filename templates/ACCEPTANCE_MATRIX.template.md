# Acceptance Matrix: [Project Name]
**Traceable Requirement-to-Test Verification Matrix**  
**Specification:** v1.0.0 | **Status:** LIVING DOCUMENT

---

## 1. Verification Summary

- **Total In-Scope Requirements**: [COUNT]
- **Verified (`PASS`)**: [COUNT]
- **Failed (`FAIL`)**: 0
- **Blocked / In Progress (`BLOCKED`)**: 0
- **Accepted Risk (`ACCEPTED_RISK`)**: 0

---

## 2. Traceability Matrix

| Requirement ID | Category | Description | Verification Method | Automated Test Reference | Status | Evidence Reference |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| `FR-001` | Functional | User authentication & session | Automated Integration Test | `tests/test_auth.py::test_login` | `PASS` | Exit 0, 200 OK |
| `FR-002` | Functional | Data persistence & query | Automated Integration Test | `tests/test_db.py::test_create` | `PASS` | SQLite insert verified |
| `NFR-001` | Performance | Response latency < 200ms | Benchmark Test | `tests/test_perf.py::test_p95` | `PASS` | Measured p95: 42ms |
| `SEC-001` | Security | Secrets masked in logs | Static Redaction Test | `tests/test_security.py` | `PASS` | Redaction filter validated |
| `SEC-002` | Security | Zero high/critical SAST findings | Static Analysis Scan | `tools/run_semgrep.py` | `PASS` | 0 findings |
| `UX-001` | Usability | Keyboard navigable controls | Browser / DOM Test | `tests/test_a11y.py` | `PASS` | Visible focus verified |
| `UX-002` | Usability | Anti-slop visual compliance | Taste Governance Scanner | `skills/taste-skill/audit-slop.mjs`| `PASS` | 0 slop patterns detected |
