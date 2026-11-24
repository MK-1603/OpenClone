---
id: rate-limit-engineering
name: Rate Limiting & Traffic Engineering Skill
version: 1.0.0
category: backend
description: Token bucket, leaky bucket, sliding window counter, distributed Redis limiters, HTTP 429, Retry-After, and differentiated endpoint protection.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/rate-limit-engineering/SKILL.md
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

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Protect backend systems, databases, APIs, and computational resources against abuse, denial-of-service, credential stuffing, scraping, and unexpected traffic spikes through deterministic, observable traffic governance.

### Boundaries
- **In Scope:** Token bucket, leaky bucket, sliding window counter algorithms, tiered endpoint policies, client key identification (IP, API key, JWT subject, tenant ID), distributed Redis coordination, and standard HTTP rate-limiting headers.
- **Out of Scope:** Network-layer DDoS mitigation (governed by CDN/Cloudflare Layer 3/4 defenses).

---

## 2. DIFFERENTIATED ENDPOINT POLICIES

Never apply a blanket universal limit to all routes. Configure differentiated limits based on endpoint risk and resource consumption:

| Endpoint Type | Recommended Limit | Algorithm | Fail Strategy |
|---|---|---|---|
| **Authentication (`/login`, `/register`)** | 5 requests / 60 sec | Sliding Window Counter | Fail Closed |
| **Password Reset / OTP** | 3 requests / 300 sec | Sliding Window Counter | Fail Closed |
| **Expensive Search / Aggregation** | 30 requests / 60 sec | Token Bucket (burst: 45) | Degraded / Cache |
| **Standard REST API (Authenticated)** | 100 requests / 60 sec | Sliding Window Counter | Fail Open |
| **AI Inference / Expensive LLM** | 15 requests / 60 sec | Token Bucket (burst: 20) | Fail Closed |
| **Data Export / Heavy Batch** | 5 requests / 300 sec | Fixed Window | Fail Closed |

## 3. STANDARD HTTP HEADERS (RFC 6585 & Draft IETF)

Every response evaluated by a rate limiter must include:
```http
RateLimit-Limit: 100
RateLimit-Remaining: 84
RateLimit-Reset: 42
```
And upon rejection (`HTTP 429 Too Many Requests`):
```http
HTTP/1.1 429 Too Many Requests
Retry-After: 42
Content-Type: application/problem+json

{
  "type": "https://api.example.com/errors/rate-limit-exceeded",
  "title": "Too Many Requests",
  "status": 429,
  "detail": "Rate limit exceeded. Please retry after 42 seconds."
}
```
