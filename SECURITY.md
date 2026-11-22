# Security Policy

OpenClone takes the security of AI-assisted engineering and autonomous agent systems seriously. We employ defensive programming, strict permission sandboxing, and deterministic verification to prevent arbitrary execution vulnerabilities and prompt injection.

---

## 1. Supported Versions

We provide security updates and patches for the following versions:

| Version | Supported | Status |
|---|---|---|
| **1.0.x** (Current) | :white_check_mark: | Active support |
| **< 1.0.0** | :x: | Deprecated / Unsupported |

---

## 2. Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in OpenClone (including secret leakage, arbitrary command execution, path traversal, or MCP authorization bypass), please report it privately:

1. **Email:** Send a detailed report to `{TODO: SECURITY_EMAIL}`.
2. **Subject:** `[Vulnerability Report] OpenClone - <Brief Summary>`
3. **Contents:**
   - Affected component (e.g. MCP Server, CLI, Lifecycle Engine, Workflow runtime).
   - Step-by-step reproduction instructions or proof of concept.
   - Impact assessment (confidentiality, integrity, availability).
   - Any proposed mitigations or patches.

---

## 3. Vulnerability Response Timeline

- **Initial Response:** Within 48 hours of receipt.
- **Triage & Reproduction:** Within 5 business days.
- **Fix & Advisory Release:** Within 30 days of confirmation.

We follow coordinated vulnerability disclosure. We ask reporters to keep vulnerability details confidential until a patched release and public advisory are published.

---

## 4. Security Principles Enforced by OpenClone

- **Least Privilege Execution:** Tool execution and filesystem access are scoped to explicitly permitted directories.
- **Redaction of Secrets:** Logs and audit ledgers automatically redact API keys, tokens, and credentials.
- **Immutable Audit Trail:** All state changes and tool approvals are hashed and recorded in a tamper-evident audit ledger.
- **Human In The Loop:** Destructive actions, cloud deployments, and permission expansions strictly require explicit human cryptographic sign-off.
