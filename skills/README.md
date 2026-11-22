# OpenClone Skills System

This directory houses reusable, versioned skills conforming to the OpenClone Universal AI Software Engineering Framework standards.

---

## Skills Catalogue

| Skill ID | Version | Description | Path |
|---|---|---|---|
| `taste-skill` | `v2.6.0` | Canonical Anti-AI-Slop Governance, Instruction-First Engineering & Adaptive Design Intelligence across 16 product domains | [`skills/taste-skill`](taste-skill/) |

---

## Operating Directives
- Every skill must declare its identity, version, location, capabilities, and governance gates in [`registries/SKILL-REGISTRY.md`](../registries/SKILL-REGISTRY.md).
- Skills operate under least-privilege principles and cannot bypass human approvals or deterministic control gates.
- For UI/UX design generation, `taste-skill` mandates pre-build gate verification (`plan-check.mjs`) and real-browser finish checks (`gate.mjs`).
