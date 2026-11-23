# AISDF — Universal AI Development Framework
## Master Product & Engineering Blueprint
**Document ID:** AISDF-UADF-001  
**Version:** 1.0  
**Status:** Proposed strategic blueprint — approval required  
**Prepared:** 21 November 2026

---

## 0. Document authority and interpretation

This document reframes AISDF as a **Universal AI Development Framework (UADF)** while preserving the existing AISDF Version 1.0 Master Blueprint v3.0 and the v4.0.0 repository as source material.

It is a strategic consolidation and forward plan, not proof that the proposed capabilities are implemented. The v3.0 master blueprint remains the detailed specification baseline. The v4.0.0 repository is the implementation baseline assessed in Document 3.

Capability labels used throughout:

- **Specified:** documented design or contract exists.
- **L1_DEFINED:** role or interface contract exists.
- **L2_EXECUTABLE:** bounded behavior executes through a configured adapter.
- **L3_VERIFIED:** repeatable tests verify behavior and safety.
- **L4_OPERATIONAL:** monitored deployment, recovery, incident process, and operational evidence exist.

Never upgrade a capability label because a document, prompt, manifest, or directory exists.

## 1. Executive decision

### 1.1 Recommended identity

**AISDF — Universal AI Development Framework**

**Tagline:** *Build with Any AI. Governed by One Engineering Standard.*

AISDF is an open-source, provider- and IDE-independent framework for coordinating AI-assisted software development across the full product and engineering lifecycle. It provides portable engineering standards, project intelligence, persistent memory, specialist workforce contracts, workflow orchestration, execution governance, tool adapters, evidence collection, and independent verification.

### 1.2 What AISDF is — and is not

AISDF is:
- A reusable framework and control plane for AI-assisted software engineering.
- A common engineering operating standard across supported coding agents and IDEs.
- A portable project knowledge, memory, workflow, skill, and governance system.
- An integration and verification layer around existing execution engines.
- An open-source ecosystem that third parties can extend.

AISDF is not:
- A new foundation model.
- A replacement IDE or editor.
- A claim that 72 role definitions equal 72 autonomous expert agents.
- A universal compatibility promise before adapters are tested.
- A guarantee that every project can be completed in six hours or one day.
- A substitute for human product ownership, security accountability, or release approval.

### 1.3 Strategic thesis

The opportunity is not to win by building the largest agent catalogue. It is to make different AI coding systems operate with shared project truth, portable skills, bounded permissions, reproducible workflows, and verifiable engineering outcomes.

## 2. Why the Universal Framework direction

| Strategic option | Strength | Structural risk | Recommended treatment |
|---|---|---|---|
| AI Software Engineering OS | Strong lifecycle and coordination story | Can be perceived as a closed orchestration product | Keep as AISDF's control-plane experience |
| Autonomous coding platform | Direct, visible code-generation value | Competes head-on with mature execution runtimes | Do not rebuild; integrate |
| AI workforce platform | Clear specialist delegation | Risks optimizing agent count instead of delivery quality | Keep as workforce subsystem |
| Universal AI Development Framework | Interoperability, portable standards, reusable workflows, ecosystem potential | Hard adapter compatibility and adoption problem | **Choose as long-term category** |

This choice is valid only if AISDF delivers real interoperability. A folder of prompts copied into several IDEs is not a universal framework.

## 3. Product outcomes

A user should be able to:

1. Provide a project brief (`PROJECT.md`) and optionally an existing repository.
2. Let AISDF inspect the brief, repository, constraints, and current state.
3. Receive a traceable product and engineering assessment.
4. Generate a project pack: requirements, architecture, decisions, delivery plan, risk register, test strategy, and agent instructions.
5. Select supported execution tools and approve a versioned plan.
6. Run bounded work through a configured coding engine and isolated workspace.
7. Collect real command, test, diff, and artifact evidence.
8. Run independent review with a separate reviewer context and read-only permissions.
9. Resolve findings, rerun required tests, and receive a truthful delivery report.
10. Resume later with relevant, scoped project memory and checkpoints.

## 4. Product principles

