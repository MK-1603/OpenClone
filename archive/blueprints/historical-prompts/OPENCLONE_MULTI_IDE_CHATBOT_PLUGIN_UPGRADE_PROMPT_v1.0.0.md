# OpenClone — Multi-IDE & Chatbot Plugin Integration Upgrade
**Execution prompt for Antigravity | Version 1.0.0**

## Mission

Upgrade the existing OpenClone repository so developers can install and use OpenClone through the IDEs and AI coding/chat surfaces already targeted by this repository.

Target integrations to verify against the actual repository and current official platform documentation:

- Google Antigravity
- Claude Code
- OpenAI Codex (CLI, desktop/app, and supported IDE surfaces)
- Cursor
- ChatGPT (plugin/MCP surface)

Do not assume every surface uses the same plugin format. Build one reusable OpenClone capability layer and thin, native distribution adapters for each supported host.

The goal is **one OpenClone product, one capability implementation, multiple host-native installation experiences** — not five duplicated implementations.

---

## 1. Non-negotiable execution rules

1. Start by inspecting the complete repository, Git status, existing adapter implementations, package manifests, runtime entry points, skills, workflows, security policies, tests, and documentation.
2. Do not overwrite or delete existing functionality simply to make the integration look clean.
3. Do not create duplicate business logic, duplicate tool implementations, or separate runtime engines per IDE.
4. Do not assume a platform supports a feature. Verify each integration against current official documentation and record the source URL and verification date in the integration documentation.
5. Treat platform capabilities as versioned and host-specific. Keep compatibility metadata and installation instructions per host.
6. Preserve existing naming, package conventions, versioning, and architecture unless an evidence-based migration is necessary.
7. Do not add an API key, token, private URL, credential, or secret to source control, plugin manifests, examples, logs, or documentation.
8. Do not execute destructive operations, publish to marketplaces, create releases, commit, or push without explicit authorization.
9. If a host integration cannot be implemented or tested in the current environment, implement only the verified package/configuration pieces and clearly report the unverified portion.
10. Avoid feature creep. Build the smallest secure integration surface that makes existing OpenClone capabilities usable.

---

## 2. Target architecture

Use this logical architecture, adapting names and locations to the repository's actual structure:

```text
IDE / CHAT HOSTS
  ├── Antigravity native plugin
  ├── Claude Code plugin + marketplace
  ├── Codex plugin package
  ├── Cursor Agent Plugin / Cursor-specific plugin where required
  └── ChatGPT plugin integration
              |
              v
HOST ADAPTERS
  ├── Native manifests and metadata
  ├── Host-specific skills / commands / rules / hooks
  ├── Installation and configuration
  └── Compatibility checks
              |
              v
PORTABLE OPENCLONE CAPABILITIES
  ├── Shared skills and workflows
  ├── Shared agent instructions
  ├── Shared resource references
  └── Host-neutral capability definitions
              |
              v
OPENCLONE CORE SERVICE
  ├── MCP server (primary interoperability interface)
  ├── Authentication and authorization
  ├── Tool registry and input validation
  ├── Policy enforcement and approval gates
  ├── Audit logging and observability
  └── Existing OpenClone runtime / domain engines
              |
              v
EXISTING OPENCLONE SYSTEM
```

### Architectural principles

- **MCP is the primary shared tool interface** where the host supports it.
- **Skills are workflow guidance**, not a second implementation of the core.
- **Native plugins are packaging and UX adapters**, not independent products.
- Keep host-neutral skills and resources portable where the relevant open standard allows it.
- Use native manifests, commands, hooks, agents, and marketplace metadata only where a host requires or benefits from them.
- Host-specific code must call the same OpenClone core service and policy layer.
- Do not expose every internal engine as an individual tool. Design a small, task-oriented tool surface.
- The MCP server must remain useful without any optional graphical UI.
- Do not make a host plugin depend on another host's plugin runtime.

---

## 3. First deliver an integration capability matrix

Before implementation, inspect the current repository and produce a matrix with these columns:

| Host | Existing adapter? | Native package format | MCP support | Skills/workflows | Host-specific features | Install method | Test method | Status |
|---|---|---|---|---|---|---|---|---|

