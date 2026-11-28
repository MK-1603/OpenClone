# AUTONOMOUS ENGINEERING EXECUTION ENGINE ARCHITECTURE
## Architecture Evolution & Controlled Execution Specification

**Document Version:** 2.0.0  
**Canonical Product:** OpenClone  
**Framework:** OpenClone AI Engineering Framework (AIEF)  
**Status:** `RATIFIED_SPECIFICATION`  
**Architect:** Principal Software Architecture & Engineering Standards

---

## 1. Executive Summary

The **Autonomous Engineering Execution Engine (AEEE)** upgrades OpenClone from a manual command-driven control plane into an intelligent, governed, autonomous engineering platform. It orchestrates software requirement understanding, repository analysis, task decomposition, provider-neutral model selection, specialist agent delegation, controlled execution, automated testing, failure recovery, and delivery.

The engine does not replace existing subsystems; it unifies:
- **Governance & State Machine:** `src/openclone/runtime/workforce.py`
- **Model Intelligence:** `src/openclone/mie/`
- **Project Intelligence:** `src/openclone/intelligence/`
- **Platform Diagnostics & Lifecycle:** `src/openclone/platform/` & `src/openclone/lifecycle/`
- **Worker Registry:** 72 specialist roles in `framework/workforce/registry/workers/`

---

## 2. Target Architecture Model

```text
                                OPENCLONE
                     UNIVERSAL AI ENGINEERING PLATFORM
                                     |
             +-----------------------+-----------------------+
             |                                               |
       INTELLIGENCE LAYER                              CONTROL LAYER
             |                                               |
     Requirement Analysis (`intelligence/`)          Governance Engine (`workforce.py`)
     Repository Intelligence (`project.py`)          Permission Engine (`agent_gateway.py`)
     Context Intelligence (`blueprints.py`)         Approval Authority (`Paperclip`)
     Task Classification (`classifier.py`)           Policy Engine (`policies.py`)
             |                                               |
             +-----------------------+-----------------------+
                                     |
                     AUTONOMOUS EXECUTION ENGINE
                                     |
                      [1] REQUEST INTAKE & CLASSIFY
                                     |
                      [2] REPOSITORY CONTEXT INSPECT
                                     |
                      [3] TASK DECOMPOSITION & PLAN
                                     |
                      [4] PLAN VALIDATION & APPROVAL
                                     |
                      [5] MODEL INTELLIGENCE ROUTING
                                     |
                      [6] SPECIALIST AGENT ASSIGNMENT
                                     |
                      [7] GOVERNED TASK EXECUTION
                                     |
                      [8] VERIFICATION & TEST PIPELINE
                                     |
                        +---- [Failure?] ----+
                        |                    |
                 [Analyse Failure]    [Bounded Repair]
                        |                    |
                        +--------------------+
                                     |
                      [9] DELIVERY & AUDIT LEDGER
                                     |
             +-----------------------+-----------------------+
             |                                               |
       INTERFACES & HOSTS                              INTEGRATIONS
             |                                               |
       CLI (`openclone autonomous`)                   AI Model Providers (MIE)
       MCP Server (`src/openclone/mcp/`)              MCP Tools & Servers
       Dashboard & Web APIs                           External Host IDE Adapters
```

---

## 3. The 12-Stage Controlled Execution Lifecycle

Every autonomous task advances through strict deterministic state transitions:

```text
REQUEST -> UNDERSTAND -> INSPECT -> PLAN -> VALIDATE PLAN -> APPROVE -> ROUTE MODEL -> ASSIGN AGENTS -> EXECUTE -> TEST -> VERIFY -> (ANALYSE FAILURE / BOUNDED REPAIR) -> DELIVER
```

### Stage Specifications:
1. **`REQUEST`:** Ingests raw developer prompt, requirement document, or issue ticket.
2. **`UNDERSTAND`:** Identifies request type (`NEW_PROJECT`, `FEATURE`, `BUGFIX`, `REFACTOR`, `TESTING`, `DOCUMENTATION`, `ARCHITECTURE`, `MAINTENANCE`, `INVESTIGATION`).
3. **`INSPECT`:** Inspects git status, active files, directory tree, and configuration context.
4. **`PLAN`:** Decomposes requirement into topological task DAG with dependencies.
5. **`VALIDATE PLAN`:** Validates task parameters against schema and computes immutable SHA-256 task digest.
6. **`APPROVE`:** Verifies human approver authorization for high-risk operations; auto-promotes low-risk tasks based on execution mode policy.
7. **`ROUTE MODEL`:** Evaluates reasoning and coding complexity, selecting the optimal model provider via MIE.
8. **`ASSIGN AGENTS`:** Matches tasks against 72 specialist worker contracts and 12 teams.
9. **`EXECUTE`:** Executes actions through governed subprocess with real-time credential redaction.
10. **`TEST`:** Runs actual test commands, capturing stdout, stderr, and exit codes.
11. **`VERIFY`:** Validates acceptance criteria and evaluates release gate blockers.
12. **`DELIVER`:** Produces structured delivery report and records tamper-evident audit ledger entries.

---

## 4. The 5 Execution Modes

| Mode | Purpose | Planning Depth | Model Tier | Verification Depth | Approval Required | Max Retries |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Instant** | Straightforward fixes, queries | Minimal (1 task) | Fast / Lightweight | Basic Syntax / Lint | None (Low Risk) | 1 |
| **Fast** | Quick implementation | Lightweight (1-3 tasks) | Balanced Coding | Unit Tests | High Risk Only | 2 |
| **Standard** | Standard engineering work | Full DAG (1-10 tasks) | High Reasoning | Unit + Integration | Normal Gate | 3 |
| **Deep** | Complex architectural changes | Exhaustive DAG | Frontier Reasoning | Full Suite + Review | Strict Human Gate | 4 |
| **Autonomous**| Multi-step bounded execution | Adaptive DAG | Frontier Multi-Model | Full + EGM Gate | Policy-Bound | 3 |

---

## 5. Failure Recovery & Bounded Repair Loop

To prevent infinite repair loops while enabling autonomous recovery:
1. When a test or verification step fails, execution halts and increments the `repair_iteration` counter.
2. The failure analyzer classifies the failure:
   - `SYNTAX_ERROR`: Mechanical syntax or import error.
   - `TEST_ASSERTION`: Logic failure on expected return values.
   - `DEPENDENCY_MISSING`: Missing package or toolchain binary.
   - `PERMISSION_DENIED`: File or security policy denial.
   - `TIMEOUT`: Execution budget or process timeout exceeded.
3. If `repair_iteration <= max_retries`:
   - A bounded repair task is generated with the failure diagnostic as context.
   - The task is scheduled, approved within the remaining budget, and re-executed.
4. If `repair_iteration > max_retries`:
   - The engine halts, logs the failure in the tamper-evident ledger, marks the state `FAILED`, and presents a diagnostic recommendation to the human operator.

---

## 6. Architecture Boundaries & Invariants

1. **Non-Negotiable Precedence:** LLMs propose; deterministic code and human approvers decide.
2. **Deterministic Governance:** Task state transitions are evaluated by code, not LLM prompts.
3. **No Unrestricted Execution:** Autonomous mode remains bounded by token, time, file scope, and retry limits.
4. **Secret Protection:** Automatic regex redaction of credentials in all standard streams and logs.
5. **No AI Slope:** Minimal viable diffs only. No unrequested refactors or unvetted external services.
