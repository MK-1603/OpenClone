---
id: rate-limit-engineering
name: Rate Limiting & Traffic Engineering Skill
version: 1.0.0
category: backend
description: Token bucket, leaky bucket, sliding window counter, distributed Redis limiters, HTTP 429, Retry-After, and differentiated endpoint protection.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/rate-limit-engineering/SKILL.md
triggers:
  - rate limit
  - rate limiting
  - throttling
  - traffic management
  - token bucket
  - sliding window
  - leaky bucket
  - 429
  - retry after
  - brute force prevention
  - abuse prevention
negative_triggers:
  - static-site
  - offline-only
precedence: 23
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
  - cli
pre_build_gates:
  - Endpoint rate limit tier matrix defined (auth, search, public, private)
  - Storage backend selected (in-memory for single instance, Redis for distributed cluster)
  - Fail-safe strategy specified (fail-closed for auth, fail-open for public content)
finish_gates:
  - Standard headers injected (RateLimit-Limit, RateLimit-Remaining, RateLimit-Reset, Retry-After)
  - HTTP 429 response formatting verified with structured error payload
  - Concurrent request burst and window reset behavior tested
verification:
  - Automated rate limit threshold test fixtures
  - Multi-client isolation verification test
---

# Rate Limiting & Traffic Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `backend` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone Backend & Traffic Intelligence  
**Workforce Alignment:** `api-architect`, `security-lead`, `backend-engineer`

See canonical specification at [`../../framework/skills/rate-limit-engineering/SKILL.md`](../../framework/skills/rate-limit-engineering/SKILL.md).
