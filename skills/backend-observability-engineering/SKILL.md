---
id: backend-observability-engineering
name: Backend Observability Engineering Skill
version: 1.0.0
category: backend
description: Structured JSON logging, trace correlation IDs, OpenTelemetry, Golden Signals, Prometheus metrics, and alerting.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/backend-observability-engineering/SKILL.md
triggers:
  - observability
  - logging
  - structured logs
  - metrics
  - tracing
  - opentelemetry
  - otel
  - correlation id
  - trace id
  - prometheus
  - golden signals
  - telemetry
negative_triggers:
  - print-logging-only
  - static-site
precedence: 28
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
  - cli
pre_build_gates:
  - Structured JSON logging schema defined (level, timestamp, trace_id, message)
  - Trace context propagation headers identified (W3C traceparent)
  - Golden signals metric instrumentation plan established
finish_gates:
  - Zero raw secrets or credentials printed in logs or traces (credential redaction verified)
  - Trace context propagated across service and database calls
  - Health checks and metric endpoints (/metrics, /health) functional
verification:
  - Automated log format and secret redaction audit test pass
  - Distributed trace span generation assertion
---

# Backend Observability Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `backend` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone Observability & SRE Intelligence  
**Workforce Alignment:** `observability-engineer`, `site-reliability-engineer`

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Provide actionable, real-time insight into backend system health, performance anomalies, distributed execution flows, and unexpected failures using structured telemetry.

### Boundaries
- **In Scope:** Structured JSON logs, trace/span correlation IDs (`trace_id`, `span_id`), OpenTelemetry SDK integration, Golden Signals (Latency, Traffic, Errors, Saturation), and secret redaction.
- **Out of Scope:** Third-party vendor dashboard styling.

---

## 2. CANONICAL OBSERVABILITY PRINCIPLES

1. **Structured JSON Logging:** Every log line must be valid single-line JSON with standard fields:
   `{"timestamp": "2026-11-24T10:00:00Z", "level": "INFO", "service": "api", "trace_id": "...", "span_id": "...", "message": "User authenticated", "user_id": "u_123"}`
2. **Strict Secret Redaction:**
   Logs and traces must NEVER contain plaintext passwords, API keys, JWT access tokens, credit card numbers, or authorization headers. All sensitive keys must be automatically redacted to `[REDACTED]`.
3. **Trace Context Propagation:**
   HTTP headers (`traceparent`) must be propagated across service boundaries, database queries (SQL comment tagging), and asynchronous worker jobs to enable end-to-end request tracing.
