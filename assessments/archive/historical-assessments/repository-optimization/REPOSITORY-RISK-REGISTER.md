# OpenClone Master Repository Risk Register

**Document ID:** `REG-MASTER-RISK-v2.0.0`  
**Status:** `ACTIVE RISK REGISTER`  

---

## 1. Master Risk Assessment

| Risk ID | Category | Scenario | Severity | Mitigation in OpenClone 2.0 | Residual Risk |
|---|---|---|---|---|---|
| **RISK-01** | Architecture | Uncontrolled AI slope and dependency bloat | HIGH | No AI Slope rule in AGENTS.md + SHA-256 approval binding | MINIMAL |
| **RISK-02** | Distribution | 41 MB repo size causes plugin install timeouts | HIGH | Decoupled 35.76 MB media assets to on-demand module; core < 350 KB | ZERO |
| **RISK-03** | Security | Path traversal escapes project workspace | HIGH | `_check_boundary()` with `os.path.realpath` enforcement | ZERO |
| **RISK-04** | Security | Replay attack on human release approvals | HIGH | Cryptographic HMAC-SHA256 signature with single-use nonce | ZERO |
| **RISK-05** | IP Compliance | Upstream copyleft contamination (GPL/LGPL) | HIGH | Quarantined strictly as external CLI subprocesses | ZERO |
| **RISK-06** | IP Compliance | Unlicensed upstream code (UI-004) | MEDIUM | Quarantined under `BLOCKED_LICENSE_REVIEW` | ZERO |
