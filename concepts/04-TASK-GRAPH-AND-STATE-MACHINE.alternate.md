# Concept 04: Task Graph & State Machine (Alternate Specification)

## 1. Alternate Paradigm: Event-Driven Reactive Kanban Stream
In dynamic development environments where requirements emerge incrementally, pre-computing a full static DAG can be premature. The alternate approach provides **Reactive Event-Driven Task Scheduling**.

## 2. How the Alternate Operates
1. **Event-Triggered Tasks:** Tasks declare event triggers (`trigger_on: [ARTIFACT_GENERATED, TEST_PASSED]`) rather than static upstream task IDs.
2. **Backlog Prioritization:** Tasks reside in a priority queue. As events are recorded in the ledger, waiting tasks evaluate their trigger conditions and dynamically enter the ready queue.
3. **Dynamic Fan-Out:** Allows an orchestrator agent to spawn sub-tasks in parallel based on runtime findings (e.g., spawning three remediation tasks after a security scan).

## 3. Trade-Off Analysis
* **Strengths:** Highly adaptive to exploratory coding and automated bug-hunting.
* **Risks:** Harder to predict total project duration, token cost, and deadlocks.
