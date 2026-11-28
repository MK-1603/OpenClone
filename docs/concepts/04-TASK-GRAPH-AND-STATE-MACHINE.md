# Concept 04: Task Graph & State Machine (Primary Specification)

## 1. Core Principle
Engineering plans are modeled as a Directed Acyclic Graph (DAG) of discrete work units. A deterministic state machine enforces valid transitions:
`DRAFT` -> `PLANNED` -> `APPROVED` -> `READY` -> `RUNNING` -> `SUCCEEDED` / `FAILED`

## 2. Invariants
1. **Cycle Rejection:** Cyclic dependencies are rejected immediately during plan ingestion.
2. **Dependency Gating:** A task cannot become `READY` until all tasks listed in its `depends_on` array have transitioned to `SUCCEEDED`.
3. **Evidence Requirement:** Transitioning to `SUCCEEDED` requires recorded execution evidence.

---

## 4. Architectural Alternatives & Operational Trade-Offs

## 1. Alternate Paradigm: Event-Driven Reactive Kanban Stream
In dynamic development environments where requirements emerge incrementally, pre-computing a full static DAG can be premature. The alternate approach provides **Reactive Event-Driven Task Scheduling**.

## 2. How the Alternate Operates
1. **Event-Triggered Tasks:** Tasks declare event triggers (`trigger_on: [ARTIFACT_GENERATED, TEST_PASSED]`) rather than static upstream task IDs.
2. **Backlog Prioritization:** Tasks reside in a priority queue. As events are recorded in the ledger, waiting tasks evaluate their trigger conditions and dynamically enter the ready queue.
3. **Dynamic Fan-Out:** Allows an orchestrator agent to spawn sub-tasks in parallel based on runtime findings (e.g., spawning three remediation tasks after a security scan).

## 3. Trade-Off Analysis
* **Strengths:** Highly adaptive to exploratory coding and automated bug-hunting.
* **Risks:** Harder to predict total project duration, token cost, and deadlocks.
