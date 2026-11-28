---
name: openclone-engineering
description: OpenClone Autonomous Engineering Execution Suite for Antigravity agents. Use when analyzing requirements, designing architectures, decomposing tasks into dependency graphs, executing governed operations, and verifying test evidence.
---

# OpenClone Engineering Skill

This skill guides Antigravity agents in coordinating engineering tasks under OpenClone governance.

## When to Use
- User requests software requirements decomposition, implementation planning, or architectural design.
- User asks to inspect repository state, git status, and project configuration.
- User requests governed execution of engineering operations with audit evidence.
- User requests verification of test suites, link health, or release readiness.

## Procedures

### 1. Repository Inspection
Call `openclone_inspect_repository` before modifying files to understand git status, tracked files, and configuration.

### 2. Task Planning
Call `openclone_generate_plan` with the engineering requirement prompt to receive a topologically sorted task list with assigned worker roles and risk classifications.

### 3. Governed Task Execution
Call `openclone_execute_task` to run the 12-stage execution lifecycle (`REQUEST` -> `UNDERSTAND` -> `INSPECT` -> `PLAN` -> `VALIDATE` -> `APPROVE` -> `ROUTE` -> `ASSIGN` -> `EXECUTE` -> `TEST` -> `VERIFY` -> `DELIVER`).

### 4. Verification Check
Call `openclone_get_verification_results` to ensure 100% of automated tests pass before declaring a task complete.
