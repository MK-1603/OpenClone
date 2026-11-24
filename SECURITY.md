# Security Policy & Engineering Governance

OpenClone enforces strict defensive engineering, verifiable zero-trust boundaries, deterministic sandboxing, and immutable audit ledgers across all autonomous workflows, CLI tools, MCP endpoints, and runtime engines.

---

## 1. Supported Versions

Security updates, patches, and threat model revisions are actively maintained for:

| Version | Supported | Status |
|---|---|---|
| **2.0.x** (Current) | :white_check_mark: | Active production standard |
| **1.0.x** | :white_check_mark: | Maintenance security support |
| **< 1.0.0** | :x: | Deprecated / Unsupported |

---

## 2. Security Architecture & Threat Model

OpenClone divides the engineering execution plane into distinct trust zones:
- **Human Developer Zone:** Retains ultimate cryptographic approval authority over sensitive actions, cloud resources, and release boundaries.
- **Agent Execution Plane:** Constrained by least-privilege capability manifests. Default-deny on all filesystem access, network sockets, and subprocess execution.
- **Model Intelligence Engine (MIE):** Isolated routing adapters with tri-state circuit breakers, dynamic provider failover, and strict prompt-secret scrubbing.
- **Runtime Ledger & Evidence Store:** Cryptographic append-only SQLite store with SHA-256 task digest bindings preventing mid-flight tampering or unauthorized transitions.

```
+-------------------------------------------------------------------------+
|                         Human Developer Zone                            |
|             (Defines Intent · Retains Final Approval Authority)         |
+------------------------------------+------------------------------------+
                                     | Signed SHA-256 Digest
                                     v
+-------------------------------------------------------------------------+
|                    OpenClone Security Control Plane                     |
|  - Least Privilege Policy Enforcement    - Git Ignore & Secret Protection |
|  - Process & Executable Allowlist        - Client/Server Env Isolation   |
|  - Immutable Audit Ledger               - Zero Static Secret Toleration |
+------------------------------------+------------------------------------+
                                     | Scoped Tool Invocations
                                     v
+-------------------------------------------------------------------------+
|                    Sandboxed Execution Environment                      |
|         (Path Confinement · Redacted Logs · Verified Diffs)             |
+-------------------------------------------------------------------------+
```

---

## 3. Git Ignore & Private-Key Protection Policy

OpenClone enforces strict version control boundaries. The following categories of files are prohibited from entering repository commits:

1. **Environment & Secret Files:**
   - `.env`, `.env.*`, `.env.local`, `.env.development`, `.env.production`, `.env.test`, `.env.staging`
   - Only explicitly safe template files (`.env.example`, `.env.template`) containing placeholder values are permitted.
2. **Private Keys & Certificates:**
   - `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `*.keystore`, `*.pkcs12`
   - SSH private keys: `id_rsa`, `id_ed25519`, `id_ecdsa`, `id_dsa`
   - TLS keys: `server.key`, `privkey.pem`, `cert.key`
3. **Cloud & Service Credentials:**
   - Cloud service account keys (`*service-account*.json`, `*service_account*.json`, `*credentials*.json`, `client_secret*.json`)
   - Secret credential files (`*.credentials`, `credentials.ini`, `credentials.yaml`, `secrets.json`, `auth.json`, `token.json`)
4. **Local Secret Stores:**
   - `.ssh/`, `.secrets/`, `*.db.key`, `database.credentials.*`

These rules are enforced deterministically by root and nested `.gitignore` policies and validated by automated tests (`SEC-001` - `SEC-008`).

---

## 4. Automated Secret Detection

OpenClone includes a built-in automated secret scanning engine (`tools/scan_secrets.py`) that scans:
- Tracked files in the repository.
- Staged Git index changes before commit.
- Working tree files and patch diffs.
- Environment configurations and test fixtures.

### Running Secret Scans Locally

```bash
# Scan all tracked files in the repository
python tools/scan_secrets.py --mode tracked

# Scan staged changes before committing
python tools/scan_secrets.py --mode staged

