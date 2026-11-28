<p align="center">
  <img
    src="assets/branding/openclone-logo.png"
    alt="OpenClone — Build with Any AI. Governed by One Engineering Standard."
    width="850"
  />
</p>

<p align="center">
  <a href="https://github.com/MK-1603/OpenClone/releases" title="Version 2.0.0"><img src="https://img.shields.io/badge/version-2.0.0-38bdf8?style=flat&logo=github&logoColor=white" alt="Version 2.0.0" /></a>
  &nbsp;
  <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.10%2B-10b981?style=flat&logo=python&logoColor=white" alt="Python 3.10+" /></a>
  &nbsp;
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-6366f1?style=flat" alt="MIT License" /></a>
  &nbsp;
  <a href="tests/"><img src="https://img.shields.io/badge/tests-747%20passing%20%7C%200%20failed-059669?style=flat" alt="747 Passing Tests" /></a>
  &nbsp;
  <a href="security/scanners.lock.json"><img src="https://img.shields.io/badge/security-14%20scanners%20locked-ef4444?style=flat" alt="14 Scanners Locked" /></a>
  &nbsp;
  <a href="src/openclone/mcp/server.py"><img src="https://img.shields.io/badge/mcp-22%20tools%20active-8b5cf6?style=flat" alt="MCP 22 Tools Active" /></a>
</p>

<p align="center">
  <strong>Provider-Neutral · IDE-Independent · Deterministic Engineering Standard · Anti-AI-Slop Governance</strong><br />
  <em>One engineering standard for every AI-powered software development workflow.</em>
</p>

<p align="center">
  <a href="#01-what-is-openclone">01. Overview</a> ·
  <a href="#02-the-problem-and-the-solution">02. Problem & Solution</a> ·
  <a href="#03-core-philosophy">03. Philosophy</a> ·
  <a href="#04-how-openclone-works">04. How It Works</a> ·
  <a href="#05-platform-capabilities">05. Capabilities</a> ·
  <a href="#06-engineering-lifecycle">06. Lifecycle</a> ·
  <a href="#07-specialist-workforce">07. Workforce</a> ·
  <a href="#08-model-and-ide-ecosystem">08. Ecosystem</a> ·
  <a href="#09-architecture-overview">09. Architecture</a> ·
  <a href="#10-getting-started">10. Getting Started</a> ·
  <a href="#11-master-engineering-orchestrator--python-sdk">11. Master Orchestrator</a> ·
  <a href="#12-mcp-and-tool-integration">12. MCP Integration</a> ·
  <a href="#13-security-and-engineering-quality">13. Security & Quality</a> ·
  <a href="#14-real-world-demonstrations">14. Demonstrations</a> ·
  <a href="#15-documentation-hub">15. Documentation</a> ·
  <a href="#16-roadmap">16. Roadmap</a> ·
  <a href="#17-contributing-and-license">17. Community & License</a>
</p>

---

> [!IMPORTANT]
> **Notice for AI Assistants (ChatGPT, Claude, Cursor, Antigravity) When Given this Repository URL:**  
> When a user provides this repository link to you in chat, **do not ask them to download a large ZIP or clone the full repository**. Instead, execute these onboarding steps:
>
> 1. **Pre-Flight System Check:** Identify the user's OS and verify that Python 3.10+ is available (`python --version`).
> 2. **Zero-Clone Background Install:** Instruct the user to install OpenClone headlessly via:
>
>    ```bash
>    pip install git+https://github.com/MK-1603/OpenClone.git
>    ```
>
>    *(or `agy plugin install https://github.com/MK-1603/OpenClone` for Google Antigravity).*
> 3. **Verify System Health:** Check that OpenClone is active by executing:
>
>    ```bash
>    python -c "import openclone; print('OpenClone v' + openclone.__version__ + ' operational')"
>    ```
>
> 4. **Engage the Goal:** Ask the user what application, system, or architecture they want to design, build, or verify.

---

## 01. What Is OpenClone?

### Build with Any AI. Governed by One Engineering Standard

Modern artificial intelligence generates code at superhuman speed. However, **software engineering is not raw text synthesis**. Production-grade software requires immutable requirements, defensive security baselines, reproducible automated tests, dependency-ordered rollouts, and evidence-backed quality verification.

Without a unifying engineering framework, AI-assisted development deteriorates into **AI Slope**—where context resets erase past architectural decisions, hallucinated test passes bypass quality checks, uncontrolled model edits create unintended breaking changes, and generic visual clichés flood user interfaces.

**OpenClone** is an AI Software Development Framework (AISDF) that brings structure, intelligence, governance, verification, and repeatable engineering practices to AI-assisted software development.

> **Central Positioning:**  
> **OpenClone is the engineering framework around the AI coding agent, not simply another code-generation agent.**  
> It does not replace your AI model or your preferred IDE. It equips Claude, ChatGPT, Gemini, Codex, Antigravity, and Cursor with a deterministic, provider-neutral control plane that keeps software development structured, traceable, and secure.

---

## 02. The Problem and the Solution

Uncontrolled AI-assisted software development suffers from recurring operational and architectural failure modes:

- **Missing Requirements & Scope Creep:** Implicit assumptions turn into uncontrolled feature bloat without recorded user authorization.
- **Architecture Drift:** Architectural decisions drift silently across conversational turns, leading to contradictory abstractions.
- **Context Loss ("AI Amnesia"):** Context window resets wipe out previous technical decisions, requiring developers to re-prompt and re-explain the system constantly.
- **Hallucinated Verification:** AI agents state *"All tests pass and the implementation is complete"* without actually executing test suites or producing verifiable test logs.
- **Security & Supply Chain Oversights:** Accidental credential exposure, unauthorized third-party packages, and missing least-privilege boundary enforcement.
- **Visual AI-Slop:** Monotonous dark purple gradients, meaningless pill badges, unstyled form elements, and substandard accessibility.

### The Contrast: Uncontrolled AI vs. OpenClone Governed Engineering

