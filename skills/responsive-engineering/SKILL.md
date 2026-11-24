---
id: responsive-engineering
name: Responsive Engineering Skill
version: 1.0.0
category: frontend
description: Mobile-first responsive layouts, 11-tier viewport matrix, adaptive navigation, touch targets, container queries, and zero overflow.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/responsive-engineering/SKILL.md
triggers:
  - responsive
  - mobile
  - mobile-first
  - breakpoint
  - viewport
  - touch
  - tablet
  - adaptive
  - overflow
  - drawer
  - sheet
  - hamburger
  - safe area
  - media query
  - flexbox
  - grid
negative_triggers:
  - backend-only
  - cli-only
  - no-ui
  - desktop-fixed-only
precedence: 14
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
pre_build_gates:
  - Mobile-first breakpoint strategy defined
  - Mobile navigation & drawer architecture specified
  - Complex desktop component adaptations planned (tables, sidebars)
finish_gates:
  - Standard 11-tier viewport matrix verification pass (320px to 1440px+)
  - Zero unintended horizontal overflow verified (overflow-x: hidden enforced)
  - Interactive touch targets meet minimum 44x44px bounding box
verification:
  - Automated viewport matrix inspection
  - Touch-target geometry and overflow checks
---

# Responsive Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `frontend` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone UX & Frontend Engineering Intelligence  
**Workforce Alignment:** `frontend-engineer`, `ui-designer`, `frontend-test-engineer`

See canonical specification at [`../../framework/skills/responsive-engineering/SKILL.md`](../../framework/skills/responsive-engineering/SKILL.md).
