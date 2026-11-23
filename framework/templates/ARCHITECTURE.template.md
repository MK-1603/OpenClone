# ARCHITECTURE.md — {{PROJECT_NAME}}
**System Architecture, Component Topologies, and Data Flows**  
*Specification:* v1.0.0 | *Status:* LIVING DOCUMENT

---

## 1. System Topology Overview

```text
       +---------------------------------------------+
       |           Client / Frontend Layer           |
       |  (Responsive Web / Mobile UI - Taste Skill) |
       +----------------------+----------------------+
                              | HTTPS / JSON-RPC
                              v
       +---------------------------------------------+
       |               API Gateway / Proxy            |
       |  (Rate Limiting, Auth Validation, Redaction) |
       +----------------------+----------------------+
                              | Internal
                              v
       +---------------------------------------------+
       |           Core Application Services         |
       |    (Domain Logic, Workflow Orchestrator)    |
       +----------------------+----------------------+
                              |
              +---------------+---------------+
              |                               |
              v                               v
    +-------------------+           +-------------------+
    | Primary Database  |           | External Services |
    | (SQLite/Postgres) |           | (AI APIs, Strix)  |
    +-------------------+           +-------------------+
```

---

## 2. Component Boundaries & Responsibilities

| Component | Responsibility Boundary | Trust Zone |
|---|---|---|
| **Presentation Layer** | UI rendering, client-side input validation, accessible navigation. | Untrusted |
| **API Layer** | Route handlers, request parsing, authentication token verification. | DMZ / Perimeter |
| **Domain Service Layer**| Business rules execution, state transitions, domain events. | Trusted Internal |
| **Persistence Layer** | Schema enforcement, transactions, query optimization. | Trusted Core |

---

## 3. Cross-Cutting Concerns

- **Error Handling**: Standardized error envelope with error codes, user-safe messages, and internal trace IDs.
- **Security Boundaries**: Server-side authorization checks on every state-changing route. Zero trust on client parameters.
- **Observability**: Structured JSON logging with automated redaction of sensitive credentials and PII.
