# Concept 03: Specialist Workforce (Primary Specification)

## 1. Core Principle
Complex software engineering requires distinct, accountable specialist capabilities rather than unconstrained generalist prompting. OpenClone defines 72 specialist roles across 12 teams (Product, UX, Architecture, Frontend, Mobile, Backend, Data, AI/ML, Security, QA, Platform/Ops, Specialized EGM).

## 2. Invariants
1. **Role Contracts:** Every worker has an explicit manifest (`workforce/registry/workers/*.json`) defining allowed actions.
2. **Least-Privilege Enforcement:** Roles without execute permissions cannot run terminal processes. Independent reviewers cannot modify files.

---

## 4. Architectural Alternatives & Operational Trade-Offs

## 1. Alternate Paradigm: Adaptive Generalist Full-Stack AI Engineer
In small teams, single-agent workflows, or early-stage startups, delegating work across 72 discrete roles can introduce handoff overhead. The alternate approach uses **Dynamic Skill Injection on a Unified Agent**.

## 2. How the Alternate Operates
1. **Unified Worker Profile:** A single worker contract (`fullstack-autonomous-engineer`) operates as the active agent.
2. **Dynamic Skill Loading:** As the task shifts from schema design to frontend coding to CI/CD pipelines, OpenClone dynamically mounts domain-specific skills from `skills/` into the agent's context without switching personas.
3. **Contextual Permission Escalation:** The agent requests elevated permissions (e.g., terminal execution) on a per-task basis with human approval.

## 3. Trade-Off Analysis
* **Strengths:** Minimal coordination latency, straightforward for single-developer workflows.
* **Risks:** Lacks independent division-of-duties security boundaries; requires vigilant human oversight.
