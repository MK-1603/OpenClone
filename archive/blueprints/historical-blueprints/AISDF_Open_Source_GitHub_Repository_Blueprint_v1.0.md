# AISDF --- Open-Source GitHub Repository Blueprint

**Project:** AI Software Development Framework (AISDF)\
**Tagline:** From Problem Statement to Production Software\
**Document:** Complete Repository Blueprint\
**Version:** 1.0.0\
**Status:** Proposed open-source repository baseline\
**Scope:** GitHub repository, documentation, knowledge assets, schemas,
rules, templates, examples, validation tools, and community governance.\
**Explicit exclusion:** This blueprint does not specify building or
hosting the AISDF application/platform. AISDF is being defined here as
an open-source software engineering framework that people and AI
development tools can read, adopt, adapt, and execute within their own
environments.

------------------------------------------------------------------------

# 1. Executive Definition

AISDF is an open-source, AI-assisted software development framework that
provides a structured, auditable, and reusable way to move from a
problem statement or an existing codebase to a well-understood,
specified, designed, implemented, tested, secured, verified, deployed,
and maintained software product.

The GitHub repository is the framework's canonical source of truth. It
contains:

-   Engineering methodology and lifecycle workflows.
-   Project discovery and existing-codebase assessment standards.
-   Requirements, product, UX/UI, architecture, and technology guidance.
-   Engineering knowledge documents and verified references.
-   AI agent role definitions, task contracts, rules, and verification
    standards.
-   Security, privacy, execution, and governance policies.
-   Reusable schemas, checklists, templates, examples, and decision
    records.
-   Lightweight scripts and CI checks that validate the repository's own
    content.
-   Contribution, versioning, release, and maintenance governance.

AISDF is **not** a hosted SaaS product, AI coding IDE, model provider,
autonomous agent runtime, project management application, or deployment
platform in this repository scope.

It may describe how to use tools such as Antigravity, Cursor, Codex,
Claude Code, Windsurf, Kiro, Cline, Roo Code, OpenHands, GitHub Copilot,
and other tools. Describing or providing rules for a tool does not make
that tool a runtime dependency.

## 1.1 Core promise

> Give people and AI development tools a reliable engineering framework
> for understanding, planning, building, verifying, and maintaining
> software---without locking them into one model, IDE, cloud provider,
> or technology stack.

## 1.2 Repository principles

1.  **Human-readable first:** Markdown is the primary content format.
2.  **Tool-independent:** Core methodology must not require a particular
    AI vendor or IDE.
3.  **Evidence over claims:** A completed checklist or agent statement
    is not proof that software works.
4.  **Approval before material change:** Scope, product direction,
    architecture, sensitive access, purchases, and production actions
    require the appropriate human authorization.
5.  **Least privilege:** Agent instructions must never grant permissions
    that the execution environment has not granted.
6.  **No AI Slope:** Avoid unnecessary features, dependencies, agents,
    abstractions, context, and infrastructure.
7.  **Change Only Law:** When asked to change one thing, change that
    thing and only the dependencies technically required; preserve
    unrelated behavior.
8.  **Right-sized engineering:** Do not impose enterprise architecture
    on a small project.
9.  **Traceability:** Connect requirements to implementation tasks,
    tests, verification, and evidence.
10. **Portable ownership:** Users own their code, project documents,
    decisions, and outputs.
11. **Verified knowledge:** Time-sensitive technical guidance must
    identify authoritative sources and verification dates.
12. **Explicit uncertainty:** Mark assumptions, unknowns, unverified
    claims, and tool limitations.

------------------------------------------------------------------------

# 2. Scope and Non-Scope

## 2.1 Included in this repository

  -----------------------------------------------------------------------
  Area                                Repository deliverable
  ----------------------------------- -----------------------------------
  Methodology                         New-product, existing-project, and
                                      transformation workflows

  Project intelligence                Inspection and assessment
                                      procedures

  Requirements                        PRD, functional/non-functional
                                      requirements, acceptance criteria

  Product engineering                 Validation, MVP, prioritization,
                                      roadmap methods

  UX/UI                               Research, flows, design-system and
                                      accessibility standards

  Technology intelligence             Evaluation criteria, comparison
                                      templates, source policy

  Architecture                        Architecture methods, diagrams, ADR
                                      templates, review checklists

  Knowledge                           Modular engineering knowledge
                                      documents

  AI/agents                           Agent roles, task contracts,
                                      prompts/rules, evaluation guidance

  Orchestration                       Tool-independent workflow, handoff,
                                      conflict, and recovery standards

  Harness                             Secure execution requirements and
                                      policy guidance

  Security/privacy                    Threat modeling, secure
                                      development, privacy and governance
                                      standards

  Data/API                            Data modeling, API, event, and
                                      integration design guidance

  Testing                             Test strategy, verification,
                                      evidence and quality standards

  Delivery/operations                 CI/CD, deployment, monitoring,
                                      incident and recovery guidance

  AFIAE                               External capability
                                      discovery/evaluation/acquisition
                                      methodology

  External tool integration           IDE, CLI, MCP, Git and
                                      human-mediated integration guidance

  Templates                           Reusable project and engineering
                                      templates

  Examples                            Small illustrative examples and
                                      reference workflows

  Validation                          Scripts and CI checks for
                                      repository quality

  Governance                          Contribution, release, versioning,
                                      security reporting and maintenance
  -----------------------------------------------------------------------

## 2.2 Explicitly excluded

The repository does not build or operate:

-   A web application or dashboard.
-   A SaaS backend or API server.
-   A hosted AI agent orchestration service.
-   A model gateway or model hosting platform.
-   A database-backed project management application.
-   A sandbox execution service.
-   A cloud deployment platform.
-   A billing or subscription system.
-   An autonomous purchasing or installation service.
-   A proprietary IDE or code editor.

A future project may implement some of these capabilities, but it must
be separately proposed and approved. Do not silently turn this
repository into an application monorepo.

## 2.3 Repository automation boundary

Lightweight repository tooling is allowed when it validates or maintains
the framework itself. Examples:

-   Markdown linting.
-   YAML and JSON schema validation.
-   Broken-link checking.
-   Required metadata checks.
-   Duplicate document ID checks.
-   Knowledge freshness reports.
-   Template/example validation.
-   Documentation site generation, if later approved.

These tools must not become a hidden application runtime.

------------------------------------------------------------------------

# 3. Intended Users and Usage Modes

## 3.1 Target audiences

