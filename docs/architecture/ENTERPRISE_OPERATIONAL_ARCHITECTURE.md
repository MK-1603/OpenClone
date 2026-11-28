# OpenClone Enterprise Operational Architecture

**Version:** 2.0.0  
**Classification:** Core Architecture Specification  
**Status:** IMPLEMENTED  

---

## 1. Executive Overview

OpenClone represents the transition of the OpenClone framework from an agentic prototyping runtime into a governed, observable, enterprise-ready AI Software Engineering Platform. The core architecture bridges autonomous multi-agent task execution with deterministic human-in-the-loop governance, cryptographic auditability, and production-grade release pipelines.

```
+-------------------------------------------------------------------------------+
|                       OpenClone Enterprise Control Plane                    |
+-------------------------------------------------------------------------------+
|                                                                               |
|   +-----------------------+     +-------------------+     +---------------+   |
|   | External Orchestrators|     | Human Supervisors |     | CI/CD & Cloud |   |
|   |  (Paperclip / AGY)    |     |  (Review / Sign)  |     | (PyPI / OIDC) |   |
|   +-----------+-----------+     +---------+---------+     +-------+-------+   |
|               |                           |                       |           |
|               v                           v                       v           |
|   +-----------------------------------------------------------------------+   |
|   |                Paperclip REST API & HMAC Auth Layer                   |   |
|   |    (Replay Nonces, Timestamp Bounds, Cryptographic Approval Digest)   |   |
|   +-----------------------------------+-----------------------------------+   |
|                                       |                                       |
|                                       v                                       |
|   +-----------------------------------------------------------------------+   |
|   |                   OpenClone Deterministic Runtime                     |   |
|   |  (Policy Engine, Approval Digest Validator, Permission Boundary)      |   |
|   +-------------------+-------------------------------+-------------------+   |
|                       |                               |                       |
|                       v                               v                       |
|   +-----------------------------------+   +-------------------------------+   |
|   |        Execution Ledger           |   |   Engineering Command Center  |   |
|   |     (SQLite3 WAL / Event Sinks)   |   |   (DAG, Metrics, Dev Dashboard)|  |
|   +-----------------------------------+   +-------------------------------+   |
|                       |                               |                       |
|                       v                               v                       |
|   +-----------------------------------------------------------------------+   |
|   |                   Cross-Platform & Device Lab Layer                   |   |
|   |    (Android ADB, iOS Sim, PyPI Wheels, Linux/macOS/Windows Runners)   |   |
|   +-----------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------+
```

---

## 2. Architectural Pillars

### 2.1 Deterministic Governance Over LLM Proposers

Under the OpenClone operating contract (`AGENTS.md`), LLM agents possess authority solely to propose mutations, task completions, or execution plans. Deterministic code components—including `PaperclipSecurityAuth`, `PolicyEngine`, and cryptographic SHA-256 digest checkers—possess sole authority to validate, allow, or reject state transitions.

### 2.2 Cryptographic Approval Binding

Human approvals must be strictly bound to immutable task signatures. A task proposal produces a SHA-256 canonical digest of its parameters, file scopes, and permission grants:
$$\text{Digest} = \text{SHA256}(\text{task\_id} \mathbin{\Vert} \text{scope} \mathbin{\Vert} \text{command} \mathbin{\Vert} \text{payload})$$

Any mutation of task parameters automatically invalidates the human approval digest, preventing execution of modified payloads without renewed human authorization.

### 2.3 Single Shared Ledger State

All worker activity, task transitions, heartbeats, and cost tracking are persisted in `workforce.sqlite3` with Write-Ahead Logging (WAL) enabled. Distributed processes access this ledger concurrently via SQLite busy handlers, ensuring ACID transactions without external database server overhead.

---

## 3. Component Interactions

### 3.1 Task Lifecycle & Delegation Flow

1. **Submission:** An external agent or human submits a task proposal via the Paperclip HTTP API (`POST /tasks`) with HMAC-SHA256 headers (`X-OpenClone-Signature`, `X-OpenClone-Timestamp`, `X-OpenClone-Nonce`).
2. **Authentication & Nonce Check:** The security layer verifies the HMAC signature using `PAPERCLIP_API_SECRET`, confirms the timestamp is within 300 seconds, and checks the nonce in SQLite memory to prevent replay attacks.
3. **Approval Validation:** If the task requires human approval, the runtime verifies that `human_approved` is accompanied by an authoritative 64-character hex digest matching the registered task policy.
4. **Execution:** The workforce worker thread picks up the task, dispatches tools within an isolated sandbox, and logs execution heartbeats to the ledger.
5. **Observation:** The Engineering Command Center reads SQLite ledger records in real-time, renders DAG execution trees, and streams status back to developers.

---

## 4. Production Security Model

| Boundary | Mechanism | Failure Action |
| :--- | :--- | :--- |
| **Network Ingestion** | HMAC-SHA256 Request Signing (`PaperclipSecurityAuth`) | HTTP 401 Unauthorized |
| **Replay Defense** | In-memory / persistent Nonce Tracking with 300s TTL | HTTP 401 Unauthorized |
| **Authorization** | Cryptographic 64-character SHA-256 Approval Digest | Task Rejected / Blocked |
| **File Access** | Strict Workspace Isolation (`run_command` Sandbox) | Access Denied |
| **Packaging & Release** | PyPI Trusted Publishing via OpenID Connect (OIDC) | Job Failure |

---

## 5. Technology Stack Summary

- **Runtime:** Python 3.10+ (Standard Library typing, dataclasses, sqlite3, hmac, hashlib)
- **Persistence:** SQLite3 with WAL mode (`workforce.sqlite3`)
- **API Server:** Built-in Python HTTP server (`http.server`) / ASGI compatible adapter
- **Observability:** Pure HTML5/CSS3/JavaScript responsive Command Center (zero external CDN dependency)
- **CI/CD:** GitHub Actions with OIDC PyPI publishing and multi-platform wheel smoke testing
