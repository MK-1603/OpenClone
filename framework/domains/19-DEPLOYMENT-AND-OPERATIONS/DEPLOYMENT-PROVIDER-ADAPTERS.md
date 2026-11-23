# Deployment Provider Adapters
## Multi-Platform Hosting Adapter Specifications

OpenClone abstracts hosting infrastructure through provider-neutral adapters. Each adapter implements the shared deployment contract while respecting provider-specific capabilities and limitations.

---

## 1. Provider Adapter Matrix

| Provider | Primary Workloads | Preview Support | Rollback Semantics | Config Artifact |
|---|---|---|---|---|
| **Cloudflare Pages / Workers** | Static frontends, edge functions, serverless APIs | Automatic per-commit branch preview | Instant instant-atomic rollback | `wrangler.toml` |
| **Vercel** | Next.js, React, Nuxt, SvelteKit, serverless web apps | Automatic PR preview URLs | Instant deployment alias repoint | `vercel.json` |
| **Render** | Web services, background workers, PostgreSQL, Redis | Pull request preview environments | Redeploy prior successful deploy ID | `render.yaml` |
| **Railway** | Full-stack apps, containers, microservices, databases | Ephemeral PR environments | One-click previous deployment restore | `railway.toml` |
| **Fly.io** | Global containerized applications, Phoenix, LiteFS | Staging apps with isolated machines | Rollback to prior image release | `fly.toml` |
| **Local / Docker Preview** | Any containerized or static application | Localhost port-bound preview container | Instant container image rollback | `docker-compose.yml` |

---

## 2. Standardized Adapter Contract Operations

Every deployment adapter exposes:
- `inspect_project(path)`: Scans workspace to detect framework, runtime, package managers, and build artifacts.
- `validate_configuration(profile)`: Validates `schemas/deployment-profile.schema.json`.
- `create_preview(commit_sha)`: Builds and deploys isolated preview surface.
- `check_health(url, endpoint)`: Performs HTTP GET with status 200 verification and latency measurement.
- `promote_to_production(preview_id, approval_id)`: Binds approval record and promotes exact preview build to production.
- `rollback(deployment_id)`: Reverts routing to previous healthy deployment record.
