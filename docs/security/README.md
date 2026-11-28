# OpenClone Security Architecture & Policy Index

## Overview

OpenClone provides an enterprise-grade, deterministic security and governance architecture.
All security mechanisms enforce:
1. **Least Privilege**: Deny by default across filesystem, environment variables, tools, and networks.
2. **Deterministic Governance**: Approval hashes, task states, and verification ledgers are mathematically verified.
3. **Defense in Depth**: Layered defense covering prompt injection, SSRF, secret exfiltration, supply-chain contamination, and unauthorized code execution.

---

## Directory Contents

| Document | Purpose |
| :--- | :--- |
| [`llm-gateway-threat-model.md`](file:///d:/New%20folder/OpenClone/docs/security/llm-gateway-threat-model.md) | Comprehensive STRIDE threat model for LLM routing, gateways, and agent tools |
| [`security-profiles.md`](file:///d:/New%20folder/OpenClone/docs/security/security-profiles.md) | Execution profiles (`quick-local`, `pull-request`, `release`, `authorized-dynamic`) |

---

## Canonical Policies & Scanners

- [`security/scanners.lock.json`](file:///d:/New%20folder/OpenClone/security/scanners.lock.json): Cryptographic version lock for 12 security engines.
- [`SECURITY.md`](file:///d:/New%20folder/OpenClone/SECURITY.md): Vulnerability reporting and security support policy.
- [`domains/14-SECURITY-AND-PRIVACY/`](file:///d:/New%20folder/OpenClone/domains/14-SECURITY-AND-PRIVACY): 14-point security and privacy domain specifications.
