---
id: reliability-engineering
name: Reliability & Resilience Engineering Skill
version: 1.0.0
category: reliability
description: Circuit breakers, timeouts, retries with exponential backoff & jitter, bulkheads, health checks, and SLO/SLI/SLA.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/reliability-engineering/SKILL.md
triggers:
  - reliability
  - resilience
  - fault tolerance
  - circuit breaker
  - timeout
  - retries
  - exponential backoff
  - jitter
  - bulkhead
  - health check
  - liveness probe
  - readiness probe
  - slo
  - sli
  - sla
negative_triggers:
  - script-only
  - toy-project
precedence: 27
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
  - cli
pre_build_gates:
  - Downstream dependency timeouts and circuit breaker thresholds defined
  - Retry policy with exponential backoff and jitter configured
  - Liveness and readiness probe specifications documented
finish_gates:
  - Circuit breaker tri-state transitions verified (Closed -> Open -> Half-Open)
  - Retry storm prevention verified (jitter prevents synchronized bursts)
  - Graceful shutdown handles in-flight transactions within deadline
verification:
  - Dependency failure and circuit breaker recovery tests
  - Timeout and retry backoff timing assertions
---

# Reliability & Resilience Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `reliability` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone SRE & Reliability Intelligence  
**Workforce Alignment:** `site-reliability-engineer`, `reliability-test-engineer`

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Build resilient backend systems capable of withstanding transient network failures, downstream service outages, traffic surges, and unexpected hardware restarts without cascading outages.

### Boundaries
- **In Scope:** Circuit breakers, bounded timeouts, retries with exponential backoff and randomized jitter, bulkheads, load shedding, graceful process termination, health probes, and SLO/SLI tracking.
- **Out of Scope:** Manual incident escalation call trees.

---

## 2. CANONICAL RELIABILITY PRINCIPLES

1. **Every Network Call Has a Timeout:** Never make an outbound HTTP request, database query, or cache call without an explicit timeout (e.g. 500ms for cache, 2s for DB query, 5s for external API).
2. **Exponential Backoff with Full Jitter:**
   Retries without jitter synchronize clients, creating destructive **retry storms** that keep downed services from recovering. Always apply randomized jitter:
   ```python
   sleep_duration = random.uniform(0, min(max_backoff, base_backoff * (2 ** attempt)))
   ```
3. **Tri-State Circuit Breakers:**
   - **CLOSED:** Normal operation; failures are counted.
   - **OPEN:** After threshold failures (e.g. 5 in 10s), trip immediately and fast-fail outbound requests without executing.
   - **HALF-OPEN:** After a cooldown (e.g. 30s), allow a limited probe request to test downstream recovery.
4. **Health Check Probes:**
   - `/health/liveness`: Checks if the process is responsive (if failing, restart container).
   - `/health/readiness`: Checks if DB and critical dependencies are ready (if failing, remove from load balancer).