Include Antigravity, Claude Code, Codex, Cursor, and ChatGPT.

For each host:
- Verify current official documentation.
- Identify exactly which features are supported by that host and the relevant version/surface.
- Separate confirmed support from assumptions.
- Record whether it supports a portable Agent Plugin format or requires a native format.
- Identify whether the same package can be reused or a host-specific manifest/overlay is required.
- Document any limitations, approval requirements, authentication constraints, and distribution restrictions.

Do not begin packaging until this matrix is complete.

---

## 4. Build the shared OpenClone MCP service

Inspect whether an MCP server already exists. Reuse and improve it rather than creating a second server.

If it does not exist, implement a minimal production-minded MCP server using the language and runtime conventions already established by the repository.

### Required service capabilities

Expose only stable, validated, user-facing capabilities that already exist or can be implemented safely. Candidate tools, subject to repository audit:

- `openclone_get_status` — return runtime and integration health.
- `openclone_search_knowledge` — search approved OpenClone knowledge sources.
- `openclone_explain_concept` — retrieve and explain a supported concept/domain/engine.
- `openclone_run_workflow` — execute an explicitly supported workflow.
- `openclone_validate_project` — run available project validation checks.
- `openclone_get_guidance` — retrieve relevant standards, templates, or project guidance.
- `openclone_list_capabilities` — list capabilities available to the current user/session.

Do not implement a tool merely because it appears in this list. Confirm the underlying capability exists, define its contract, and implement only what is justified.

### MCP engineering requirements

- Use the official MCP SDK for the selected implementation language.
- Prefer Streamable HTTP for hosted/remote deployment where supported; support stdio for local developer workflows where useful.
- Validate every input with strict schemas.
- Return predictable structured output with stable error codes.
- Apply timeouts, bounded output sizes, pagination for large results, and cancellation where supported.
- Separate read-only tools from state-changing tools.
- Require explicit confirmation/approval for destructive or externally visible actions.
- Enforce authorization on the server, not only in prompt instructions.
- Do not trust model-generated paths, shell commands, URLs, or identifiers.
- Prevent path traversal, arbitrary file access, command injection, SSRF, and unauthorized workspace access.
- Never return secrets or raw environment variables.
- Add structured audit events without logging credentials or sensitive payloads.
- Add health/readiness checks and graceful shutdown.
- Add unit, integration, and protocol-level tests.
- Document local and hosted configuration separately.

### Tool design

For every tool define:
- Name and purpose.
- JSON input schema.
- Output schema.
- Read/write classification.
- Required permission.
- Approval behavior.
- Timeout and resource limits.
- Error codes.
- Audit event.
- Tests.

Keep tools narrow, composable, and understandable. Do not expose a generic `execute_shell`, unrestricted filesystem tool, arbitrary SQL tool, or unrestricted HTTP proxy.

---

## 5. Create the shared portable plugin capabilities

Create or consolidate a host-neutral plugin source directory only after examining existing `skills/`, `prompts/`, `workflows/`, `adapters/`, and resource directories.

Package:
- A concise OpenClone overview skill.
- A capability-discovery skill.
- A knowledge-search skill.
- A workflow-execution skill, only for workflows actually supported.
- A project-validation skill, only if validation exists.
- Shared reference material and examples required by those skills.

Each skill must have:
- Clear name and description.
- Explicit activation/use conditions.
- Step-by-step workflow.
- Required inputs and expected outputs.
- Safety boundaries.
- Examples.
- A clear statement of when not to use it.

Avoid copying entire documentation libraries into every plugin. Use references or MCP retrieval for larger knowledge sources. Keep context usage efficient.

---

## 6. Implement each host adapter

### A. Google Antigravity

- Inspect the current Antigravity adapter.
- Build a valid native Antigravity plugin package using the currently documented manifest and directory conventions.
- Include shared skills, MCP configuration, and only necessary Antigravity-specific rules, agents/subagents, hooks, and suggested prompts.
- Verify manifest fields against the official schema.
- Add local validation/install instructions using the currently documented Antigravity CLI or UI.
- Do not assume that a generic Cursor or Claude manifest is a valid Antigravity manifest.

