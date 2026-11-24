# OpenClone Zero-Trust Security Architecture & Layered Firewall Specification

This document defines the production zero-trust security architecture, network firewall controls, Web Application Firewall (WAF), AI agent execution gateway, and standards alignment across OpenClone.

---

## 1. Zero-Trust Security Principles

OpenClone enforces five non-negotiable zero-trust principles:
1. **Never Trust, Always Verify:** Every inbound request, outbound call, agent subprocess, and database query must be authenticated, authorized, and validated regardless of origin.
2. **Least Privilege by Default:** Agents, services, and human users operate with the minimum capabilities required for task completion.
3. **Explicit Blast-Radius Confinement:** Subprocesses, database tables, and object storage are segregated through network segmentation, tenant isolation, and path confinement.
4. **Cryptographic Approval Binding:** Sensitive operations (code execution, destructive file operations, cloud deployment) are cryptographically bound to immutable SHA-256 digests.
5. **Tamper-Evident Immutable Audit:** All state transitions, authorization events, and firewall blocks are recorded in an append-only, hash-chained ledger.

---

## 2. Layered Firewall Architecture

```
                                  [ INTERNET ]
                                       |
                                       v
                     +-----------------------------------+
                     |   Layer 1: Network Inbound Gate   |
                     |   - Default-Deny Inbound Ports    |
                     |   - Block Public Internal DB/Redis|
                     +-----------------+-----------------+
                                       |
                                       v
                     +-----------------------------------+
                     |   Layer 2: Web App Firewall (WAF) |
                     |   - SQL Injection & XSS Filtering |
                     |   - Path Traversal Block          |
                     |   - Sliding-Window Rate Limiting  |
                     |   - OWASP Secure Header Injection |
                     +-----------------+-----------------+
                                       |
                                       v
                     +-----------------------------------+
                     |   Layer 3: AI Agent Gateway       |
                     |   - Shell Executable Allowlist    |
                     |   - Shell Injection Token Block   |
                     |   - Workspace Path Confinement    |
                     |   - Prompt Injection Detection    |
                     |   - Credential File Access Guard  |
                     +--------+-----------------+--------+
                              |                 |
                +-------------+                 +-------------+
                v                                             v
+-------------------------------+             +-------------------------------+
| Layer 4: Outbound SSRF Guard  |             | Layer 5: Database Security    |
| - Prohibit Non-HTTP Schemes   |             | - Parameterized Queries Only  |
| - Block Cloud Metadata IPs    |             | - Workspace/Tenant Isolation  |
| - Block RFC1918 Private Nets  |             | - Mandatory TLS/SSL in Prod   |
+-------------------------------+             +-------------------------------+
```

---

## 3. Defense Layer Specifications

### Layer 1: Network & Port Security (`src/openclone/security/firewall.py`)
- **Default-Deny Inbound:** Only approved service ports (`80`, `443`, `3000`, `8000`, `8080`) accept connections. All other ports are dropped.
- **Internal Service Protection:** Prohibits binding internal management or persistence ports (`5432` PostgreSQL, `6379` Redis, `3306` MySQL, `27017` MongoDB, `2375` Docker) to public interfaces (`0.0.0.0` or `::`). Internal services must bind strictly to loopback (`127.0.0.1`) or private container networks.

### Layer 2: Web Application Firewall (`src/openclone/security/waf.py`)
- **SQL Injection Filter:** Blocks UNION SELECT, boolean tautologies (`' OR '1'='1`), DDL tampering (`DROP TABLE`), and blind time-based attacks (`SLEEP()`).
- **XSS & DOM Filter:** Blocks `<script>` tags, inline event handlers (`onerror=`, `onload=`), `javascript:` pseudo-protocols, and DOM cookies.
- **Path Traversal Guard:** Detects directory climbing (`../`, `%2e%2e`, `%2f`) across paths, query strings, and payloads.
- **Sliding-Window Rate Limiter:** Enforces per-client request limits over a sliding temporal window to mitigate automated scraping and brute-force attacks.
- **Secure Headers Injection:** Automatically sets OWASP-recommended headers: `Content-Security-Policy`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, and `Strict-Transport-Security`.

