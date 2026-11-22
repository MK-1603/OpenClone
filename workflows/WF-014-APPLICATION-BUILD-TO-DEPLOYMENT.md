# WF-014 — Application Build to Deployment
## End-to-End Delivery Workflow for Applications Engineered with OpenClone

- Workflow ID: `WF-014`
- Canonical Name: `APPLICATION-BUILD-TO-DEPLOYMENT`
- Responsible Role: `release-engineer`
- Primary Domain: `domains/19-DEPLOYMENT-AND-OPERATIONS/`
- Schema: `schemas/deployment-profile.schema.json`

---

## 1. Purpose
Execute an automated, policy-governed delivery pipeline for applications built or maintained by OpenClone, ensuring reproducible builds, isolated preview verification, mandatory human production approval, and automated rollback protection.

---

## 2. Prerequisites
1. Application codebase has cleared unit and integration tests with zero failing checks.
2. If the application has a UI surface, Taste Skill pre-build gate (`GATE: READY`) and finish gate (`GATE: PASS`) have cleared.
3. A valid deployment profile conforming to `schemas/deployment-profile.schema.json` exists in the project.

---

## 3. Workflow Stages

```
Stage 1: Preflight & Build Validation
  ├── Run tests in clean isolated subshell
  ├── Build production artifacts (e.g. npm run build, cargo build --release)
  └── Compute and record artifact SHA-256 hash
          ↓
Stage 2: Preview Environment Provisioning
  ├── Trigger preview deployment on selected provider (Cloudflare, Vercel, Render, etc.)
  ├── Obtain isolated preview URL
  └── Execute automated health probes (`GET /health` or HTTP 200 OK)
          ↓
Stage 3: Stakeholder Review & Verification
  ├── Post preview URL and test evidence to task ledger
  └── Run visual and functional smoke verification
          ↓
Stage 4: Production Approval Gate (MANDATORY)
  ├── Verify deployment policy: `PRODUCTION_APPROVAL` halts for human sign-off
  ├── Registered human owner executes: `aisdf.py approve --task-id <deploy-task>`
  └── SHA-256 digest verified against preview artifact
          ↓
Stage 5: Production Deployment & Health Monitoring
  ├── Deploy exact validated artifact to production
  ├── Monitor latency and error rates for 5 minutes post-release
  └── On failure: Automatically trigger `rollback` to previous stable deployment ID
```

---

## 4. Exit Evidence
- Deployment record with timestamp, provider deployment ID, preview URL, and production URL.
- Hash-chained audit event recorded in `.aisdf/workforce.sqlite3`.
- Smoke test and health probe output logs.
