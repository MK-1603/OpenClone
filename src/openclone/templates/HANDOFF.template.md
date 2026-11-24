# HANDOFF.md — {{PROJECT_NAME}}
**Inter-Session Context & Continuation Protocol**  
*Crucial document for resuming development across new AI context windows or different coding agents.*

---

## 1. Session Boundary Snapshot

| Property | Value |
|---|---|
| **Project Name** | {{PROJECT_NAME}} |
| **Handoff Timestamp** | {{YYYY-MM-DDTHH:MM:SSZ}} |
| **Departing Agent** | {{AGENT_NAME_OR_ROLE}} |
| **Current Git Branch** | `feature/{{BRANCH_NAME}}` |
| **Last Working Commit** | `{{COMMIT_HASH}}` — {{COMMIT_SUBJECT}} |
| **Working Tree Status** | Clean / Uncommitted changes recorded below |

---

## 2. What Was Completed in This Session

1. **{{FEATURE_OR_TASK_1}}**:
   - Implemented {{DESCRIPTION}}.
   - Files modified: `{{PATH_1}}`, `{{PATH_2}}`.
   - Verification command: `{{TEST_COMMAND_1}}` (Status: `PASSED`).
2. **{{FEATURE_OR_TASK_2}}**:
   - Configured {{DESCRIPTION}}.
   - Evidence logged in `{{EVIDENCE_PATH}}`.

---

## 3. Exact Current State & Pre-Flight Checklist

Before making ANY code edits in the new session, the incoming agent MUST:

- [ ] Run `git status --short` to verify working tree state.
- [ ] Confirm active branch matches `feature/{{BRANCH_NAME}}`.
- [ ] Read `PROJECT.md` and `ACCEPTANCE_MATRIX.md` for active requirements.
- [ ] Read `PROGRESS.md` for milestone context.
- [ ] Execute existing test suite: `{{TEST_SUITE_COMMAND}}` to verify baseline integrity.

---

## 4. Exact Next Task to Execute

| Property | Value |
|---|---|
| **Task ID** | `{{NEXT_TASK_ID}}` |
| **Goal** | {{NEXT_TASK_GOAL}} |
| **Allowed Files** | `{{ALLOWED_FILE_1}}`, `{{ALLOWED_FILE_2}}` |
| **Prohibited Actions** | Do not refactor unrelated modules; do not add unapproved dependencies. |
| **Acceptance Criteria** | 1. {{CRITERIA_1}}<br/>2. {{CRITERIA_2}} |
| **Verification Command** | `{{NEXT_VERIFICATION_COMMAND}}` |

---

## 5. Architectural & Technical Decisions Recorded

- **Decision 1**: {{EXPLANATION_OF_DECISION_AND_RATIONALE}}
- **Decision 2**: {{EXPLANATION_OF_DECISION_AND_RATIONALE}}

---

## 6. Open Warnings, Tech Debt, or Blockers

- *None* / {{LIST_ANY_KNOWN_WARNINGS_OR_LIMITATIONS}}
