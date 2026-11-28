# OpenClone Prompt Library

OpenClone provides structured, role-specific prompts for project intelligence, architectural analysis, security auditing, and coding agent execution.

## Featured Master Prompts

| Prompt | Target Environment | Purpose |
|---|---|---|
| [`PORTABLE-PROJECT-INTELLIGENCE-MASTER-PROMPT.md`](PORTABLE-PROJECT-INTELLIGENCE-MASTER-PROMPT.md) | **ChatGPT / Claude** | **Primary Entry Prompt.** Turns a raw `PROJECT.md` or brief into a complete, 6-file portable project package without installing OpenClone. |
| [`PROJECT-ASSESSMENT-ENTRY-PROMPT.md`](PROJECT-ASSESSMENT-ENTRY-PROMPT.md) | **AI Coding IDE / Local CLI** | Assesses an existing brownfield codebase, maps architecture, and generates an evidence-backed gap analysis. |
| [`SECURITY-ASSESSMENT-ENTRY-PROMPT.md`](SECURITY-ASSESSMENT-ENTRY-PROMPT.md) | **Security Auditor Agent** | Performs a 12-vector security and threat assessment on a repository. |
| [`MASTER-ENTRY-PROMPT.md`](MASTER-ENTRY-PROMPT.md) | **General Coding Agent** | Foundational AISDF governance prompt for tool-independent agent execution. |

## Lifecycle Phase Prompts

Specialized prompts for discrete engineering phases:

- [`PHASE-REQUIREMENTS.md`](PHASE-REQUIREMENTS.md) — Feature inventory and user story specification.
- [`PHASE-UX-DESIGN.md`](PHASE-UX-DESIGN.md) — Taste Skill anti-slop UI design system and component specification.
- [`PHASE-ARCHITECTURE.md`](PHASE-ARCHITECTURE.md) — Modular boundaries, data models, and API topologies.
- [`PHASE-IMPLEMENTATION.md`](PHASE-IMPLEMENTATION.md) — Governed vertical-slice code generation.
- [`PHASE-TESTING.md`](PHASE-TESTING.md) — Test pyramid generation and mutation testing.
- [`PHASE-RELEASE.md`](PHASE-RELEASE.md) — Gate evaluation, deployment verification, and changelog generation.

## Recovery & Continuity Prompts

- [`HANDOFF-AGENT-TO-AGENT.md`](HANDOFF-AGENT-TO-AGENT.md) — Structured inter-agent context transfer.
- [`RECOVERY-CONTEXT-LOSS.md`](RECOVERY-CONTEXT-LOSS.md) — Safe continuation protocol after an AI context window reset.
- [`RECOVERY-BLOCKED-TASK.md`](RECOVERY-BLOCKED-TASK.md) — Diagnostic protocol when an agent encounters unexpected errors or blocks.
