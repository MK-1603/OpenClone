# Concept 02: Project Source of Truth (Primary Specification)

## 1. Core Principle
Every project must maintain an immutable, human-approved single source of truth (`PROJECT.md` accompanied by `AGENTS.md`). Requirements, domain invariants, architectural decisions, and operational constraints are formally recorded and updated based only on verified evidence.

## 2. Invariants
1. **Explicit Separation:** Facts, assumptions, and unknowns must be rigorously separated.
2. **Traceable IDs:** Functional requirements (FR-xxx) and non-functional requirements (NFR-xxx) use permanent identifiers.
3. **Template Preservation:** Running project initialization (`init`) must never overwrite an existing `PROJECT.md`.
