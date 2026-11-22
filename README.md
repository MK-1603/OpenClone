<p align="center">
  <img src="assets/openclone-wordmark.svg" alt="OpenClone Universal AI Software Engineering Framework" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/MK-1603/OpenClone/releases" title="Version 1.0.0"><img src="https://img.shields.io/badge/version-1.0.0-38bdf8?style=flat&logo=github&logoColor=white" alt="Version 1.0.0" /></a>
  &nbsp;
  <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.10%2B-10b981?style=flat&logo=python&logoColor=white" alt="Python 3.10+" /></a>
  &nbsp;
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-6366f1?style=flat" alt="MIT License" /></a>
  &nbsp;
  <a href="tests/"><img src="https://img.shields.io/badge/tests-76%20passed%20%7C%200%20failed-059669?style=flat" alt="76 Passing Tests" /></a>
  &nbsp;
  <a href="security/scanners.lock.json"><img src="https://img.shields.io/badge/security-12%20scanners%20locked-ef4444?style=flat" alt="12 Scanners Locked" /></a>
  &nbsp;
  <a href="adapters/INTEGRATION-MATRIX.md"><img src="https://img.shields.io/badge/mcp-2024--11--05-8b5cf6?style=flat" alt="MCP Protocol 2024-11-05" /></a>
</p>

<p align="center">
  <strong>Provider-Neutral · IDE-Independent · Deterministic Control Plane · Anti-AI-Slop Governance</strong><br />
  <em>Build with Any AI. Governed by One Engineering Standard.</em>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="#multi-ide-and-chatbot-integrations">Multi-IDE & Chatbots</a> ·
  <a href="#mcp-service">Shared MCP Server</a> ·
  <a href="#anti-ai-slop-governance">Anti-Slop UX (Taste Skill)</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="domains/README.md">31 Domains</a> ·
  <a href="workforce/ROLE-CATALOGUE.md">72 Workforce Roles</a> ·
  <a href="blueprints/README.md">27 Master Blueprints</a>
</p>

---

## What is OpenClone?

**OpenClone** (canonical framework standard: **AISDF** — AI Software Development Framework) is an open-source, provider-independent engineering framework and deterministic local control plane for orchestrating complex software engineering with autonomous and human-assisted AI coding agents.

Modern AI models synthesize code at astonishing velocity. Yet real-world engineering is not raw code synthesis: it requires deep problem discovery, immutable requirements, defensive security baselines, reproducible automated test suites, dependency-ordered rollouts, and independent release verification.

Without a unifying engineering control plane, AI development inevitably collapses into **AI Slope**: scope creep, hallucinated passes, unverified claims, unmonitored lateral tool privileges, and prompt injection vulnerabilities.

**OpenClone provides the missing operating system.** It cleanly decouples *engineering governance* from *underlying models or IDEs*. Whether work is executed by **Google Antigravity, Claude Code, Cursor, OpenAI Codex, ChatGPT**, or a human engineer, all changes conform to a single verifiable standard.

---

## Architectural Topology

<p align="center">
  <img src="assets/architecture-topology.svg" alt="OpenClone Architecture Topology" width="100%" />
</p>

---

## The Instruction-First Engineering Lifecycle

OpenClone halts low-quality AI code generation by enforcing a strict seven-phase deterministic lifecycle:

<p align="center">
  <img src="assets/lifecycle-diagram.svg" alt="OpenClone Engineering Lifecycle" width="100%" />
</p>

