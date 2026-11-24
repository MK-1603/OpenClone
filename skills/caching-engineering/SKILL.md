---
id: caching-engineering
name: Caching Engineering Skill
version: 1.0.0
category: backend
description: Cache-aside, read/write-through, stampede prevention, TTL strategies, invalidation, Redis data structures, and multi-tenant cache isolation.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/caching-engineering/SKILL.md
triggers:
  - cache
  - caching
  - redis
  - memcached
  - cache-aside
  - cache invalidation
  - ttl
  - stampede
  - thundering herd
  - xfetch
negative_triggers:
  - no-cache
  - static-only
precedence: 24
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
  - cli
pre_build_gates:
  - Cache topology selected (in-memory LRU vs distributed Redis)
  - Key namespacing scheme defined (including tenant prefix)
  - Invalidation strategy documented (TTL-based vs event-driven)
finish_gates:
  - Cache key collisions and leakage prevented via strict namespacing
  - Cache stampede protection verified (probabilistic early expiration or mutex)
  - Fallback on cache backend failure verified (graceful database fallback)
verification:
  - Automated cache hit/miss/invalidation unit tests
  - Multi-tenant cache isolation test pass
---

# Caching Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `backend` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone Backend & Caching Intelligence  
**Workforce Alignment:** `backend-architect`, `backend-engineer`, `performance-test-engineer`

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Accelerate data access, reduce database load, and improve backend throughput while preventing data inconsistency, cache stampedes, and cross-tenant data leakage.

### Boundaries
- **In Scope:** Application-layer caching (Cache-Aside, Write-Through), Redis data structures (Strings, Hashes, Sorted Sets), TTL strategies, cache invalidation, stampede prevention (XFetch / distributed mutex), and multi-tenant key isolation.
- **Out of Scope:** CDN static asset caching and browser HTTP caching.

---

## 2. CANONICAL CACHING RULES

1. **Cache-Aside Pattern:** The application reads from the cache; on a miss, reads from the database, populates the cache with a defined TTL, and returns. On mutation, invalidate the cache key immediately.
2. **Deterministic Key Namespacing:**
   - Single-tenant: `{service}:{entity}:{id}` (e.g., `user-service:user:42`)
   - Multi-tenant: `tenant:{tenant_id}:{service}:{entity}:{id}` (e.g., `tenant:acme:billing:subscription:active`)
   - Never use raw un-namespaced keys.
3. **Cache Stampede Prevention:**
   When high-traffic keys expire, thousands of concurrent requests can overwhelm the database. Prevent this via:
   - **XFetch (Probabilistic Early Expiration):** Background worker recalculates the cache before true expiration.
   - **Distributed Mutex Lock:** Only one worker acquires a lock to recompute the value; others wait or receive stale data.
4. **Resilient Failure Mode:** If Redis or the caching tier fails, the application must gracefully fall back to the primary database rather than returning 500 errors.