1. **Human authority:** humans own product direction, risk acceptance, and release decisions.
2. **Evidence over claims:** never report a command, test, scan, deployment, or review as complete unless execution evidence exists.
3. **Portable by default:** project standards and skills should be usable across supported tools.
4. **Provider-neutral core:** model providers are adapters, not the framework's identity.
5. **Deterministic control:** permissions, approvals, task states, budgets, evidence, and audit records are enforced by code.
6. **Model-driven reasoning:** LLMs analyze, plan, generate, summarize, and review within bounded contracts.
7. **Least privilege:** default to read-only; grant narrow write and execution permissions.
8. **Scope discipline / No AI Slope:** do not add features, tools, agents, services, or architecture without a demonstrated requirement.
9. **Source of truth:** canonical project artifacts outrank summaries and memory.
10. **Memory provenance:** every durable memory has scope, source, status, confidence, and freshness.
11. **Independent verification:** implementation authors do not self-certify critical work.
12. **Graceful failure:** timeouts, unavailable providers, missing evidence, conflicts, and adapter failures are explicit states.
13. **Open-source integrity:** verify license, provenance, version, and security posture before reuse.
14. **Reproducibility:** benchmark and release claims must be independently repeatable.

## 5. Target users and primary use cases

- Individual developers using several AI coding tools.
- Small engineering teams needing consistent AI-assisted workflows.
- Open-source maintainers coordinating AI contributions.
- Startups turning project briefs into governed implementation.
- Organizations needing traceability, approval gates, and audit evidence.
- Framework/plugin authors building adapters, skills, and specialist packs.

Primary use cases:
- New project from brief.
- Existing repository X-ray and modernization plan.
- Feature delivery with approval.
- Bug diagnosis and bounded remediation.
- Security review and vulnerability remediation.
- Architecture and specification review.
- Cross-tool handoff and session continuation.
- Release-readiness and evidence-backed audit.

## 6. Core architecture

```text
                 AISDF UNIVERSAL FRAMEWORK
                            |
       +--------------------+--------------------+
       |                    |                    |
 PROJECT INTELLIGENCE   MASTER ENGINEERING   GOVERNANCE & POLICY
       |                    AGENT                  |
       |                     |                     |
       +---------------------+---------------------+
                             |
                 MEMORY & KNOWLEDGE FOUNDATION
              AKIS + Persistent Memory + Project State
                             |
                 DYNAMIC WORKFORCE & SKILLS
                             |
                  WORKFLOW / TASK ORCHESTRATOR
                             |
                   EXECUTION ADAPTER SDK
                             |
        +--------------------+---------------------+
        |                    |                     |
   Coding agents          IDE agents           Human/tool
   and runtimes           and CLIs             execution
        |                    |                     |
        +--------------------+---------------------+
                             |
                  EVIDENCE & VERIFICATION
                             |
                    EGM INDEPENDENT AUDIT
                             |
                  HUMAN ACCEPTANCE / RELEASE
```

### 6.1 Control plane vs execution plane

**AISDF control plane owns:**
- Project and requirement state.
- Workforce registry and capability routing.
- Task DAG and state transitions.
- Approval records and policy enforcement.
- Budget, timeout, retry, and concurrency limits.
- Memory scope and retrieval policy.
- Audit events and evidence contracts.
- Adapter capability negotiation.
- Verification and release gates.

**Execution plane owns:**
- Model reasoning loops.
- File edits and terminal commands.
- Browser and external tool operations.
- Workspace and sandbox lifecycle.
- Runtime-specific sessions and events.

AISDF should integrate mature execution planes instead of duplicating them.

## 7. Product subsystem map

| Subsystem | Responsibility | Primary output |
|---|---|---|
| Project Intelligence | Understand user intent and repository state | Project assessment and source-of-truth map |
| Product Intelligence | Validate problem, users, value, scope, and success measures | Product brief and prioritized requirements |
| Requirements Engineering | Make needs testable and traceable | Requirements and acceptance criteria |
| Technology Intelligence | Research alternatives, compatibility, licenses, and support | Evidence-backed technology decision |
| AKIS | Organize, retrieve, rank, and assess knowledge freshness | Grounded knowledge results |
| Persistent Memory | Capture, validate, version, recall, consolidate, expire | Scoped memory records |
| Project State (E-040) | Maintain authoritative project continuity | Canonical current state |
| Context/Handoff (E-038) | Package and transfer authorized context | Context pack and acknowledged handoff |
| Workforce Engine | Select and assign qualified role contracts | Worker assignments |
| Skill System | Load versioned, executable procedural guidance | Skill package and execution instructions |
| Orchestrator | Validate and schedule task dependencies | Task DAG and state events |
| Governance | Enforce permission, approval, and budget rules | Policy decisions and approval records |
| Execution Harness | Run bounded work through adapters | Execution events and artifacts |
| Universal Adapter Layer | Connect IDEs, CLIs, agents, tools, and providers | Capability-negotiated adapter |
| Verification | Test requirements and collect evidence | Verification report |
| EGM | Independently challenge implementation claims | Findings and audit verdict |
| Operations | Monitor, recover, update, and support deployments | Operational evidence |

