# Blueprint 02: SaaS Web Application

**Project Family:** `web_engineering`  
**Primary Project Type:** `saas_web_app`  
**Maturity Status:** `OPERATIONAL`  
**Complexity Level:** `MEDIUM` to `LARGE`  
**Default Delivery Targets:** `web_browser`, `containers_cloud`

---

## 1. Goals & Scope
- Multi-tenant software-as-a-service application providing authenticated dashboards, user management, database persistence, external integrations, and subscription billing.
- Enforces strict tenant data isolation, role-based access control (RBAC), idempotency, and audit logging.

## 2. Classification Rules
- Matched when the project requires user authentication, database persistence, CRUD workflows, APIs, multi-tenancy, or team permissions.

## 3. Intake Questions & Required Information
1. Multi-tenancy model: schema-per-tenant, row-level security (`tenant_id`), or isolated databases.
2. Authentication provider: Auth0, Supabase Auth, Clerk, NextAuth, or custom JWT/sessions.
3. Database technology: PostgreSQL, SQLite, MySQL with Prisma/Drizzle ORM.
4. Billing integration: Stripe checkout, customer portal, webhook lifecycle, or free tier.
5. Frontend framework: Next.js App Router, Remix, React + Vite, Vue/Nuxt.

## 4. Conditional Requirements
- If payment processing: webhook reconciliation with HMAC signature verification.
- If real-time notifications: WebSocket or Server-Sent Events (SSE) presence.
- If background processing: Redis/BullMQ task queue.

## 5. Domain & Capability Mapping
- **Mandatory Domains:** `00-GOVERNANCE`, `01-SPECIFICATION`, `02-ARCHITECTURE`, `03-DATA-INTEGRITY`, `04-SECURITY-CONTROLS`, `05-DESIGN-SYSTEMS`, `08-API-CONTRACTS`, `10-TESTING-AND-QA`, `11-PERMISSIONS-AND-ACCESS-CONTROL`.
- **Mandatory Engines:** `E-001`, `E-002`, `E-003`, `E-004`, `E-007`, `E-008`, `E-010`, `E-013`.

## 6. Specialist Workforce
- `fullstack-engineer`: End-to-end integration of server actions, API routes, and client state.
- `database-architect`: Relational schema design, migrations, indexing, and row-level security.
- `security-engineer`: CSRF, CORS, session fixation, least-privilege RBAC, and secret redaction.
- `qa-engineer`: E2E user journeys, integration tests, and edge case validation.

## 7. Tool & Model Allocation
- **Primary Model:** `gpt-6.2-sol` for business logic; `gpt-6.2-astra` for database schemas and multi-tenant isolation architectures.

## 8. Workflow Stages
1. `WF-001` → `WF-002`: Discovery, PRD, and acceptance matrix sign-off.
2. `WF-003`: Task DAG decomposition with dependency ordering.
3. `WF-009`: Human approval of data model and security plan.
4. `WF-004`: Minimal viable diff implementation.
5. `WF-005` & `WF-006`: Pinned security scanner audit and automated test suite.
6. `WF-007`: Independent verification (Goldfish Protocol).
7. `WF-014`: Release gate checklist.

## 9. Verification & Delivery Artifacts
- Database migrations with rollback scripts.
- Unit and integration tests covering multi-tenant isolation.
- OpenAPI 3.1 specification for API endpoints.
- Dockerfile for containerized deployment.