1. **01 · DISCOVER:** Automatically scans repository context, project guidelines, and inherited rules (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`).
2. **02 · AUDIT SLOP:** Evaluates UI against Taste Skill v2.6.0 anti-slop rules; halts decorative clichés, purple gradients, and floating blur blobs.
3. **03 · SPECIFY:** Establishes testable acceptance criteria (Given/When/Then), design tokens, and structured task contracts.
4. **04 · GATE CHECK:** Binds human approvals cryptographically to the SHA-256 digest of the task specification. Any scope change invalidates approval.
5. **05 · BUILD:** Executes changes within bounded permissions, output redaction, and strict file allow-lists.
6. **06 · VERIFY:** Enforces independent code review in an isolated, clean context ("Goldfish" protocol) with evidence logging.
7. **07 · DEPLOY:** Manages the user application build-to-deployment pipeline (`WF-014`) across 6 cloud platforms with 21 non-reentrant lifecycle states.

---

## What OpenClone Is vs What It Is Not

| OpenClone Is | OpenClone Is Not |
|---|---|
| **A deterministic, self-hostable control plane** enforcing permissions, task graphs, human approvals, and hash-chained audit ledgers. | An LLM model or proprietary model provider. |
| **A universal standard and role catalogue** for 72 specialist engineering roles across 12 teams. | A claim that role prompt contracts equal 72 autonomous general intelligences. |
| **A portable framework** defining 31 engineering domains, 56 capability engines, and 14 executable workflows. | A replacement for your preferred IDE or editor. |
| **A zero-dependency Python 3.10+ reference runtime** (`openclone.py` / `aisdf.py`) using only standard library and SQLite. | An unconstrained shell sandbox (sandboxing requires container or VM isolation). |
| **An evidence-driven verification gate** requiring observable proof before task completion or release. | An automatic pass machine that trusts LLM self-attestation. |

---

<h2 id="multi-ide-and-chatbot-integrations">Multi-IDE & Chatbot Integrations (Model Context Protocol)</h2>

OpenClone exposes its full engineering intelligence through a **Shared Model Context Protocol (MCP) Service** (`src/openclone/mcp/server.py`), allowing seamless integration into any supported coding environment:

<table width="100%">
  <tr>
    <th width="20%">Environment</th>
    <th width="30%">Integration Surface</th>
    <th width="25%">MCP Connection</th>
    <th width="25%">Status</th>
  </tr>
  <tr>
    <td><strong>Google Antigravity</strong></td>
    <td>Native Plugin & Workspace Rules</td>
    <td><code>stdio</code> via <code>plugin.json</code></td>
    <td><img src="https://img.shields.io/badge/status-VERIFIED-10b981?style=flat" alt="Verified" /></td>
  </tr>
  <tr>
    <td><strong>Claude Code</strong></td>
    <td>CLI & Terminal Plugin</td>
    <td><code>stdio</code> via <code>.mcp.json</code></td>
    <td><img src="https://img.shields.io/badge/status-VERIFIED-10b981?style=flat" alt="Verified" /></td>
  </tr>
  <tr>
    <td><strong>Cursor</strong></td>
    <td>Editor Composer & Agent Rules</td>
    <td><code>stdio</code> via <code>.cursor/mcp.json</code></td>
    <td><img src="https://img.shields.io/badge/status-VERIFIED-10b981?style=flat" alt="Verified" /></td>
  </tr>
  <tr>
    <td><strong>OpenAI Codex</strong></td>
    <td>CLI, Desktop & VSCode Extension</td>
    <td><code>stdio</code> via <code>mcp.json</code></td>
    <td><img src="https://img.shields.io/badge/status-VERIFIED-10b981?style=flat" alt="Verified" /></td>
  </tr>
  <tr>
    <td><strong>ChatGPT</strong></td>
    <td>Custom GPT & Remote MCP Gateway</td>
    <td>Remote HTTPS / SSE</td>
    <td><img src="https://img.shields.io/badge/status-DOCUMENTED-38bdf8?style=flat" alt="Documented" /></td>
  </tr>
</table>

### Connect in 30 Seconds

<details>
<summary><strong>Claude Code (<code>.mcp.json</code>)</strong></summary>

Add to your project's `.mcp.json`:
```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "src.openclone.mcp.server"],
      "description": "OpenClone Universal AI Software Engineering Framework MCP Server"
    }
  }
}
```
</details>

<details>
<summary><strong>Cursor (<code>.cursor/mcp.json</code>)</strong></summary>

Add to `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "src.openclone.mcp.server"],
      "description": "OpenClone Universal AI Software Engineering Framework MCP Server"
    }
  }
}
```
</details>

<details>
<summary><strong>Google Antigravity</strong></summary>

Antigravity auto-discovers OpenClone from [`adapters/antigravity/plugin/`](adapters/antigravity/plugin/). Simply open the OpenClone workspace or register the plugin directory with the `agy` CLI.
</details>

<details>
<summary><strong>OpenAI Codex</strong></summary>

Add to `.codex/mcp.json` or project root `mcp.json`:
```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "src.openclone.mcp.server"]
    }
  }
}
```
</details>

<details>
<summary><strong>ChatGPT (Remote MCP / Custom GPT)</strong></summary>

1. Deploy `src/openclone/mcp/server.py` with an HTTPS/SSE gateway (e.g. FastAPI / Cloudflare Worker).
2. Configure authentication using Bearer tokens.
3. Import actions into your Custom GPT using [`adapters/chatgpt/custom-gpt-instructions.md`](adapters/chatgpt/custom-gpt-instructions.md).
</details>

---

<h2 id="mcp-service">Shared MCP Tool Capabilities</h2>

Every connected host gains direct access to the 7 canonical OpenClone tools:

| Tool Name | Action Type | Purpose |
|---|---|---|
| `openclone_get_status` | `Inspection` | Real-time framework status, version, git branch, metrics, and passing test counts. |
| `openclone_search_knowledge` | `Discovery` | Semantic keyword search across 31 domains, 56 engines, 14 workflows, and blueprints. |
| `openclone_explain_concept` | `Knowledge` | Deep documentation and execution contracts for any ID (`E-XXX`, `WF-XXX`, domain). |
| `openclone_run_workflow` | `Orchestration` | Inspects phase checklists and execution prerequisites for workflows. |
| `openclone_validate_project` | `Quality` | Executes repository integrity, schema conformance, and structural validation checks. |
| `openclone_get_guidance` | `Guidance` | Retrieves Taste Skill anti-slop rules, morphism tokens, or application deployment guides. |
| `openclone_list_capabilities` | `Catalog` | Complete directory of domains, engines, workflows, workforce roles, and active adapters. |

---

<h2 id="anti-ai-slop-governance">Anti-AI-Slop Governance (Taste Skill v2.6.0)</h2>

OpenClone integrates **Taste Skill v2.6.0** ([`skills/taste-skill/`](skills/taste-skill/)) as its standard for front-end visual engineering. It directly eliminates the generic "AI aesthetic" by mandating an **Instruction-First, Context-First, Design-First, Code-Second** lifecycle:

- **Static Slop Scanner (`audit-slop.mjs`):** Detects decorative glassmorphism, ambient background blur blobs, neon glows, purple/indigo gradients, and redundant card grids.
- **Pre-Build Gate (`plan-check.mjs`):** Blocks code generation until `.taste-skill/design-plan.md` passes validation (`GATE: READY`), scaling from Level 1 micro-fixes to Level 5 full products.
- **User-Choice Aesthetics Supported ([`05-UX-UI-ENGINEERING/USER-CHOICE-DESIGN-PATTERNS.md`](domains/05-UX-UI-ENGINEERING/USER-CHOICE-DESIGN-PATTERNS.md)):** When explicitly requested, provides complete design tokens and WCAG 2.2 AA backing scrims for:
  - **Glassmorphism:** Frosted translucent surfaces with high-contrast backing scrims (`rgba(15,23,42,0.85)`).
  - **UI Morphism / Neumorphism:** Dual-source soft bevel lighting with tactile inset active states.
  - **Swiss International Style:** Asymmetric grid layout, Inter/Akzidenz-Grotesk typography, high-contrast monochrome.
  - **Industrial Brutalism:** Monospaced type, exposed borders, stark geometry, zero decorative fluff.

---

<h2 id="quick-start">Quick Start in 3 Minutes</h2>

### Prerequisites
- Python 3.10 or higher installed.
- Git installed.
- Zero mandatory external pip packages required for the core control plane!

### Step 1: Clone and Validate

```bash
# Clone the canonical repository
git clone https://github.com/MK-1603/OpenClone.git
cd OpenClone