## 8. Memory and knowledge foundation

Memory is a foundational layer, not an optional agent feature.

Preserve the existing boundaries:
- **AKIS / E-031:** knowledge organization, retrieval, ranking, and freshness.
- **Persistent Memory:** what survives sessions, how it is scoped, versioned, validated, and recalled.
- **E-038:** context packaging and ownership transfer.
- **E-040:** authoritative project state.
- **Context Engine:** selects the minimum relevant authorized context for each operation.

Memory scopes should include project, decision, session, reusable knowledge, agent/work-unit continuity, and explicitly approved preference. Keep personal and organization/project scopes separate.

Never let a summary overwrite a canonical requirement or decision. Memory is a recall layer with provenance; canonical project artifacts remain authoritative.

## 9. Workforce and skill philosophy

AISDF's existing 72 worker contracts across 12 teams are a useful catalogue foundation, not evidence of 72 autonomous agents. Keep the catalogue, but introduce capability maturity and execution evidence for each role.

Every work unit must have:
- One accountable owner.
- Required capability and skill versions.
- Inputs and source references.
- Expected outputs and artifact schema.
- Allowed actions and file scope.
- Dependencies and deadline.
- Model/tool requirements.
- Token, cost, time, and retry budgets.
- Acceptance criteria and Definition of Done.
- Reviewer and evidence requirements.

Specialists are activated dynamically. Do not instantiate every role for every task.

## 10. Universal interoperability model

A supported adapter must declare:
- Adapter ID, version, supported platform/tool versions.
- Authentication and secret-handling method.
- Read/write/execute/browser/network capabilities.
- Workspace and isolation guarantees.
- Session start, resume, cancel, and event-stream behavior.
- File and artifact transfer semantics.
- Tool permission mapping.
- Approval integration.
- Cost/token/usage reporting where available.
- Failure, timeout, and recovery semantics.
- Conformance test results and last verified date.

Integration maturity:
- **I0 — documented:** instructions/templates only.
- **I1 — portable configuration:** native rule/skill files install correctly.
- **I2 — assisted handoff:** context and work packages transfer with human operation.
- **I3 — controlled execution:** adapter invokes bounded work and returns structured evidence.
- **I4 — verified integration:** conformance, security, recovery, and compatibility tests pass across supported versions.

Never label a tool “fully supported” based only on a template.

## 11. Security and trust boundaries

Threat model must cover:
- Direct and indirect prompt injection.
- Malicious repository files, issue text, web pages, and tool output.
- Credential and secret exfiltration.
- Unsafe shell commands and destructive Git operations.
- Cross-project and cross-tenant memory leakage.
- Malicious skills, MCP servers, adapters, and dependencies.
- Agent privilege escalation and untrusted delegation.
- Memory poisoning and stale decision reuse.
- Sandbox escape and host filesystem access.
- Provider data leakage and unapproved network egress.

Required controls:
- Default read-only inspection.
- Explicit project/workspace identity.
- Least-privilege, short-lived credentials.
- Isolated worktrees and sandboxed execution.
- Command and path allow/deny policy.
- Human approval for sensitive actions.
- Secret redaction in prompts, logs, and artifacts.
- Untrusted content treated as data, never policy.
- Append-only audit events where practical.
- Independent security review and vulnerability lifecycle.

## 12. Human approval model

Approval is bound to:
- Project identity and repository commit.
- Plan/document version and content hash.
- Scope, actions, and permission grant.
- Approver identity and timestamp.
- Expiration and invalidation conditions.

Material plan changes invalidate affected approvals. Approval must not be inferred from silence or from a prior approval of a different content hash.

Suggested gates:
- G0: project intake and data access.
- G1: product scope and requirements.
- G2: architecture and technology decisions.
- G3: implementation plan and permissions.
- G4: high-risk execution actions.
- G5: release candidate and verification.
- G6: production deployment or destructive operations.

## 13. Verification and delivery contract

Every completion report must distinguish:
- Planned vs attempted vs executed.
- Passed vs failed vs skipped vs blocked.
- Locally tested vs CI-tested vs staging-tested vs production-observed.
- Model-generated assertion vs tool-generated evidence vs human acceptance.
- Findings fixed vs accepted risk vs unresolved.