-   Students and beginners.
-   Individual developers.
-   Professional software engineers.
-   Product designers.
-   Technical founders.
-   Startups and small teams.
-   Engineering organizations.
-   AI-assisted development tool users.

## 3.2 Framework usage modes

### Beginner Mode

Guided explanations, plain-language questions, staged decisions, and
explicit approval points.

### Developer Mode

Technical specifications, architecture, APIs, database design,
implementation mapping, test planning, and engineering review.

### Team Mode

Task ownership, reviews, handoffs, shared decisions, and team
governance.

### Enterprise Adoption Mode

Organization policies, security controls, evidence requirements,
auditability, and compliance mapping. AISDF provides guidance and
templates; it does not certify compliance.

------------------------------------------------------------------------

# 4. Development Methodology

AISDF provides three connected paths.

## 4.1 Path 0 --- Venture and Business Validation (optional)

1.  Starving Crowd Check.
2.  Model a Proven Winner.
3.  Founder-Market Fit.
4.  Inversion Thinking.
5.  Premortem.
6.  Pre-Commit Kill Criteria.
7.  Market Timing.
8.  Build Offer.
9.  Disciplined Execution.
10. Feedback Loops.
11. Check Kill Criteria.
12. Resource Reinvestment.
13. Defend Moat.
14. Systemize and Delegate.

This path is optional. It must not block technical work when the user is
building an internal, educational, experimental, or non-commercial
project.

## 4.2 Path A --- New Product Development

1.  Problem and user check.
2.  Proven-product and alternatives check.
3.  Product/build fit.
4.  Inversion and premortem.
5.  Go/kill criteria.
6.  Product and MVP definition.
7.  Scope freeze.
8.  UX/UI and design system.
9.  Architecture and source of truth.
10. Implementation mapping.
11. AI-assisted development.
12. Verification, security, and QA.
13. Deployment, observation, and launch.
14. Feedback, iteration, and scaling.

## 4.3 Path B --- Existing Project Development

1.  Project X-Ray.
2.  Current-state check.
3.  Exact change request.
4.  Impact and dependency analysis.
5.  Scope and acceptance criteria.
6.  Minimum safe plan.
7.  AI implementation map.
8.  Controlled changes.
9.  Verification.
10. Regression testing.
11. Security, performance, and UX QA.
12. Build and deployment.
13. Documentation and source-of-truth updates.
14. Close and monitor.

## 4.4 Product transformation

-   **Direction A --- Improve:** Improve the existing product while
    preserving its concept.
-   **Direction B --- Redesign:** Redesign while preserving the core
    purpose.
-   **Direction C --- Transform:** Change the product direction,
    architecture, or purpose. Explicitly decide what to reuse, replace,
    migrate, retire, or run in parallel.

AISDF must not choose a transformation direction without approval.

## 4.5 Core existing-project workflow

**Inspect → Understand → Analyze → Discover → Compare → Document →
Approve → Implement → Verify.**

## 4.6 Universal workflow

**Discovery → Problem Definition → Validation → Requirements → Product
Definition → Technology Intelligence → UX/UI → Architecture →
Documentation → Implementation Planning → Development → Testing/Security
→ Independent Verification → Delivery → Production Verification →
Maintenance.**

------------------------------------------------------------------------

# 5. Mandatory Framework Laws

These rules apply across all methodology paths and agent instructions.

## 5.1 Change Only Law

When the request targets a specific feature or behavior:

-   Modify the requested scope.
-   Modify only technically necessary dependencies.
-   Preserve unrelated features, design, behavior, and architecture.
-   Identify unavoidable collateral changes before making them.
-   Record and explain any deviation.

## 5.2 No AI Slope

Do not add unnecessary:

-   Features.
-   Abstractions.
-   Dependencies.
-   Services.
-   Agents.
-   Prompts.
-   Context.
-   Infrastructure.
-   Refactors.
-   Configuration.
-   Automation.

Every addition must solve an identified requirement or risk.

## 5.3 Approval First

Require the appropriate approval before material changes to:

-   Product direction.
-   Scope.
-   Requirements.
-   Architecture.
-   Data migrations with material risk.
-   Security policy.
-   Sensitive permissions.
-   Paid services or purchases.
-   Production deployment.
-   Destructive operations.

## 5.4 Evidence Over Claims

"Implemented," "tested," "secure," "deployed," and "complete" are claims
that require evidence appropriate to the claim.

## 5.5 No Authority Escalation

Delegation, provider switching, task splitting, MCP use, CLI execution,
or tool chaining must not increase the authority granted to an agent.

## 5.6 Default Deny and Least Privilege

Agent instructions are not security enforcement. The operating system,
sandbox, credentials, network, and external platform must enforce
permissions.

## 5.7 Right-Sized Engineering

Select the simplest architecture that satisfies verified requirements
and foreseeable constraints.

## 5.8 Source-of-Truth Law

Project state, approved decisions, requirements, and evidence must live
in the project's authoritative records. Chat memory is not the project's
source of truth.

------------------------------------------------------------------------

# 6. Repository Information Architecture

## 6.1 Recommended root structure

``` text
AISDF/
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── GOVERNANCE.md
├── SUPPORT.md
├── CHANGELOG.md
├── VERSION
├── CITATION.cff
├── .gitignore
├── .editorconfig
├── .markdownlint.jsonc
│
├── 00-GOVERNANCE/
├── 01-METHODOLOGY/
├── 02-PROJECT-INTELLIGENCE/
├── 03-REQUIREMENTS-ENGINEERING/
├── 04-PRODUCT-ENGINEERING/
├── 05-UX-UI-ENGINEERING/
├── 06-TECHNOLOGY-INTELLIGENCE/
├── 07-ENGINEERING-KNOWLEDGE/
├── 08-SOFTWARE-ARCHITECTURE/
├── 09-PLATFORM-ENGINEERING/
├── 10-AI-AND-MODEL-ENGINEERING/
├── 11-AGENT-ENGINEERING/
├── 12-ORCHESTRATION-AND-CONTEXT/
├── 13-HARNESS-AND-EXECUTION/
├── 14-SECURITY-AND-PRIVACY/
├── 15-DATA-AND-DATABASE-ENGINEERING/
├── 16-API-AND-INTEGRATION-ENGINEERING/
├── 17-TESTING-AND-VERIFICATION/
├── 18-DEVOPS-AND-CLOUD-ENGINEERING/
├── 19-DEPLOYMENT-AND-OPERATIONS/
├── 20-RELIABILITY-AND-OBSERVABILITY/
├── 21-DISTRIBUTED-SYSTEMS-AND-SCALABILITY/
├── 22-COST-AND-RESOURCE-GOVERNANCE/
├── 23-LEGAL-AND-COMPLIANCE/
├── 24-PRODUCT-ANALYTICS-AND-SUPPORT/
├── 25-FRAMEWORK-MAINTENANCE/
├── 26-DISTRIBUTION-AND-EXTENSIONS/
├── 27-STANDARDS-AND-COMPATIBILITY/
├── 28-TEMPLATES-AND-EXAMPLES/
├── 29-BENCHMARKS-AND-EVALUATION/
├── 30-AGENT-RULES-AND-VERIFICATION/
│
├── schemas/
├── registries/
├── workflows/
├── templates/
├── examples/
├── tests/
├── tools/
├── assets/
│
└── .github/
    ├── ISSUE_TEMPLATE/
    ├── PULL_REQUEST_TEMPLATE.md
    ├── DISCUSSION_TEMPLATE/
    ├── workflows/
    ├── CODEOWNERS
    └── dependabot.yml
```

