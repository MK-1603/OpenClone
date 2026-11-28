# OpenClone Security Incident Response Runbook

This document defines the formal protocol for triage, containment, eradication, recovery, and post-incident verification across OpenClone engineering and deployment environments.

---

## 1. Incident Response Lifecycle

OpenClone follows the 8-phase NIST/OWASP Incident Response Lifecycle:

```
[ Phase 1: Detection ]
         |
         v
[ Phase 2: Classification ] (SEV-1 Critical to SEV-4 Low)
         |
         v
[ Phase 3: Containment ] (Network isolation, token revocation, agent kill-switch)
         |
         v
[ Phase 4: Investigation ] (Audit ledger analysis, git log forensic inspection)
         |
         v
[ Phase 5: Revocation & Rotation ] (Issue fresh credentials, re-keying)
         |
         v
[ Phase 6: Recovery ] (State verification, restored ledgers)
         |
         v
[ Phase 7: Verification ] (Automated security gate re-run)
         |
         v
[ Phase 8: Post-Incident Review ] (Root Cause Analysis, preventive hardening)
```

---

## 2. Threat Scenarios & Remediation Protocols

### Scenario 1: Exposed API Keys or External Tokens
1. **Immediate Revocation:** Revoke the exposed API key in the provider console (OpenAI, Anthropic, GCP, AWS, GitHub) immediately.
2. **Quarantine:** Check `tools/scan_secrets.py --mode tracked` to identify all files referencing the token.
3. **Rotation:** Re-generate token with least privilege and inject into local `.env` (never commit).
4. **Resolution:** Navigate to GitHub Secret Scanning alerts and close as **Revoked**.

### Scenario 2: Compromised Private Keys or Certificates
1. **Revoke Certificate:** Contact issuing CA to add serial number to Certificate Revocation List (CRL) or OCSP.
2. **Re-Keying:** Generate new 4096-bit RSA or Ed25519 key pair offline.
3. **Deployment:** Deploy updated public certificate and update server TLS configuration.
4. **Audit:** Ensure `.gitignore` continues blocking `*.pem`, `*.key`, `*.p12`.

### Scenario 3: Unauthorized Agent Execution Attempt
1. **Process Termination:** Kill unauthorized agent subprocesses immediately.
2. **Ledger Inspection:** Query `security_events` table for actor, timestamp, and command attempted.
3. **Policy Lockdown:** Verify `allowed_executables` in `policy.json`. Remove any overly permissive binary entries.
4. **State Machine Verification:** Ensure unapproved tasks remain in `BLOCKED` status.

### Scenario 4: Database Tampering or Unauthorized Access
1. **Network Isolation:** Terminate external connections to database port (5432/3306).
2. **Credential Rotation:** Immediately reset database service user passwords.
3. **Integrity Check:** Run `SecurityMonitor.verify_ledger_integrity()` to detect hash-chain breaks.
4. **Restoration:** Restore from verified immutable snapshot if tampering is confirmed.

### Scenario 5: SSRF or Suspicious Outbound Network Traffic
1. **Destination Lockdown:** Check outbound logs for metadata queries (`169.254.169.254`) or internal IP sweeps.
2. **Firewall Enforcement:** Ensure `NetworkFirewall.validate_outbound_url()` is active on all agent URL parameters.
3. **Domain Whitelisting:** Restrict outbound traffic strictly to approved API domains.

### Scenario 6: Malicious Dependency Introduction
1. **Lockfile Audit:** Compare `security/scanners.lock.json` and `pyproject.toml` against upstream pinned commit hashes.
2. **Quarantine:** Immediately revert PR or commit introducing unvetted dependency.
3. **Supply-Chain Verification:** Run dependency vulnerability check with Trivy / Safety.

### Scenario 7: Unauthorized Deployment Attempt
1. **Deployment Lock:** Revoke CI/CD deployment tokens and freeze deployment pipelines.
2. **Approval Verification:** Validate why release gate allowed transition without registered human approver signature.
3. **Re-Gate:** Require dual-custody cryptographic approval before unfreezing releases.

### Scenario 8: Data Exposure or Cross-Tenant Leakage
1. **Egress Block:** Stop affected API endpoints immediately via WAF block rule.
2. **Query Scoping:** Verify `DatabaseSecurityGuard.validate_tenant_isolation()` is applied to the failing query.
3. **Impact Assessment:** Identify specific records exposed and notify affected stakeholders under privacy SLAs.

---

## 3. Human Authorization Requirement

Disruptive remediations (rewriting Git history with BFG/filter-repo, wiping databases, terminating live production nodes) strictly require explicit human cryptographic sign-off. Autonomous agents must never execute unapproved destructive operations during incident response.
