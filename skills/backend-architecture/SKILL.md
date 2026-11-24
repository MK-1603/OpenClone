---
id: backend-architecture
name: Backend Architecture Engineering Skill
version: 1.0.0
category: backend
description: Modular monoliths, service boundaries, layered architecture, ports & adapters, clean architecture, CQRS, and domain-driven design.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/backend-architecture/SKILL.md
triggers:
  - backend
  - backend architecture
  - modular monolith
  - microservices
  - service boundaries
  - domain-driven design
  - clean architecture
  - hexagonal architecture
  - ports and adapters
  - cqrs
  - event sourcing
negative_triggers:
  - frontend-only
  - static-site
  - ui-only
precedence: 20
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
  - cli
pre_build_gates:
  - Architecture justification documented (monolith-first validated)
  - Service and domain module boundaries defined
  - Architecture Decision Record (ADR) authored
finish_gates:
  - Package boundary isolation verified (no circular dependencies)
  - Data mutation transaction boundaries verified
verification:
  - Static dependency analysis / architecture linter pass
  - Domain integration tests pass
---

# Backend Architecture Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `backend` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone Backend & System Design Intelligence  
**Workforce Alignment:** `principal-architect`, `backend-architect`, `backend-engineer`

See canonical specification at [`../../framework/skills/backend-architecture/SKILL.md`](../../framework/skills/backend-architecture/SKILL.md).
