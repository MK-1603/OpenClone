# OpenClone Alternatives & Fallback Engineering Suite
**Version:** 1.0.0  
**Scope:** Architectural alternatives, fallback paths, and replacement strategies for all major repositories, providers, skills, and tools.

---

## 1. Core Principle: Alternative Does Not Mean Install Every Option

OpenClone is designed with deliberate architectural choices:
- Every capability has a **recommended primary implementation**.
- A **tested fallback path** is documented for critical failure domains (provider outages, rate limits, license changes).
- Integrations remain modular and replaceable without requiring complex plugin bloat.
- Alternatives are adopted only when a concrete product need, measurable reliability gain, or security advantage justifies the engineering effort.

---

## 2. Alternatives Documentation Index

| Document | Scope & Contents |
|---|---|
| **[ALTERNATIVES_CATALOGUE.md](ALTERNATIVES_CATALOGUE.md)** | Master catalogue of alternatives across all 7 core capability areas. |
| **[REPOSITORY_ALTERNATIVES_MATRIX.md](REPOSITORY_ALTERNATIVES_MATRIX.md)** | Evaluation of the 27 external reference repositories with candidate alternatives. |
| **[PROVIDER_AND_MODEL_ALTERNATIVES.md](PROVIDER_AND_MODEL_ALTERNATIVES.md)** | Direct model providers, 8 router candidates, and IDE host fallback strategies. |
| **[UI_UX_AND_DESIGN_ALTERNATIVES.md](UI_UX_AND_DESIGN_ALTERNATIVES.md)** | Component primitives, design token systems, typography, animation, and visual review tools. |
| **[SECURITY_TOOL_ALTERNATIVES.md](SECURITY_TOOL_ALTERNATIVES.md)** | SAST, DAST, secret scanning, software composition analysis (SCA), and container auditing. |
| **[BACKEND_AND_INFRA_ALTERNATIVES.md](BACKEND_AND_INFRA_ALTERNATIVES.md)** | Frameworks, databases, ORMs, caching, job queues, object storage, and deployment options. |
| **[AGENT_AND_SKILL_ALTERNATIVES.md](AGENT_AND_SKILL_ALTERNATIVES.md)** | Skill formats, tool-calling protocols, agent execution harnesses, and context managers. |
| **[DECISION_AND_FALLBACK_POLICY.md](DECISION_AND_FALLBACK_POLICY.md)** | Criteria and triggers for keeping, switching, or activating a fallback component. |
| **[DEFERRED_AND_REJECTED_OPTIONS.md](DEFERRED_AND_REJECTED_OPTIONS.md)** | Explicit register of rejected or deferred tools with technical rationale. |

---

## 3. Alternative Classification Labels

- `PRIMARY`: Default supported implementation used in standard workflows.
- `FALLBACK`: Tested replacement activated only when primary fails.
- `OPTIONAL`: User-enabled extension for specific project requirements.
- `SPECIALIST`: Invoked strictly for a specialized task (e.g., dynamic penetration testing).
- `REFERENCE`: Architectural or design guidance; not installed as a dependency.
- `EXPERIMENTAL`: Under isolated evaluation; excluded from production release gates.
- `REJECTED`: Formally evaluated and rejected with recorded rationale.
