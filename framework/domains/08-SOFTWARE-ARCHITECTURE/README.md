# 08 — Software Architecture & System Design
**OpenClone Canonical Engineering Domain**  
*Governed by OpenClone Global Standards | Domain Owner: System Architect / Principal Architect*

---

## 1. Purpose & Scope
This domain defines the canonical OpenClone guidance for system-level software architecture, component boundaries, communication protocols, and architectural trade-off evaluations. It establishes when to choose a modular monolith versus microservices, synchronous versus asynchronous communication, and serverless versus long-running services.

## 2. Core Architectural Pillars
- **Monolith-First Principle:** Start with a well-structured Modular Monolith with strict internal package boundaries and database transactions. Introduce distributed microservices, message brokers, and distributed transactions only when measurable concurrency (>10k writes/sec), data volume (>10TB), or independent organizational scaling demands it.
- **Architectural Patterns:**
  - Layered Architecture, Clean Architecture, and Hexagonal (Ports & Adapters).
  - Domain-Driven Design (DDD) with clear bounded contexts and ubiquitous language.
  - CQRS (Command Query Responsibility Segregation) and Event Sourcing where auditability or read/write divergence is proven necessary.
  - Backend-for-Frontend (BFF) and API Gateway patterns for multi-client ecosystems.
- **Decision Governance:** Every non-trivial architectural choice requires a documented Architecture Decision Record (ADR) detailing context, options considered, trade-offs, and conditions for revisiting.

## 3. Related Specialist Skills
- [`backend-architecture`](../../skills/backend-architecture/SKILL.md) — Modular monoliths, service boundaries, layering, and design patterns.
- [`distributed-systems-engineering`](../../skills/distributed-systems-engineering/SKILL.md) — CAP theorem, consensus, leader election, and saga patterns.

## 4. References & Catalogues
- Knowledge Catalogue: [`../../../docs/reference/guidance/backend-system-design-catalogue.md`](../../../docs/reference/guidance/backend-system-design-catalogue.md)
- Workforce Alignment: `principal-architect`, `solution-architect`, `backend-architect`
