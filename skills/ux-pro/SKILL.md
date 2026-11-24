---
id: ux-pro
name: UX Pro Skill
version: 1.0.0
category: ux
description: User research, product UX, information architecture, user journeys, interaction design, UX writing, and usability testing.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/ux-pro/SKILL.md
triggers:
  - ux
  - user experience
  - user research
  - user journey
  - task flow
  - usability
  - information architecture
  - wireframe
  - interaction design
  - ux writing
  - empty state
  - onboarding
  - persona
  - user flow
negative_triggers:
  - backend-only
  - cli-only
  - no-ui
  - headless
  - script-only
precedence: 8
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
pre_build_gates:
  - User problem definition & target goals approved
  - Primary user journeys & task flows mapped
  - Information architecture & navigation hierarchy specified
  - Mandatory application states identified
finish_gates:
  - Usability walkthrough pass with zero high-friction blockers
  - Error recovery paths verified for all critical inputs
  - Contextual microcopy & validation feedback verified
verification:
  - Task-based usability inspection
  - State completeness audit (initial, loading, empty, error, recovery)
---

# UX Pro — Specialist Engineering Skill
**Version:** `1.0.0` | **Category:** `ux` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone UX & Frontend Engineering Intelligence  
**Workforce Alignment:** `ux-researcher`, `ux-designer`

See canonical specification at [`../../framework/skills/ux-pro/SKILL.md`](../../framework/skills/ux-pro/SKILL.md).
