---
id: backend-observability-engineering
name: Backend Observability Engineering Skill
version: 1.0.0
category: backend
description: Structured JSON logging, trace correlation IDs, OpenTelemetry, Golden Signals, Prometheus metrics, and alerting.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/backend-observability-engineering/SKILL.md
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

See canonical specification at [`../../framework/skills/backend-observability-engineering/SKILL.md`](../../framework/skills/backend-observability-engineering/SKILL.md).
