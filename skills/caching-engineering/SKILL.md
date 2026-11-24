---
id: caching-engineering
name: Caching Engineering Skill
version: 1.0.0
category: backend
description: Cache-aside, read/write-through, stampede prevention, TTL strategies, invalidation, Redis data structures, and multi-tenant cache isolation.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/caching-engineering/SKILL.md
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

See canonical specification at [`../../framework/skills/caching-engineering/SKILL.md`](../../framework/skills/caching-engineering/SKILL.md).