### B. Claude Code

- Inspect the current Claude Code adapter.
- Build a Claude Code plugin with the required plugin manifest, skills, commands, agents, hooks, and MCP configuration where justified.
- Add marketplace metadata and a repository-based installation path if supported by the current official format.
- Keep hooks minimal, transparent, safe, and opt-in where appropriate.
- Document installation, update, uninstall, permissions, and troubleshooting.
- Do not silently execute scripts during installation.

### C. OpenAI Codex

- Inspect the existing Codex adapter.
- Verify current Codex plugin support separately for CLI, desktop/app, and IDE extension surfaces.
- Build the currently supported Codex-compatible plugin package and manifest.
- Package portable skills and MCP configuration, plus Codex-specific metadata only where required.
- Document plugin installation/discovery, session restart requirements, MCP approval configuration, and supported surfaces.
- Do not claim that all Codex surfaces have identical plugin behavior.

### D. Cursor

- Inspect the current Cursor adapter.
- Prefer the portable Agent Plugin format for shared skills and MCP configuration when supported.
- Add a Cursor-native plugin overlay only for features that require Cursor-specific rules, commands, agents, hooks, or variables.
- Keep shared capabilities in one canonical location; generate or reference host packages without maintaining duplicate skill content.
- Document local testing, workspace/user installation, updates, and uninstall.

### E. ChatGPT

- Treat ChatGPT as a separate hosted plugin/MCP integration, not as an IDE plugin.
- Reuse the same remote OpenClone MCP service where compatible.
- Verify current ChatGPT plugin creation, authentication, tool, and optional UI requirements.
- Provide a secure hosted HTTPS MCP endpoint and documented connection setup.
- Use OAuth or another supported secure authentication mechanism where user identity and protected data require it.
- Do not place server secrets in a client-side manifest.
- Add optional ChatGPT UI only if a real user workflow benefits from an interactive view; do not build UI merely for appearance.
- Clearly document feature limitations compared with IDE integrations.

---

## 7. Plugin distribution and repository layout

Inspect the current structure first. Do not force this exact layout if the repository already has a better canonical arrangement.

A possible organized layout:

```text
plugins/
├── shared/
│   ├── skills/
│   ├── references/
│   └── examples/
├── antigravity/
│   ├── plugin manifest
│   ├── MCP configuration
│   ├── agents/
│   ├── rules/
│   └── README.md
├── claude-code/
│   ├── plugin manifest
│   ├── .mcp.json
│   ├── commands/
│   ├── agents/
│   ├── hooks/
│   └── README.md
├── codex/
│   ├── plugin manifest
│   ├── MCP configuration
│   └── README.md
├── cursor/
│   ├── portable plugin manifest
│   ├── optional Cursor-native overlay
│   └── README.md
└── chatgpt/
    ├── connection guide
    ├── deployment configuration
    └── README.md
```

The shared directory is the canonical source for portable skill content. If a host requires copied or generated files, create a deterministic packaging script and verify generated files are in sync. Do not manually maintain multiple divergent copies.

Add:
- A root plugin catalog/index.
- Per-host installation guides.
- A compatibility matrix.
- A plugin development guide.
- A release/versioning guide.
- A troubleshooting guide.
- A security and permissions guide.

Keep root README concise. Add a clear “Integrations” section that links to the integration guide rather than embedding a large technical catalog.

---

## 8. Security and privacy requirements

Perform a threat model for the MCP server and every host adapter.

At minimum:
- Least-privilege tool permissions.
- Read-only by default.
- Explicit approval for writes, external requests, destructive operations, and deployment actions.
- Authentication and authorization for hosted access.
- Per-user and per-workspace isolation.
- No cross-workspace data leakage.
- Input validation and output sanitization.
- Safe handling of prompt injection from repository files, external content, and MCP results.
- SSRF and path traversal protections.
- Rate limits and request size limits.
- Secret redaction and secure secret storage.
- Dependency and manifest validation.
- Audit logging with privacy-aware retention.
- No hidden telemetry.
- No automatic shell execution or background modification of user projects.
- Clear user-facing permissions and data-handling documentation.