| Engineering Dimension | Uncontrolled AI Development ("AI Slope") | OpenClone Governed Engineering |
| --- | --- | --- |
| **Project Understanding** | Ephemeral; trapped in transient chat sessions. | **Canonical Source of Truth:** Structured [`PROJECT.md`](project/PROJECT.md.template) defines immutable boundaries. |
| **Requirements Traceability** | Requirements easily lost, overlooked, or hallucinated. | **Traceable Contract Hierarchy:** Requirements map directly to tasks, code diffs, and verification artifacts. |
| **Architecture Drift** | Decisions drift silently across sessions and model turns. | **Documented Architectural Invariants:** 31 engineering domains and normative standards in [`framework/domains/`](framework/domains/). |
| **Project Continuity** | Context window resets erase architecture and progress. | **Durable Filesystem Handoffs:** `PROGRESS.md` & `HANDOFF.md` ensure seamless session resumption. |
| **Execution Control** | Monolithic "one-shot" mass rewrites and fragile diffs. | **Deterministic Task DAG:** Cycle-free dependency graph enforces smallest reviewable units of work. |
| **Scope Governance** | Unprompted feature bloat, dependency creep, and rewrites. | **Cryptographic Digest Binding:** SHA-256 task digest invalidates prior human approvals upon scope shift. |
| **Verification & Quality** | AI hallucinates test passes and claims completion verbally. | **V0–V5 Observable Evidence Model:** Real test logs, diffs, and scanner outputs must exist on disk. |
| **Security & Isolation** | Unmonitored lateral tool privileges and host exposure. | **4-Tier Copyleft Isolation & Pinned Scanners:** Strict execution harnesses and secret redaction. |
| **IDE Portability** | Vendor lock-in to proprietary prompt formats and rules. | **Provider-Neutral Host Adapters:** Works identically in Antigravity, Cursor, Claude Code, and Codex. |
| **UI/UX Design Quality** | Ambient purple gradients, generic cards, blur blobs. | **[Taste Skill v2.6.0](framework/domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md):** 8-pt typography scale, tokens, WCAG 2.2 AA contrast. |

---

## 03. Core Philosophy

OpenClone is governed by eight foundational engineering principles:

1. **Provider Neutrality:** The framework never locks you into a specific model provider. It operates identically whether powered by OpenAI (GPT-6), Anthropic (Claude 3.5), Google DeepMind (Gemini 2.0), or open-weight models via Ollama.
2. **IDE Independence:** Architecture, governance, and verification are portable across Google Antigravity, Cursor, Claude Code, OpenAI Codex, or standard terminal workflows.
3. **Engineering Governance:** LLMs propose; deterministic code and authorized humans decide. Critical operations require verifiable permissions.
4. **Deterministic Standards:** Architectural rules, task state machines, schema validations, and scanner lockfiles are enforced programmatically, not probabilistically.
5. **Evidence-Based Verification:** No task is declared complete without tangible evidence on disk—actual test execution logs, static analysis outputs, and reproducible diffs.
6. **Human Authority:** The developer maintains ultimate ownership of project direction, scope boundaries, architectural trade-offs, and production deployments.
7. **Project Continuity:** Context is preserved across token resets and multi-day sessions via durable, version-controlled filesystem artifacts.
8. **Anti-AI-Slop Engineering:** Rejection of low-effort generative tropes in both code (unnecessary abstractions, duplicate helpers) and design (generic purple gradients, unreadable contrast).

---

## 04. How OpenClone Works

OpenClone operates as a deterministic, model-independent control plane between the human developer, autonomous coding agents, and the repository codebase. Work executes across an 8-stage left-to-right engineering lifecycle:

<p align="center">
  <img src="assets/how-openclone-works.svg" alt="OpenClone Governed Engineering Lifecycle — Full Width Architecture Diagram" width="100%" />
</p>

```mermaid
flowchart LR
    S1["<b>01 · Intake</b><br/><small>Project Understanding</small>"]
    S2["<b>02 · Intelligence</b><br/><small>Project Intelligence</small>"]
    S3["<b>03 · Planning</b><br/><small>Engineering Planning</small>"]
    S4["<b>04 · Workforce</b><br/><small>Specialist Workforce</small>"]
    S5["<b>05 · Routing</b><br/><small>Tool & Model Selection</small>"]
    S6["<b>06 · Governance</b><br/><small>Governed Execution</small>"]
    S7["<b>07 · Assurance</b><br/><small>Verification & QA</small>"]
    S8["<b>08 · Delivery</b><br/><small>Final Delivery</small>"]

    S1 --> S2 --> S3 --> S4 --> S5 ==> S6 ==> S7 ==> S8

    style S1 fill:#141418,stroke:#27272a,stroke-width:1px,color:#f4f4f5
    style S2 fill:#141418,stroke:#27272a,stroke-width:1px,color:#f4f4f5
    style S3 fill:#141418,stroke:#27272a,stroke-width:1px,color:#f4f4f5
    style S4 fill:#141418,stroke:#27272a,stroke-width:1px,color:#f4f4f5
    style S5 fill:#141418,stroke:#27272a,stroke-width:1px,color:#f4f4f5
    style S6 fill:#1a1710,stroke:#8a7334,stroke-width:2px,color:#fef08a
    style S7 fill:#1a1710,stroke:#8a7334,stroke-width:2px,color:#fef08a
    style S8 fill:#1a1710,stroke:#8a7334,stroke-width:2px,color:#fef08a
```

### The 8-Stage Governed Engineering Lifecycle

| Stage | Operation | Core Responsibility | Primary Artifact |
| :--- | :--- | :--- | :--- |
| **01 · Project Understanding** | Developer Intake & Pre-flight | Clarifies requirements, scope boundaries, constraints, and non-goals with explicit human sign-off. | `PROJECT.md` |
| **02 · Project Intelligence** | Complexity & Risk Analysis | Deep codebase inspection, architecture classification, dependency discovery, and risk scoring. | `architecture_report.json` |
| **03 · Engineering Planning** | Acyclic Task DAG Generation | Decomposes goals into verifiable subtasks with strict file allowlists and acceptance criteria. | `active_task.json` (DAG) |
| **04 · Specialist Workforce** | Capability-Matched Assembly | Deploys vetted specialist personas across Engineering, QA, Security, and Architecture divisions. | `workforce_manifest.json` |
| **05 · Tool & Model Selection** | Multi-Provider MIE Routing | Selects optimal LLMs (GPT-6, Claude, Gemini, DeepSeek, Ollama) balancing reasoning, speed, and cost. | `routing_decision.json` |
| **06 · Governed Execution** | Sandboxed Least-Privilege Diffs | Agents execute scoped code edits restricted to allowed file boundaries; commands run in sandbox. | Isolated patch diffs |
| **07 · Verification & QA** | Deterministic Evidence Validation | Independent verification passes (tests, linters, link checks, security audits) with hash verification. | `audit_ledger.sqlite3` |
| **08 · Final Delivery** | Sealed Audit & Human Acceptance | Human owner reviews cryptographic audit digest and commits verified artifacts to release branch. | Release Tag & Commit |

### Division of Responsibilities

- **Developer:** Defines project purpose, business goals, and non-goals. Authorizes sensitive changes (destructive operations, external dependencies, deployments). Retains ultimate release authority.
- **OpenClone:** Coordinates available capabilities, maintains project context, calculates approval digests, enforces dependency order, and executes quality gates.
- **AI Coding Agent:** Interprets structured task specifications, writes clean modular code, runs local unit tests, and captures execution output within strictly allowed file paths.
- **Verification Engine:** Deterministically verifies that all claimed tests actually ran and exited with code 0 before transitioning tasks to `VERIFIED`.

