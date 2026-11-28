# OpenClone Integration Security Model
## Multi-Platform Security, Boundary Enforcement, and Secret Governance

**Version:** 1.0.0  
**Status:** ENFORCED  
**Canonical Product:** OpenClone 2.0

---

## 1. Security Architecture & Threat Vectors

Extending OpenClone to diverse third-party IDEs introduces specific threat boundaries:

1. **Malicious Workspace Injections:** Untrusted repositories attempting to execute unauthorized shell commands via IDE context.
2. **Secret Exfiltration:** Exposure of local `.env` files, API keys, or cloud credentials to connected AI platforms.
3. **Privilege Escalation:** IDE plugins bypassing OpenClone approval gates to execute high-risk operations.
4. **Configuration Tampering:** Corrupting host IDE configuration files during setup or uninstallation.

---

## 2. Core Security Invariants

### 2.1. Default-Deny & Least Privilege
- External integrations (MCP, ACP, REST) receive read-only permissions (`read`, `inspect`, `plan`) by default.
- Mutation or execution permissions (`execute`, `write`, `deploy`) require explicit authorization.

### 2.2. Human Approval Authority
- Operations classified as `MEDIUM_RISK` (e.g. database schema migrations) or `HIGH_RISK` (e.g. deployment, production updates, destructive commands) **cannot** be executed autonomously by any connected IDE.
- An operation halts until an authorized human approval record with a valid cryptographic signature and payload digest is verified by the Gateway.

### 2.3. Workspace Isolation & Confinement
- All file access and subprocess execution are bounded by the workspace root directory.
- Directory traversal attacks (e.g. `../../etc/passwd` or `..\..\Windows`) are detected and rejected immediately with a security alert.

### 2.4. Zero-Leak Secret Redaction
- In-memory regex filtering scrubs credentials across all inputs and outputs before transmission over stdio, HTTP, or SSE:
  - AWS Access Keys (`AKIA...`)
  - GitHub Personal Access Tokens (`ghp_...`)
  - Generic Bearer tokens, private keys, and passwords.
- Secret patterns are replaced with `[REDACTED]` tokens.

### 2.5. Configuration Safety & Rollback
- Before writing to any IDE configuration file (such as `settings.json`, `mcp.json`, or Antigravity plugins), the Integration Manager creates a timestamped backup in `.openclone/backups/<platform>_<timestamp>.json`.
- If writing or validating fails, the backup is restored automatically.
- `oc integrations remove <platform>` safely reverts changes.

---

## 3. Audit Ledger & Cryptographic Verification

All integration operations generate structured audit events stored in the tamper-evident SQLite ledger:
- `EVENT_TYPE`: `MCP_TOOL_CALLED`, `ACP_SESSION_CREATED`, `PLATFORM_CONNECTED`, `SECURITY_DENIAL`
- `PAYLOAD`: Caller identity, platform ID, tool name, sanitized arguments, execution verdict.
- `DIGEST`: SHA-256 hash chaining ensuring non-repudiation.
