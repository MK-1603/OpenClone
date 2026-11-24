---
id: api-engineering
name: API Engineering Skill
version: 1.0.0
category: api
description: REST, GraphQL, gRPC, WebSockets, OpenAPI contracts, pagination, idempotency keys, versioning, status codes, and OWASP API Top 10.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/api-engineering/SKILL.md
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

See canonical specification at [`../../framework/skills/api-engineering/SKILL.md`](../../framework/skills/api-engineering/SKILL.md).
