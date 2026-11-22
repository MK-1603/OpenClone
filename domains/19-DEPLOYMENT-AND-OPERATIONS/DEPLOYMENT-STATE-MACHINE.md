# Deployment State Machine
## Formal 21-State Application Deployment Lifecycle

To eliminate deployment failures and prevent untracked drift, OpenClone implements a deterministic, auditable 21-state deployment state machine.

---

## 1. State Topology

```
[NOT_ANALYZED]
      │ (inspect_project)
      ▼
  [ANALYZED]
      │ (generate_plan)
      ▼
[DEPLOYMENT_PLAN_READY]
      │
      ├───────────────────────────────┐ (Missing credentials)
      ▼                               ▼
[AWAITING_CONFIGURATION]   [AWAITING_PROVIDER_CONNECTION]
      │                               │
      └──────────────┬────────────────┘
                     ▼
             [READY_FOR_PREVIEW]
                     │ (trigger_preview)
                     ▼
              [PREVIEW_QUEUED]
                     │
                     ▼
             [PREVIEW_DEPLOYING]
                     │
                     ▼
             [PREVIEW_DEPLOYED]
                     │
                     ▼
           [PREVIEW_VERIFICATION]
                     │
                     ▼
       [AWAITING_PRODUCTION_APPROVAL] ◄─── Mandatory Human Gate
                     │
                     ├───────────────────────────────┐ (Rejected / Altered)
                     │ (Approved by Human Owner)     ▼
                     ▼                          [CANCELLED]
            [PRODUCTION_QUEUED]
                     │
                     ▼
           [PRODUCTION_DEPLOYING]
                     │
                     ▼
           [PRODUCTION_DEPLOYED]
                     │
                     ▼
         [POST_DEPLOY_VERIFICATION]
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
      [HEALTHY]            [DEGRADED / FAILED]
                                │ (trigger_rollback)
                                ▼
                        [ROLLBACK_QUEUED]
                                │
                                ▼
                          [ROLLED_BACK]
```

---

## 2. Invariant Rules
1. **Zero Self-Approval**: AI agents cannot transition a project from `AWAITING_PRODUCTION_APPROVAL` to `PRODUCTION_QUEUED`.
2. **Digest Verification**: The SHA-256 digest of the build deployed to production must match the exact digest verified during `PREVIEW_VERIFICATION`.
3. **Audit Ledger Events**: Every transition writes an immutable event into the SQLite audit ledger with actor name, timestamp, and verification evidence.
