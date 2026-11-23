# Requirements System Audit — OpenClone Framework
## Architectural Audit of OpenClone Requirements & Documentation System

- **Audited Repository:** `OpenClone` (`MK-1603/OpenClone`)
- **Framework Version:** `1.0.0`
- **Audit Date:** 2026-11-22
- **Auditor Role:** Principal Product Architect & Requirements Engineer
- **Status:** APPROVED BASELINE

---

## 1. Executive Summary

This audit assesses OpenClone's requirements engineering mechanisms, source-of-truth document architecture, and generated application requirement lifecycle.

The primary requirement separation established by this audit is:
1. **OpenClone Framework Product Definition:** The canonical requirements defining OpenClone itself—its local control plane, 31 domains, 56 capability engines, 14 workflows, 72 specialist roles, MCP interoperability service, and security release gates.
2. **Generated Application Requirements:** The requirements generated for specific software applications created by OpenClone users, managed through `templates/PROJECT.template.md`, `templates/AGENTS.template.md`, and `tools/openclone_runtime/project.py`.

---

## 2. Requirement Taxonomy & Knowledge States

OpenClone adopts an unambiguous, evidence-backed knowledge taxonomy to ensure AI agents never conflate suggestions with authorized commitments:

| Knowledge State | Definition | Authority Level | Can Transition To |
|---|---|---|---|
| `VERIFIED_FACT` | Confirmed by direct repository inspection, test output, or provenance proof. | Empirical Fact | N/A (immutable unless invalid) |
| `USER_REQUESTED` | Explicitly stated by the human owner in instructions or chat. | High Intent | `USER_APPROVED` |
| `USER_APPROVED` | Explicitly confirmed by authorized human signature or digest binding. | Binding Decision | `IMPLEMENTED` |
| `AI_RECOMMENDATION` | Synthesized by an AI model/agent as an architectural or implementation proposal. | Advisory Only | `USER_APPROVED` / `REJECTED` |
| `ASSUMPTION` | Temporary hypothesis required for planning pending verification. | Tentative | `VERIFIED_FACT` / `REJECTED` |
| `OPEN_QUESTION` | Unresolved ambiguity requiring human stakeholder decision. | Blocking Item | `USER_APPROVED` / `DECIDED` |
| `UNKNOWN` | Fact or capability currently unverified or unmeasured. | Investigation Item | `VERIFIED_FACT` |
| `CONFLICT` | Contradiction between multiple sources or directives. | Immediate Block | `USER_APPROVED` (Resolution) |

---

## 3. Requirement Engineering Standard

Each requirement in the OpenClone ecosystem must adhere to this structured format:

```markdown
### [REQ-XXX] Requirement Title
- **Statement:** The system SHALL [unambiguous testable capability].
- **Category:** Functional | Architecture | Security | Workforce | Adapter | Quality
- **Source:** User Need | Architectural Invariant | Safety Policy | Regulatory Standard
- **Priority:** MUST | SHOULD | COULD | WONT
- **Status:** PROPOSED | APPROVED | IMPLEMENTED | VERIFIED
- **Knowledge State:** VERIFIED_FACT | USER_APPROVED | AI_RECOMMENDATION
- **Owner:** [Authorized Role / Owner]
- **Acceptance Criteria:**
  - AC-1: Given [precondition], When [action], Then [expected observable outcome].
- **Verification Method:** Unit Test | Static Analysis | Schema Validation | Human Inspection
- **Traceability:** Linked Domain(s), Engine(s), Workflow(s), and Test File(s).
```

---

## 4. Current Audit Findings & Recommendations

1. **Root `PROJECT.md` Alignment:** Ensure root `PROJECT.md` exclusively documents OpenClone as a product, using this structured standard, without generic application placeholders.
2. **Template Separation:** Retain `templates/PROJECT.template.md` as the gold standard for user applications generated via `openclone.py init` or `project.py`.
3. **Verification Coupling:** Every requirement must reference concrete tests in `tests/` or validators in `tools/validate_repository.py`.