# Run repository structural validation
python tools/validate_repository.py

# Run the complete automated test suite (63 Python tests + 13 Taste Skill tests = 76 tests)
python -m unittest discover -s tests -v
node skills/taste-skill/tests/test-governance.mjs
```

### Step 2: Launch the Shared MCP Service

```bash
# Start OpenClone MCP server for IDEs
python openclone.py mcp
```

### Step 3: Scaffold a Governed User Application

```bash
# Initialize a new governed project workspace
python openclone.py init --project ../my-awesome-app --name "My Awesome App" --owner "Lead Architect"
```

This generates `PROJECT.md`, `AGENTS.md`, and an initialized `.aisdf/` state directory with a hash-chained SQLite ledger.

---

<h2 id="architecture">The 31 Engineering Domains</h2>

All 31 domains are consolidated under [`domains/`](domains/), providing standardized templates, operational protocols, architectural rules, and validation checks:

| Domain ID | Domain Title | Focus Area & Deliverables |
|---|---|---|
| **00** | [Governance](domains/00-GOVERNANCE/) | Rulebook, precedence rules, human authority boundaries, tamper-evident audit standards. |
| **01** | [Methodology](domains/01-METHODOLOGY/) | Engineering methodologies and the optional venture-scale MK Framework. |
| **02** | [Project Intelligence](domains/02-PROJECT-INTELLIGENCE/) | Project profiling, source-of-truth ingestion, brownfield repository scanning. |
| **03** | [Requirements Engineering](domains/03-REQUIREMENTS-ENGINEERING/) | Feature inventory, user stories, boundary definition, acceptance criteria contracts. |
| **04** | [Product Engineering](domains/04-PRODUCT-ENGINEERING/) | Roadmap phasing, user journeys, value metric mapping, feature prioritization. |
| **05** | [UX/UI Engineering](domains/05-UX-UI-ENGINEERING/) | Design systems, information architecture, WCAG 2.2 accessibility, Taste Skill. |
| **06** | [Technology Intelligence](domains/06-TECHNOLOGY-INTELLIGENCE/) | Tech stack selection matrices, framework deprecation tracking, ecosystem audits. |
| **07** | [Engineering Knowledge](domains/07-ENGINEERING-KNOWLEDGE/) | Persistent memory architecture, decision logs (ADRs), lesson capture, AKIS engine. |
| **08** | [Software Architecture](domains/08-SOFTWARE-ARCHITECTURE/) | Component topologies, modular boundaries, cross-cutting concerns, data contracts. |
| **09** | [Platform Engineering](domains/09-PLATFORM-ENGINEERING/) | Internal developer platforms, build tools, packaging, dependency management. |
| **10** | [AI & Model Engineering](domains/10-AI-AND-MODEL-ENGINEERING/) | Prompt engineering, evaluation harnesses, fine-tuning specs, RAG architectures. |
| **11** | [Agent Engineering](domains/11-AGENT-ENGINEERING/) | Agent lifecycle, subagent delegation constraints, tool use protocols, loop protection. |
| **12** | [Orchestration & Context](domains/12-ORCHESTRATION-AND-CONTEXT/) | Task DAG generation, context window optimization, session handoff serialization. |
| **13** | [Harness & Execution](domains/13-HARNESS-AND-EXECUTION/) | Local execution control, command allowlisting, stdout/stderr redaction, timeouts. |
| **14** | [Security & Privacy](domains/14-SECURITY-AND-PRIVACY/) | Threat modeling (STRIDE), static scanning lock, secrets hygiene, GDPR baselines. |
| **15** | [Data & Database Engineering](domains/15-DATA-AND-DATABASE-ENGINEERING/) | Relational/NoSQL schemas, migration rollback scripts, transaction boundaries. |
| **16** | [API & Integration Engineering](domains/16-API-AND-INTEGRATION-ENGINEERING/) | REST, GraphQL, gRPC contracts, OpenAPI specs, idempotency keys, rate limits. |
| **17** | [Testing & Verification](domains/17-TESTING-AND-VERIFICATION/) | Test pyramid specs, unit, integration, mutation, property-based testing suites. |
| **18** | [DevOps & Cloud Engineering](domains/18-DEVOPS-AND-CLOUD-ENGINEERING/) | Infrastructure-as-Code (Terraform), container specs, GitOps deployment manifests. |
| **19** | [Deployment & Operations](domains/19-DEPLOYMENT-AND-OPERATIONS/) | Application build-to-deploy engine, 6 cloud adapters, zero-downtime rollouts. |
| **20** | [Reliability & Observability](domains/20-RELIABILITY-AND-OBSERVABILITY/) | SLI/SLO definitions, structured logging, distributed tracing, alerting runbooks. |
| **21** | [Distributed Systems & Scalability](domains/21-DISTRIBUTED-SYSTEMS-AND-SCALABILITY/) | Consensus protocols, event-driven architectures, partitioning, caching topologies. |
| **22** | [Cost & Resource Governance](domains/22-COST-AND-RESOURCE-GOVERNANCE/) | Cloud finops, token budget consumption, compute limits, idle resource reclamation. |
| **23** | [Legal & Compliance](domains/23-LEGAL-AND-COMPLIANCE/) | Open-source license attribution, intellectual property, regulatory compliance. |
| **24** | [Product Analytics & Support](domains/24-PRODUCT-ANALYTICS-AND-SUPPORT/) | Telemetry schemas, funnel metrics, customer feedback loops, incident post-mortems. |
| **25** | [Framework Maintenance](domains/25-FRAMEWORK-MAINTENANCE/) | Continuous hygiene, deprecation policy, schema migration, framework self-upgrades. |
| **26** | [Distribution & Extensions](domains/26-DISTRIBUTION-AND-EXTENSIONS/) | Plugin packaging, SDK publishing, package manager distribution, extensions. |
| **27** | [Standards & Compatibility](domains/27-STANDARDS-AND-COMPATIBILITY/) | Cross-IDE compatibility matrices, language style guides, protocol conformance. |
| **28** | [Templates & Examples](domains/28-TEMPLATES-AND-EXAMPLES/) | Canonical template libraries, starter packs, reference project implementations. |
| **29** | [Benchmarks & Evaluation](domains/29-BENCHMARKS-AND-EVALUATION/) | Deterministic benchmarks, LLM code eval harnesses, regression tracking. |
| **30** | [Agent Rules & Verification](domains/30-AGENT-RULES-AND-VERIFICATION/) | Machine-readable rule engines, permission evaluators, verification hooks. |

---

## 72 Specialist Roles Across 12 Teams

OpenClone establishes 72 specialist role contracts ([`workforce/teams/`](workforce/teams/)) backed by machine-readable JSON manifests ([`workforce/registry/workers/`](workforce/registry/workers/)):

- **Product & Strategy (6 roles):** Chief Product Officer, Product Manager, Technical Writer, Business Analyst, Market Research Specialist, Domain Expert.
- **UX & UI Design (6 roles):** UX Designer, UI Designer, Design System Engineer, Accessibility Specialist, UX Researcher, Information Architect.
- **Software Architecture (6 roles):** Chief Architect, Solutions Architect, System Architect, Enterprise Architect, Integration Architect, Security Architect.
- **Core Engineering (6 roles):** Principal Engineer, Frontend Engineer, Backend Engineer, Full-Stack Engineer, Systems Engineer, Mobile Engineer.
- **Data Engineering (6 roles):** Chief Data Officer, Data Architect, Data Engineer, Database Administrator, Analytics Engineer, ML Engineer.
- **Quality Engineering (6 roles):** QA Director, Test Automation Engineer, Manual QA Specialist, Performance Test Engineer, Security Test Engineer, Accessibility Auditor.
- **Security & Privacy (6 roles):** Chief Information Security Officer, Security Engineer, AppSec Specialist, Privacy Engineer, Compliance Specialist, Threat Modeler.
- **Platform & DevOps (6 roles):** VP Infrastructure, Platform Engineer, DevOps Engineer, Cloud Architect, Site Reliability Engineer, Release Engineer.
- **AI & Intelligence (6 roles):** Chief AI Officer, Prompt Engineer, AI Evaluation Specialist, Context Engineer, Model Fine-Tuning Specialist, Knowledge Architect.
- **Operations & Support (6 roles):** Director Operations, Technical Support Engineer, Incident Commander, Documentation Specialist, Customer Success Engineer, Operations Analyst.
- **Legal & Compliance (6 roles):** General Counsel, Compliance Officer, IP Specialist, Open-Source License Auditor, Ethics Officer, Regulatory Affairs Specialist.
- **Specialized Domains (6 roles):** Cryptographic Engineer, Real-Time Systems Specialist, Embedded Systems Engineer, FinOps Specialist, Internationalization Engineer, Developer Advocate.

---

## 14 Executable Workflows

1. [`WF-001: New Project from Document`](workflows/WF-001-NEW-PROJECT-FROM-DOCUMENT.md) — Greenfield bootstrap from brief to verified architecture, tasks, and initial milestone.
2. [`WF-002: Existing Project X-Ray`](workflows/WF-002-EXISTING-PROJECT-XRAY.md) — Comprehensive brownfield audit, mapping dependencies, tech debt, and security gaps.
3. [`WF-003: Work Unit Handoff`](workflows/WF-003-WORK-UNIT-HANDOFF.md) — Protocol for transferring assignment, context, and evidence between specialist roles.
4. [`WF-004: Quality & Release Gate`](workflows/WF-004-QUALITY-AND-RELEASE-GATE.md) — Multi-tier gating protocol enforcing test passage, scanner clearance, and human sign-off.
5. [`WF-005: Security Assurance`](workflows/WF-005-SECURITY-ASSURANCE.md) — Continuous threat modeling, static security analysis, dependency vulnerability locks.
6. [`WF-006: Persistent Memory Lifecycle`](workflows/WF-006-PERSISTENT-MEMORY-LIFECYCLE.md) — Capturing, validating, and recalling durable engineering knowledge.
7. [`WF-007: Concept Challenge`](workflows/WF-007-CONCEPT-CHALLENGE.md) — Pre-implementation dialectic stress-testing of technical decisions.
8. [`WF-008: Sectional Spec Draft`](workflows/WF-008-SECTIONAL-SPEC-DRAFT.md) — Standardized authoring of modular, implementation-grade specifications.
9. [`WF-009: Independent Design Review`](workflows/WF-009-INDEPENDENT-DESIGN-REVIEW.md) — Clean-context architectural and security critique (Goldfish protocol).
10. [`WF-010: Review Finding Resolution`](workflows/WF-010-REVIEW-FINDING-RESOLUTION.md) — Tracking, fixing, verifying, or obtaining authorized human risk waivers.
11. [`WF-011: Codebase Context Bootstrap`](workflows/WF-011-CODEBASE-CONTEXT-BOOTSTRAP.md) — Rapid, bounded ingestion and structural indexing of active repositories.
12. [`WF-012: Specification Drift Report`](workflows/WF-012-SPECIFICATION-DRIFT-REPORT.md) — Real-time comparison between working-tree git changes and approved specifications.
13. [`WF-013: Project Definition & Assessment`](workflows/WF-013-PROJECT-DEFINITION-ASSESSMENT-AND-IMPLEMENTATION-PLANNING.md) — End-to-end orchestration uniting `PROJECT.md`, task planning, and evidence validation.
14. [`WF-014: Application Build to Deployment`](workflows/WF-014-APPLICATION-BUILD-TO-DEPLOYMENT.md) — 7-phase build, isolated preview verification, human approval gating, and production deployment across 6 cloud platforms.

---

## Integrations & Security Toolchain

OpenClone provides an adapter-first integration architecture connecting the deterministic control plane with AI coding IDEs, external model routers, and security analysis toolchains:

- **[Multi-Host Compatibility Matrix](docs/integrations/compatibility-matrix.md):** Verification status for Antigravity, Claude Code, Cursor, Codex, and ChatGPT.
- **[External LLM Router Comparison](docs/integrations/llm-router-comparison.md):** Technical comparison of 8 external router candidates and the OpenClone normalized provider contract.
- **[Security Toolchain Architecture](docs/integrations/security-toolchain.md):** 12-tool classification and execution boundaries for SAST, secrets, supply-chain, and dynamic testing.
- **[LLM Gateway Threat Model](docs/security/llm-gateway-threat-model.md):** STRIDE boundary analysis for prompt injection, SSRF, credential isolation, and audit integrity.
- **[Security Profiles](docs/security/security-profiles.md):** Tiered profiles from `quick-local` (offline pre-commit) to `release` (SBOM & provenance).
- **[Third-Party Notices](THIRD_PARTY_NOTICES.md):** Attribution and licensing register for Taste Skill, MCP, and referenced open-source projects.

---

## Verified Capability Maturity Matrix

In strict adherence to OpenClone truthfulness standards, every subsystem's maturity is transparently disclosed:

| Subsystem / Capability | Status | Evidence & Test Coverage |
|---|---|---|
| **31 Engineering Domain Specs** | `SPECIFIED` | Fully documented in directory `domains/` (`00-GOVERNANCE` through `30-AGENT-RULES-AND-VERIFICATION`). |
| **56 Engine Execution Contracts** | `SPECIFIED` | Validated by `tools/validate_repository.py`. |
| **14 Executable Workflows** | `SPECIFIED` | Documented in `workflows/` (WF-001–WF-014). |
| **72 Role Manifests & Schemas** | `L1_DEFINED` | Verified against JSON schema in `test_workforce_registry.py`. |
| **12 Pinned Security Scanners** | `PINNED & LOCKED` | Pinned with hashes in `security/scanners.lock.json` and documented in `docs/integrations/security-toolchain.md`. |
| **External Router & Gateway Specs** | `SPECIFIED & ARCHITECTED` | Evaluated across 8 candidates in `docs/integrations/llm-router-comparison.md`. |
| **Local Deterministic Runtime** | `IMPLEMENTED & TESTED` | 63 passing unittests in `tests/` across runtime hardening, DAG, registry, lifecycle, and MCP. |
| **Shared OpenClone MCP Server** | `IMPLEMENTED & TESTED` | JSON-RPC 2.0 stdio/SSE server with 7 tools tested in `tests/test_mcp_server.py`. |
| **Multi-IDE Host Adapters** | `INTEGRATED & VERIFIED` | Native packages for Antigravity, Claude Code, Codex, Cursor, and ChatGPT. |
| **Task DAG & Dependency Gating** | `IMPLEMENTED & TESTED` | Cycle detection & ordering tested in `test_workforce_runtime.py`. |
| **Human Approver Allow-List** | `IMPLEMENTED & TESTED` | Rejects unregistered/AI actors in `ApprovalTests`. |
| **SHA-256 Task Digest Binding** | `IMPLEMENTED & TESTED` | Scope modifications revoke approval in `ReadinessTests`. |
| **Hash-Chained Audit Ledger** | `IMPLEMENTED & TESTED` | Tamper detection verified in `ReadinessTests.test_ledger_tampering_detected`. |
| **Governed Command Executor** | `IMPLEMENTED & TESTED` | Process execution, env isolation, and redaction tested in `ExecutionTests`. |
| **Schema-Validated Findings Engine** | `IMPLEMENTED & TESTED` | Verified in `GateAndFindingTests`. |
| **Deterministic Release Gate** | `IMPLEMENTED & TESTED` | Enforces policies and blocks on missing evidence in `GateAndFindingTests`. |
| **Independent Review Bundler** | `IMPLEMENTED & TESTED` | Tested in `ReviewAndMemoryTests`. |
| **Obsidian Memory Vault Checker** | `IMPLEMENTED & TESTED` | Validates frontmatter & flags injections in `ReviewAndMemoryTests`. |
| **Taste Skill v2.6.0 (Anti-Slop UX)** | `INTEGRATED & TESTED` | 13 automated tests in `skills/taste-skill/tests/test-governance.mjs`. |
| **Canonical Master Blueprints** | `INTEGRATED & INDEXED` | 27 foundational blueprints and prompts indexed in `blueprints/`. |
| **OS-Level Kernel Sandbox** | `NOT_INCLUDED` | Local runtime provides process isolation; production execution requires Docker/VM. |
| **Production Cloud Service** | `NOT_INCLUDED` | OpenClone is designed as a self-hostable, local-first control plane. |

---

## Contributing & License

OpenClone is released under the **MIT License**. Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), and [GOVERNANCE.md](GOVERNANCE.md) before submitting pull requests.

<p align="center">
  <sub>OpenClone · Built with Any AI. Governed by One Engineering Standard.</sub>
</p>
