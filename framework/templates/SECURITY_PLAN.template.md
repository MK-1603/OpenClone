# Security Plan: [Project Name]
**Risk-Based Security Specification & Verification Checkpoints**  
**Specification:** v1.0.0 | **Authority:** Security Standard

---

## 1. Threat Profile & Boundaries

| Asset / Endpoint | Sensitivity | Threat Boundary | Enforced Controls |
| :--- | :--- | :--- | :--- |
| **API Endpoints** | High | Public Internet | Token auth, rate limiting, payload size limits |
| **Database** | Critical | Internal VPC | Parameterized queries, least-privilege credentials |
| **Secrets / Keys** | Critical | Process Environment | Multi-pattern redaction, no committed `.env` files |
| **Tool Execution** | High | Local Container | Restricted path arguments, zero shell interpolation |

---

## 2. Checkpoints & Verification Schedule

| Milestone / Gate | Checkpoint Type | Tools / Scanners | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Pre-Commit** | Static / Secrets | TruffleHog (diff), Semgrep (fast) | 0 high/critical findings |
| **PR Merge** | Dependency / SBOM | Trivy (vuln), Secret Scan | 0 unpatched CVEs in lockfile |
| **Feature Complete** | Dynamic Pentest | Strix (headless source / test app)| Scoped findings triaged |
| **Pre-Release** | Release Clearance | Trivy (SBOM), Full SAST, License Lock | Release gate signed off |

---

## 3. Strix Dynamic Security Testing Protocol (Opt-in)

- **Target Scope**: Local test application (`http://localhost:PORT`) or authorized staging only.
- **Pre-Conditions**:
  - Target URL listed in `security/authorized_targets.json`.
  - Strix CLI and Docker runtime verified.
  - Explicit budget cap specified (default: max budget 10).
- **Execution Command Example**:
  ```bash
  strix -n -t ./ --scan-mode standard --max-budget 10
  ```
- **Finding Remediation Protocol**:
  1. Capture reproduction PoC.
  2. Implement root-cause fix in source.
  3. Run regression unit tests.
  4. Perform targeted Strix re-test to verify resolution.
