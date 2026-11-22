# Concept 04: Task Graph & State Machine (Primary Specification)

## 1. Core Principle
Engineering plans are modeled as a Directed Acyclic Graph (DAG) of discrete work units. A deterministic state machine enforces valid transitions:
`DRAFT` -> `PLANNED` -> `APPROVED` -> `READY` -> `RUNNING` -> `SUCCEEDED` / `FAILED`

## 2. Invariants
1. **Cycle Rejection:** Cyclic dependencies are rejected immediately during plan ingestion.
2. **Dependency Gating:** A task cannot become `READY` until all tasks listed in its `depends_on` array have transitioned to `SUCCEEDED`.
3. **Evidence Requirement:** Transitioning to `SUCCEEDED` requires recorded execution evidence.
