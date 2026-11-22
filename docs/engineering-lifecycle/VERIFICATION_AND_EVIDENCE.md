# OpenClone Verification Levels & Evidence Standards
**Version:** 1.0.0  
**Scope:** Verification rigor levels, evidence provenance, and independent checking rules.

---

## 1. The Six Verification Levels

| Level | Identifier | Definition & Rigor |
|---|---|---|
| **V0** | `V0_UNVERIFIED` | No evidence submitted; task is unverified. |
| **V1** | `V1_DECLARATION_ONLY`| AI agent or developer claims completion; no independent evidence checked. |
| **V2** | `V2_ARTIFACT_PRESENT`| Referenced code, document, or migration file verified present on disk. |
| **V3** | `V3_AUTOMATED_CHECK_PASSED` | Unit tests, static analyzers, or linters executed with passing exit code. |
| **V4** | `V4_BEHAVIOR_VERIFIED` | Functional behavior verified in live runtime, headless browser, or staging. |
| **V5** | `V5_INDEPENDENTLY_REVIEWED` | Separate reviewer or automated auditor validated output against acceptance criteria. |

---

## 2. Evidence Record Requirements

Every attached evidence record MUST include:
- **`ref`:** Verifiable path on disk (e.g. `src/auth.py`), commit hash, test ID, or screenshot path.
- **`produced_by`:** Identity of human, agent, or tool that produced the evidence.
- **`proves`:** Specific acceptance criteria proven by this artifact.
- **`limitations`:** What this artifact does NOT prove (e.g., unit test passes but integration not tested).
- **`checksum`:** Cryptographic SHA-256 hash binding the evidence to the task.

---

## 3. Honest Verification Outcomes

Independent checks output one of six honest outcomes:
- `PASS`: Verifiable evidence meets criteria.
- `FAIL`: Evidence does not prove criteria, or tests fail.
- `BLOCKED`: Prerequisite dependency is unverified.
- `NOT_RUN`: Check was configured but not executed.
- `INCONCLUSIVE`: Ambiguous result requiring human review.
- `WAIVED`: Formally waived by project owner.

*Rule: `NOT_RUN` and `INCONCLUSIVE` are NEVER converted to `PASS`.*
