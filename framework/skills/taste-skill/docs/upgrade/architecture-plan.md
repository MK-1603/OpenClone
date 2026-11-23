# Taste Skill Minimal Architecture Plan
**Target:** Instruction-First, Context-Aware, Anti-Slop Governance Upgrade

---

## 1. Architectural Strategy

We preserve the entire core asset library and browser testing pipeline while inserting a robust **Governance and Pre-Build Intelligence Layer**:

```text
[ USER BRIEF / TASK ]
         │
         ▼
[ 1. INSTRUCTION DISCOVERY ENGINE ] ────────► references/instruction-governance.md
  Discovers AGENTS.md, CLAUDE.md,             scripts/instruction-audit.mjs
  .cursorrules, project tokens, rules         Output: .taste-skill/reports/instruction-audit.md
         │
         ▼
[ 2. EXISTING PROJECT & SLOP AUDIT ] ───────► references/existing-project-audit.md
  Audits frameworks, tokens, UI patterns      references/anti-slop-governance.md
  Identifies unnecessary visual slop          scripts/audit-slop.mjs
  Enforces REMOVE BEFORE ADDING               Output: .taste-skill/reports/anti-slop-audit.md
         │
         ▼
[ 3. ADAPTIVE DESIGN STRATEGY ] ────────────► references/adaptive-design-intelligence.md
  Selects design language by domain           references/design-system-governance.md
  (Enterprise, Healthcare, Finance, Devtools) references/pre-build-gate.md
  Applies Task-Size Scaling (L1 to L5)
         │
         ▼
[ 4. PRE-BUILD DESIGN GATE ] ───────────────► scripts/plan-check.mjs
  Validates .taste-skill/design-plan.md        Gate States: DISCOVERY_REQUIRED -> READY
  Rejects unvalidated code synthesis
         │
         ▼
[ 5. IMPLEMENTATION & EXISTING GATE ] ──────► Existing scripts/gate.mjs
  Maintains consistency.mjs, copy-lint.mjs     Existing assets/layout/check.mjs
  Browser verification & delivery
```

---

## 2. Planned Components & Locations

### A. References (`skills/taste-skill/references/`)
1. `instruction-governance.md`: Rules for discovering and prioritizing project instructions.
2. `anti-slop-governance.md`: Identification, scoring, and remediation of AI visual slop patterns.
3. `existing-project-audit.md`: Protocols for inspecting brownfield applications without rewrites.
4. `adaptive-design-intelligence.md`: Category-specific design principles (16 industry verticals).
5. `design-system-governance.md`: Token reuse, surface hierarchy, and component consistency rules.
6. `pre-build-gate.md`: 25-point design plan specification and gate state machine.

### B. Scripts (`skills/taste-skill/scripts/`)
1. `instruction-audit.mjs`: CLI tool scanning current and parent directories for instruction files.
2. `audit-slop.mjs`: Pattern-matching scanner detecting CSS, HTML, and design token visual slop.
3. `plan-check.mjs`: Pre-build gate validator verifying `.taste-skill/design-plan.md`.

### C. Skill & Plugin Integration
1. `skills/taste-skill/SKILL.md`: Update lifecycle instructions and enforce pre-build gate before synthesis.
2. `README.md` & `CHANGELOG.md`: Document new capabilities and usage instructions.
3. `tests/test-governance.mjs`: Automated test suite exercising discovery, slop auditing, and plan validation.