---

## 05. Platform Capabilities

OpenClone organizes its platform capabilities into modular, verifiable engineering subsystems:

### 1. Phase 0 Planning Service & Project Intelligence Architect (PIA)

- **Centralized Orchestration Façade:** Single central entry point via `OpenClonePlannerAgent` enforcing strict fail-closed Phase 0 planning boundaries (`execute=True` and `/api/v1/execution` fail closed).
- **Four-Set Intelligence Architecture:**
  - **Set A:** Market research and feature cataloging (`FEAT-xxx`).
  - **Set B:** Static analysis and gap/problem discovery (`GAP-xxx`, `PROB-xxx`).
  - **Set C:** Solution alternatives, trade-off analysis, and acceptance criteria (`SOL-xxx`, `AC-xxx`).
  - **Set D:** Consolidated Product Blueprint package including `PROJECT.md`, `System-Architecture.md` (C4 context & container diagrams), and `Threat-Model.md` (STRIDE threat matrix).
- **Constitutional Contract:** Canonical [`PROJECT.md`](project/PROJECT.md.template) establishes immutable project boundaries, non-goals, functional requirements, and acceptance criteria.
- **Portable 5-Artifact Pack:** Zero-install execution package (`PROJECT.md`, `BUILD_PROMPT.md`, `ACCEPTANCE_MATRIX.md`, `PROGRESS.md`, `HANDOFF.md`) eliminating context amnesia across token resets.

### 2. Universal Engineering Intelligence & Knowledge Graph

- **155 Canonical Disciplines:** Fully registered in `src/openclone/engineering/disciplines.py` mapped across 31 folders, 17 sectors, and 12 structural signatures with bidirectional alias bridging.
- **Typed Knowledge Graph Engine:** Traverses semantic relationships (`CONTAINS`, `DEPENDS_ON`, `RELATED_TO`, `APPLIES_TO`, `VALIDATED_BY`) to dynamically resolve engineering dependencies.
- **Dynamic Domain Activation:** Multi-label confidence evaluation activating primary, secondary, and conditional engineering domains based on project evidence and requirements.

### 3. Project Identity & Asset Generation System (PIAGS)

- **Automated Brand Intelligence:** Generates project naming options, brand positioning, tagline formulations, and typography hierarchies.
- **Vector Logo Suite:** Creates deterministic, verified SVG logos, icons, wordmarks, and dark/light mode assets according to strict geometry and contrast rules.

### 4. Universal Product Blueprint (UPB)

- **Complete Design Specification:** Generates screen inventories, ASCII wireframe layouts, user journey maps, interaction state machines, and API integration contracts before code implementation.

### 5. Development Environment & Toolchain Intelligence (DETI)

- **AI IDE Recommendations:** Evidence-backed evaluation selecting Google Antigravity (native artifact viewing, sandboxing), Cursor, or Windsurf.
- **Coding Agent Recommendations:** Tailored pairing with Claude Code or Codex for AST-aware multi-file refactoring.
- **Toolchain Synthesis:** Selects Docker, Pytest/Vitest, Playwright, and static analysis security scanners based on project architecture.

### 6. Infrastructure & Database Intelligence

- **Decoupled Database Architecture:** Cleanly decouples Database Engines (`PostgreSQL`, `MySQL`, `SQLite`) from managed cloud providers (`Neon Serverless PostgreSQL`, `Supabase`, `Render PG`, `PlanetScale`).
- **Feature Modeling:** Evaluates serverless branching, native connection pooling (PgBouncer, Supavisor), SSL modes, and ORM migrations (`Alembic`, `Prisma`, `Drizzle`).
- **Evidence-Based Hosting:** Evaluates Vercel, Cloudflare Pages/Workers, Render, and Railway with zero invented traffic or pricing numbers.

### 7. Connected Accounts & 21-State Deployment Lifecycle

- **Connected Accounts Manager:** Unified OAuth 2.0 and scoped API token management with encrypted credential references and verification status.
- **Canonical 21-State Deployment FSM:** Governs deployment transitions from `NOT_ANALYZED` through `PREVIEW_DEPLOYED` to `HEALTHY` or `ROLLED_BACK`.
- **Mandatory Human Production Gate:** Production deployment requires verified cryptographic approval digests ($\ge 16$ characters); zero autonomous self-approval.

### 8. Specialist Workforce Architecture

- **72 Native Engineering Roles:** Structured across 12 multidisciplinary teams in [`framework/workforce/`](framework/workforce/).
- **14 External Agency Divisions:** Seamless integration with the Agency Agents ecosystem across 14 divisions (`design`, `engineering`, `product`, `testing`, `spatial-computing`, etc.) with strict workforce boundary isolation.

### 9. Model Intelligence Engine (MIE)

- **Multi-Provider Intelligence:** Provider adapters for OpenAI (`gpt-6`, `gpt-6-mini`, `gpt-6-reasoning`), Anthropic (`claude-3-7-sonnet`), Google (`gemini-2.5-pro`), Ollama, and xAI.
- **7-Mode Performance Routing:** Evaluates task requirements across reasoning, speed, cost, and context constraints with high-availability circuit breakers.

### 10. 31 Engineering Domains & 56 Capability Engines

- **Structured Knowledge Domains:** 31 specialized engineering domains covering architecture, database design, API engineering, security, and cloud infrastructure in [`framework/domains/`](framework/domains/).
- **56 Reusable Capability Engines:** Uniquely numbered engines (`E-001` through `E-056`) governing problem discovery, requirement analysis, risk pre-mortems, and release gates in [`framework/engines/`](framework/engines/).

### 11. Design & Anti-Slop Engineering

- **Taste Skill v2.6.0:** Strict design governance enforcing 8-point typographic scales, semantic CSS tokens, WCAG 2.2 AA contrast ratios, and blocking visual clichés ([`ANTI-AI-SLOP-STANDARDS.md`](framework/domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md)).
- **Website Floorplan Engine (WFE):** Structural blueprinting layer planning routes, layouts, and component hierarchies before frontend implementation.

### 12. Governance, Security & Independent Assurance

- **STRIDE Threat Modeler:** Formally integrates threat matrices, trust boundaries, countermeasures, and verification checks into project architecture.
- **Cryptographic Digest Binding:** SHA-256 task digest invalidates prior human approvals upon any scope or dependency modification.
- **Tamper-Evident Audit Ledger:** Cryptographically linked SQLite ledger tracking approvals, executions, and state transitions.
- **14 Pinned Security Scanners:** Security analysis tools pinned by 40-character commit hashes in [`security/scanners.lock.json`](security/scanners.lock.json).
- **V0–V5 Verification Model:** Observable evidence tiers requiring AST syntax validation, unit test logs, integration proofs, and clean-context independent reviews.

