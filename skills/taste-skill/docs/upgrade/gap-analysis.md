# Taste Skill Gap Analysis & Target Upgrade Specification
**Target:** `taste-skill` v2.5.1 -> v2.6.0 (Instruction-First & Anti-Slop Governance)

---

## 1. Requirement Comparison Matrix

| Requirement from Upgrade Charter | Existing Status in v2.5.1 | Gap Severity | Target Implementation in v2.6.0 |
|---|---|---|---|
| **1. Stop Immediate Code Generation** | NOT IMPLEMENTED. Agent immediately starts generating HTML. | CRITICAL | Mandatory Pre-Build Gate requiring `.taste-skill/design-plan.md` before coding. |
| **2. Instruction Discovery Engine** | NOT IMPLEMENTED. Only reads `library/*.json` and brief. | CRITICAL | `scripts/instruction-audit.mjs` & `references/instruction-governance.md`. |
| **3. Project-Level Rules & Precedence** | NOT IMPLEMENTED. Ignores `.cursorrules`, `AGENTS.md`, `CLAUDE.md`. | HIGH | Inherited discovery + conflict resolution engine. |
| **4. Anti-AI-Slop Governance Engine** | PARTIAL. Has `copy-lint.mjs` for text, but visual anti-slop is reactive post-render. | CRITICAL | `scripts/audit-slop.mjs` & `references/anti-slop-governance.md` evaluating visual patterns (REQUIRED / JUSTIFIED / OPTIONAL / UNNECESSARY / PROHIBITED). |
| **5. Existing Project First** | NOT IMPLEMENTED. Assumes greenfield HTML/CSS build. | HIGH | `references/existing-project-audit.md` + token/framework inspection protocol. |
| **6. Adaptive Design Intelligence** | PARTIAL. Has 6 basic `--page` kinds, lacks fine-grained domain reasoning. | MEDIUM | `references/adaptive-design-intelligence.md` covering 16 product domains (SaaS, AI, Healthcare, Finance, etc.). |
| **7. Pre-Build Design Gate** | NOT IMPLEMENTED. Only has finish gate (`gate.mjs`). | CRITICAL | `scripts/plan-check.mjs` & `references/pre-build-gate.md` enforcing 25-point design plan. |
| **8. Removal Before Adding** | NOT IMPLEMENTED. Adds sections additively. | HIGH | Mandatory `PRESERVE / MODIFY / REMOVE / ADD` classification in design plan. |
| **9. Design System Governance** | PARTIAL. Rigid palette/type dealers, no host token reuse. | MEDIUM | `references/design-system-governance.md` + token reuse engine. |
| **10. Task-Size Intelligence** | NOT IMPLEMENTED. Treats all tasks with uniform weight. | MEDIUM | 5-level task taxonomy (Level 1 Micro-Fix to Level 5 New Product Interface). |
| **11. Automated Plan Validation** | NOT IMPLEMENTED. | HIGH | Automated CLI validator `node scripts/plan-check.mjs` checking plan validity. |
| **12. Backward Compatibility** | EXISTING. Chrome CDP testing and finish gate work well. | ESSENTIAL | Preserve `consistency.mjs`, `copy-lint.mjs`, and `gate.mjs` without regressions. |

---

## 2. Architectural Risks & Mitigations

1. **Risk: Process Overhead for Minor Tasks.**  
   *Mitigation:* Task-Size Intelligence (Levels 1–2 require only a lightweight 4-point plan; Levels 3–5 require the full 25-point plan).
2. **Risk: Breaking Existing Finish Gate.**  
   *Mitigation:* `plan-check.mjs` acts upstream as a Pre-Build Gate. The finish gate (`gate.mjs`) remains unchanged or lightly extended to confirm plan presence.
3. **Risk: External Dependency Bloat.**  
   *Mitigation:* Zero npm dependencies. All new scripts (`instruction-audit.mjs`, `audit-slop.mjs`, `plan-check.mjs`) are authored in native Node.js 22 ES modules.