The 31 numbered domains are retained as the canonical knowledge domains.
The root-level `templates/` and `examples/` folders may contain
cross-domain starter assets; domain-specific authoritative material
belongs in its numbered domain. Avoid duplicate canonical documents.

## 6.2 Domain ownership

  -----------------------------------------------------------------------
  Domain                              Canonical responsibility
  ----------------------------------- -----------------------------------
  00 Governance                       Rules, ownership, contribution,
                                      release policy

  01 Methodology                      Path 0, Path A, Path B, lifecycle
                                      and laws

  02 Project Intelligence             Intake, X-Ray, assessment, state
                                      analysis

  03 Requirements Engineering         Requirements, scope, acceptance and
                                      traceability

  04 Product Engineering              Validation, product strategy, MVP
                                      and roadmap

  05 UX/UI Engineering                Research, flows, design systems and
                                      accessibility

  06 Technology Intelligence          Technology evaluation and
                                      official-source research

  07 Engineering Knowledge            Cross-cutting engineering
                                      fundamentals and practices

  08 Software Architecture            Architecture methods, diagrams and
                                      ADRs

  09 Platform Engineering             Developer platforms, environments
                                      and platform practices

  10 AI and Model Engineering         Models, inference, evaluation and
                                      provider concepts

  11 Agent Engineering                Agent roles, contracts, memory,
                                      tools and evaluation

  12 Orchestration and Context        Workflows, routing, retrieval and
                                      context management

  13 Harness and Execution            Sandboxes, tool execution and
                                      permission enforcement

  14 Security and Privacy             Threats, controls, privacy and
                                      incident security

  15 Data and Database Engineering    Data modeling, databases,
                                      migrations and lifecycle

  16 API and Integration Engineering  APIs, events, connectors and
                                      contracts

  17 Testing and Verification         Test design, independent
                                      verification and evidence

  18 DevOps and Cloud Engineering     CI/CD, infrastructure as code and
                                      cloud practices

  19 Deployment and Operations        Releases, deployment, rollback and
                                      operational procedures

  20 Reliability and Observability    SLOs, logs, metrics, traces and
                                      incident reliability

  21 Distributed Systems and          Concurrency, queues, scaling and
  Scalability                         distributed design

  22 Cost and Resource Governance     Budgets, quotas, cost measurement
                                      and optimization

  23 Legal and Compliance             Licenses, privacy obligations and
                                      compliance mapping

  24 Product Analytics and Support    Product metrics, support and
                                      feedback

  25 Framework Maintenance            Knowledge freshness, framework
                                      upgrades and deprecation

  26 Distribution and Extensions      Repository distribution,
                                      CLI/SDK/plugin guidance

  27 Standards and Compatibility      Standards registry, compatibility
                                      and lifecycle

  28 Templates and Examples           Reusable project and engineering
                                      assets

  29 Benchmarks and Evaluation        Framework and agent evaluation
                                      scenarios

  30 Agent Rules and Verification     Agent-specific rules, constraints
                                      and verification
  -----------------------------------------------------------------------

## 6.3 Required domain landing pages

Every domain must contain:

-   `README.md` --- domain overview and navigation.
-   `INDEX.md` --- canonical document registry for the domain.
-   `01-...md` --- primary topic documents.
-   `02-...-ALTERNATIVES.md` --- alternatives where meaningful.
-   `03-...-AGENT-RULES-AND-VERIFICATION.md` --- conditional agent
    rules.
-   `examples/` --- only where examples materially help.
-   `templates/` --- only where reusable templates are needed.

Do not create empty placeholder files merely to make every folder look
complete. A domain may be marked `Planned` until it has useful content.

------------------------------------------------------------------------

# 7. Documentation Standard

## 7.1 Document types

  Type           Purpose
  -------------- -----------------------------------------------
  Principle      Stable rule or engineering principle
  Methodology    Repeatable workflow
  Standard       Normative requirement
  Guide          Explanatory implementation guidance
  Reference      Structured technical facts or API information
  Decision       Recorded choice and alternatives
  Checklist      Review or execution aid
  Template       Reusable document structure
  Example        Illustrative application
  Benchmark      Repeatable evaluation
  Agent Rule     Agent behavior and boundaries
  Verification   Evidence and acceptance requirements

## 7.2 Standard topic document structure

``` markdown
---
id: AISDF-EXAMPLE-001
title: Example Engineering Topic
domain: 07-ENGINEERING-KNOWLEDGE
version: 1.0.0
status: Draft
document_type: guide
owner: AISDF Maintainers
last_verified: YYYY-MM-DD
next_review: YYYY-MM-DD
related_documents: []
official_sources: []
---

# Title

## 1. Purpose
## 2. Scope
## 3. Definitions
## 4. Fundamentals
## 5. Internal Working
## 6. Architecture
## 7. Workflow
## 8. Implementation Guidance
## 9. Best Practices
## 10. Security and Privacy
## 11. Testing and Verification
## 12. Production Considerations
## 13. Limitations and Trade-offs
## 14. Alternatives
## 15. Common Mistakes
## 16. AISDF Integration
## 17. Examples
## 18. Checklist
## 19. References
## 20. Change History
```

Not every heading is mandatory for every document. Authors must remove
irrelevant sections rather than fill them with meaningless text.

## 7.3 Metadata rules

Required metadata:

-   `id`
-   `title`
-   `domain`
-   `version`
-   `status`
-   `document_type`
-   `owner`
-   `last_verified`
-   `related_documents`

Recommended metadata:

