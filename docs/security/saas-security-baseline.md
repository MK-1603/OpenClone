# SaaS Security Baseline & Verification Checklist
**19 Essential Controls + Mature Application Security Standards**  
*OpenClone Global Security Intelligence | Defensible Security by Construction*

---

## 1. Principles of Defensible Security

1. **Server-Side Enforcement**: Client-side validation, hidden UI links, and front-end guards provide user guidance, NOT security. Every authorization, validation, and business rule MUST execute on the server.
2. **Deny by Default & Least Privilege**: Every private endpoint denies access unless authenticated; every database query is scoped to the tenant/user.
3. **Evidence-Based Compliance**: A security control is only marked `PASS` if it is verified with observable tests, automated scans, or reproducible configuration checks.

---

## 2. The 19-Point SaaS Security Baseline Matrix

| # | Security Control | Threat Mitigated | Primary Enforcement Location | Verification Method | Required Test / Evidence |
|---|---|---|---|---|---|
| **01** | **Row Level Security (RLS)** | Cross-tenant data leakage | PostgreSQL RLS policies / DB session context | Integration test | Attempt cross-tenant read/write; verify `0 rows` or `403 Forbidden`. |
| **02** | **Auth on Every API Route** | Unauthenticated access | Server route middleware / API Gateway | Route matrix scan | Automated test crawling all routes without Bearer token; verify `401 Unauthorized`. |
| **03** | **Never Trust Frontend** | Client tampering, parameter tampering | Server-side validation schema (Zod/Pydantic) | Mutation test | Send tampered role (`role=admin`) or price (`price=0`); verify server rejects with `400 Bad Request`. |
| **04** | **Rate Limiting** | Brute force, scraping, DoS | Redis sliding-window / API Gateway | Load benchmark | Exceed 60 req/min on login or sensitive route; verify `429 Too Many Requests`. |
| **05** | **Input Sanitization & Validation** | XSS, command injection, malformed data | Strict input schemas & contextual encoding | Schema validator | Test with SQL metacharacters, HTML tags, and overflow strings; verify safe rejection. |
| **06** | **Parameterized Queries** | SQL Injection (SQLi) | ORM (Prisma/SQLAlchemy) / Parameterized SQL | Static Analysis (Semgrep) | Verify zero string concatenation in SQL queries (`f"SELECT * WHERE id={id}"` strictly prohibited). |
| **07** | **Lock Down CORS** | Cross-Origin Data Theft | Server CORS middleware | HTTP OPTIONS request | Test unapproved origin; verify `Access-Control-Allow-Origin` header is absent or denied. |
| **08** | **HTTPS Everywhere & HSTS** | Man-in-the-Middle (MitM), eavesdropping | Proxy / Cloudflare / Nginx configuration | TLS handshake test | Verify HTTP strictly redirects to HTTPS; `Strict-Transport-Security` header present. |
| **09** | **Stop IDOR / BOLA** | Insecure Direct Object References | Domain service object ownership check | Unit/Integration test | User A requests `/api/documents/{user_b_id}`; verify server verifies ownership and returns `404/403`. |
| **10** | **Debug Mode Off in Prod** | Information disclosure, stack trace leak | Environment configuration (`DEBUG=False`) | Production smoke test | Trigger error on production build; verify generic error response with zero stack traces or internal paths. |
| **11** | **CAPTCHA / Bot Protection** | Automated spam, credential stuffing | Cloudflare Turnstile on public signup/login | Integration review | Verify bot challenge blocks automated scripted submissions on exposed public forms. |
| **12** | **Admin Audit Logging** | Repudiation, insider threat | Audit service with tamper-evident log | Audit log test | Execute privileged admin action (role change, user deletion); verify structured log with redacted secrets. |
| **13** | **Private Storage Buckets** | Data exfiltration, exposed assets | S3/GCS bucket IAM policies | Bucket scan / URL test | Verify bucket blocks public anonymous access; private objects accessible only via short-lived signed URLs. |
| **14** | **Hide Admin Pages Properly** | Privilege escalation | Server-side RBAC guards on routes & data | Browser / API test | Navigate directly to `/admin` as normal user; verify server redirects or returns `403`, not merely hidden link. |
| **15** | **Update Vulnerable Packages** | Known CVE exploitation | Dependency lockfiles (`npm audit`, `trivy`) | Lockfile CVE scan | Verify zero high/critical vulnerabilities in `package.json` / `requirements.txt`. |
| **16** | **Validate File Upload Types** | Malicious file upload, web shell execution | Magic byte inspection, filename sanitization | File upload test | Upload `.php`/`.sh` disguised as `.jpg`; verify magic byte validator rejects file with `400`. |
| **17** | **AI Security Review** | Human blind spots, logic bugs | Automated PR review / Claude security check | Review findings log | AI review checks PR diff against OWASP Top 10; findings triaged and confirmed resolved. |
| **18** | **Security Headers** | Clickjacking, MIME sniffing, XSS | Server HTTP response headers | Security header scan | Verify presence of `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, and `Content-Security-Policy`. |
| **19** | **Verify Webhook Signatures** | Webhook forgery, replay attacks | HMAC-SHA256 signature & timestamp check | Integration test | Send forged webhook with invalid signature; verify `401/403` and rejection. Reject timestamps >5m old. |

---

## 3. Additional Mature SaaS & AI Security Controls

Beyond the baseline 19 controls, enterprise applications must enforce:
- **CSRF Protection**: SameSite cookies and anti-CSRF tokens on state-changing browser requests.
- **SSRF Defenses**: Whitelist outgoing HTTP destinations; block internal IP ranges (`127.0.0.1`, `169.254.169.254`, `10.0.0.0/8`).
- **Session Rotation**: Invalidate old session identifier upon login and privilege escalation.
- **Prompt Injection Defense**: Sanitize inputs to LLMs; treat model outputs as untrusted data before executing tool actions.
- **Secret Hygiene**: Enforce pre-commit TruffleHog checks; never commit `.env` or hardcoded tokens.

---

## 4. Controlled Status Standard

In all OpenClone security evaluations, use strictly:
- `PASS`: Tested and proven with observable command output or automated test.
- `FAIL`: Vulnerability detected or control missing.
- `BLOCKED`: Test blocked by external impediment.
- `NOT_RUN`: Scheduled check not yet performed.
- `NOT_APPLICABLE`: Control irrelevant to project architecture (with documented reason).
- `ACCEPTED_RISK`: Human owner signed off on authorized waiver in `DECISIONS.md`.
