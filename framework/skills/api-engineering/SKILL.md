---
id: api-engineering
name: API Engineering Skill
version: 1.0.0
category: api
description: REST, GraphQL, gRPC, WebSockets, OpenAPI contracts, pagination, idempotency keys, versioning, status codes, and OWASP API Top 10.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/api-engineering/SKILL.md
triggers:
  - api
  - rest
  - rest api
  - openapi
  - graphql
  - grpc
  - websocket
  - webhooks
  - endpoints
  - http status
  - pagination
  - idempotency
  - idempotency key
  - api contract
negative_triggers:
  - frontend-only
  - static-site
  - no-api
precedence: 22
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
  - cli
pre_build_gates:
  - OpenAPI 3.1 / JSON Schema contract authored
  - Authentication and authorization scopes defined for each route
  - Idempotency policy specified for non-idempotent mutations
finish_gates:
  - API schema contract conformance pass (request & response validation)
  - Semantic HTTP status code validation (200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 500)
  - OWASP API Security Top 10 pre-flight audit pass
verification:
  - Automated API contract testing (e.g. Schemathesis or pytest HTTP test fixtures)
  - Idempotency replay test pass
---

# API Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `api` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone Backend & API Intelligence  
**Workforce Alignment:** `api-architect`, `backend-engineer`, `integration-architect`

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Design, specify, document, implement, and secure production-grade APIs. Enforce contract-first development, strict payload schema validation, semantic HTTP standards, idempotent operations, and OWASP API Top 10 defenses.

### Boundaries
- **In Scope:** REST, GraphQL, gRPC, WebSockets, Server-Sent Events, Webhooks, OpenAPI specifications, request validation, response serialization, cursor/offset pagination, versioning (`/v1`), idempotency keys, and API gateway routing.
- **Out of Scope:** Internal database schema design and frontend rendering.

---

## 2. CORE API ENGINEERING RULES

1. **Contract-First Development:** Author and validate the OpenAPI specification or Protobuf schema before writing endpoint handler code.
2. **Standardized Response Shapes:**
   - **Success (Single):** `{ "data": { ... } }`
   - **Success (Paginated):** `{ "data": [ ... ], "pagination": { "next_cursor": "...", "has_more": true, "total": 120 } }`
   - **Error (RFC 7807):** `{ "type": "https://api.example.com/errors/invalid-input", "title": "Validation Error", "status": 422, "detail": "...", "errors": [ ... ] }`
3. **Idempotency on Mutations:** Non-idempotent operations (payment processing, resource creation) must require an `Idempotency-Key` header with atomic cache locking and cached replay responses.
4. **Server-Side Authorization:** Every endpoint must explicitly enforce authentication and authorization. Never rely on client-side route guards or hidden URLs.
