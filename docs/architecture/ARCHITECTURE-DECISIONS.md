# OPENCLONE — ARCHITECTURE DECISION RECORDS (ADR)

## ADR-001: Four-Set Project Intelligence Architecture
- **Status:** APPROVED & IMPLEMENTED
- **Context:** Project Intelligence previously lacked a dedicated problem-to-solution mapping layer and rigid linear array indexing tied features to solutions artificially.
- **Decision:** Establish four canonical sets: Set A (Product/Market), Set B (Gap/Problem Discovery - NEVER architecture), Set C (Solution Intelligence with acceptance criteria and proactive ops), and Set D (Consolidated Blueprint with relational many-to-many traceability).
- **Consequences:** Provides bidirectional traceability from requirement to defect, solution, and acceptance criteria without dropping findings.

## ADR-002: Preservation of the Native 72-Worker Registry
- **Status:** APPROVED & IMPLEMENTED
- **Context:** Adding a generic `software-architect.json` worker to `framework/workforce/registry/workers/` would violate workforce registry validation tests locking the registry to exactly 72 workers.
- **Decision:** Retain the 72-worker registry untouched. Implement `resolve_software_architect(scope, domain)` in `ProjectRouter` to route requests to existing registered workers (`principal-architect`, `solution-architect`, or specialist architects).
- **Consequences:** 100% backward compatibility preserved; zero registry drift.

## ADR-003: System Design Zero-Invention Rule
- **Status:** APPROVED & IMPLEMENTED
- **Context:** `TrafficProfile` previously injected hardcoded 100,000 DAU defaults when user metrics were absent, risking skewed architectural sizing.
- **Decision:** When workload metrics are missing, return `UnestimatedCapacityReport` with `NOT_ESTIMATED` status. Allow qualitative structural modeling to proceed without fabricating quantitative figures.
- **Consequences:** Eliminates synthetic metrics while allowing qualitative C4 modeling.

## ADR-004: Reverse Engineering Intelligence as an Independent Service
- **Status:** APPROVED & IMPLEMENTED
- **Context:** Brownfield legacy code inspection was previously limited to a 30-line AST counter in `project_intelligence.py`.
- **Decision:** Create `src/openclone/reverse_engineering/` as an independent service operating across 3 execution levels and 9 engineering domains. Wire it into `PIA-EVOLUTION` as its primary evidence source.
- **Consequences:** Reconstructs AS-IS architecture, polyglot dependencies, and database models from empirical evidence before modernization planning begins.

## ADR-005: Plan Builder Workforce Schema Compliance
- **Status:** APPROVED & IMPLEMENTED
- **Context:** Task planning was previously divided between document generators and manual `tasks.json` authoring without programmatic validation against workforce schema.
- **Decision:** Create `src/openclone/planning/builder.py` (`PlanBuilder`) importing `_validate_task` and `topo` from `workforce.py` to validate every task before outputting plans.
- **Consequences:** Guarantees all generated plans can immediately execute in the workforce runtime without schema rejection.

## ADR-006: Windows Job Objects Process-Tree Confinement
- **Status:** APPROVED & IMPLEMENTED
- **Context:** `proc.kill()` on Windows terminates only the parent process, leaving child processes running in the background as orphans on timeouts.
- **Decision:** Implement Windows Job Objects via `ctypes.windll.kernel32` in `_execute_command` to ensure atomic process-tree termination on Windows timeouts, with graceful fallback to `taskkill /F /T /PID`.
- **Consequences:** Complete process isolation and cleanup across POSIX and Windows platforms.