### Layer 3: AI Agent Firewall & Security Gateway (`src/openclone/security/agent_gateway.py`)
- **Subprocess Command Allowlist:** Agent processes can only invoke binaries explicitly listed in `policy.allowed_executables`. Raw shell strings and dangerous operators (`;`, `&&`, `||`, `|`, `` ` ``, `$()`) are blocked.
- **Filesystem Sandbox Confinement:** All file reads, writes, and working directory targets (`cwd`) must resolve strictly within the project directory. Traversal outside the root is blocked.
- **Prompt Injection Defense:** Multi-pattern heuristic detectors analyze user inputs and untrusted data for instruction override, system prompt exfiltration, and jailbreak attempts.
- **Credential Access Blocker:** Prevents agents from reading `.env*`, `*.pem`, `*.key`, `id_rsa`, and `service-account*.json`.

### Layer 4: Outbound SSRF & Metadata Protection (`src/openclone/security/firewall.py`)
- **Protocol Allowlist:** Only `http` and `https` protocols are permitted. Prohibits dangerous schemes (`file://`, `gopher://`, `ftp://`, `dict://`).
- **Cloud Metadata Guard:** Explicitly drops outbound requests to `169.254.169.254`, `metadata.google.internal`, `metadata.aws.internal`, and link-local IPv6 addresses.
- **Private RFC1918 Blocking:** Blocks requests to `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`, and loopback interfaces unless local testing is explicitly declared.

### Layer 5: Database & Storage Security (`src/openclone/security/database.py`)
- **Parameterized Query Enforcement:** Blocks unparameterized dynamic string concatenation and destructive DDL statements (`DROP TABLE/DATABASE`).
- **Tenant & Workspace Isolation:** Queries targeting multi-tenant tables (`projects`, `tasks`, `users`, `audit_ledgers`, `artifacts`) must include mandatory scoping clauses (`workspace_id = ?`).
- **Storage Boundary Confinement:** Object storage keys with traversal tokens (`../`) or absolute paths are rejected.
- **Production Connection Standards:** Enforces TLS/SSL (`sslmode=require`) and rejects weak default passwords.

---

## 4. Security Standards Alignment

OpenClone aligns with leading international security frameworks:

| Standard / Framework | Benchmark Domain | OpenClone Implementation Alignment |
|---|---|---|
| **OWASP Top 10 (2021)** | A01: Broken Access Control | Role-based worker manifests & SHA-256 approval digest binding (`AG-003`, `AG-006`) |
| **OWASP Top 10 (2021)** | A03: Injection | WAF inspection and parameterized SQL query enforcement (`API-003`, `DB-001`) |
| **OWASP Top 10 (2021)** | A05: Security Misconfiguration | Production sandbox enforcement & default-deny inbound firewall (`FW-001`, `SEC-008`) |
| **OWASP Top 10 (2021)** | A10: Server-Side Request Forgery | Outbound URL validator blocking cloud metadata and private networks (`FW-005`, `FW-006`) |
| **OWASP API Security Top 10** | API1: Broken Object Level Auth | Mandatory tenant/workspace isolation on all multi-tenant queries (`DB-002`) |
| **OWASP API Security Top 10** | API4: Unrestricted Resource Consumption | Sliding-window rate limiter & payload body size limits (`API-005`, `API-006`) |
| **OWASP Agentic Security (2025)** | Prompt Injection & Goal Hijack | Multi-signature heuristic prompt injection detector (`AG-004`) |
| **OWASP Agentic Security (2025)** | Tool Execution Sandbox Escape | Subprocess binary allowlists and directory path confinement (`AG-001`, `AG-002`) |
| **NIST SSDF (SP 800-218)** | Protect Software from Tampering | Cryptographic hash-chained audit ledgers & pinned commit SHAs in scanner locks (`SEC-005`, `SEC-007`) |

---

## 5. Verification Test Suite Mapping

All controls are validated deterministically in the continuous integration test suite:

- **Firewall & Network Security:** [`tests/test_advanced_security_firewall.py`](file:///d:/New%20folder/OpenClone/tests/test_advanced_security_firewall.py) (Tests `FW-001` through `FW-007`)
- **AI Agent Security Gateway:** [`tests/test_advanced_security_firewall.py`](file:///d:/New%20folder/OpenClone/tests/test_advanced_security_firewall.py) (Tests `AG-001` through `AG-006`)
- **API & Application Security:** [`tests/test_advanced_security_firewall.py`](file:///d:/New%20folder/OpenClone/tests/test_advanced_security_firewall.py) (Tests `API-001` through `API-006`)
- **Database & Storage Security:** [`tests/test_advanced_security_firewall.py`](file:///d:/New%20folder/OpenClone/tests/test_advanced_security_firewall.py) (Tests `DB-001` through `DB-003`)
- **Governance & Secret Scanning:** [`tests/test_security_governance.py`](file:///d:/New%20folder/OpenClone/tests/test_security_governance.py) (Tests `SEC-001` through `SEC-020`)