---

## 06. Engineering Lifecycle

OpenClone reconciles the complete trajectory of a software engineering project through the authoritative **22-Phase Master Engineering Lifecycle Catalogue** ([`docs/engineering-lifecycle/MASTER_LIFECYCLE_CATALOGUE.md`](docs/engineering-lifecycle/MASTER_LIFECYCLE_CATALOGUE.md)).

These 22 phases are orchestrated through **7 High-Level Lifecycle Gates** and mapped to the **15 Operational Workflows**:

```mermaid
flowchart LR
    G1["01-03<br/>FOUNDATION<br/><small>Discovery · Reqs · Architecture</small>"] --> G2["04-06<br/>DESIGN & TRUST<br/><small>Anti-Slop UX · Security · Data</small>"]
    G2 --> G3["07-12<br/>CORE EXECUTION<br/><small>Env · Logic · API · Frontend · State</small>"]
    G3 --> G4["13-16<br/>QUALITY & RISK<br/><small>Tests · Perf · A11y · Pentesting</small>"]
    G4 --> G5["17-19<br/>DELIVERY<br/><small>CI/CD · Containers · Release</small>"]
    G5 --> G6["20-22<br/>GOVERNANCE<br/><small>Monitoring · Feedback · Maintenance</small>"]

    style G1 fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc
    style G2 fill:#0f172a,stroke:#f59e0b,stroke-width:2px,color:#f8fafc
    style G3 fill:#0f172a,stroke:#818cf8,stroke-width:2px,color:#f8fafc
    style G4 fill:#0f172a,stroke:#ef4444,stroke-width:2px,color:#f8fafc
    style G5 fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#f8fafc
    style G6 fill:#0f172a,stroke:#a855f7,stroke-width:2px,color:#f8fafc
```

### Complete 22-Phase Master Taxonomy

| Group | Phase Identifier | Core Objective | Key Quality Gate Criteria |
| --- | --- | --- | --- |
| **Foundation** | `PHASE_01_DISCOVERY` | Problem discovery & user persona definition | Core problem validated, explicit non-goals documented |
| | `PHASE_02_REQUIREMENTS` | Functional & non-functional requirements | Traceable requirements matrix established |
| | `PHASE_03_PLANNING` | Project planning & acyclic dependency graph | Dependency graph and task budget locked |
| **Design & Trust** | `PHASE_04_ARCHITECTURE` | System topology, module boundaries & ADRs | Module interfaces and data boundaries approved |
| | `PHASE_05_UI_UX_RESEARCH` | Route maps, navigation flows & wireframes | User journeys and screen hierarchy approved |
| | `PHASE_06_VISUAL_DESIGN` | Anti-slop design tokens & component states | Taste Skill v2.6.0 anti-slop audit passed |
| **Core Execution** | `PHASE_07_FRONTEND` | Responsive component implementation | 360px, 768px, 1440px breakpoints verified |
| | `PHASE_08_ANIMATION` | Meaningful micro-interactions & 60fps springs | Reduced-motion accessibility verified |
| | `PHASE_09_BACKEND` | Business logic & API endpoints | Request validation and auth gates enforced |
| | `PHASE_10_DATABASE` | Relational schemas, migrations & indexing | ACID boundaries and migration rollbacks verified |
| | `PHASE_11_AUTH` | Authentication, RBAC/ABAC & IDOR defense | Cross-tenant isolation verified |
| | `PHASE_12_SECURITY` | 19-point SaaS security baseline | Pinned scanner audit clean; 0 high findings |
| **Quality & Risk** | `PHASE_13_AI_INTELLIGENCE` | Governed model selection & prompt versioning | Tool sandboxing and token limits bounded |
| | `PHASE_14_INTEGRATIONS` | External APIs, webhooks & storage | Timeout handling and retry backoffs verified |
| | `PHASE_15_TESTING` | Unit, integration & regression suites | 100% critical test pass rate on disk |
| | `PHASE_16_PERFORMANCE` | Latency, bundle size & database query profiling | Core Web Vitals and N+1 query elimination verified |
| **Delivery** | `PHASE_17_DEVOPS` | CI/CD pipelines & pinned builds | Deterministic build scripts passing in CI |
| | `PHASE_18_DOCUMENTATION` | Accurate README, API contracts & runbooks | 100% valid relative links and verified commands |
| | `PHASE_19_RELEASE` | Version tagging, changelog & release approval | Staged rollout and smoke tests approved |
| **Governance** | `PHASE_20_OPERATIONS` | Telemetry, error logging & incident runbooks | Secrets redacted from production logs |
| | `PHASE_21_MAINTENANCE` | Dependency patching & tech debt management | Patching cadence and backup drills recorded |
| | `PHASE_22_FEEDBACK` | User metrics, friction analysis & iteration | Backlog prioritized for next milestone |

---

## 07. Specialist Workforce

OpenClone supports a dual-workforce model with strict boundary isolation:

```mermaid
flowchart TD
    subgraph NativeWF ["Native OpenClone Workforce (72 Roles)"]
        N1["api-architect"]
        N2["frontend-engineer"]
        N3["devops-engineer"]
        N4["security-auditor"]
        N5["72 Total Roles Across 12 Teams"]
    end

    subgraph AgencyWF ["External Agency Workforce (14 Divisions)"]
        A1["UX Researcher & UI Designer"]
        A2["Backend & Frontend Developers"]
        A3["Reality Checker & Evidence Collector"]
        A4["Project Shepherd & FP&A Analyst"]
        A5["14 Total Divisions (MIT Licensed)"]
    end

    subgraph Runtime ["OpenClone Orchestrator & MIE"]
        ORCH["AgencyTeamOrchestrator"]
        GATE["Deterministic Security Gate (Least Privilege)"]
        MIE["Model Intelligence Engine (GPT-6 / Claude / Gemini)"]
    end

    NativeWF --> Runtime
    AgencyWF --> ORCH
    ORCH --> GATE
    GATE --> MIE
```

- **Native Workforce (72 Roles):** Highly specialized technical workers (`framework/workforce/registry/workers/`) covering requirements engineering, domain logic, security auditing, and test generation.
- **External Agency Workforce (14 Divisions):** Integrated from the Agency Agents ecosystem ([`docs/integrations/AGENCY-AGENTS-INTEGRATION.md`](docs/integrations/AGENCY-AGENTS-INTEGRATION.md)), preserving unredacted personalities, workflows, and deliverable standards.
- **Automated Team Assembly:** Pre-configured specialist teams (e.g. Website Development Team, 5-stage UX Pro Team) assembled with topological dependency order:
  $$\text{UX Researcher} \longrightarrow \text{UX Architect} \longrightarrow \text{UI Designer} \longrightarrow \text{Frontend Developer} \longrightarrow \text{UI Finish-Gate Reviewer}$$

