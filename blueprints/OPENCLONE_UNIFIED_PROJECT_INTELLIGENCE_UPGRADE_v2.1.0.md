# OpenClone Unified Project Intelligence & Portable IDE Execution Upgrade
**Version:** v2.1.0 | **Category:** Architecture & Specification Intelligence

---

## 1. Executive Summary

This specification establishes OpenClone's unified, zero-install project intelligence pipeline and portable IDE execution standard:

$$\text{PROJECT.md} \longrightarrow \text{ChatGPT / Claude} \longrightarrow \text{Portable Project Package} \longrightarrow \text{Any AI Coding IDE} \longrightarrow \text{Verified Project}$$

### Non-Negotiable Tenets
1. **PROJECT.md-First**: Grounded in human intent without hallucinated repository awareness.
2. **Zero OpenClone Dependency**: Generated packages are 100% portable and self-contained.
3. **Traceability Engine**: Strict lifecycle mapping from requirement ID to code, tests, and evidence.
4. **Change-Impact Management**: Systematic change propagation across requirements, decisions, and tasks.
5. **Session Continuity**: Durable filesystem state (`PROGRESS.md` & `HANDOFF.md`) enabling safe resumption without relying on hidden model memory.
6. **Risk-Based Security**: Opt-in, target-authorized security tools with zero unverified scans.

---

## 2. Traceability Matrix Standard

The `ACCEPTANCE_MATRIX.md` mandates the following 10-column schema:
- `Requirement ID`: Stable source identifier (`FR-XXX`, `NFR-XXX`, `SEC-XXX`, `UX-XXX`, `BR-XXX`, `DATA-XXX`, `OPS-XXX`).
- `Requirement Summary`: Faithful summary of the requirement.
- `Priority / Risk`: High / Medium / Low and risk profile.
- `Design / Decision`: Architecture document or ADR link.
- `Implementation Task`: Task or milestone reference in `IMPLEMENTATION_PLAN.md`.
- `Code Location`: File paths and modules where implemented.
- `Verification Method`: Unit, integration, benchmark, or static analysis test.
- `Evidence`: Test command, exit code, and log reference.
- `Status`: Strictly controlled: `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`, `NOT_APPLICABLE`, `ACCEPTED_RISK`.
- `Notes`: Open questions, waivers, or exceptions.

---

## 3. The 12-Phase Project Delivery Lifecycle

| Phase | Phase Name | Primary Objective | Exit Criteria |
|---|---|---|---|
| **P0** | Repository Discovery | Baseline Git status, stack, and existing features | Startup inspection report |
| **P1** | Requirements & Feasibility | Audit requirements, resolve blockers, state assumptions | Approved normalized `PROJECT.md` |
| **P2** | Architecture & Decisions | Define component topologies and ADRs | `ARCHITECTURE.md`, `DECISIONS.md` |
| **P3** | Foundation & Quality Gates | Establish test harnesses, linters, and CI | Clean test baseline |
| **P4** | Data, Identity & Contracts | Build schemas, permissions, and API endpoints | Passing integration tests |
| **P5** | Core User Journeys | Implement primary end-to-end vertical slices | Working demonstrable slices |
| **P6** | Secondary Features | Deliver remaining approved functional features | Verified tests and diff review |
| **P7** | UX & Anti-Slop Hardening | Eliminate generic UI tropes, verify WCAG 2.2 AA | Taste Skill gate pass |
| **P8** | Security & Supply Chain | Secret scan, SAST, optional bounded pentesting | Zero high/critical findings |
| **P9** | Reliability & Performance | Load benchmarks, health checks, error logging | Latency/throughput verified |
| **P10** | Release Readiness | Verify packaging, migrations, and rollback plans | Deployment dry-run passed |
| **P11** | Final Audit & Delivery | Independent review against original requirements | Completed acceptance matrix |
