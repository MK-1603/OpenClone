---
id: accessibility-engineering
name: Accessibility Engineering Skill
version: 1.0.0
category: accessibility
description: Semantic HTML, WCAG 2.2 AA standards, keyboard navigation, focus trapping, screen reader landmarks, color contrast, and reduced motion.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/accessibility-engineering/SKILL.md
triggers:
  - accessibility
  - a11y
  - wcag
  - aria
  - screen reader
  - keyboard navigation
  - focus trap
  - contrast
  - color contrast
  - reduced motion
  - semantic html
  - landmark
  - alt text
negative_triggers:
  - backend-only
  - cli-only
  - no-ui
  - headless
precedence: 16
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
pre_build_gates:
  - Semantic HTML heading & landmark hierarchy mapped
  - Color contrast ratio pre-flight check (4.5:1 text, 3:1 controls)
  - Modal focus trap & keyboard navigation strategy specified
finish_gates:
  - WCAG 2.2 AA compliance verified with zero critical defects
  - Full keyboard-only walkthrough verified (no keyboard traps)
  - prefers-reduced-motion media query verified across animations
verification:
  - Automated axe-core / a11y linter checks
  - Screen reader landmark & accessibility tree audit
---

# Accessibility Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `accessibility` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone UX & Frontend Engineering Intelligence  
**Workforce Alignment:** `accessibility-specialist`, `frontend-engineer`, `frontend-test-engineer`

See canonical specification at [`../../framework/skills/accessibility-engineering/SKILL.md`](../../framework/skills/accessibility-engineering/SKILL.md).
