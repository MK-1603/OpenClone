# Concept 03: Specialist Workforce (Alternate Specification)

## 1. Alternate Paradigm: Adaptive Generalist Full-Stack AI Engineer
In small teams, single-agent workflows, or early-stage startups, delegating work across 72 discrete roles can introduce handoff overhead. The alternate approach uses **Dynamic Skill Injection on a Unified Agent**.

## 2. How the Alternate Operates
1. **Unified Worker Profile:** A single worker contract (`fullstack-autonomous-engineer`) operates as the active agent.
2. **Dynamic Skill Loading:** As the task shifts from schema design to frontend coding to CI/CD pipelines, OpenClone dynamically mounts domain-specific skills from `skills/` into the agent's context without switching personas.
3. **Contextual Permission Escalation:** The agent requests elevated permissions (e.g., terminal execution) on a per-task basis with human approval.

## 3. Trade-Off Analysis
* **Strengths:** Minimal coordination latency, straightforward for single-developer workflows.
* **Risks:** Lacks independent division-of-duties security boundaries; requires vigilant human oversight.
