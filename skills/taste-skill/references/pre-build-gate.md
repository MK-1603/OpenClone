# Pre-Build Design Gate Specification

**Operating Rule:** No code implementation before a validated design plan.

---

## 1. The Pre-Build Gate Lifecycle

```text
[ DISCOVERY ] ──► [ AUDIT ] ──► [ DESIGN PLAN ] ──► [ PLAN-CHECK GATE ] ──► [ IMPLEMENTATION ]
```

### Gate State Machine

* `GATE: DISCOVERY_REQUIRED` — Instruction audit has not been executed.
* `GATE: AUDIT_REQUIRED` — Existing project or visual slop audit is missing.
* `GATE: PLAN_REQUIRED` — `.taste-skill/design-plan.md` does not exist.
* `GATE: PLAN_INVALID` — Plan is missing required sections, has empty placeholders, or violates constraints.
* `GATE: APPROVAL_REQUIRED` — Material architectural, design-system, or destructive changes require human sign-off.
* `GATE: READY` — Plan is validated and approved. Implementation may proceed.
* `GATE: BUILDING` — Implementation is actively underway.
* `GATE: VERIFYING` — Pre-finish verification running (`gate.mjs`, `consistency.mjs`, `copy-lint.mjs`).
* `GATE: PASS` — Build is complete, verified, and ready for delivery.
* `GATE: BLOCKED` — Open critical findings or unfulfilled requirements halt delivery.

---

## 2. Design Plan Requirements (`.taste-skill/design-plan.md`)

For Level 3 to Level 5 tasks, the design plan must explicitly address all 25 core criteria:
1. Product understanding
2. User and business context
3. Existing application audit
4. Instruction audit summary
5. Existing design-system analysis
6. Identified UI problems
7. Anti-slop findings
8. Proposed visual direction
9. Color strategy
10. Typography strategy
11. Spacing strategy
12. Component strategy
13. Layout strategy
14. Responsive strategy
15. Interaction strategy
16. Animation strategy
17. Accessibility requirements
18. Performance requirements
19. Components to preserve
20. Components to modify
21. Components to remove
22. Components to introduce
23. Implementation sequence
24. Validation strategy
25. Risks and assumptions

For Level 1 and 2 tasks (Micro-fix and Component updates), a lightweight 5-point plan is accepted:
1. Task scope and level
2. Problem description
3. Proposed change (classified as PRESERVE / MODIFY / REMOVE / ADD)
4. Accessibility check
5. Verification command
