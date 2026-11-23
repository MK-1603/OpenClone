# Concept 02: Project Source of Truth (Primary Specification)

## 1. Core Principle
Every project must maintain an immutable, human-approved single source of truth (`PROJECT.md` accompanied by `AGENTS.md`). Requirements, domain invariants, architectural decisions, and operational constraints are formally recorded and updated based only on verified evidence.

## 2. Invariants
1. **Explicit Separation:** Facts, assumptions, and unknowns must be rigorously separated.
2. **Traceable IDs:** Functional requirements (FR-xxx) and non-functional requirements (NFR-xxx) use permanent identifiers.
3. **Template Preservation:** Running project initialization (`init`) must never overwrite an existing `PROJECT.md`.

---

## 4. Architectural Alternatives & Operational Trade-Offs

## 1. Alternate Paradigm: Lean Issue-Driven Micro-Spec
For fast-moving teams operating with GitHub Issues, Jira, or Linear, keeping a large monolithic `PROJECT.md` synchronized can create duplication. The alternate approach uses **Distributed Issue-Centric Specifications**.

## 2. How the Alternate Operates
1. **Directory of Feature Micro-Specs:** Instead of a single root file, project requirements live in modular markdown files inside `.openclone/specs/SPEC-<id>.md`.
2. **Issue Synchronization:** Feature specs are linked directly to GitHub/GitLab issue bodies via webhook or CLI metadata.
3. **Dynamic Compilation:** When OpenClone compiles a context bundle for an agent, it combines the root architectural invariants with only the active feature micro-spec, reducing token overhead by up to 80%.

## 3. Trade-Off Analysis
* **Strengths:** Fits standard agile sprint tools; zero token bloat for large enterprise repos.
* **Risks:** Cross-feature architectural consistency requires proactive global schema validation.
