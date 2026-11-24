---
id: multi-tenant-engineering
name: Multi-Tenant SaaS Engineering Skill
version: 1.0.0
category: security
description: Shared database vs database-per-tenant, Row-Level Security, tenant context propagation, and cross-tenant leakage testing.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/multi-tenant-engineering/SKILL.md
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

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Guarantee strict data isolation, resource fairness, and security boundaries between independent organizations, accounts, or tenants sharing a common backend infrastructure.

### Boundaries
- **In Scope:** Tenancy architectures (Shared DB + RLS, Schema-per-tenant, DB-per-tenant), tenant context propagation in async workers and request headers, tenant-scoped caching, and automated cross-tenant leakage tests.
- **Out of Scope:** Multi-tenant billing checkout screens.

---

## 2. CANONICAL MULTI-TENANCY RULES

1. **Never Trust Client-Supplied Tenant IDs:**
   A client-supplied header (`X-Tenant-ID`) or URL parameter (`/tenant-42/projects`) must NEVER be used to query data without server-side validation against the authenticated user's verified organization memberships.
2. **Defense-in-Depth Isolation:**
   - **Application Layer:** ORM queries filtered by `where: { tenant_id: ctx.tenant_id }`.
   - **Database Layer (RLS):** Database Row-Level Security policies active on all multi-tenant tables (`USING (tenant_id = current_setting('app.current_tenant_id'))`).
3. **Tenant-Aware Caching & Queues:**
   Every cache key and background job payload must include the `tenant_id` prefix (e.g. `tenant:123:user:456`) to prevent cache contamination and cross-tenant job execution.
4. **Automated Cross-Tenant Penetration Tests:**
   Release pipelines must run automated tests verifying that Tenant A credentials cannot read, update, or delete Tenant B records under any endpoint.
