---
id: backend-architecture
name: Backend Architecture Engineering Skill
version: 1.0.0
category: backend
description: Modular monoliths, service boundaries, layered architecture, ports & adapters, clean architecture, CQRS, and domain-driven design.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/backend-architecture/SKILL.md
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

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Guide the design, structure, and decomposition of backend software systems, ensuring appropriate complexity, clear domain boundaries, maintainable codebases, and sustainable operational costs.

### Boundaries
- **In Scope:** Monolith vs Modular Monolith vs Microservices trade-offs, layered architecture, Clean Architecture, Hexagonal (Ports & Adapters), Domain-Driven Design (DDD), CQRS, transactional boundaries, and Architecture Decision Records (ADRs).
- **Out of Scope:** Frontend UI widgets and low-level CSS styling.

---

## 2. ARCHITECTURAL DECISION RULES

1. **The Monolith-First Rule:** Always start with a Modular Monolith with clean internal package boundaries unless write traffic exceeds 10,000 writes/second, data volume exceeds 5TB, or organizational boundaries require decoupled deployment pipelines.
2. **Layer Separation:**
   - **Transport Layer:** HTTP/gRPC/WebSocket controllers parsing inputs and formatting responses. Zero business logic.
   - **Application / Service Layer:** Orchestrates domain workflows, transactions, and authorizations.
   - **Domain Layer:** Pure business entities, value objects, and domain invariants. Zero database or network imports.
   - **Infrastructure / Adapter Layer:** Database repositories, external API clients, message publishers.
3. **No Premature Microservices:** Microservices introduce distributed transactions, network latency, and eventual consistency. Never adopt microservices without measurable evidence of operational necessity.
