# OpenClone Specialist Skills Directory
**Canonical Specialist Skills Directory for System Design, Backend, Communication & Frontend Engineering**  
*Managed by `src/openclone/skills/engine.py` | Registered in `framework/registries/SKILL-REGISTRY.md`*

---

## 1. Directory Overview

This directory contains reusable, versioned, independently verifiable engineering skills bundled with OpenClone:

### UI/UX, Design Systems & Frontend
- [`ux-pro/`](ux-pro/SKILL.md) — **UX Pro Skill (v1.0.0, Precedence 8)**: User research, product UX, information architecture, primary user journeys, critical task decision flows, interaction models, UX writing, and usability testing.
- [`taste-skill/`](taste-skill/SKILL.md) — **Taste Skill (v2.6.0, Precedence 10)**: Core anti-AI-slop design governance, visual hierarchy, responsive layout, and adaptive design intelligence.
- [`design-system-engineering/`](design-system-engineering/SKILL.md) — **Design System Engineering Skill (v1.0.0, Precedence 12)**: Tiered design tokens, theme architecture (light/dark/custom), component primitives, variant matrices, and design governance.
- [`responsive-engineering/`](responsive-engineering/SKILL.md) — **Responsive Engineering Skill (v1.0.0, Precedence 14)**: Mobile-first responsive development, standard 11-tier viewport matrix (320px to 1440px+), touch target sizing (44x44px), adaptive navigation, and zero overflow.
- [`accessibility-engineering/`](accessibility-engineering/SKILL.md) — **Accessibility Engineering Skill (v1.0.0, Precedence 16)**: Semantic HTML, WCAG 2.2 AA standards, keyboard navigation, modal focus trapping, visible focus rings, screen reader landmarks, and reduced motion.
- [`frontend-engineering/`](frontend-engineering/SKILL.md) — **Frontend Engineering Skill (v1.0.0, Precedence 18)**: Production frontend architecture, state management, API integration, routing, schema-based forms, CSR/SSR/SSG, XSS prevention, and observability.

### Backend, Database & Distributed Systems
- [`backend-architecture/`](backend-architecture/SKILL.md) — **Backend System Architecture Skill (v1.0.0, Precedence 20)**: Monolith-first principle, bounded contexts, clean/hexagonal architecture, and ADR governance.
- [`database-engineering/`](database-engineering/SKILL.md) — **Database & Data Modeling Skill (v1.0.0, Precedence 21)**: Relational schema normalization, composite indexing, expand-and-contract zero-downtime migrations, and restore verification.
- [`api-engineering/`](api-engineering/SKILL.md) — **API & Integration Engineering Skill (v1.0.0, Precedence 22)**: REST/gRPC/GraphQL contracts, cursor pagination, idempotent mutating endpoints, and RFC 7807 error responses.
- [`rate-limit-engineering/`](rate-limit-engineering/SKILL.md) — **Traffic & Rate Limiting Skill (v1.0.0, Precedence 23)**: Token bucket, sliding window counter, and distributed Redis traffic limiters with standard HTTP 429 headers.
- [`caching-engineering/`](caching-engineering/SKILL.md) — **Caching Topologies Skill (v1.0.0, Precedence 24)**: Cache-aside pattern, explicit TTL invalidation, XFetch probabilistic stampede prevention, and multi-tenant cache keys.
- [`async-processing-engineering/`](async-processing-engineering/SKILL.md) — **Asynchronous Messaging Skill (v1.0.0, Precedence 25)**: Message queues, transactional outbox pattern, dead-letter queues (DLQ), and idempotent consumer workers.
- [`distributed-systems-engineering/`](distributed-systems-engineering/SKILL.md) — **Distributed Systems Skill (v1.0.0, Precedence 26)**: CAP/PACELC trade-offs, Raft consensus, distributed locking with leases, and saga choreography/orchestration.
- [`reliability-engineering/`](reliability-engineering/SKILL.md) — **Reliability & Resilience Skill (v1.0.0, Precedence 27)**: Tri-state circuit breakers, bounded timeouts, exponential backoff with full jitter, bulkheads, and health probes.
- [`backend-observability-engineering/`](backend-observability-engineering/SKILL.md) — **Backend Observability Skill (v1.0.0, Precedence 28)**: Structured JSON logging, trace correlation IDs, OpenTelemetry standards, Golden Signals, and credential redaction.
- [`multi-tenant-engineering/`](multi-tenant-engineering/SKILL.md) — **Multi-Tenant SaaS Skill (v1.0.0, Precedence 29)**: Row-Level Security (RLS), tenant context propagation, tenant-scoped caching, and cross-tenant leakage testing.

