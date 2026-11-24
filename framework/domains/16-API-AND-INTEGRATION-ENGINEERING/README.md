# 16 — API & Integration Engineering
**OpenClone Canonical Engineering Domain**  
*Governed by OpenClone Global Standards | Domain Owner: API Architect / Integration Architect*

---

## 1. Purpose & Scope
This domain defines the canonical OpenClone guidance for designing, implementing, securing, documenting, and versioning APIs across REST, GraphQL, gRPC, WebSockets, and Webhooks.

## 2. Core API Engineering Standards
- **Contract-First Design:** Author clear OpenAPI 3.1 / JSON Schema specifications before writing endpoint logic. Enforce strict request and response schema validation.
- **REST Conventions:** Consistent HTTP verbs (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`), semantic status codes (`200`, `201`, `204`, `400`, `401`, `403`, `404`, `409`, `422`, `429`, `500`), cursor-based or offset pagination, and structured error payloads (RFC 7807 Problem Details).
- **Idempotency & Safe Retries:** Mandate `Idempotency-Key` headers on non-idempotent mutation endpoints (`POST /payments`, `POST /orders`) with atomic request deduplication.
- **OWASP API Security Top 10:** Enforce server-side object-level authorization (BOLA/IDOR prevention), function-level authorization (BFLA), mass-assignment protection, and SSRF prevention on webhook receivers.
- **Rate Limiting & Throttling:** Tiered rate limits per IP, user, tenant, and route with standard `RateLimit-*` and `Retry-After` response headers.

## 3. Related Specialist Skills
- [`api-engineering`](../../skills/api-engineering/SKILL.md) — REST/gRPC/GraphQL contracts, pagination, idempotency, and versioning.
- [`rate-limit-engineering`](../../skills/rate-limit-engineering/SKILL.md) — Token bucket, sliding window, and distributed Redis traffic limiters.

## 4. References & Catalogues
- Knowledge Catalogue: [`../../../docs/reference/guidance/backend-system-design-catalogue.md`](../../../docs/reference/guidance/backend-system-design-catalogue.md)
- WAF Engine: `src/openclone/security/waf.py` (`WafInspector`)
