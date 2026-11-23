# Taste Skill Upgrade Deliverable Manifest

| Artifact Path | Category | Purpose | Status | Implementation Notes | Test Reference |
|---|---|---|---|---|---|
| `docs/upgrade/repository-inventory.md` | Phase 0 Audit | Full repository baseline inventory | VALIDATED | Completed in Phase 0 | Manual review |
| `docs/upgrade/gap-analysis.md` | Phase 0 Audit | Gap analysis vs upgrade charter | VALIDATED | Completed in Phase 0 | Manual review |
| `docs/upgrade/architecture-plan.md` | Phase 0 Audit | Minimal target architecture plan | VALIDATED | Completed in Phase 0 | Manual review |
| `docs/upgrade/DELIVERABLE-MANIFEST.md` | Phase 0 Audit | File-by-file tracking manifest | VALIDATED | Active manifest | Manual review |
| `skills/taste-skill/references/instruction-governance.md` | Phase 3 Governance | Instruction discovery & precedence rules | VALIDATED | Discovers local and parent instructions, precedence ladder, conflict resolution | `tests/test-governance.mjs` |
| `skills/taste-skill/scripts/instruction-audit.mjs` | Phase 3 Governance | CLI for instruction discovery | VALIDATED | Zero-dependency Node 22 ESM CLI, outputs `.taste-skill/reports/instruction-audit.md` | `tests/test-governance.mjs` |
| `skills/taste-skill/references/existing-project-audit.md` | Phase 3 Governance | Brownfield inspection protocol | VALIDATED | Framework, token, and asset audit with PRESERVE/MODIFY/REMOVE/ADD model | `tests/test-governance.mjs` |
| `skills/taste-skill/references/pre-build-gate.md` | Phase 3 Governance | Pre-build gate & plan spec | VALIDATED | 25-point plan spec, Task Levels 1–5 sizing, gate states (READY, PLAN_REQUIRED, PLAN_INVALID) | `tests/test-governance.mjs` |
| `skills/taste-skill/scripts/plan-check.mjs` | Phase 3 Governance | Automated design plan validator | VALIDATED | Deterministic CLI gate validating `.taste-skill/design-plan.md` | `tests/test-governance.mjs` |
| `skills/taste-skill/references/anti-slop-governance.md` | Phase 4 Anti-Slop | Visual slop catalogue & justification | VALIDATED | Anti-slop taxonomy, treatment classification (REQUIRED to PROHIBITED) | `tests/test-governance.mjs` |
| `skills/taste-skill/scripts/audit-slop.mjs` | Phase 4 Anti-Slop | Static anti-slop code & token scanner | VALIDATED | Scans CSS/HTML/JS for glassmorphism, floating blobs, neon glows, purple gradients | `tests/test-governance.mjs` |
| `skills/taste-skill/references/adaptive-design-intelligence.md` | Phase 5 Adaptive Design | 16 product domain design standards | VALIDATED | Design profiles across SaaS, AI apps, DevTools, Dashboards, Healthcare, Finance, etc. | `tests/test-governance.mjs` |
| `skills/taste-skill/references/design-system-governance.md` | Phase 5 Adaptive Design | Design tokens & surface hierarchy | VALIDATED | Token reuse, 4-tier surface hierarchy (Base, S1, S2, Overlay), contrast rules | `tests/test-governance.mjs` |
| `skills/taste-skill/SKILL.md` | Phase 6 Integration | Updated lifecycle & gate hooks | VALIDATED | v2.6.0 header, Mandatory Workflow, House Rule 0 (Pre-Build Gate & Instruction-First) | `tests/text-encoding.mjs` |
| `README.md` | Phase 8 Documentation | Updated public documentation | VALIDATED | Documents v2.6.0 features, 5-phase workflow, and new CLI tools | Manual review |
| `CHANGELOG.md` | Phase 8 Documentation | v2.6.0 release notes | VALIDATED | Complete release notes for 2.6.0 (2026-11-22) | Manual review |
| `tests/test-governance.mjs` | Phase 7 Testing | Unit tests for new scripts | VALIDATED | 13 automated tests covering instruction audit, anti-slop scanner, and plan validator | `tests/test-governance.mjs` |
