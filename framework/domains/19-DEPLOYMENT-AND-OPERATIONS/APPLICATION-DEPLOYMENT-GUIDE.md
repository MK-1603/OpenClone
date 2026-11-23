# Application Build-to-Deployment Guide
## Automated Delivery of Applications Engineered with OpenClone

OpenClone provides an automated bridge between AI-assisted software generation and production cloud deployment. When an agent constructs or refactors an application, OpenClone handles packaging, containerization, preview generation, health checks, and production promotion.

---

## 1. The Build-to-Deployment Lifecycle

```
[1. Application Build]
  ├── Code generated & local tests pass (Unit/Integration)
  └── Taste Skill real-browser gate passes (GATE: PASS)
          ↓
[2. Deployment Analysis]
  ├── Detect framework & runtime (Node.js, Python, Go, Rust, Static, Docker)
  ├── Extract required build commands and artifact output directories
  └── Detect required environment variable names (zero secret exposure)
          ↓
[3. Provider Selection & Configuration]
  ├── Select provider: Cloudflare, Vercel, Render, Railway, Fly.io, AWS, Docker
  └── Generate verified provider manifest (e.g. wrangler.toml, vercel.json, Dockerfile)
          ↓
[4. Preview Deployment (Automated)]
  ├── Isolated preview URL provisioned
  └── Automated smoke tests and health probe verification (`/health`, 200 OK)
          ↓
[5. Human Production Gate (Mandatory)]
  ├── Policy check: PRODUCTION_APPROVAL requires registered human approver sign-off
  └── SHA-256 digest binding ensures zero drift between preview and production
          ↓
[6. Production Promotion & Rollback Monitoring]
  ├── Exact tested artifact promoted to live custom domain
  ├── Real-time telemetry monitoring (latency, 5xx errors)
  └── Instant automated rollback on critical health failure
```

---

## 2. Supported Deployment Modes

1. **`MANUAL`**: OpenClone analyzes the repository and outputs production-grade configuration files and deployment scripts. The human engineer runs deployment manually.
2. **`PREVIEW_AUTO`**: Pull requests and approved local milestones automatically trigger preview environment deployments for human stakeholder testing.
3. **`PRODUCTION_APPROVAL` (Default)**: Previews deploy automatically; promotion to production custom domains is gated by an explicit human approval record in the OpenClone ledger.
4. **`PRODUCTION_AUTO`**: Continuous deployment directly to production for authorized, low-risk services with automated rollback triggers.

---

## 3. Security & Credential Isolation

- **Zero Secrets in Repository**: OpenClone never writes production tokens, database passwords, or private keys to source code, prompts, or Git history.
- **Provider Scopes**: Deployment provider connectors must use least-privilege tokens bounded to the specific project.
- **OIDC Federation**: Preferred over long-lived API keys for GitHub Actions and CI environments.
