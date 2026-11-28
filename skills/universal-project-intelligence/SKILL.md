---
name: universal-project-intelligence
description: Analyzes project ideas, PRDs, or codebases; performs multi-label classification across 14 engineering disciplines (ENG-01 to ENG-14); operates the Four-Set Intelligence Architecture (Set A Features, Set B Gaps/Problems, Set C Solutions, Set D Final Product Blueprint); and generates complete governed project specifications across PIA-NEW, PIA-DEFINED, and PIA-EVOLUTION modes.
version: 2.2.0
---

# Universal Project Intelligence Skill (PIA-001)

## Purpose
Enables coding agents to understand natural-language project requests, extract requirements, classify project archetypes, assemble minimum effective workforce teams, evaluate technology alternatives, harmonize documentation, and execute the **Four-Set Intelligence Architecture** across three standardized operating modes.

## The Four-Set Intelligence Architecture
1. **Set A — Feature Intelligence:**
   - Product and domain research, market capabilities, user expectations, competitor analysis.
   - Categorizes capabilities into essential, advanced, optional, and future features (`FEAT-xxx`).
   - Evidence classifications: `PROMPT_EXTRACTED`, `MARKET_INFERENCE`, `VERIFIED_MARKET_RESEARCH`.
2. **Set B — Gap & Problem Intelligence:**
   - Identifies missing capabilities, functional gaps, product weaknesses, technical limitations, UX flaws, and architecture debt (`GAP-xxx`, `PROB-xxx`).
   - *Boundary Rule:* Set B is strictly problem/gap discovery and must never be defined as target architecture.
   - Evidence classifications: `STATIC_INSPECTION`, `AUTOMATED_SCAN`, `RUNTIME_EXECUTION`, `UX_EVALUATION`, `ARCHITECTURE_DEBT`.
3. **Set C — Solution Intelligence (NEW):**
   - Develops concrete solutions for Set B gaps/problems and proactive improvements (`SOL-xxx`).
   - Maps problems to solutions with complexity estimates, alternatives considered, dependencies, trade-offs, and acceptance criteria (`AC-xxx`).
   - Statuses: `PROPOSED`, `RECOMMENDED`, `ALTERNATIVE`, `APPROVED`, `REJECTED`.
4. **Set D — Final Product Intelligence:**
   - Consolidates Sets A, B, and C into an advanced, traceable product blueprint.
   - Emits master specification artifacts: `PROJECT.md`, `Project-Requirement.md`, `Features-List.md`, `Gaps-And-Problems.md`, `Solution-Blueprint.md`, `Tech-Stack.md`, `Decision-Log.md`, and `Project-Details.md`.

## Architectural Boundaries
- **PIA (WHAT):** Determines WHAT the product needs and WHICH problems must be solved.
- **Set C (WHICH):** Determines WHICH solutions address identified defects and gaps.
- **Software Architect (HOW):** Consumes approved Set D requirements and determines HOW the system should be architected without modifying product requirements.
- **System Design:** Develops quantitative capacity dimensioning (QPS, storage, cache), architectural patterns, and C4 diagrams.
- **Plan Builder:** Converts approved engineering requirements into an executable, dependency-ordered task DAG.

## Operating Modes
1. **PIA-NEW:** New project discovery and definition from scratch or user prompt. Synthesizes Set A -> Set B -> Set C -> Set D.
2. **PIA-DEFINED:** Documentation harmonization and gap assessment. Ingests fragmented PRDs, design docs, or notes, detects contradictions, establishes document authority precedence, and generates reconciled specifications.
3. **PIA-EVOLUTION:** Codebase static X-Ray and system evolution. Parses existing codebase ASTs, measures technical debt, identifies architectural drift against documented specs, and formulates phased migration plans. *(Note: PIA-EXISTING is a deprecated historical alias for PIA-EVOLUTION).*

## Applicable Disciplines
- ENG-01 Artificial Intelligence
- ENG-02 Machine Learning
- ENG-03 Data Science & Data Engineering
- ENG-04 AI Model Engineering
- ENG-05 Software Application Engineering
- ENG-06 Backend & API Engineering
- ENG-07 Enterprise Software Engineering
- ENG-08 SaaS & Cloud Service Engineering
- ENG-09 DevOps & Cloud Engineering
- ENG-10 Automation & Integration Engineering
- ENG-11 Cybersecurity Engineering
- ENG-12 Specialized Technology Engineering
- ENG-13 Software Quality Engineering
- ENG-14 UI/UX & Product Engineering

## Workforce Role Integration
- **Role Identifier:** `project-intelligence-architect` (PIA-001)
- **Role Team:** `architecture`
- **Governance:** Operates under OpenClone Two-Gate Governance:
  - **Gate A (Phase-Start Approval):** `approve(PHASE-XX-START)` -> `transition(READY)` -> `complete(SUCCEEDED)`
  - **Gate B (Phase-Completion Acceptance):** `approve(PHASE-XX-COMPLETION)` -> `transition(READY)` -> `complete(SUCCEEDED)`

## Workflow Procedure
1. **Understand & Classify:** Run classification via MCP tool `openclone_classify_project` or internal CLI.
2. **Evaluate Technology:** Run technology evaluation via MCP tool `openclone_evaluate_technology`.
3. **Route Governance & Workforce:** Compute deterministic domain activation and minimum effective workforce via `openclone_route_project`.
4. **Generate Four-Set Governed Package:** Run package generation via MCP tool `openclone_generate_package` with modular envelope support (`PROJECT.md`, `Features-List.md`, `Gaps-And-Problems.md`, `Solution-Blueprint.md`, `Project-Requirement.md`, `Tech-Stack.md`, `Decision-Log.md`).
5. **Phase Governance:** Follow the two-gate milestone lifecycle (`PHASE-XX-START` and `PHASE-XX-COMPLETION`) to unblock child work units without circular deadlock.