-   `next_review`
-   `official_sources`
-   `tags`
-   `applicability`
-   `technology_versions`
-   `supersedes`

Allowed statuses:

-   Draft.
-   In Review.
-   Approved.
-   Deprecated.
-   Retired.

A Draft document must not be presented as an approved standard.

## 7.4 Document IDs

Use stable IDs, for example:

-   `AISDF-METH-001`
-   `AISDF-REQ-001`
-   `AISDF-ARCH-001`
-   `AISDF-AKIS-001`
-   `AISDF-AFIAE-001`
-   `AISDF-SEC-001`
-   `AISDF-AGENT-001`

Do not reuse IDs after retirement.

## 7.5 Links and references

-   Use relative Markdown links for repository portability.
-   Link to canonical documents rather than duplicating them.
-   Prefer official documentation for technical claims.
-   Record source title, URL, publisher, version/date where available,
    and last-verified date.
-   Clearly distinguish normative rules from recommendations and
    examples.
-   Do not cite a source as support for a claim it does not establish.

------------------------------------------------------------------------

# 8. Core Repository Registries

Registries are structured records that make the framework navigable and
machine-checkable. They are not a runtime database.

## 8.1 Document Registry

Tracks document ID, path, title, domain, type, status, version, owner,
review date, and relationships.

## 8.2 Technology Registry

Tracks:

-   Technology ID and name.
-   Category.
-   Official website and documentation.
-   Supported versions.
-   License.
-   Maturity and maintenance state.
-   Security advisories.
-   Compatibility.
-   Alternatives.
-   Last verified date.
-   Source references.

## 8.3 Standards Registry

Tracks:

-   Standard ID.
-   Publisher.
-   Standard name.
-   Version.
-   Official source.
-   Applicability.
-   AISDF mapping.
-   Adoption status.
-   Review date.

Standards may include OWASP, NIST SSDF, NIST CSF, NIST AI RMF, CWE/CVE,
SLSA, OpenSSF, and WCAG. AISDF must record the exact version and
applicability it discusses. Listing a standard does not establish
compliance.

## 8.4 Agent Registry

Tracks:

-   Agent ID.
-   Role.
-   Purpose.
-   Responsibilities.
-   Non-responsibilities.
-   Required inputs.
-   Expected outputs.
-   Tools.
-   Permission assumptions.
-   Prohibited actions.
-   Handoff rules.
-   Verification requirements.
-   Evaluation scenarios.

## 8.5 Tool and Connector Registry

Tracks:

-   Tool ID.
-   Provider.
-   Product.
-   Category.
-   Official documentation.
-   Integration methods.
-   Verified capabilities.
-   Authentication model.
-   Permission scopes.
-   Data handling.
-   Pricing model.
-   License/terms.
-   Limitations.
-   Compatibility.
-   Security review.
-   Last verified date.

A tool's inclusion in the registry does not mean AISDF has a working
integration with it.

## 8.6 Template Registry

Tracks template ID, purpose, file path, required fields, applicable
lifecycle phase, version, owner, and validation method.

## 8.7 Workflow Registry

Tracks workflow ID, trigger, inputs, stages, decision gates, outputs,
responsible roles, failure paths, and acceptance criteria.

------------------------------------------------------------------------

# 9. Knowledge Engineering and AKIS

AKIS is the repository's knowledge organization and retrieval
methodology. In this repository scope, it is documented and may have
lightweight indexing/validation scripts. It is not a hosted retrieval
service.

## 9.1 Authoring and source of truth

-   Obsidian may be used as a local authoring interface.
-   Markdown files in Git are the canonical content.
-   GitHub is the collaboration and version history location.
-   AISDF documentation must remain readable without Obsidian.
-   Runtime systems, if separately developed in the future, must not
    depend on the Obsidian application.

## 9.2 Knowledge document quality

Each technical knowledge document should answer, as applicable:

1.  What is it?
2.  Why does it exist?
3.  How does it work internally?
4.  What architecture does it use?
5.  When should it be used?
6.  When should it not be used?
7.  What are its alternatives?
8.  What are its limitations?
9.  What security concerns apply?
10. How is it tested?
11. How is it operated in production?
12. How does it connect to AISDF workflows?

## 9.3 Retrieval design guidance

A future AKIS implementation may use:

1.  Metadata filtering.
2.  Domain and section selection.
3.  Keyword retrieval.
4.  Semantic retrieval when justified.
5.  Dependency-aware retrieval.
6.  Permission filtering.
7.  Deduplication.
8.  Ranking.
9.  Context budgeting.
10. Source/version attachment.

Obsidian does not itself guarantee token savings. Savings come from
modular content, selective retrieval, ranking, deduplication, and
context budgets.

## 9.4 Knowledge freshness

-   Mark fast-changing documentation with a review interval.
-   Prefer official sources.
-   Track technology version applicability.
-   Re-check links and critical technical claims.
-   Retain the last known valid content if an update fails.
-   Mark unverified or stale content clearly.
-   Do not automatically promote a newly ingested document to Approved
    status.

------------------------------------------------------------------------

# 10. AFIAE --- Feature Intelligence and Acquisition Methodology

AFIAE is a framework methodology for discovering and evaluating external
capabilities. It is not an automated purchasing service in this
repository.

## 10.1 Discovery categories

-   APIs.
-   SDKs.
-   Libraries.
-   Plugins.
-   MCP servers.
-   Agent skills.
-   AI models.
-   Developer tools.
-   Infrastructure.
-   Templates.
-   Premium services.
-   Integration connectors.

## 10.2 Workflow

**Requirement → Capability Gap → Discovery → Source Verification →
Feature Evaluation → Pricing/License Review → Security Review →
Compatibility Review → Comparison → Approval → Authorized Acquisition →
Integration → Verification → Monitoring.**

## 10.3 Capability evaluation criteria

-   Relevance to the requirement.
-   Functional completeness.
-   Official source confidence.
-   Maintenance and release activity.
-   Version compatibility.
-   Security posture.
-   License and usage terms.
-   Pricing and total cost.
-   Data handling and privacy.
-   Permissions required.
-   Portability and exit cost.
-   Operational support.
-   Alternatives.
-   Failure and rollback behavior.

## 10.4 Acquisition rules

-   Discovery and comparison may be automated within policy.
-   Installation, credential access, purchases, paid subscriptions, and
    production changes require authorization.
-   No paywall or license bypass.
-   No untrusted installation.
-   No automatic privilege expansion.
-   No credential publication.
-   No silent dependency replacement.

------------------------------------------------------------------------

