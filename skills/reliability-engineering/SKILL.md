---
id: reliability-engineering
name: Reliability & Resilience Engineering Skill
version: 1.0.0
category: reliability
description: Circuit breakers, timeouts, retries with exponential backoff & jitter, bulkheads, health checks, and SLO/SLI/SLA.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/reliability-engineering/SKILL.md
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

See canonical specification at [`../../framework/skills/reliability-engineering/SKILL.md`](../../framework/skills/reliability-engineering/SKILL.md).
