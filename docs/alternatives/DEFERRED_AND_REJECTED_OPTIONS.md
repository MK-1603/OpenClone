# OpenClone — Deferred & Rejected Options Register
**Version:** 1.0.0  
**Scope:** Explicit audit record of evaluated tools, libraries, routers, and frameworks that were rejected or deferred.

---

## 1. Rejected Candidates Register

| Candidate | Category | Evaluated Role | Technical Rationale for Rejection | Status |
|---|---|---|---|---|
| **Devansh-365/freellm** | LLM Router | Free Model Proxy | Relies on scraping undocumented web endpoints; breaks frequently; violates provider TOS | `REJECTED` |
| **kaiser-data/...** | LLM Router | Free Model Proxy | Reverse-engineered proxy with high token-theft and credential leakage risk | `REJECTED` |
| **nabinkhadka/...** | LLM Router | Free Model Proxy | Fragile scraping architecture; unsuitable for production software engineering | `REJECTED` |
| **YeomanYe/...** | LLM Router | Free Model Proxy | Abandoned repository with unmaintained endpoints | `REJECTED` |
| **MajidAsghariTabrizi/...**| LLM Router | Free Model Proxy | Fragile wrapper; zero SLA or security guarantees | `REJECTED` |
| **tashfeenahmed/...** | LLM Router | Free Model Proxy | Experimental proxy with unverified reliability | `REJECTED` |
| **Autonomous Swarms** | Orchestration | Unbounded Multi-Agent | Prone to retry storms, runaway API costs, hallucinated state transitions | `REJECTED` |
| **Arbitrary Shell Execution**| Tool Execution | Host Terminal Access | Violates least privilege; allows catastrophic host compromise | `REJECTED` |

---

## 2. Deferred Candidates Register

| Candidate | Category | Evaluated Role | Technical Rationale for Deferral | Status |
|---|---|---|---|---|
| **alienz-dev/llm-router** | LLM Router | Model Proxy | Small ecosystem and limited documentation; LiteLLM is significantly more mature | `DEFERRED` |
| **qybaihe/bla** | Security | Binary Analysis | Out of scope for standard web SaaS engineering; deferred to low-level systems | `DEFERRED` |
| **Vector DB for Core State**| Architecture| Vector Storage | Unnecessary complexity for project metadata; flat markdown and SQLite provide faster, simpler retrieval | `DEFERRED` |
| **Multi-Cloud Mesh** | Infrastructure| Distributed Deployment | Premature optimization for initial project launches; adds severe DevOps overhead | `DEFERRED` |
