# Security Architecture & Threat Model

OpenClone operates as an AI Software Development Framework (AISDF) providing deterministic engineering governance over autonomous coding agents, LLM providers, and development environments.

---

## 1. Trust Boundaries

OpenClone divides system interactions into seven isolated trust domains:

1. **Human Operator (Highest Authority):** Defines project goals, signs off on architectural decisions, and approves sensitive actions (writes, execution, deployments, external network access).
2. **Project Control Plane (OpenClone Runtime):** Enforces state transitions, calculates SHA-256 approval digests, manages the acyclic task graph, and records immutable audit ledger entries.
3. **AI Specialist Workforce:** Persona-based agent roles operating under least-privilege capability manifests (`framework/workforce/registry/workers`).
4. **Model Intelligence Engine (MIE):** Multi-provider LLM abstraction layer with health monitoring, tri-state circuit breakers, dynamic fallback chains, and secret-scrubbed telemetry.
5. **Execution Sandbox:** Restricted local subprocess runner with executable allowlists, workspace directory confinement, and environment variable allowlisting.
6. **External Tool & MCP Integrations:** Model Context Protocol (MCP) endpoints and CLI adapters requiring explicit parameter validation and error boundary isolation.
7. **Artifact & Release Gate:** Release policy evaluation engine that blocks unapproved tasks, failing security scans, or unverified evidence.

---

## 2. Threat Model & Mitigations

| Threat Category | Potential Impact | OpenClone Deterministic Mitigation |
|---|---|---|
| **Exposed Credentials & Secret Leaks** | Unauthorized API or cloud access | Root and nested `.gitignore` blocks `.env*`, `*.pem`, `*.key`, service-account files. Automated pre-commit and CI scanner (`tools/scan_secrets.py`) blocks secrets. |
| **Arbitrary Subprocess Execution** | Host system compromise | Runtime policy `allowed_executables` enforces a strict allowlist. Shell command strings are rejected; argv lists are required. |
| **Workspace Directory Traversal** | Access to host files outside repo | Path confinement enforces that `cwd` must resolve strictly within the project root directory. |
| **Prompt Injection & Instruction Confusion** | Agent hijacked into unauthorized actions | Runtime pattern matching detects injection vectors; tool capability boundaries prevent unauthorized tool calls regardless of prompt content. |
| **Approval Bypass & Tampering** | Unapproved tasks executed | SHA-256 approval digest binding invalidates approvals if task parameters, budgets, or dependencies change. |
| **Client-Side Secret Leakage** | Private API keys leaked to browser | `src.openclone.security.env` validates client-side bundles and rejects any server secret terms or tokens. |
| **Supply-Chain Dependency Vulnerability** | Malicious packages introduced | `security/scanners.lock.json` pins external scanner dependencies by immutable 40-character commit SHAs. |
| **Audit Trail Forgery** | Erased or tampered execution evidence | Tamper-evident, hash-chained SQLite audit ledger (`MieTelemetry` & `workforce.sqlite3`) records all transitions and executions. |

---

## 3. Defense-in-Depth Layering

```
Level 1: Version Control & Git Ignore
   ├── Strict .gitignore rules for .env*, *.pem, *.key, id_rsa, service accounts
   └── Pre-commit and CI automated secret scanning (tools/scan_secrets.py)

Level 2: Configuration & Environment
   ├── Separate dev / test / production environment modes
   ├── Safe .env.example with placeholders only
   └── Client bundle safety validator (validate_client_bundle_safety)

Level 3: Runtime Control Plane
   ├── Strict state machine (PLANNED -> APPROVED -> READY -> RUNNING -> SUCCEEDED)
   ├── SHA-256 task digest approval binding
   └── Capability-based worker authorization manifests

Level 4: Execution Sandbox
   ├── Subprocess executable allowlists (allowed_executables)
   ├── Workspace directory path confinement (no ../ traversal)
   └── Strict environment variable allowlist (SAFE_ENV)

Level 5: Telemetry & Logging
   ├── Automatic redaction of Bearer tokens, API keys, passwords
   └── Append-only cryptographically hashed audit ledgers
```

---

## 4. Verification Evidence & Compliance

The implementation of all security controls is deterministically verified via the `SEC-001` - `SEC-020` automated test suite in [`tests/test_security_governance.py`](file:///d:/New%20folder/OpenClone/tests/test_security_governance.py).
