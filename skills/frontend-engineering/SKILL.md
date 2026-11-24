---
id: frontend-engineering
name: Frontend Engineering Skill
version: 1.0.0
category: frontend
description: Production frontend architecture, state management, API integration, routing, forms, rendering (CSR/SSR/SSG), XSS prevention, and observability.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/frontend-engineering/SKILL.md
triggers:
  - frontend
  - ui
  - react
  - next.js
  - nextjs
  - vue
  - nuxt
  - svelte
  - sveltekit
  - astro
  - angular
  - component
  - tailwind
  - css
  - html
  - web app
  - state management
  - client-side
  - routing
negative_triggers:
  - backend-only
  - cli-only
  - no-ui
  - headless
precedence: 18
dependencies:
  - responsive-engineering
  - accessibility-engineering
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
pre_build_gates:
  - Component architecture & folder structure specified
  - State management & API contract integration strategy defined
  - Form schema validation rules established
finish_gates:
  - Zero TypeScript compiler errors & zero linter errors
  - Production build succeeds without warnings
  - Critical error boundaries & API retry flows verified
verification:
  - Automated component & unit test suite pass
  - End-to-end integration test pass
---

# Frontend Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `frontend` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone UX & Frontend Engineering Intelligence  
**Workforce Alignment:** `frontend-architect`, `frontend-engineer`, `web-performance-engineer`

See canonical specification at [`../../framework/skills/frontend-engineering/SKILL.md`](../../framework/skills/frontend-engineering/SKILL.md).
