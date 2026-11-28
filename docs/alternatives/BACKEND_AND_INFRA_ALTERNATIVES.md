# OpenClone — Backend & Infrastructure Alternatives
**Version:** 1.0.0  
**Scope:** Alternatives for backend runtimes, databases, ORMs, caching, job queues, storage, and deployment targets.

---

## 1. Backend Architecture & Runtime Alternatives

| Subsystem | Primary Choice | Fallback Candidate | Specialist Alternative | Recommendation & Trade-Offs |
|---|---|---|---|---|
| **Backend Runtime** | Node.js (TypeScript) / Python | Go (Golang) | Rust | Node.js/Python have the richest AI/agent ecosystems; Go for high throughput |
| **Relational Database** | PostgreSQL v15+ | SQLite3 (WAL mode) | MySQL / MariaDB | PostgreSQL is standard for production SaaS; SQLite for local workbench/CLI |
| **ORM / Query Builder** | Drizzle ORM / Prisma | SQLAlchemy (Python) | Kysely (TypeScript) | Drizzle offers SQL-like performance with zero bloat; Prisma for rapid prototyping |
| **Authentication** | Auth.js / Supabase Auth / Lucia | Clerk (SaaS) | Keycloak (Self-Hosted) | Use self-hosted, portable auth models; avoid proprietary lock-in |
| **Authorization / RBAC** | Custom Database RBAC + RLS | CASL / Permit.io | Open Policy Agent (OPA / Rego) | Centralized database roles provide simplicity; OPA for distributed microservices |
| **Caching & Invalidation** | Redis (ioredis / redis-py) | Dragonfly (Redis compatible) | In-Memory LRU Cache | Redis provides distributed pub/sub and caching; in-memory LRU for single instances |
| **Background Queues** | BullMQ (Redis backed) | Celery (Python) | Temporal (Durable Workflows) | BullMQ for standard async jobs; Temporal for complex long-running state machines |
| **Object / Blob Storage** | AWS S3 / Cloudflare R2 | MinIO (Self-Hosted S3) | Google Cloud Storage | S3 API is universal standard; Cloudflare R2 eliminates egress fees |
| **Search Engine** | PostgreSQL Full-Text Search | Meilisearch | Elasticsearch / Typesense | PostgreSQL FTS eliminates extra infrastructure; Meilisearch for instant search UI |
| **Edge / Web Hosting** | Vercel / Cloudflare Pages | Netlify | AWS ECS / Hetzner VPS | Cloudflare/Vercel for zero-config global edge; Docker on VPS for cost control |
| **Container & CI/CD** | GitHub Actions + Docker | GitLab CI | Woodpecker / Drone CI | GitHub Actions is standard; pin all actions by commit SHA for supply-chain safety |

---

## 2. Database Migration Justification Policy

- **Default Stance:** Do NOT migrate databases or ORMs without a documented, measurable failure in performance, data integrity, or cost.
- **Portability Rule:** Any schema defined in OpenClone must support standard SQL migrations (Flyway, Liquibase, or Drizzle Kit) to prevent database lock-in.