### System Design, Communication & Notifications
- [`system-design-engineering/`](system-design-engineering/SKILL.md) — **System Design & Capacity Engineering Skill (v1.0.0, Precedence 30)**: Back-of-the-envelope capacity calculations, C4 architecture diagrams, ADR generation, and 20 real-world case studies.
- [`communication-infrastructure/`](communication-infrastructure/SKILL.md) — **Communication Infrastructure Skill (v1.0.0, Precedence 31)**: Decoupled provider abstraction, priority routing tiers, provider failover, and cryptographic audit ledgers.
- [`email-engineering/`](email-engineering/SKILL.md) — **Email Infrastructure Skill (v1.0.0, Precedence 32)**: SMTP/STARTTLS protocols, SPF/DKIM/DMARC authentication, bounce/complaint suppression, and responsive HTML templates.
- [`sms-engineering/`](sms-engineering/SKILL.md) — **SMS & Verification Skill (v1.0.0, Precedence 33)**: GSM-7 vs UCS-2 encoding calculation, OTP security, attempt rate limits, delivery receipts, and regional compliance (TRAI/DLT).
- [`push-notification-engineering/`](push-notification-engineering/SKILL.md) — **Push Notification Skill (v1.0.0, Precedence 34)**: FCM, APNs, Web Push VAPID keys, device token rotation, and invalid token pruning.
- [`realtime-systems-engineering/`](realtime-systems-engineering/SKILL.md) — **Real-Time Systems & WebSocket Skill (v1.0.0, Precedence 35)**: WebSockets, SSE, handshake authentication, room broadcasting, heartbeats, and online presence tracking.
- [`notification-platform/`](notification-platform/SKILL.md) — **Unified Notification Platform Skill (v1.0.0, Precedence 36)**: User preference matrix, time-zone quiet hours, mandatory security override, and dead-letter processing.

---

## 2. Skill Precedence & Engineering Lifecycle

When multiple skills are activated for a task, they operate under strict deterministic precedence:

```text
PROJECT IDEA
    |
    v
PROJECT CLASSIFICATION (Website, SaaS, Dashboard, Mobile, E-commerce, Distributed, Communication, CLI)
    |
    v
TASK CLASSIFICATION (Intent, discipline, archetype, category)
    |
    v
SKILL SELECTION (Security -> UX -> Taste -> Design System -> Responsive -> A11y -> Frontend -> Backend -> System Design -> Communication)
    |
    v
SKILL LOADING (Manifest validation, on-disk contract resolution)
    |
    v
PRE-BUILD QUALITY GATES (Capacity estimation, token check, plan-check.mjs, ADR validation)
    |
    v
IMPLEMENTATION (PRESERVE, MODIFY, REMOVE, ADD)
    |
    v
FINISH QUALITY GATES (WCAG 2.2 AA, 11-tier viewports, 0 overflow, ADR review, circuit breaker test)
    |
    v
VERIFIED DELIVERY
```

See [`../framework/registries/SKILL-REGISTRY.md`](../framework/registries/SKILL-REGISTRY.md) for full metadata, gates, and CLI instructions.
