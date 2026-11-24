---
id: design-system-engineering
name: Design System Engineering Skill
version: 1.0.0
category: design
description: Design tokens (color, type, space, elevation), theme architecture, component primitives, variants, states, and design governance.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/design-system-engineering/SKILL.md
triggers:
  - design system
  - design tokens
  - tokens
  - color palette
  - theme
  - dark mode
  - light mode
  - component library
  - typography scale
  - spacing tokens
  - ui components
  - variants
  - primitives
negative_triggers:
  - backend-only
  - cli-only
  - no-ui
  - headless
precedence: 12
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
pre_build_gates:
  - Design token contract defined (color, spacing, radius, typography)
  - Theme switching & semantic color mapping specified
  - Component primitive variant matrix documented
finish_gates:
  - Token consistency audit pass (zero hardcoded ad-hoc values)
  - Component state coverage verified (hover, active, focus, disabled)
  - Theme switching verified without layout shift or contrast break
verification:
  - Automated token schema validator
  - Component variant & accessibility test pass
---

# Design System Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `design` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone UX & Frontend Engineering Intelligence  
**Workforce Alignment:** `design-systems-engineer`, `ui-designer`

See canonical specification at [`../../framework/skills/design-system-engineering/SKILL.md`](../../framework/skills/design-system-engineering/SKILL.md).