# 11. AI, Agent, and External Tool Standards

## 11.1 Tool-independent design

AISDF defines common task and verification standards. It must not assume
all AI tools expose the same features or APIs.

Candidate tools to document and evaluate include:

-   Google Antigravity.
-   Cursor.
-   Windsurf.
-   Kiro.
-   Trae.
-   Codex.
-   Claude Code.
-   GitHub Copilot.
-   Cline.
-   Roo Code.
-   Aider.
-   OpenHands.
-   Devin.
-   Replit.
-   Lovable.
-   Bolt.new.
-   v0.

The repository must separate:

-   **Knowledge compatibility:** Can the tool read and follow AISDF
    documents?
-   **Execution compatibility:** Can it perform the required operations
    in its own environment?
-   **Integration compatibility:** Can AISDF or another controller
    interact with it through a verified interface?

These are different claims.

## 11.2 Standard agent task contract

A task contract should include:

-   Task ID.
-   Project ID.
-   Agent role.
-   Objective.
-   Input references.
-   Requirements.
-   Dependencies.
-   Allowed files.
-   Allowed tools.
-   Permission assumptions.
-   Expected output.
-   Acceptance criteria.
-   Budget/deadline where applicable.
-   Verification requirements.
-   Status.
-   Evidence references.

## 11.3 Agent rules

Agent instructions must define:

-   Role and scope.
-   Required context.
-   Expected output format.
-   Allowed tools.
-   Prohibited actions.
-   Approval gates.
-   Security constraints.
-   Handoff requirements.
-   Failure behavior.
-   Verification expectations.

Never present prompt instructions as a substitute for technical access
control.

## 11.4 Collaboration and conflict rules

-   One explicit owner per task.
-   Explicit file ownership for parallel work.
-   Separate branches/worktrees for concurrent edits.
-   No uncontrolled simultaneous edits to the same working directory.
-   Review diffs before merging.
-   Run relevant tests after merging.
-   Escalate conflicting architectural decisions.
-   Record the final decision.

## 11.5 Independent verification

The implementing agent should not be the sole source of acceptance for
critical changes. Use a separate reviewer, test process, or verification
context where practical. Different agents using the same model and
identical context are not automatically independent.

------------------------------------------------------------------------

# 12. Security, Privacy, and Safe Use

## 12.1 Security principles

-   Default deny.
-   Least privilege.
-   Explicit trust boundaries.
-   Project and tenant isolation.
-   Scoped credentials.
-   Secure secret handling.
-   Sandboxed execution.
-   Network restrictions.
-   Dependency verification.
-   Auditability.
-   Human approval for high-impact actions.
-   Emergency stop and recovery.

## 12.2 Threat categories to document

-   Prompt injection.
-   Malicious repository content.
-   Malicious tool output.
-   Credential theft.
-   Secret leakage.
-   Unauthorized file access.
-   Command abuse.
-   Sandbox escape.
-   SSRF.
-   Network exfiltration.
-   Dependency/supply-chain compromise.
-   Tenant boundary violation.
-   Privilege escalation.
-   Destructive migration.
-   Unauthorized deployment.
-   Denial of service.
-   Data retention/deletion failure.

## 12.3 Security documentation requirements

Each security guide should include:

-   Threat.
-   Assets.
-   Trust boundaries.
-   Attack surface.
-   Preconditions.
-   Preventive controls.
-   Detection.
-   Response.
-   Recovery.
-   Verification tests.
-   Residual risk.

## 12.4 Privacy

Guidance must address:

-   Purpose limitation.
-   Data minimization.
-   Consent where required.
-   Retention.
-   Export.
-   Deletion propagation.
-   Derived data and indexes.
-   Backups.
-   Third-party processors.
-   Cross-border transfers.
-   Incident handling.
-   Legal holds.

## 12.5 Responsible disclosure

`SECURITY.md` must state how maintainers receive vulnerability reports,
expected response process, supported versions, and what information
reporters should provide. Do not publish exploitable details before
coordinated disclosure.

------------------------------------------------------------------------

# 13. Data, API, and Integration Engineering Guidance

These are knowledge and design standards for projects using AISDF, not
services built by this repository.

## 13.1 Data modeling

Every project data model should define:

-   Entity identity.
-   Ownership.
-   Attributes.
-   Relationships.
-   Constraints.
-   Validation.
-   Lifecycle.
-   Versioning.
-   Access rules.
-   Retention.
-   Audit requirements.
-   Migration behavior.

## 13.2 API design

Document:

-   API purpose and consumers.
-   Authentication and authorization.
-   Request/response schemas.
-   Validation.
-   Versioning.
-   Error format.
-   Pagination.
-   Rate limits.
-   Timeouts.
-   Idempotency.
-   Deprecation.
-   Observability.
-   Contract tests.

## 13.3 Event design

Document:

-   Event name and owner.
-   Schema and version.
-   Producer and consumers.
-   Delivery guarantees.
-   Ordering requirements.
-   Duplicate handling.
-   Retry policy.
-   Dead-letter handling.
-   Replay.
-   Retention.
-   Privacy classification.

## 13.4 External integration lifecycle

**Register → Authenticate → Discover → Evaluate → Approve → Connect →
Verify → Monitor → Upgrade → Revoke.**

------------------------------------------------------------------------

# 14. Testing, Verification, and Evidence Standards

## 14.1 Test categories

-   Unit.
-   Integration.
-   Contract.
-   End-to-end.
-   Regression.
-   Acceptance.
-   Performance.
-   Load.
-   Stress.
-   Spike.
-   Endurance.
-   Accessibility.
-   Visual.
-   Browser/device compatibility.
-   Recovery.
-   Security.
-   Dependency.
-   Secret scanning.
-   Infrastructure.
-   AI behavior.
-   Retrieval quality.
-   Agent workflow.

Select tests based on project risk and requirements. Not every project
needs every test category.

## 14.2 Traceability chain

**Requirement → Task → Code Change → Test → Verification → Evidence →
Release.**

## 14.3 Evidence record

An evidence record should identify:

-   Evidence ID.
-   Project.
-   Requirement.
-   Task.
-   Source revision.
-   Environment.
-   Test or verification procedure.
-   Runner/tool.
-   Timestamp.
-   Result.
-   Logs and artifacts.
-   Status.
-   Reviewer where applicable.

Evidence for an older revision must not be used to claim a newer
revision is verified.

## 14.4 Quality gates

Critical failures cannot be hidden by averaging a quality score. Define
blockers for security, data integrity, authorization, requirement
failures, and release safety.