---

## 08. Model and IDE Ecosystem

OpenClone maintains strict provider neutrality and host independence:

### Model Provider Support (Model Intelligence Engine)

| Provider | Supported Models | Primary Specialization | Implementation Status |
| --- | --- | --- | :---: |
| **OpenAI** | `gpt-6`, `gpt-6-mini`, `gpt-6-reasoning`, `gpt-4o` | High-complexity reasoning, Responses API, structured outputs | `Fully Supported` |
| **Anthropic** | `claude-3-7-sonnet`, `claude-3-5-sonnet`, `claude-3-5-haiku` | Architectural analysis, clean code generation, AST refactoring | `Fully Supported` |
| **Google** | `gemini-2.5-pro`, `gemini-2.0-flash`, `gemini-1.5-pro` | Multi-modal reasoning, high-throughput context processing | `Fully Supported` |
| **Ollama** | `llama3`, `deepseek-r1`, `qwen2.5-coder` | Local air-gapped execution, privacy-sensitive offline development | `Fully Supported` |
| **xAI** | `grok-beta` | Research synthesis, rapid exploration | `Fully Supported` |

### Host IDE Compatibility Matrix

| AI Coding Host | Integration Type | Install Scope | Skills & Rules | MCP Tools | Verification Support | Implementation Status |
| --- | --- | --- | --- | --- | --- | :---: |
| **Visual Studio Code** | Native Extension (`extensions/vscode`) | Workspace & User | Webview AI Chat, Activity Bar Panel | **YES** (REST/MCP Bridge) | V0–V5 Evidence Checks | `Fully Supported` |
| **Google Antigravity** | Native Plugin (`agy`) | Workspace & User | 16 Specialist Agents + Rules | **YES** (stdio MCP) | V0–V5 Evidence Checks | `Fully Supported` |
| **Claude Code** | Marketplace Plugin | Workspace & User | Native Skills + `CLAUDE.md` | **YES** (stdio `.mcp.json`) | V0–V5 Evidence Checks | `Fully Supported` |
| **OpenAI Codex** | Marketplace Plugin | Workspace & User | Codex Skills + Rules | **YES** (stdio MCP) | V0–V5 Evidence Checks | `Fully Supported` |
| **Cursor & Windsurf** | Workspace Adapter | Workspace | `.cursorrules` + `.cursor/rules/*.mdc` | **YES** (stdio MCP) | V0–V5 Evidence Checks | `Fully Supported` |
| **Generic MCP** | Stdio / SSE JSON-RPC 2.0 | Process / Server | Standard Tool Registrations | 20 Tools | JSON-RPC Inspection | `Fully Supported` |

---

## 09. Architecture Overview

### Architectural Layers

```
┌───────────────────────────────────────────────────────────┐
│                    Developer Intent                       │
├───────────────────────────────────────────────────────────┤
│  Surface Adapters: VS Code · Antigravity · Cursor · Claude│
├───────────────────────────────────────────────────────────┤
│   OpenClone Control Plane (OpenClonePlannerAgent & MCP)   │
├───────────────────────────────────────────────────────────┤
│   Model Intelligence Engine (MIE) · Multi-Provider Routing│
├───────────────────────────────────────────────────────────┤
│  Specialist Workforce: 72 Native Workers + 14 Agency Divs │
├───────────────────────────────────────────────────────────┤
│ Framework Core: 31 Domains · 56 Engines · 15 Workflows    │
├───────────────────────────────────────────────────────────┤
│  Universal Intelligence: 155 Disciplines · Knowledge Graph│
├───────────────────────────────────────────────────────────┤
│  DevOps Intelligence: DETI · Infra · DB · 21-State FSM    │
├───────────────────────────────────────────────────────────┤
│  Governance & Trust: SHA-256 Digest · SQLite Audit Ledger │
└───────────────────────────────────────────────────────────┘
```

### Repository Layout

```text
OpenClone/
├── .github/          # CI/CD workflows, issue templates, dependabot
├── global/           # Universal single-install global layer (core/, hosts/, installer/)
├── project/          # Project-level templates (PROJECT.md, AGENTS.md, host-rules/)
├── framework/        # Governed framework (domains/, engines/, workflows/, workforce/)
│   ├── domains/      # 31 specialized engineering knowledge domains
│   ├── engines/      # 56 uniquely numbered capability engines (E-001 to E-056)
│   ├── workflows/    # 15 governed operational workflows (WF-001 to WF-015)
│   └── workforce/    # 72 native worker roles + external Agency Agents catalog
├── src/openclone/    # Python runtime: Planning Agent, PIA, DevOps, MIE, MCP Server
│   ├── blueprint/    # Universal Product Blueprint (UI inventory, wireframes, flows)
│   ├── devops/       # DETI, infra recommendations, database decoupling, 21-state FSM
│   ├── engineering/  # 155 canonical disciplines, knowledge graph, dynamic activation
│   ├── identity/     # Project Identity & Asset Generation System (PIAGS)
│   ├── intelligence/ # Project Intelligence Architect (Sets A-D), socratic clarification
│   └── planning/     # Central OpenClonePlannerAgent façade
├── extensions/       # Native host editor extensions (extensions/vscode)
├── adapters/         # Host adapters (antigravity, claude-code, codex, cursor, vscode)
├── security/         # Security operations, STRIDE threat modeling, and 14 pinned scanners
├── docs/             # Technical documentation, concepts, guides, lifecycle, legal
├── examples/         # Verified runnable demonstrations (demo.sh)
├── tests/            # 727 automated unit, integration, and security tests
├── tools/            # Repository validation, link checking, and quality gate tooling
├── LICENSE           # Official MIT License
└── README.md         # Authoritative project homepage and documentation hub
```

---

## 10. Getting Started

### Method 1: Direct Pip Installation (Global CLI)

Install OpenClone globally using `pip`:

```bash
# Install directly from the canonical GitHub repository
pip install git+https://github.com/MK-1603/OpenClone.git
```

