# Skill Portability & Lifecycle Management

OpenClone skills (such as [Taste Skill v2.6.0](../../domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md)) follow a strict, portable packaging format usable across all supported hosts.

---

## 1. Canonical Skill Package Structure

Every OpenClone skill contains:
- `skill.json`: Skill manifest defining ID, name, version, triggers, negative triggers, prerequisites, and tools.
- `SKILL.md`: Human-readable and agent-executable procedure guidelines.
- `rules/`: Deterministic constraints and lint specifications.
- `tests/`: Automated unit and governance tests.

---

## 2. Six-Stage Skill Lifecycle

```
[ DISCOVERED ] ──> [ ELIGIBLE ] ──> [ SELECTED ] ──> [ LOADED ] ──> [ APPLIED ] ──> [ VERIFIED ]
```

1. **DISCOVERED:** Skill manifest found in `registries/SKILL-REGISTRY.md` or local directory.
2. **ELIGIBLE:** Triggers match current task type and no negative triggers fired.
3. **SELECTED:** Deterministic skill engine chooses skill for task context.
4. **LOADED:** Minimal instruction tokens injected into IDE workspace context.
5. **APPLIED:** AI agent executes implementation following skill rules.
6. **VERIFIED:** Independent evidence verification tests pass against skill rules.

A skill being present or discovered does not prove it was applied. Only observable evidence transitions a skill to `VERIFIED`.