# Scan all working tree files
python tools/scan_secrets.py --mode all
```

The scanner matches high-entropy strings, API keys (OpenAI, Anthropic, Google, GitHub, Slack, AWS), private keys, and credential filenames. **All findings are masked as `[REDACTED]`; no sensitive content is ever written to logs or console outputs.**

---

## 5. Environment & Configuration Security

Environment configurations are parsed safely through `src.openclone.security.env`:
- **Separation of Scopes:** Development, test, and production configurations are strictly separated.
- **Production Guardrails:** In `production` mode, missing variables or placeholder values trigger hard `SecurityValidationError` exceptions. Strict sandboxing (`OPENCLONE_STRICT_SANDBOX=true`) cannot be disabled.
- **Client Bundle Protection:** Client-accessible bundles (e.g. `NEXT_PUBLIC_*`) are audited to ensure server secrets, database URLs, and private keys cannot leak to client browsers.

---

## 6. AI Agent Execution & Sandbox Restrictions

OpenClone agents run under strict runtime boundaries:
- **Executable Allowlist:** Subprocesses must match `policy.allowed_executables` (e.g., explicitly permitted binaries). Unlisted binaries (such as `curl` or `rm`) are rejected immediately.
- **Filesystem Confinement:** Working directories (`cwd`) must stay strictly inside the project root. Directory traversal (`../`) is blocked.
- **Undeclared Action Rejection:** Worker roles cannot execute actions outside their capability manifest. For example, `technical-writer` cannot execute destructive changes.
- **Human Approval & Cryptographic Binding:** Tasks requiring sensitive actions (`execute`, `write`, `destructive_change`, `release`) require non-interactive or interactive human approval bound to a cryptographic SHA-256 task digest. Any modification to task parameters invalidates the approval.
- **Telemetry & Secret Redaction:** All terminal logs, stdout/stderr streams, and audit ledgers automatically redact API tokens, Authorization headers, and private key strings.

---

## 7. CI/CD Security Gate

OpenClone's CI/CD pipeline (`.github/workflows/security.yml`) executes mandatory security checks before merging pull requests or generating releases:

1. **Security Scanners Lock Verification:** Asserts that all external security scanners in `security/scanners.lock.json` are cryptographically pinned to 40-character commit SHAs.
2. **Automated Secret Detection:** Scans all repository files to ensure zero exposed credentials.
3. **Governance Test Suite:** Executes tests `SEC-001` through `SEC-020` to verify Git ignore behavior, environment safety, and agent sandboxing.
4. **Repository Validation Gate:** Validates JSON schemas, engine execution contracts, and internal documentation links.

---

## 8. Security Governance Verification (SEC-001 - SEC-020)

Automated tests in [`tests/test_security_governance.py`](file:///d:/New%20folder/OpenClone/tests/test_security_governance.py) verify the implementation of all 20 governance controls:

| Test ID | Control Name | Verification Mechanism | Status |
|---|---|---|---|
| **SEC-001** | `.env` Ignore Protection | `git check-ignore .env` | **VERIFIED** |
| **SEC-002** | `.env.local` Protection | `git check-ignore .env.local` | **VERIFIED** |
| **SEC-003** | `.env.production` Protection | `git check-ignore .env.production` | **VERIFIED** |
| **SEC-004** | `.env.example` Allowed | Template allowed in Git; placeholders verified | **VERIFIED** |
| **SEC-005** | `*.pem` Key Protection | `git check-ignore server.pem` | **VERIFIED** |
| **SEC-006** | `*.key` Key Protection | `git check-ignore private.key` | **VERIFIED** |
| **SEC-007** | SSH Private Key Protection | `git check-ignore id_rsa` / `id_ed25519` | **VERIFIED** |
| **SEC-008** | Service Account Credentials | `git check-ignore service-account.json` | **VERIFIED** |
| **SEC-009** | Tracked Secret Detection | Scanner validates all tracked files are clean | **VERIFIED** |
| **SEC-010** | Staged Secret Detection | Secret scanner blocks staged keys & credentials | **VERIFIED** |
| **SEC-011** | Hardcoded Secret Scanning | Codebase audit confirms 0 unredacted secrets | **VERIFIED** |
| **SEC-012** | Environment Validation | Rejects placeholder keys & disabled sandbox in prod | **VERIFIED** |
| **SEC-013** | Client Bundle Secret Protection | Blocks server secrets from client-side bundles | **VERIFIED** |
| **SEC-014** | Sensitive Data Redaction | `redact_secrets` strips keys and Bearer tokens | **VERIFIED** |
| **SEC-015** | Unauthorized Command Rejection | Denies unlisted executables via policy allowlist | **VERIFIED** |
| **SEC-016** | Unauthorized Tool Access | Rejects actions outside worker capability manifest | **VERIFIED** |
| **SEC-017** | Human Approval Enforcement | State machine blocks unapproved sensitive actions | **VERIFIED** |
| **SEC-018** | Workspace Path Confinement | Blocks directory traversal (`../outside`) | **VERIFIED** |
| **SEC-019** | Dependency & Scanner Audit | Verifies 40-character pinned SHAs in lockfile | **VERIFIED** |
| **SEC-020** | Platform Regression Suite | Confirms core engine and CLI initialization | **VERIFIED** |

---

## 9. Credential Rotation & Incident Response Protocol

If an actual credential or private key is accidentally committed or leaked:

1. **Immediate Revocation:** Revoke the exposed token, API key, or certificate immediately at the provider/issuer (e.g. OpenAI, Anthropic, GCP, AWS, GitHub).
2. **Issue New Credentials:** Generate new credentials and populate them into private local secret stores or environment variables.
3. **Repository History Quarantine:** Contact repository maintainers to sanitize commit history using `git-filter-repo` or BFG Repo-Cleaner.
4. **Resolution in Security Center:** Navigate to the repository's GitHub Secret Scanning Alerts, review the alert, and close it as **"Revoked"** or **"Used in tests"**.

---

## 10. Developer Security Checklist

Before pushing changes to OpenClone, verify:
- [ ] `.env` and local credentials are NOT tracked (`git status --short`).
- [ ] All new variables in `.env.example` use non-secret placeholders (`your_key_here`).
- [ ] Automated secret scanner passes: `python tools/scan_secrets.py --mode tracked`.
- [ ] All security governance tests pass: `pytest tests/test_security_governance.py`.
- [ ] Repository validator passes: `python tools/validate_repository.py`.
- [ ] No private keys or service account JSON files were created in tracked directories.

---

## 11. Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a vulnerability in OpenClone, submit a confidential report to:
- **Email:** `security@openclone.org`
- **Subject:** `[Vulnerability Report] OpenClone - <Component>`
- **Response SLA:** Initial triage within 48 hours; coordinated resolution within 30 days.