------------------------------------------------------------------------

# 15. Delivery, Operations, and Maintenance Guidance

The repository documents how projects should approach:

-   Source control.
-   Branching and code review.
-   CI/CD.
-   Build reproducibility.
-   Artifact provenance.
-   SBOM and dependency scanning where appropriate.
-   Environment configuration.
-   Secrets management.
-   Release versioning.
-   Feature flags.
-   Canary, rolling, and blue-green deployments where appropriate.
-   Deployment authorization.
-   Post-deployment verification.
-   Monitoring.
-   SLOs/SLIs.
-   Incident response.
-   Backup and restore.
-   Disaster recovery.
-   Rollback.
-   Maintenance windows.
-   Deprecation and end-of-life.

AISDF must not prescribe universal SLO numbers without project
requirements and measurements.

------------------------------------------------------------------------

# 16. Technology and Tool Evaluation Policy

## 16.1 Technology selection criteria

Evaluate:

-   Requirement fit.
-   Compatibility.
-   Security.
-   Performance.
-   Scalability.
-   Reliability.
-   Maintainability.
-   Maturity.
-   Community and support.
-   License.
-   Pricing and total cost.
-   Data portability.
-   Vendor lock-in.
-   Upgrade path.
-   End-of-life risk.

## 16.2 Tool catalog policy

The repository may include a catalog of tools such as Antigravity,
Cursor, Codex, Claude Code, Windsurf, Kiro, Figma, GitHub, Obsidian,
Postman, and others.

Every entry must state:

-   What it is.
-   What problem it solves.
-   Relevant capabilities.
-   Limitations.
-   Supported integration method, if verified.
-   Pricing model with verification date.
-   License/terms reference.
-   Data and privacy considerations.
-   Alternatives.
-   Last checked date.

Do not hard-code pricing in stable methodology documents. Keep dynamic
pricing in a separately reviewed catalog.

Do not imply endorsement, partnership, sponsorship, or official
integration without evidence.

------------------------------------------------------------------------

# 17. Templates and Examples

The repository should provide reusable templates.

## 17.1 Project templates

-   Project Intake.
-   Problem and Solution Specification.
-   Project X-Ray.
-   Existing Project Assessment.
-   Product Requirements Document.
-   Functional Requirements.
-   Non-Functional Requirements.
-   MVP Scope.
-   Feature Inventory.
-   User Stories.
-   Acceptance Criteria.
-   Risk Register.
-   Product Roadmap.
-   Project State Summary.

## 17.2 Engineering templates

-   UX Research.
-   User Journey.
-   User Flow.
-   Design System Specification.
-   Technology Evaluation.
-   Architecture Specification.
-   Architecture Decision Record.
-   Component Specification.
-   Database Design.
-   API Specification.
-   Event Contract.
-   Integration Specification.
-   Threat Model.
-   Test Plan.
-   Verification Report.
-   Deployment Plan.
-   Incident Report.
-   Recovery Plan.

## 17.3 AI and agent templates

-   Agent Definition.
-   Agent Task Contract.
-   Prompt Specification.
-   Provider Evaluation.
-   Tool/Connector Evaluation.
-   Agent Handoff.
-   Agent Conflict Report.
-   Execution Report.
-   AI Evaluation Report.
-   Independent Verification Report.

## 17.4 Example projects

Start with small, illustrative examples:

1.  Static website.
2.  CRUD web application.
3.  SaaS application with tenant boundaries.
4.  Backend API.
5.  Mobile application.
6.  AI/RAG application.
7.  Existing project improvement.
8.  Product transformation.
9.  Security-sensitive workflow.
10. Multi-agent controlled implementation.

Examples must be labeled illustrative, not production-certified
reference implementations.

------------------------------------------------------------------------

# 18. Repository Validation Tooling

This repository may include lightweight scripts under `tools/` and
validation cases under `tests/`.

## 18.1 Required validation checks

  Check                     Purpose
  ------------------------- -----------------------------------------
  Markdown lint             Consistent Markdown
  YAML parse                Valid front matter
  JSON validation           Valid structured registries
  Schema validation         Registry records match schemas
  Document ID check         No duplicate IDs
  Required metadata check   Required fields exist
  Link check                Internal links resolve
  Registry/path check       Registry paths exist
  Status check              Drafts not presented as approved
  Source metadata check     Technical claims have source metadata
  Template validation       Required fields are present
  Navigation check          Domain indexes point to valid documents

## 18.2 Suggested tooling

Use simple, maintainable tools. Candidate tools include:

-   Markdownlint.
-   Prettier for supported formatting.
-   A YAML parser.
-   JSON Schema validator.
-   Link checker.
-   Small scripts in Python or Node.js.

Choose one implementation language for repository validation scripts
unless a clear reason requires more than one. Pin tool versions and
document how to run checks locally.

## 18.3 CI workflow

A pull request should run:

1.  Markdown lint.
2.  YAML/JSON parse.
3.  Schema validation.
4.  Duplicate ID detection.
5.  Internal link validation.
6.  Registry consistency.
7.  Required metadata checks.
8.  Template validation.
9.  Example validation where automated.
10. Documentation build, if a documentation site is introduced.

CI validates repository quality. It does not prove that the engineering
advice is universally correct.

------------------------------------------------------------------------

# 19. GitHub Collaboration and Governance

## 19.1 Required repository files

### README.md

Must explain:

-   What AISDF is.
-   What it is not.
-   Who should use it.
-   Core principles.
-   Development paths.
-   Repository navigation.
-   Quick-start adoption path.
-   Contribution links.
-   License.
-   Current maturity and limitations.

### CONTRIBUTING.md

Must explain:

-   Issue-first contribution for significant changes.
-   Branch naming.
-   Document ID rules.
-   Metadata requirements.
-   Writing style.
-   Source requirements.
-   Testing requirements.
-   Pull request requirements.
-   Review and approval process.

### CODE_OF_CONDUCT.md

Defines respectful participation and enforcement.

### GOVERNANCE.md

Defines maintainer roles, decision-making, standards approval, release
authority, and dispute resolution.

### SECURITY.md

Defines vulnerability reporting and response.

### SUPPORT.md

Explains where users ask questions, report documentation problems, or
request changes.

### CHANGELOG.md

Records user-visible framework changes by release.

### CITATION.cff

Provides citation metadata for academic and research use.

## 19.2 GitHub issue types

Recommended issue categories:

-   Bug in documentation.
-   Incorrect or stale technical guidance.
-   New engineering topic.
-   Methodology improvement.
-   Template request.
-   Agent rule proposal.
-   Tool compatibility report.
-   Security issue.
-   Benchmark proposal.
-   Governance proposal.

