---
trigger: always_on
---

# OpenClone 19-Point SaaS Security Baseline Rules

- **Zero Secrets Policy:** Never commit secrets, API keys, tokens, or private customer data. Redact credentials from all logs.
- **Server-Side Enforcement:** Never trust client-side validation alone. Enforce authentication and object-level authorization (IDOR/BOLA prevention) on every protected route.
- **Parameterized Queries:** All SQL and database operations must use parameterized queries or trusted ORM mappings.
- **Strict Sandboxing:** External commands must execute in bounded, least-privilege processes without lateral network traversal.
