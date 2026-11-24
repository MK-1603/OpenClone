---
id: multi-tenant-engineering
name: Multi-Tenant SaaS Engineering Skill
version: 1.0.0
category: security
description: Shared database vs database-per-tenant, Row-Level Security, tenant context propagation, and cross-tenant leakage testing.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/multi-tenant-engineering/SKILL.md
triggers:
  - multi-tenant
  - multi-tenancy
  - tenant
  - tenant isolation
  - rls
  - row level security
  - cross tenant
  - tenant context
  - workspace isolation
negative_triggers:
  - single-tenant-only
  - standalone-app
precedence: 29
dependencies:
  - database-engineering
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
  - cli
pre_build_gates:
  - Tenancy model selected (shared DB with RLS vs schema per tenant vs DB per tenant)
  - Tenant context propagation middleware and database session scoping specified
  - Cross-tenant data isolation test matrix designed
finish_gates:
  - Database Row-Level Security (RLS) policies verified active
  - Cross-tenant read and write attempts strictly rejected
  - Tenant-scoped cache keys and asynchronous jobs verified
verification:
  - Automated cross-tenant leakage test suite pass
  - Unauthenticated / mismatched tenant access rejection test pass
---

# Multi-Tenant SaaS Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `security` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone Multi-Tenant SaaS Intelligence  
**Workforce Alignment:** `security-lead`, `database-architect`, `backend-architect`

See canonical specification at [`../../framework/skills/multi-tenant-engineering/SKILL.md`](../../framework/skills/multi-tenant-engineering/SKILL.md).
