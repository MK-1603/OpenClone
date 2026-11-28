# 21 — Distributed Systems & Scalability
**OpenClone Canonical Engineering Domain**  
*Governed by OpenClone Global Standards | Domain Owner: Distributed Systems Engineer / Cloud Architect*

---

## 1. Purpose & Scope
This domain defines the canonical OpenClone guidance for distributed architectures, messaging, asynchronous background jobs, caching strategies, horizontal scalability, and distributed coordination.

## 2. Core Distributed Systems Standards
- **Consistency & State:**
  - CAP theorem and PACELC trade-offs. Distinguish strong consistency (RDBMS) from eventual consistency (replicated distributed stores).
  - Outbox Pattern: Ensure atomic state mutations and message publishing using the transactional outbox pattern to prevent two-phase commit overhead.
  - Idempotent Message Consumers: Handle duplicate deliveries gracefully via message deduplication tables and unique event IDs.
- **Asynchronous Processing:**
  - Dead-Letter Queues (DLQ) for poison messages with alerting and replay capabilities.
  - Worker pool sizing and backpressure monitoring to prevent queue starvation.
- **Caching Topologies:**
  - Cache-Aside pattern with explicit TTLs and cache warming.
  - Cache stampede prevention using probabilistic early expiration (XFetch) or distributed mutexes.
  - Multi-tenant cache key namespacing (`{tenant_id}:{entity}:{id}`) to prevent cross-tenant data leakage.

## 3. Related Specialist Skills
- [`distributed-systems-engineering`](../../skills/distributed-systems-engineering/SKILL.md) — Distributed consensus, outbox pattern, and saga orchestration.
- [`caching-engineering`](../../skills/caching-engineering/SKILL.md) — Cache-aside, TTL invalidation, Redis structures, and stampede prevention.
- [`async-processing-engineering`](../../skills/async-processing-engineering/SKILL.md) — Message queues, background workers, and dead-letter queues.

## 4. References & Catalogues
- Knowledge Catalogue: [`../../../docs/reference/guidance/backend-system-design-catalogue.md`](../../../docs/reference/guidance/backend-system-design-catalogue.md)
