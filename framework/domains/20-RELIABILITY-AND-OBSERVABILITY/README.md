# 20 — Reliability & Observability
**OpenClone Canonical Engineering Domain**  
*Governed by OpenClone Global Standards | Domain Owner: Site Reliability Engineer (SRE) / Observability Architect*

---

## 1. Purpose & Scope
This domain defines the canonical OpenClone guidance for system reliability, fault tolerance, graceful degradation, and full-stack observability (logging, metrics, distributed tracing, and health checks).

## 2. Core Reliability & SRE Standards
- **Fault-Tolerance Patterns:**
  - Timeouts on all outbound network calls and database queries.
  - Bounded retries with exponential backoff and randomized jitter to prevent retry storms.
  - Tri-state Circuit Breakers (`CLOSED`, `OPEN`, `HALF_OPEN`) to isolate failing downstream dependencies.
  - Bulkheads and backpressure to prevent cascading resource exhaustion.
  - Health checks: Distinct `/health/liveness`, `/health/readiness`, and `/health/startup` probes.
- **Golden Signals Observability:**
  - **Latency:** Request duration percentiles (p50, p95, p99).
  - **Traffic:** Request rate and throughput.
  - **Errors:** Failed request rate and unhandled exception counts.
  - **Saturation:** CPU, memory, connection pool, and queue depth utilization.
- **Telemetry Standards:**
  - Structured JSON logging with trace/span correlation IDs (`trace_id`, `span_id`).
  - Mandatory credential and PII redaction before log serialization.
  - OpenTelemetry (OTel) semantic conventions for traces and metrics.

## 3. Related Specialist Skills
- [`reliability-engineering`](../../skills/reliability-engineering/SKILL.md) — Circuit breakers, bounded retries with jitter, and health probes.
- [`backend-observability-engineering`](../../skills/backend-observability-engineering/SKILL.md) — Structured logging, metrics, and OpenTelemetry distributed tracing.

## 4. References & Catalogues
- Telemetry Engine: `src/openclone/security/monitoring.py` (`SecurityMonitor`)
- Circuit Breaker Engine: `src/openclone/mie/circuit.py` (`CircuitBreaker`)
