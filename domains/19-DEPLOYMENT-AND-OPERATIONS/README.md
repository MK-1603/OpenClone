# 19 — Deployment & Operations

## Mission & Scope
This domain governs both:
1. **OpenClone Self-Deployment**: Packaging and releasing the OpenClone framework itself.
2. **User Application Build-to-Deployment Automation**: Automatically testing, packaging, preview-deploying, promoting, and monitoring applications built by users through OpenClone.

---

## Architectural Principles
- **User Ownership**: The built application belongs to the user. OpenClone never provisions billable infrastructure or deploys to production without explicit human authorization.
- **Dual Lifecycle**: Distinguishes preview environments from production environments.
- **Default Policy (`PRODUCTION_APPROVAL`)**: Automatic preview deployment on approved PRs/builds; production deployment strictly requires recorded human sign-off.
- **Immutable Artifacts**: The exact commit SHA and build artifact validated in the preview stage is deployed to production—never rebuilt from an unverified branch.

---

## Domain Manuals
1. [`APPLICATION-DEPLOYMENT-GUIDE.md`](file:///APPLICATION-DEPLOYMENT-GUIDE.md) — End-to-end user application deployment lifecycle from build to preview to production.
2. [`DEPLOYMENT-PROVIDER-ADAPTERS.md`](file:///DEPLOYMENT-PROVIDER-ADAPTERS.md) — Specifications and capabilities for Cloudflare, Vercel, Render, Railway, Fly.io, and Container platforms.
3. [`DEPLOYMENT-STATE-MACHINE.md`](file:///DEPLOYMENT-STATE-MACHINE.md) — Formal 21-state deployment state machine and transition rules.

---

## Workflow Contracts
- Workflow: [`WF-014: Application Build to Deployment`](file:///../../workflows/WF-014-APPLICATION-BUILD-TO-DEPLOYMENT.md)
- Schema: [`schemas/deployment-profile.schema.json`](file:///../../schemas/deployment-profile.schema.json)
- Responsible Role: [`workforce/teams/PLATFORM-OPERATIONS/roles/RELEASE-ENGINEER.md`](file:///../../workforce/teams/PLATFORM-OPERATIONS/roles/RELEASE-ENGINEER.md)