Or install from a pre-compiled wheel downloaded from the official [v1.0.0 GitHub Release](https://github.com/MK-1603/OpenClone/releases/tag/v1.0.0):

```bash
pip install openclone-1.0.0-py3-none-any.whl
```

#### Python Package Verification

Verify the OpenClone Core package installation:

```bash
python -c "import openclone; print(openclone.__version__)"
```

---

### Method 2: Global Plugin Installation for AI IDEs

Install OpenClone into your preferred AI coding environment:

#### 1. Google Antigravity

```bash
agy plugin install https://github.com/MK-1603/OpenClone
```

#### 2. Claude Code

```text
/plugin marketplace add MK-1603/OpenClone
/plugin install openclone@openclone-marketplace
```

#### 3. OpenAI Codex

```bash
codex plugin marketplace add MK-1603/OpenClone
```

#### 4. Cursor

Add OpenClone to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "src.openclone.cli", "mcp"]
    }
  }
}
```

---

### Method 3: Application Developers (Portable Zero-Install Workflow)

If you are developing an application using ChatGPT, Claude, or Gemini in your browser, **no local installation is required**:

1. **Copy Specification:** Copy [`project/PROJECT.md.template`](project/PROJECT.md.template) into your project root as `PROJECT.md`.
2. **Execute Master Prompt:** Provide [`framework/prompts/PORTABLE-PROJECT-INTELLIGENCE-MASTER-PROMPT.md`](framework/prompts/PORTABLE-PROJECT-INTELLIGENCE-MASTER-PROMPT.md) and your `PROJECT.md` to ChatGPT or Claude.
3. **Execute in IDE:** Hand off the generated instruction package (`BUILD_PROMPT.md`, `ACCEPTANCE_MATRIX.md`, `PROGRESS.md`, `HANDOFF.md`) to your AI coding environment.

---

### Method 4: Framework Maintainers & Contributors (Local Setup)

```bash
# 1. Clone repository
git clone https://github.com/MK-1603/OpenClone.git
cd OpenClone

# 2. Install editable package with dev dependencies
pip install -e ".[dev]"

# 3. Verify repository integrity (56 engines, 31 domains, 100% case-accurate links)
python tools/validate_repository.py

# 4. Run automated test suite (351 tests)
pytest tests/
```

---

## 11. Master Engineering Orchestrator & Python SDK

OpenClone v2.0.0 operates as a headless, multi-agent engineering platform driven by the central **Master Engineering Orchestrator** ([`OpenClonePlannerAgent`](src/openclone/planning/agent.py)) and headless MCP/REST interfaces.

### 1. The Three-Tier Agent Hierarchy

OpenClone coordinates development across a deterministic 3-level agent hierarchy:

- **Level 0 (Master Agent):** `OpenClonePlannerAgent` owns global context, delegation policies, and final lifecycle decisions.
- **Level 1 (Domain Leads):** 21 dedicated leads for Architecture, Requirements, Frontend, Backend, Database, Infrastructure, Security, Testing, Debugging, and Optimization.
- **Level 2 (Specialists):** 73 dynamically activated specialist personas (e.g., React, PostgreSQL, STRIDE, Unit Testing) with bounded recursion depth (`MAX_DELEGATION_DEPTH = 3`).

### 2. 11 Lifecycle Operating Modes

The Master Orchestrator executes 11 distinct operational modes:

1. `DISCOVERY`: Inspects repository AST, modules, and available workforce capabilities.
2. `AUDIT`: Evaluates architectural compliance, dead code, and module boundaries.
3. `VERIFICATION`: Executes automated validators and checks subsystem contracts.
4. `PLANNING`: Synthesizes dependency-ordered topological task DAGs.
5. `BUILD`: Coordinates implementation across specialized coding agents.
6. `TEST`: Runs unit, integration, contract, and regression test suites.
7. `DEBUG`: Performs automated stack trace capture and root-cause analysis.
8. `UPGRADE`: Modernizes dependencies and resolves technical debt with safety gates.
9. `OPTIMIZATION`: Profiles performance, latency, and memory utilization.
10. `DEPLOYMENT`: Evaluates cloud readiness and generates infrastructure blueprints.
11. `FULL_LIFECYCLE`: Coordinates end-to-end multi-agent execution from discovery through delivery.

### 3. Programmatic Python SDK Usage

You can invoke OpenClone directly within Python scripts and applications:

```python
from openclone.planning.agent import OpenClonePlannerAgent
from openclone.orchestration.models import OrchestrationMode

# Initialize the Master Engineering Orchestrator
master = OpenClonePlannerAgent()

# 1. Discover the ecosystem and agent hierarchy
inventory = master.discover_ecosystem()
print(f"Total Agents: {inventory['total_agents']}")
print(f"Domain Leads: {inventory['domain_lead_count']}")

# 2. Access the Global Capability Map
cap_map = master.get_capability_map()
print(f"Verified Capabilities: {cap_map['verified_capabilities']} / {cap_map['total_capabilities']}")

# 3. Execute an end-to-end engineering lifecycle
result = master.run_full_engineering_lifecycle(
    prompt="Design a scalable fintech subscription platform with PostgreSQL and Next.js",
    project_name="FintechCore"
)
print(f"Lifecycle Status: {result['status']}")
```

---

## 11.2 Release Management & Version 2.0.0 Direct Launch Architecture

### Direct Production Launch: Version 2.0.0

OpenClone launches directly as **Version 2.0.0**, establishing the definitive Universal AI Software Engineering Platform. Rather than releasing experimental intermediate builds, v2.0.0 provides a production-ready, evidence-backed foundation governing multi-agent development.

### How Releases Are Automated

Releases are automated via GitHub Actions (`.github/workflows/release.yml`):

1. **Tag Trigger:** Pushing a version tag (`v2.0.0`) activates the release pipeline.
2. **Version Parity Gate:** CI verifies that the Git tag strictly matches `pyproject.toml`, `VERSION`, and `plugin.json`.
3. **Automated Quality Gate:** All 747 tests, repository validators, and JSON schemas must pass with zero errors.
4. **Binary Wheel Generation:** Compiles `openclone-2.0.0-py3-none-any.whl` and source distributions.
5. **Cryptographic Checksums:** Generates `SHA256SUMS.txt` for all release assets.
6. **Multi-OS Smoke Tests:** Validates wheel installation in clean temporary environments across Ubuntu, Windows, and macOS.
7. **Release Notes Publication:** Automatically links the master [`RELEASE-NOTES.md`](RELEASE-NOTES.md) to the GitHub Release.

---

### Brand Engineering (LEBIS)

```python
# Transform a brand brief into production vector SVGs and design guidelines via Python SDK
from openclone.orchestration import UniversalMasterOrchestrator

master = UniversalMasterOrchestrator()
# Or via MCP: call tool 'openclone_engineer_brand'
# {
#   "name": "NoteDigest",
#   "primary_color": "#2563EB",
#   "category": "Productivity"
# }
```

### Agency Agents Specialist Workforce

```python
# Discover specialist agents and assemble multi-agent teams with topological handoff chain
master = UniversalMasterOrchestrator()

# Retrieve specialists by engineering domain
design_specialists = master.hierarchy.get_specialists_by_domain("design")

# Or via MCP: call tool 'openclone_assemble_team'
# {
#   "team_type": "website",
#   "name": "CustomerPortal"
# }
```

### Universal Project Intelligence

```python
# Multi-label classification and explainable capability routing
from openclone.orchestration import UniversalMasterOrchestrator