Minimum delivery evidence:
- Baseline commit and changed-file list.
- Requirement-to-task-to-test traceability.
- Commands executed and exit codes.
- Test names, results, and logs.
- Security scan/tool versions and results, if run.
- Screenshots/browser evidence where relevant.
- Independent audit findings and dispositions.
- Known limitations and unverified areas.
- Human acceptance record.

## 14. Competitive positioning

AISDF should not claim to be better than every coding agent. It should own a distinct category: the portable engineering standard and governance layer across coding agents.

| Dimension | OpenHands | OpenCode | AISDF target |
|---|---|---|---|
| Primary role | Agent SDK/runtime and execution ecosystem | Provider-flexible coding agent and developer workflow | Universal lifecycle framework and control plane |
| Execution runtime | Strong first-party focus | Strong local coding-agent experience | Integrate; do not duplicate initially |
| Developer interaction | SDK/server/apps and agent workflows | Terminal-first coding experience and configured agents | CLI/API plus portable integrations |
| Skills/agents | SDK skills/tools and extension ecosystem | Native skills, agents, permissions | Versioned skill contracts, dynamic selection, cross-tool packaging |
| Memory/context | Conversation state, persistence, event log, condensation | Session/tool ecosystem; capabilities vary by configured backend | Scoped project memory, AKIS, E-038, E-040 with provenance |
| Governance | Runtime/security policies and workspace controls | Configurable permissions and policies | Cross-tool approvals, policy ledger, task contracts, evidence |
| Interoperability | SDK/API and integrations | Providers, MCP, skills, tools | Adapter SDK and conformance suite |
| Independent verification | Can support tests/reviews through tools | Can support tests/reviews through tools | First-class EGM and evidence-backed release gate |
| Benchmark ambition | Agent execution quality | Coding-agent task quality and DX | Lifecycle quality, portability, governance, and delivery evidence |

This is a positioning comparison, not a measured ranking. Capabilities evolve and must be rechecked against current releases.

## 15. Differentiation that can be defensible

AISDF's defensible value should emerge from the combination of:
1. A stable cross-tool engineering contract.
2. Project-aware memory with authority, provenance, and conflict handling.
3. Dynamic workforce selection backed by capability evidence.
4. Portable skills with versioning and tests.
5. Approval and policy enforcement independent of the coding agent.
6. End-to-end traceability from user intent to verified output.
7. EGM independent review and reproducible benchmark data.
8. Open extension interfaces and an active contributor ecosystem.

No single item is unique by itself. The integrated, tested system is the differentiation.

## 16. Product roadmap overview

- **R0 — Audit and baseline:** establish what exists in code, what is documentation, and what runs.
- **R1 — Working vertical slice:** one project brief through plan, approval, external execution, verification, report.
- **R2 — Memory and context:** AKIS, persistent memory, E-038, E-040 integrated and tested.
- **R3 — Adapter interoperability:** three real adapters with conformance tests.
- **R4 — Skills and workforce:** dynamic capability routing and skill lifecycle.
- **R5 — Quality leadership:** EGM, AEB benchmark, security and recovery tests.
- **R6 — Ecosystem:** public SDK, extension documentation, examples, contributors, release process.

See Document 3 for implementation sequence and gates.

## 17. Global top-two ambition: measurable definition

“Top two” is an ambition, not a current status. No single authoritative global ranking covers universal AI development frameworks. AISDF should define a transparent scorecard and earn recognition through independent evidence.

Proposed dimensions:
- Real-world task success and regression rate.
- Cross-tool adapter conformance.
- Security and permission-boundary reliability.
- Memory retrieval precision, freshness, and leakage resistance.
- Skill effectiveness and portability.
- End-to-end traceability and evidence completeness.
- Cost and time efficiency under equal conditions.
- Reproducibility across repositories and environments.
- Active users, contributors, external extensions, and maintainer response.
- Reliability, release quality, and incident transparency.

Do not claim global top-two status until independent evaluators can reproduce the results and adoption evidence supports the claim.

## 18. Final decision

Adopt **Universal AI Development Framework** as AISDF's long-term category. Retain the AI Software Engineering OS as the internal control-plane product experience, the AI workforce as a subsystem, and autonomous execution as an adapter-backed capability.

The immediate objective is not another blueprint expansion. It is a tested vertical slice that proves the framework's central promise.
