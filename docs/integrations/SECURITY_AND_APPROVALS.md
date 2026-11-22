# Security, Policy Engine & Human Approval Binding

Autonomous AI coding agents can propose actions, but deterministic code and authorized human engineers decide.

---

## 1. Policy Engine Rules

The Integration Gateway (`src/openclone/integrations/gateway.py`) evaluates three layers of policy before permitting execution:

1. **Authentication:** Validates Bearer JWT / API Key against known scopes.
2. **Project Isolation:** Verifies caller has permission to operate on the target `project_id`.
3. **Approval Gating:** Evaluates risk classification:
   - `READ_ONLY`: Allowed immediately.
   - `LOW_RISK_WRITE`: Allowed with valid token.
   - `HIGH_RISK_WRITE`: Allowed only with supporting evidence artifacts.
   - `PRODUCTION_IMPACT` / `DESTRUCTIVE`: Strictly blocked unless accompanied by a verified human cryptographic approval digest (`SHA-256`).

---

## 2. Cryptographic Approval Binding

Approvals cannot be forged or reused across tasks:
- An approval digest is computed as:
  $$\text{digest} = \text{SHA-256}(\text{task\_id} \mathbin{\Vert} \text{scope} \mathbin{\Vert} \text{plan\_hash} \mathbin{\Vert} \text{approver\_id})$$
- Any modification to the plan, task parameters, or target environment invalidates the digest, requiring fresh human sign-off.
- AI agents cannot sign their own approvals.