## 19.3 Pull request requirements

Every PR should state:

-   Purpose.
-   Scope.
-   Related issue.
-   Affected domains.
-   Documents added/changed/retired.
-   Source verification.
-   Security/privacy impact.
-   Compatibility impact.
-   Validation performed.
-   Migration or deprecation notes.
-   Required reviewer approval.

## 19.4 CODEOWNERS

Assign maintainers by domain when the project has enough maintainers.
Until then, use a small maintainer group and avoid fictitious ownership
assignments.

## 19.5 Decision authority

-   Contributors propose changes.
-   Domain maintainers review technical content.
-   Security maintainers review security-sensitive guidance.
-   Project maintainers approve cross-domain or framework-level changes.
-   Release maintainers publish versions.

The exact people and team names must be filled in by repository owners.

------------------------------------------------------------------------

# 20. Open-Source Licensing and Intellectual Property

## 20.1 Recommended default

Evaluate **Apache License 2.0** as the preferred initial license because
it is permissive and includes an express patent grant. MIT is a simpler
permissive alternative.

This is a project recommendation, not legal advice. The repository owner
should confirm ownership of all contributed material and review
third-party content before publishing.

## 20.2 Licensing rules

-   Put the selected license in the root `LICENSE`.
-   Add copyright/attribution notices where required.
-   Preserve third-party license obligations.
-   Do not copy proprietary documentation or large copyrighted passages.
-   Prefer original explanations and links to official sources.
-   Record third-party assets and licenses.
-   Define a contribution policy.
-   Consider a Developer Certificate of Origin (DCO) or Contributor
    License Agreement only after an explicit governance decision.

## 20.3 Trademarks

AISDF may refer to third-party product names for compatibility and
descriptive purposes. Do not use third-party logos or imply endorsement
without permission.

------------------------------------------------------------------------

# 21. Versioning and Release Policy

## 21.1 Framework version

Use Semantic Versioning:

-   **MAJOR:** Breaking methodology, schema, or normative-rule changes.
-   **MINOR:** Backward-compatible additions.
-   **PATCH:** Corrections and non-breaking clarifications.

For a documentation framework, define what counts as a breaking change
in `GOVERNANCE.md`.

## 21.2 Document versions

Individual documents may have their own version and status. The
repository release records a coherent snapshot of all approved
documents.

## 21.3 Release channels

-   Draft/pre-release.
-   Stable.
-   Long-term-support (only if maintainers commit to supporting it).

Do not promise LTS until maintenance capacity exists.

## 21.4 Deprecation

A deprecated document must state:

-   Why it is deprecated.
-   Replacement document, if any.
-   Effective version/date.
-   Migration guidance.
-   Retirement conditions.

Never silently delete an important normative standard without recording
the change.

------------------------------------------------------------------------

# 22. Open-Source Adoption Workflow

A new user should be able to adopt AISDF without installing a
proprietary AISDF application.

## 22.1 Quick adoption

1.  Read the root README.
2.  Select Beginner, Developer, Team, or Enterprise Governance guidance.
3.  Choose Path A for a new product or Path B for an existing project.
4.  Copy the relevant templates into the user's own project repository.
5.  Complete the project intake.
6.  Record assumptions and constraints.
7.  Follow the relevant workflow.
8.  Select compatible AI tools if desired.
9.  Give the AI tool the relevant AISDF rules and knowledge.
10. Review all plans and approvals.
11. Implement in the user's own development environment.
12. Run tests and collect evidence.
13. Maintain the project's own source of truth.

## 22.2 AI tool adoption

AISDF should provide a tool-independent core instruction file and
optional tool-specific adapters/rules.

Do not make the core framework dependent on one IDE's configuration
format.

Suggested structure:

``` text
30-AGENT-RULES-AND-VERIFICATION/
├── CORE/
│   ├── AISDF-CORE-RULES.md
│   ├── CHANGE-ONLY-LAW.md
│   ├── NO-AI-SLOPE.md
│   ├── APPROVAL-FIRST.md
│   ├── EVIDENCE-OVER-CLAIMS.md
│   └── SECURITY-BOUNDARIES.md
│
└── ADAPTERS/
    ├── ANTIGRAVITY/
    ├── CURSOR/
    ├── CLAUDE-CODE/
    ├── CODEX/
    ├── WINDSURF/
    ├── KIRO/
    ├── CLINE/
    └── GENERIC/
```

Each adapter must identify its supported features, version assumptions,
limitations, and last verification date. A generic adapter remains
available for tools not listed.

------------------------------------------------------------------------

# 23. Repository Maintenance

## 23.1 Maintenance responsibilities

-   Review technical sources.
-   Update version-specific guidance.
-   Check broken links.
-   Review security guidance.
-   Validate schemas and templates.
-   Retire obsolete material.
-   Resolve duplicate documents.
-   Review tool compatibility.
-   Maintain benchmark scenarios.
-   Publish release notes.

## 23.2 Review frequency

Use risk-based review intervals rather than one universal schedule.

  -----------------------------------------------------------------------
  Content                             Suggested review
  ----------------------------------- -----------------------------------
  Security and vulnerability guidance Frequent and event-driven

  AI tools and provider capabilities  Frequent

  Framework methodology               Periodic

  Stable engineering fundamentals     Less frequent

  Version-specific technology guides  Around supported-version changes

  Legal and compliance guidance       When laws/standards change and on
                                      scheduled review
  -----------------------------------------------------------------------

Every document must show its last verification date when it makes
time-sensitive claims.

## 23.3 Knowledge change workflow

**Propose → Source Check → Review → Validate → Approve → Merge → Release
→ Monitor.**

------------------------------------------------------------------------

# 24. Repository Maturity and Acceptance Criteria

The repository is ready for its first public release when all mandatory
criteria below are satisfied.

## 24.1 V1.0 release gates

### Governance

-   [ ] License selected and added.
-   [ ] Contribution policy published.
-   [ ] Code of conduct published.
-   [ ] Governance policy published.
-   [ ] Security reporting instructions published.
-   [ ] Maintainer ownership assigned.

### Structure

-   [ ] Root README complete.
-   [ ] All 31 domain landing pages created or explicitly marked
    planned.
-   [ ] Domain indexes exist.
-   [ ] Document IDs are unique.
-   [ ] Metadata conventions documented.

### Core framework