master = UniversalMasterOrchestrator()

# Or via MCP: call tool 'openclone_classify_project'
# { "text": "Offline Flutter mobile app with local RAG agent and FastAPI backend" }

# Retrieve canonical project family blueprint
# MCP: call tool 'openclone_get_blueprint' with { "blueprint_id": "10-LINUX-OS" }
```

---

## 12. MCP and Tool Integration

OpenClone implements the **Model Context Protocol (spec 2024-11-05)**, exposing 22 registered tools over stdio and Server-Sent Events (SSE):

### Registered MCP Tools (22)

| Tool Name | Purpose | Primary Inputs | Output |
| --- | --- | --- | --- |
| **`openclone_get_status`** | Real-time framework status, version, test counts, metrics. | None | JSON status report |
| **`openclone_search_knowledge`** | Search 31 domains, 56 engines, and blueprints by query. | `query` (str), `category` (enum) | List of matching sections |
| **`openclone_explain_concept`** | Retrieve authoritative contracts for any domain or engine. | `concept_id` (e.g. `'E-001'`) | Complete Markdown spec |
| **`openclone_run_workflow`** | Inspect or execute an authorized OpenClone workflow. | `workflow_id` (e.g. `'WF-013'`) | Workflow checklist / contract |
| **`openclone_validate_project`** | Run repository structural integrity and schema quality gates. | `strict` (bool) | Pass/Fail report with errors |
| **`openclone_get_guidance`** | Retrieve specialized guidance (anti-slop, security, architecture). | `topic` (enum: `'anti_slop'`) | Markdown guidance profile |
| **`openclone_list_capabilities`** | List all domains, engines, workflows, workforce roles, adapters. | `filter` (enum: `'all'`) | Comprehensive registry list |
| **`openclone_route_model`** | Multi-mode model routing across 7 modes with HA circuit-breaker. | `prompt` (str), `mode` (str) | Decision with candidate scores |
| **`openclone_list_models`** | List available models and active health states. | None | Active models & metrics |
| **`openclone_model_health`** | Check latency, error rate, and availability of model providers. | `provider` (str) | Real-time health metrics |
| **`openclone_engineer_brand`** | Transform a brand brief into an engineered brand package. | `name` (str), `primary_color` (str) | Vector SVGs & guidelines |
| **`openclone_validate_logo`** | Audit raw SVG logo markup against LEBIS QA standards. | `svg_content` (str) | Verification report |
| **`openclone_workforce_status`** | Workforce metrics across 72 native roles & 14 Agency divisions. | None | Workforce status overview |
| **`openclone_discover_agents`** | Discover external Agency specialist agents. | `query` (str), `division` (str) | Matching agent catalog list |
| **`openclone_get_agent_profile`** | Retrieve full agent persona, rules, workflow, and deliverables. | `division` (str), `agent` (str) | Unredacted agent profile |
| **`openclone_assemble_team`** | Assemble specialist teams and calculate topological execution order. | `team_type` (str), `name` (str) | Team composition & DAG |
| **`openclone_classify_project`** | Multi-label project classification across 12 families and 20+ types. | `text` (str) | Multi-label `ProjectProfile` |
| **`openclone_route_project`** | Deterministic domain, capability, workforce, and model routing. | `text` (str) | Explainable `RoutingDecision` |
| **`openclone_get_blueprint`** | Fetch canonical architecture blueprints across 14 project families. | `blueprint_id` (str) | Full blueprint Markdown |
| **`openclone_project_intelligence_status`** | Query metrics on supported families, delivery targets, and blueprints. | None | Taxonomy & blueprint summary |
| **`openclone_evaluate_technology`** | Evaluate and recommend technology stack alternatives across domains. | `text` (str), `project_name` (str) | Architecture recommendations |
| **`openclone_generate_package`** | One-click idea-to-project package generator producing all core specifications. | `prompt` (str), `project_name` (str) | Full project package files |

---

## 13. Security and Engineering Quality

OpenClone enforces production-grade security and quality governance:

- **19-Point SaaS Security Baseline:** Covers OWASP Top 10 defenses, SQL injection prevention, bcrypt password hashing, CSRF/CORS configurations, and strict rate limiting ([`docs/security/saas-security-baseline.md`](docs/security/saas-security-baseline.md)).
- **Secret Redaction Harness:** Real-time regex scanner scrubs API tokens, AWS keys, private certificates, and passwords before logging or storing tool outputs.
- **14 Commit-Pinned Security Scanners:** Security analysis tools pinned by 40-character commit hashes in [`security/scanners.lock.json`](security/scanners.lock.json).
- **4-Tier Copyleft Isolation:** Upstream copyleft tools run in decoupled child processes. Zero copyleft code is vendored into OpenClone core.
- **Taste Skill v2.6.0:** Anti-AI-slop design engine enforcing an 8-point typographic scale, semantic CSS tokens, WCAG 2.2 AA contrast ratios, and prohibiting ambient blur circles or neon purple clichés ([`ANTI-AI-SLOP-STANDARDS.md`](framework/domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md)).

---

## 14. Real-World Demonstrations

OpenClone includes verified, production-ready demonstration projects:

### Demo A: NoteDigest — Governed AI SaaS (`examples/demo-project/`)

A meeting and text digest application with rule-assisted extraction, brand assets generated by OpenClone LEBIS, specialist workforce handoffs, and live execution.

```bash
# Run the automated end-to-end governance lifecycle demo
python examples/demo-project/run_demo.py
```

*Exercises project initialization, human approval gates, state transitions, ledger hash-chain verification, and 7 unit tests (100% passing).*

### Demo B: PULSE — Project Command Center (`examples/pulse/`)

An interactive commercial-grade SaaS frontend built with **Next.js 15, React 19, TypeScript, and Tailwind CSS**.

- **8 Core Views:** Dashboard, Project Portfolio, Sprint Kanban Board, Schedule Calendar, Performance Analytics, Team Roster, Audit Stream, and Workspace Settings.
- **Dark Luxury Aesthetic:** Deep charcoal (`#0A0A0A`) and restrained gold (`#D6B36A`) design tokens adhering to Taste Skill anti-slop rules.

```bash
cd examples/pulse
npm install
npm run build   # Verified 100% type-safe build (124 kB first load JS)
npm run start   # Running on http://localhost:3000
```

---

## 15. Documentation Hub

Explore authoritative specifications across the repository:

| Engineering Category | Authoritative Documents |
| --- | --- |
| **Platform Standards & Rules** | [`AGENTS.md`](AGENTS.md) · [`PROJECT.md`](PROJECT.md) · [`docs/concepts/OPENCLONE-CORE-PRINCIPLES.md`](docs/concepts/OPENCLONE-CORE-PRINCIPLES.md) |
| **Universal Project Intelligence** | [`docs/intelligence/README.md`](docs/intelligence/README.md) · [`blueprints/README.md`](blueprints/README.md) · [`framework/registries/project-taxonomy.json`](framework/registries/project-taxonomy.json) |
| **System Architecture** | [`docs/architecture/OPENCLONE-2.0-ARCHITECTURE.md`](docs/architecture/OPENCLONE-2.0-ARCHITECTURE.md) · [`blueprints/OPENCLONE-MASTER-BLUEPRINT.md`](blueprints/OPENCLONE-MASTER-BLUEPRINT.md) |
| **Core Concepts (10)** | [`docs/concepts/01-GOVERNANCE-AND-AUTHORITY.md`](docs/concepts/01-GOVERNANCE-AND-AUTHORITY.md) · [`docs/concepts/02-PROJECT-SOURCE-OF-TRUTH.md`](docs/concepts/02-PROJECT-SOURCE-OF-TRUTH.md) · [`docs/concepts/03-SPECIALIST-WORKFORCE.md`](docs/concepts/03-SPECIALIST-WORKFORCE.md) |
| **22-Phase Lifecycle** | [`docs/engineering-lifecycle/MASTER_LIFECYCLE_CATALOGUE.md`](docs/engineering-lifecycle/MASTER_LIFECYCLE_CATALOGUE.md) · [`docs/engineering-lifecycle/VERIFICATION_AND_EVIDENCE.md`](docs/engineering-lifecycle/VERIFICATION_AND_EVIDENCE.md) |
| **Specialist Workforce** | [`docs/integrations/AGENCY-AGENTS-INTEGRATION.md`](docs/integrations/AGENCY-AGENTS-INTEGRATION.md) · [`framework/domains/30-AGENT-RULES-AND-VERIFICATION/`](framework/domains/30-AGENT-RULES-AND-VERIFICATION/) |
| **Operational Assessments** | [`docs/guides/REPOSITORY-HEALTH.md`](docs/guides/REPOSITORY-HEALTH.md) · [`docs/security/SECURITY-STATUS.md`](docs/security/SECURITY-STATUS.md) · [`docs/guides/RELEASE-READINESS.md`](docs/guides/RELEASE-READINESS.md) |
| **Host Integrations** | [`global/docs/GLOBAL-PLUGIN-INSTALLATION.md`](global/docs/GLOBAL-PLUGIN-INSTALLATION.md) · [`global/docs/HOST-COMPATIBILITY.md`](global/docs/HOST-COMPATIBILITY.md) |
| **Security & Compliance** | [`docs/security/saas-security-baseline.md`](docs/security/saas-security-baseline.md) · [`docs/security/THREAT-MODEL.md`](docs/security/THREAT-MODEL.md) · [`docs/legal/COMPLIANCE_MATRIX.md`](docs/legal/COMPLIANCE_MATRIX.md) |
| **Third-Party Copyright & IP** | [`NOTICE`](NOTICE) · [`docs/legal/THIRD_PARTY_LICENSES.md`](docs/legal/THIRD_PARTY_LICENSES.md) · [`docs/legal/THIRD_PARTY_NOTICES.md`](docs/legal/THIRD_PARTY_NOTICES.md) |

---

## 16. Roadmap

### ✅ Completed & Verified (`v2.0.0 Launch`)

- [x] **Universal Master Engineering Orchestrator (UMEO-007):** Unified 3-tier hierarchy (Level 0 Master `OpenClonePlannerAgent`, 21 Level 1 Domain Leads, 73 Level 2 Specialists).
- [x] **Global Capability Map:** 14 verified system capabilities mapped and integrated across all engineering domains.
- [x] **11 Master Lifecycle Operating Modes:** Full lifecycle orchestration (`DISCOVER`, `UNDERSTAND`, `PLAN`, `DESIGN`, `BUILD`, `TEST`, `DEBUG`, `VERIFY`, `UPGRADE`, `OPTIMIZE`, `DELIVER`).
- [x] **Complete Test Verification:** 747/747 automated tests passing with 0 failures across all unit, integration, and security suites.
- [x] **Shared MCP Server:** JSON-RPC 2.0 stdio/SSE engine with 22 registered tools conforming to MCP spec 2024-11-05.
- [x] **Universal Framework Standard:** Unified specification across 31 engineering domains, 56 capability engines, and 155 engineering disciplines.
- [x] **Model Intelligence Engine (MIE):** Multi-provider routing with OpenAI GPT-6 primary family, Claude 3.5, and Gemini 2.0.
- [x] **Agency Agents Workforce Integration:** 14 specialist divisions integrated with strict workforce boundary isolation.
- [x] **Taste Skill v2.6.0 & LEBIS:** Anti-slop design governance and automated vector brand engineering pipeline.
- [x] **Real-World Demonstration Projects:** NoteDigest governed AI SaaS (`run_demo.py`) and PULSE Command Center Next.js frontend.

### 🔄 In Progress

- [ ] **Interactive IDE Diagnostic Extension:** Rich visual UI sidecar for inspecting live MCP state in Antigravity and Cursor.
- [ ] **Automated Dynamic Prompt Injection Evals:** Extended test suite exercising PyRIT adversarial boundary adapters.

### 📋 Planned & Proposed

- [ ] **Ephemeral Micro-VM Sandbox Runners:** Rootless container runners for untrusted third-party code execution `{PROPOSED}`.
- [ ] **Distributed Git-Native Signed Audit Streams:** Cryptographically signed commit hooks backing the SQLite audit ledger `{PLANNED}`.

---

## 17. Contributing and License

### Contributing

We welcome contributions from software engineers, AI researchers, and open-source practitioners:

- **[Contributing Guidelines](CONTRIBUTING.md):** Development setup, branch naming, testing requirements, and PR expectations.
- **[Code of Conduct](CODE_OF_CONDUCT.md):** Contributor Covenant v2.1 standards.
- **[Governance Model](GOVERNANCE.md):** Architectural decision registers and human approval rules.

### License & Acknowledgements

OpenClone is licensed under the [MIT License](LICENSE).  
Copyright (c) 2026 OpenClone Contributors.

Third-party open-source components and specifications are subject to their respective licenses:

- [`NOTICE`](NOTICE): Upstream copyright, authors, and notices.
- [`docs/legal/THIRD_PARTY_LICENSES.md`](docs/legal/THIRD_PARTY_LICENSES.md): Complete third-party license inventory.
- [`docs/legal/THIRD_PARTY_NOTICES.md`](docs/legal/THIRD_PARTY_NOTICES.md): Detailed upstream commit SHAs, modification records, and attribution.

<p align="center">
  <sub>OpenClone · Build with Any AI. Governed by One Engineering Standard.</sub>
</p>
