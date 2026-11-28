# External Security Subprocess Integration Boundaries

This document defines the strict external subprocess isolation boundaries enforced by OpenClone for third-party security scanners and dynamic assessment engines.

---

## 1. Zero-Linkage & Subprocess Isolation Principle

To maintain a zero-core-dependency architecture and ensure strict license isolation (quarantining copyleft tools like GPL-3.0 or LGPL-2.1):

1. **Zero Python Imports:** External tools are never imported or linked directly into the OpenClone Python runtime.
2. **Piped CLI Invocation:** All invocations must be executed as isolated subprocesses (`subprocess.run`) with:
   - Explicit execution timeouts (preventing hanging child processes).
   - Standard output / error capture.
   - Piped JSON or delimited outputs parsed purely as untrusted data.
   - Pinned CLI flags preventing automatic network calls or unauthorized updates.

---

## 2. Integrated Scanners

### 2.1 TruffleHog (Secret Detection)
- **Tool Type:** Git & Filesystem High-Entropy Secret Scanner.
- **License Boundary:** Pinned executable invocation via `tools/scan_secrets.py`.
- **Command Signature:**
  ```bash
  trufflehog filesystem <path> --json --no-verification
  ```
- **Fallback:** When TruffleHog binary is not present in `$PATH`, OpenClone falls back to its deterministic, zero-dependency regex & Shannon entropy scanner in `tools/scan_secrets.py`.

### 2.2 Broken Links & Security Auditing (BLA)
- **Tool Type:** Static Link Integrity & Documentation Security Audit.
- **Execution Boundary:** Invoked via `tools/check_links.py`.
- **Safety Control:** Validates local path casing, relative URL references, and file existence without making unauthorized external HTTP requests unless explicitly flagged.

---

## 3. Human Gate & Pre-Flight Enforcement
Any dynamic or external scanning engine (such as DAST or external pentest tools) strictly requires:
- Written authorization in `PROJECT.md` or a cryptographically signed approval token.
- Explicit non-production target scope definition.
- Automatic audit logging to the hash-chained SQLite ledger (`.aisdf/workforce.sqlite3`).