-   [ ] Path 0 documented.
-   [ ] Path A documented.
-   [ ] Path B documented.
-   [ ] Product transformation documented.
-   [ ] Mandatory framework laws documented.
-   [ ] Project X-Ray workflow documented.
-   [ ] Requirements and approval workflow documented.

### Engineering knowledge

-   [ ] Core architecture guidance published.
-   [ ] Core security guidance published.
-   [ ] Core testing and verification guidance published.
-   [ ] Core data/API guidance published.
-   [ ] Deployment and operations guidance published.
-   [ ] Sources and verification dates included where needed.

### AI and tools

-   [ ] Core agent rules published.
-   [ ] Task contract schema published.
-   [ ] External tool evaluation policy published.
-   [ ] Tool-specific adapters labeled by verification status.
-   [ ] No unsupported integration claims.

### Templates and examples

-   [ ] Project intake template published.
-   [ ] PRD template published.
-   [ ] Architecture template published.
-   [ ] ADR template published.
-   [ ] Test plan and verification templates published.
-   [ ] At least one complete example workflow published.

### Repository quality

-   [ ] Markdown lint passes.
-   [ ] YAML/JSON validation passes.
-   [ ] Internal links pass.
-   [ ] Duplicate IDs check passes.
-   [ ] Registry validation passes.
-   [ ] License and attribution review completed.
-   [ ] Pull request checks are enabled.

## 24.2 What V1.0 does not require

-   Building an AISDF SaaS application.
-   Implementing a hosted AI orchestrator.
-   Creating a database server.
-   Building an IDE.
-   Integrating every AI coding tool.
-   Providing an automated sandbox service.
-   Guaranteeing production outcomes.
-   Claiming compliance certification.

------------------------------------------------------------------------

# 25. Recommended Build Order for the GitHub Repository

This is the order for creating repository content---not an application
development roadmap.

  -----------------------------------------------------------------------
  Phase                   Repository work         Completion output
  ----------------------- ----------------------- -----------------------
  R0                      Repository governance   License, README,
                                                  contribution and
                                                  security files

  R1                      Repository skeleton     Root structure, domain
                                                  READMEs and indexes

  R2                      Core methodology        Path 0, A, B,
                                                  transformation and
                                                  framework laws

  R3                      Project and             Intake, X-Ray,
                          requirements knowledge  requirements and
                                                  approval standards

  R4                      Product and design      Product, UX/UI and
                          knowledge               design standards

  R5                      Engineering knowledge   Technology,
                                                  architecture, data,
                                                  APIs and platform
                                                  guidance

  R6                      AKIS knowledge base     Metadata, document
                                                  standards, retrieval
                                                  methodology

  R7                      AFIAE methodology       Discovery, evaluation,
                                                  licensing, security and
                                                  acquisition

  R8                      AI and agent standards  Provider-neutral agent
                                                  rules, task contracts
                                                  and evaluation

  R9                      Execution and security  Harness requirements,
                                                  threat models and
                                                  permission standards

  R10                     Quality and operations  Testing, evidence,
                                                  deployment, reliability
                                                  and maintenance

  R11                     Templates and examples  Reusable templates and
                                                  complete sample
                                                  workflows

  R12                     Repository validation   Schemas, scripts, tests
                                                  and GitHub Actions

  R13                     Public release          Review, attribution,
                          preparation             release notes and V1.0
                                                  tag
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 26. Final Repository Architecture

The repository is the deliverable. Its contents should be organized
around these six outcomes:

``` text
                    AISDF OPEN-SOURCE REPOSITORY
                                  |
       +--------------------------+--------------------------+
       |                          |                          |
       v                          v                          v
  METHODOLOGY                KNOWLEDGE BASE             AI RULES
  Path 0 / A / B             Engineering topics         Agent contracts
  Project lifecycle          Standards and sources      Tool adapters
       |                          |                          |
       +--------------------------+--------------------------+
                                  |
       +--------------------------+--------------------------+
       |                          |                          |
       v                          v                          v
   TEMPLATES                  REGISTRIES                EXAMPLES
   PRD / ADR / Tests          Tools / Tech / Docs       Reference workflows
       |                          |                          |
       +--------------------------+--------------------------+
                                  |
                                  v
                       REPOSITORY VALIDATION
                                  |
                                  v
                       GITHUB GOVERNANCE
                                  |
                                  v
                       OPEN-SOURCE RELEASES
```

------------------------------------------------------------------------

# 27. Final Decisions and Items Requiring Owner Approval

The blueprint is detailed, but the following project-owner decisions
must be made before public release:

  -----------------------------------------------------------------------
  ID                      Decision                Recommendation
  ----------------------- ----------------------- -----------------------
  OPEN-001                License                 Apache-2.0, subject to
                                                  ownership review

  OPEN-002                Repository visibility   Public

  OPEN-003                Default branch          `main`

  OPEN-004                Documentation format    Markdown + YAML front
                                                  matter

  OPEN-005                Knowledge authoring     Obsidian optional; Git
                                                  Markdown canonical

  OPEN-006                Versioning              Semantic Versioning

  OPEN-007                Contribution model      Issue + pull request

  OPEN-008                Governance              Maintainer-led,
                                                  transparent decisions

  OPEN-009                Tool independence       Mandatory

  OPEN-010                Application             Explicitly out of scope
                          implementation          

  OPEN-011                Documentation website   Optional future
                                                  distribution, not
                                                  required for V1

  OPEN-012                Automated repository    Required for V1
                          checks                  

  OPEN-013                Tool-specific rules     Optional adapters;
                                                  generic core is
                                                  mandatory

  OPEN-014                Compliance claims       Prohibited without
                                                  independent evidence
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 28. Final Definition

**AISDF is an open-source, tool-independent AI-assisted software
engineering framework distributed through a GitHub repository.**

It provides the methodology, engineering knowledge, standards, agent
instructions, templates, schemas, examples, validation rules, and
governance required to guide software development from problem
definition through production maintenance.

Its core deliverable is not an application.

Its core deliverable is a **reusable engineering framework that people
and compatible AI development tools can adopt inside their own software
projects.**

## Final scope statement

> AISDF Repository V1.0 will publish a complete, modular, versioned, and
> maintainable open-source software engineering framework. It will not
> build or host the AISDF application. It will provide the knowledge,
> rules, workflows, templates, schemas, examples, and repository
> validation required for developers and AI tools to apply AISDF
> independently.

**Recommended next action:** Create the GitHub repository skeleton and
governance files first, then publish the core methodology before filling
all 31 knowledge domains. Do not create empty documentation simply to
claim that every domain is complete.