Do not claim a security property unless it is implemented and tested.

---

## 9. Testing and quality gates

Create a test plan and implement the tests that can run in the current environment.

Required checks:
1. Shared skills lint/metadata validation.
2. Every plugin manifest validates against its official schema.
3. MCP server starts successfully in local mode.
4. MCP tool discovery returns only expected tools.
5. Each tool validates valid and invalid inputs.
6. Authorization denies unauthorized operations.
7. Read-only tools do not mutate state.
8. Write tools require the configured approval.
9. No secrets appear in logs or test output.
10. Host package paths resolve correctly.
11. Packaging scripts produce reproducible outputs.
12. Existing repository tests and checks still pass.
13. Installation instructions are checked against actual package contents.
14. Compatibility limitations are documented.

Where a host application is unavailable, label the test **not run**. Never report it as passed.

---

## 10. Documentation and user experience

Create a simple integration landing page that answers:
- What is OpenClone?
- Which IDEs and chat surfaces are supported?
- What can OpenClone do inside each host?
- How do I install it?
- What permissions does it request?
- How do I configure authentication?
- How do I update or uninstall it?
- Where do I report an issue?

For each host, provide:
- Prerequisites.
- Installation steps.
- Configuration example with placeholders only.
- First-run test prompt.
- Expected result.
- Permission explanation.
- Update and uninstall instructions.
- Troubleshooting.
- Known limitations.

Use accurate, modest claims. Do not advertise features that are not implemented.

---

## 11. Implementation phases

Execute in this order. After each phase, run relevant checks and report results.

### Phase 0 — Audit and design
- Inspect repository and Git status.
- Map existing adapters and capabilities.
- Verify official host documentation.
- Produce the capability matrix, architecture decision record, migration plan, and risk list.
- Identify code that can be reused.
- Do not modify files until the audit is complete.

### Phase 1 — Shared capability layer
- Establish canonical shared skills and resources.
- Define tool contracts and permissions.
- Reuse or implement the MCP server.
- Add tests and local developer configuration.

### Phase 2 — Host packaging
- Implement Antigravity, Claude Code, Codex, and Cursor packages.
- Add ChatGPT remote MCP connection instructions and hosted deployment configuration.
- Use native formats where required.
- Generate repeated content from canonical sources.

### Phase 3 — Security and validation
- Run threat-model review.
- Add/complete auth, authorization, approval, validation, logging, and rate limits.
- Validate manifests and MCP behavior.
- Run all existing and new tests.

### Phase 4 — Documentation and release readiness
- Create integration landing page and per-host guides.
- Update root README with a short integrations section.
- Add versioning and release instructions.
- Produce a final compatibility and test report.

Do not publish marketplace packages or deploy a public service unless explicitly authorized.

---

## 12. Acceptance criteria

The upgrade is complete only when:

- There is one canonical OpenClone capability implementation.
- All five target surfaces have an evidence-based support status.
- Each supported host has the correct native or portable package/configuration.
- Shared skills are not manually duplicated and allowed to drift.
- The MCP service exposes only documented, validated, permission-controlled tools.
- Hosted ChatGPT access is secured and does not expose secrets.
- Installation, configuration, update, and uninstall steps are documented.
- Plugin manifests and package paths validate.
- Automated tests pass where executable.
- Unavailable host tests are explicitly marked not run.
- Existing OpenClone functionality and tests remain intact.
- No unsupported features or marketplace publication claims appear in the README.
- No commit, push, release, or public deployment occurs without authorization.

---

## 13. Final report format

At completion, report:

1. Repository audit findings.
2. Existing integrations reused.
3. New/updated files.
4. Shared MCP capabilities implemented.
5. Host-by-host status: implemented / partial / documented only / blocked.
6. Official documentation references and verification date.
7. Security controls implemented.
8. Tests run, passed, failed, and not run.
9. Any migration or compatibility concerns.
10. Exact local installation steps for each supported host.
11. Remaining work, ordered by priority.
12. Confirmation that no commit, push, marketplace publication, or deployment was performed.

**Start with Phase 0. Do not skip the audit and do not implement speculative integrations.**
