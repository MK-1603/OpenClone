# OpenClone — Global AI IDE, Agent & Chat Platform Integration Upgrade
**Single master execution prompt for Antigravity | Version 1.1.0**

## Mission

Upgrade OpenClone into a genuinely cross-platform, multi-agent, multi-model, multi-provider framework that can be used from a broad ecosystem of AI coding IDEs, editors, terminal agents, and developer environments—and provide a unified, provider-agnostic chatbot experience comparable in interaction scope to ChatGPT, Claude, Gemini, Grok, Qwen, DeepSeek, and other supported assistants.

This is an **integration and compatibility upgrade of the existing OpenClone repository**, not a greenfield rewrite. Preserve the existing architecture, governance, Taste Skill, global anti-AI-slop work, domain standards, workflows, and working integrations unless an evidence-backed change is necessary.

The goal is not to claim that OpenClone is itself ChatGPT, Claude, or an IDE. The goal is to make OpenClone's reusable instructions, skills, agents, tools, workflows, governance, and optional chat interface accessible through supported integration mechanisms—with honest capability boundaries.

---

# 1. First principles — understand the product correctly

OpenClone must separate three concepts that are related but are **not interchangeable**:

### A. AI development environment adapters
Connect OpenClone to the user's coding environment or coding agent. Examples include:
- Google Antigravity
- Claude Code
- OpenAI Codex CLI and supported Codex environments
- Qwen Code
- Gemini CLI / Antigravity CLI, where currently supported
- Kiro
- Kilo Code
- Cursor
- Visual Studio Code and compatible editors
- Windsurf / any successor product or renamed environment verified at implementation time
- Zed
- Cline
- Roo Code
- OpenCode
- Aider
- GitHub Copilot (supported instruction/extension surfaces only)
- JetBrains IDEs and their supported AI integrations
- Continue or other projects only if they are active and supported at implementation time
- Other credible AI IDEs, editor extensions, terminal coding agents, and agent runtimes discovered during the compatibility audit.

This is an evolving ecosystem. Do not hard-code this list as a claim of current support. Verify each candidate's current status, official documentation, integration surface, licensing, and maintenance state.

### B. Model and inference provider adapters
Connect a chat or agent to models through **official APIs, documented SDKs, supported local runtimes, or explicitly supported gateways**. Candidate providers and routes to evaluate include:
- OpenAI API and supported OpenAI model endpoints
- Anthropic API
- Google Gemini API / Google AI Studio
- Google Vertex AI
- Azure OpenAI / Microsoft Foundry where applicable
- xAI API (Grok)
- Alibaba Cloud Model Studio / Qwen
- DeepSeek
- Mistral
- Cohere
- Meta models through legitimate hosting providers
- Amazon Bedrock
- Groq
- Cerebras
- Together AI
- Fireworks AI
- OpenRouter
- Hugging Face Inference Providers
- Perplexity API
- NVIDIA NIM / hosted inference where relevant
- Cloudflare Workers AI / AI Gateway where relevant
- Ollama
- LM Studio
- vLLM
- llama.cpp server
- other OpenAI-compatible or documented inference endpoints.

Do not imply that a model family and a provider endpoint are the same thing. A model may be available through multiple providers, with different features, pricing, limits, and data handling.

### C. Unified chatbot / assistant interface
Evaluate and, if consistent with the current architecture and scope, implement an optional OpenClone chat surface that allows a user to:
- choose a configured provider and model;
- maintain conversations and conversation history;
- stream responses;
- start a new chat, rename, search, archive, and delete conversations;
- switch models/providers without losing conversation context;
- configure system instructions and per-workspace instructions;
- attach supported files and images where the selected model/provider supports them;
- use tool calling only when supported and explicitly enabled;
- display provider/model identity and capability limitations;
- show usage, latency, token counts, and estimated cost when reliable data is available;
- handle provider errors, rate limits, timeouts, and unavailable models gracefully;
- optionally use local models for supported tasks;
- preserve user privacy and make data retention controls explicit.

The interface may offer a familiar, high-quality conversational workflow, but **must not copy proprietary branding, logos, protected UI assets, or imply official affiliation** with ChatGPT, Claude, Gemini, Grok, Qwen, or any vendor.

---

# 2. Mandatory repository audit before implementation

Start by inspecting the actual repository checkout. Do not trust old tree snapshots or assumed paths.

1. Read root documentation, package manifests, lockfiles, workspace configuration, architecture docs, governance rules, agent instructions, adapters, skills, scripts, tests, and CI workflows.
2. Identify existing adapter conventions, agent contracts, shared schemas, provider abstractions, chat components, persistence layers, authentication, secrets handling, telemetry, and deployment boundaries.
3. Inspect the existing Taste Skill and anti-AI-slop governance. Preserve them and integrate the global quality policy; do not fork or silently weaken them.
4. Identify the existing OpenClone runtime model:
   - Is it primarily a prompt/skill/framework repository?
   - Does it already include an application, API, CLI, extension, or chat UI?
   - Which parts are executable today versus documentation-only?
5. Map all existing IDE/agent integrations and their actual capabilities.
6. Inspect current dependency versions and supported runtime targets.
7. Identify the smallest architecture extension that supports the requested integrations without creating an unnecessary platform rewrite.

### Required baseline report

Before changing files, produce:
- current repository architecture summary;
- existing adapters and integration mechanisms;
- existing model/provider support, if any;
- existing chat UI/backend capabilities, if any;
- authentication and secrets-management approach;
- storage and conversation-history approach, if any;
- current tests and CI coverage;
- missing capabilities;
- integration candidates classified as `existing`, `partial`, `missing`, `unsupported`, or `deprecated`;
- risks, breaking-change risks, and recommended implementation phases.

Do not start implementation until this baseline is recorded. Continue automatically after recording it; do not stop merely to ask for approval unless a destructive, externally visible, paid, or security-sensitive action is required.

---

# 3. Global compatibility research

Research the ecosystem as it exists **on the day this task is executed**. Use official vendor documentation, official repositories, release notes, supported extension APIs, and maintained protocol specifications as primary evidence. Secondary directories may help discover candidates but cannot establish compatibility by themselves.

For every candidate, verify:
- official product name and current status;
- product category: IDE, editor, extension, CLI agent, desktop assistant, hosted agent, or model provider;
- official documentation and repository links;
- supported operating systems and installation requirements where relevant;
- supported instruction/rules files and their precedence;
- supported skills/commands/agent configuration format;
- MCP support and whether it is client, server, or both;
- hooks, lifecycle events, tools, extension APIs, or plugin mechanisms;
- project-level and user-global configuration locations;
- context limits or instruction-size limits, if documented;
- file access, terminal, network, and approval/permission model;
- authentication methods and supported model providers;
- limitations and known incompatibilities;
- last meaningful maintenance/release signal.

Use a compatibility status:
- `Verified`: confirmed using current official documentation or maintained official code.
- `Partially verified`: some integration surfaces confirmed; others unknown.
- `Experimental`: technically plausible but not validated.
- `Unsupported`: no safe/documented integration surface or incompatible.
- `Deprecated/Retired`: no new integration should be built unless migration support is necessary.

Do not infer support because two tools both read Markdown, claim MCP support without verifying the protocol role and transport, or assume that a VS Code fork supports every VS Code extension.

### Ecosystem discovery checklist

At minimum investigate the current state of:
- Antigravity
- Claude Code
- Codex
- Qwen Code
- Kiro
- Kilo Code
- Cursor
- VS Code
- Zed
- Cline
- Roo Code
- OpenCode
- Aider
- Gemini CLI / Antigravity CLI
- GitHub Copilot
- JetBrains IDE AI integrations
- Windsurf or its current successor
- other significant maintained AI coding environments found through research.

Investigate provider/model access separately, including the providers listed in Section 1B. Add new candidates only when they offer meaningful user value and can be integrated safely.

Produce a dated compatibility matrix with evidence links. Do not present a provider, model, IDE, or feature as supported until its adapter is implemented and tested.

---

# 4. Target architecture

Design an adapter-first architecture with strict boundaries. Adapt it to the repository's existing stack rather than imposing a new stack.

Conceptual architecture:

```text
                         OPENCLONE
                             |
             +---------------+----------------+
             |                                |
       IDE / AGENT LAYER                 CHAT APPLICATION
             |                                |
    +--------+---------+             +--------+---------+
    |        |         |             |        |         |
 Antigravity Claude   Codex        Chat UI  Chat API  Conversation
    |        |         |             |        |         |
 Qwen Code  Kiro   Kilo/Cursor       +--------+---------+
    |        |         |                      |
    +--------+---------+              MODEL ROUTER
             |                                |
     ADAPTER CONTRACTS                PROVIDER ADAPTERS
             |                                |
   Rules / Skills / MCP / CLI        +---------+---------+
   Hooks / Commands / Plugins        |         |         |
                                  OpenAI   Anthropic   Gemini
                                    |         |         |
                                 Qwen      DeepSeek     Grok
                                    |         |         |
                                 OpenRouter / gateways / local runtimes
                                             |
                                   Capability normalization
                                             |
                              Observability / policy / limits
```

This is a conceptual model, not a demand to create every component. Implement only the components justified by the current repository and requirements.

### Architectural principles
- One canonical source of truth for OpenClone policies, agent instructions, and reusable skills.
- Thin environment-specific adapters; do not duplicate the complete framework per IDE.
- Provider adapters are separate from IDE adapters.
- Chat UI is separate from provider implementation and agent runtime.
- A normalized internal contract with provider-specific feature preservation.
- Explicit capability discovery; never pretend all models support the same features.
- Optional components remain optional; users can use the framework without running the chat application.
- Local-first options where practical, but do not promise offline capability for cloud models.
- Backward compatibility and safe migration.
- No unnecessary microservices or abstraction layers.

---

# 5. IDE and agent adapter system

Create or upgrade a common adapter contract. Each adapter should declare:

```yaml
adapter:
  id: unique-stable-id
  name: Human-readable product name
  category: ide | editor | cli-agent | desktop-agent | hosted-agent
  status: verified | partial | experimental | unsupported | deprecated
  integration_surfaces:
    instructions: []
    skills: []
    commands: []
    mcp: client | server | both | none | unknown
    hooks: []
    plugins: []
    cli: []
  configuration:
    project_level: []
    user_global: []
  capabilities:
    file_context: unknown
    terminal_execution: unknown
    tool_approval: unknown
    model_selection: unknown
  compatibility:
    min_version: unknown
    tested_versions: []
  evidence:
    official_docs: []
    official_repo: []
    last_verified: YYYY-MM-DD
  limitations: []
```

Use a schema format already present in the repository where possible. The example is conceptual; do not introduce YAML solely because it appears here.

### Adapter responsibilities
Each adapter should:
1. Detect or document the target environment and prerequisites.
2. Install or link the smallest set of native files needed.
3. Translate canonical OpenClone rules into the target's supported format without changing their meaning.
4. Expose the correct skills, commands, and workflows.
5. Configure MCP only when supported and with the correct client/server role.
6. Configure hooks only when the environment documents and supports them.
7. Respect project-level versus user-global configuration.
8. Avoid overwriting user-managed files.
9. Be idempotent: repeated installation must not create duplicate rules or corrupt configuration.
10. Support validation, diagnostics, and uninstall/rollback where appropriate.
11. Report unsupported capabilities honestly.
12. Include automated tests or reproducible manual verification steps.

### Do not force one universal configuration file

Use a canonical policy source and generate/copy/link environment-native artifacts as needed. Examples of formats to investigate—not assumptions of current support—include:
- `AGENTS.md`
- `CLAUDE.md` or Claude Code's currently documented project/user instructions
- Codex-supported instruction and configuration files
- `GEMINI.md` or currently documented Gemini/Antigravity instruction formats
- Qwen Code's documented instruction/configuration files
- Kiro steering files
- Cursor rules and project configuration
- Windsurf/Devin rules and configuration
- Zed rules/assistant configuration
- VS Code extension settings
- Cline/Roo/Kilo custom instructions and MCP settings
- OpenCode configuration and commands
- Aider conventions
- JetBrains-supported project instructions or plugin mechanisms.

Verify exact names, paths, syntax, precedence, inclusion rules, and version compatibility from official documentation before generating files.

### Avoid adapter sprawl

- Prefer a shared adapter SDK/base contract and small declarative manifests.
- Do not create a separate copy of every OpenClone domain document for every IDE.
- Generate target-specific files from canonical sources where safe.
- Use explicit compatibility tests and snapshots for generated outputs.
- Keep installation optional and scoped.
- Do not install or modify global user configuration without explicit user consent.
- Never silently replace existing user instructions. Offer merge, backup, or conflict reporting.

---

# 6. Unified multi-provider chatbot

If the repository already contains a chat application, upgrade it. If it does not, first determine whether an application belongs in the current project. Do not turn a framework-only repository into a large SaaS application without documenting the scope and architectural implications.

### Core chat experience
Implement a polished, accessible, responsive interface with:
- provider/model selector;
- conversation list and search;
- new conversation;
- streaming message rendering;
- stop generation and retry;
- copy response;
- edit/resubmit user message where supported;
- regenerate response;
- code blocks with syntax highlighting and copy;
- markdown rendering with safe sanitization;
- clear loading, empty, error, and offline states;
- responsive mobile and desktop layouts;
- keyboard accessibility and screen-reader labels;
- model/provider badge on each assistant response;
- settings for provider credentials and preferences;
- conversation export and deletion controls.

Do not add features merely because another chatbot has them. Prioritize a reliable, fast, understandable core.

### Provider adapter contract

Create a normalized provider interface appropriate to the current language and framework. It should cover, where supported:

```text
ProviderAdapter
  - id / displayName
  - validateConfiguration()
  - listModels()
  - getModelCapabilities(model)
  - generate(request)
  - stream(request)
  - cancel(requestId)
  - countTokens(request)             [optional]
  - estimateCost(usage)              [optional]
  - normalizeError(error)
  - healthCheck()                    [optional]
```

Use native provider SDKs for high-value provider-specific functionality. An OpenAI-compatible endpoint can be supported as a generic adapter, but do not assume it implements all OpenAI features or behaves identically.

### Provider capability model

Represent capabilities explicitly, such as:
- text generation;
- streaming;
- tool/function calling;
- structured output / JSON schema;
- vision and image input;
- audio input/output;
- file/document input;
- embeddings;
- reranking;
- reasoning controls;
- prompt caching;
- system/developer instruction support;
- context window metadata;
- model availability and lifecycle status.

Use `supported`, `unsupported`, or `unknown`, with evidence/version where useful. Never silently downgrade a request. If a requested feature is unsupported, explain the limitation and offer a safe fallback only when semantically valid.

### Provider categories to evaluate

1. **Direct first-party APIs:** OpenAI, Anthropic, Google Gemini, xAI, DeepSeek, Alibaba Qwen, Mistral, Cohere, Perplexity, and other verified providers.
2. **Cloud platforms:** Azure OpenAI/Microsoft Foundry, Google Vertex AI, Amazon Bedrock, and other relevant managed platforms.
3. **Model gateways/routers:** OpenRouter, LiteLLM, AI gateways, and other maintained compatible services.
4. **Inference hosts:** Groq, Cerebras, Together AI, Fireworks AI, Hugging Face Inference Providers, and other verified hosts.
5. **Local/self-hosted runtimes:** Ollama, LM Studio, vLLM, llama.cpp server, and other supported local endpoints.
6. **Custom endpoints:** user-defined OpenAI-compatible endpoints with explicit URL validation and capability limitations.

Do not hard-code this as an exhaustive list. Provider additions must be evidence-backed and maintainable.

### Model catalog
- Separate model identity from provider deployment.
- Store provider ID, provider model ID, display name, context metadata, capability metadata, availability state, and last-verified timestamp.
- Support manual model IDs when automatic discovery is unavailable.
- Do not assume model names or capabilities remain stable.
- Do not scrape consumer chatbot websites to populate the catalog.
- Do not misrepresent a consumer subscription as API access.

### Critical subscription and authentication boundary
A user's ChatGPT Plus/Pro, Claude Pro, Gemini subscription, or other consumer plan does **not automatically grant API access**. Do not reuse browser cookies, private endpoints, session tokens, undocumented OAuth flows, or subscription entitlements unless the vendor explicitly documents and authorizes that integration.

Use official API keys, supported OAuth flows, enterprise identity, or explicitly documented sign-in integrations only. Explain billing and entitlement differences clearly.

---

# 7. Chatbot security, privacy, and reliability

Treat provider credentials, conversation history, attachments, and tool execution as sensitive.

### Credentials
- Never expose provider API keys in browser bundles, client-side storage, URLs, logs, analytics, or error messages.
- Store secrets server-side using the repository's established secure secret mechanism.
- Encrypt credentials at rest when persisted; use a managed KMS/envelope encryption approach where available.
- Support environment variables for local development and secret managers for deployment.
- Redact credentials from logs and telemetry.
- Provide key rotation and revocation guidance.
- Do not store raw credentials in ordinary conversation records.
- If BYOK is supported, make credential ownership and storage behavior explicit.

### Authorization and tenancy
- Enforce authentication and authorization on every protected server operation.
- Enforce tenant/workspace isolation at the data-access layer, not only in UI logic.
- Apply least privilege and deny-by-default permissions.
- Prevent insecure direct object references across conversations, files, and provider configurations.
- Add rate limits, quotas, request size limits, and abuse controls.
- Protect against CSRF, XSS, SSRF, injection, path traversal, and unsafe file handling as applicable.
- Validate custom provider base URLs and block private/internal network targets unless an administrator explicitly configures a safe local deployment mode. Prevent DNS rebinding and redirect-based SSRF.
- Use allowlisted outbound destinations where feasible.

### Conversation and attachment privacy
- Define retention and deletion behavior.
- Give users export/delete controls.
- Avoid sending conversation data to a provider until the user submits a request.
- Explain that selected providers receive the content required to process a request.
- Do not use conversation content for training or secondary purposes unless explicitly authorized and disclosed.
- Apply file type, size, content, and malware scanning controls where applicable.
- Do not claim end-to-end encryption unless it is genuinely implemented and accurately scoped.

### Tool execution
- Chat generation must not automatically imply permission to execute shell commands, modify files, access repositories, or call arbitrary external tools.
- Separate chat-only mode from agent/tool-enabled mode.
- Require explicit permissions and clear confirmation for consequential actions.
- Apply sandboxing, command allowlists, timeouts, resource limits, and audit logs.
- Treat model output and tool arguments as untrusted input.
- Protect against prompt injection from user content, repository files, web pages, and attachments.
- Provide a kill/cancel path for long-running operations.

### Reliability
- Implement bounded retries with exponential backoff and jitter for retryable failures.
- Respect provider rate limits and `Retry-After`.
- Add request timeouts, cancellation, streaming disconnect handling, and circuit breakers where justified.
- Do not retry non-idempotent tool actions blindly.
- Preserve partial streaming state safely.
- Normalize errors without leaking secrets or internal stack traces.
- Add provider health and diagnostic information without exposing sensitive data.

---

# 8. Routing, fallback, and model selection

Provide a simple routing layer only where it improves reliability or user control.

Possible policies:
- manual provider/model selection;
- preferred model with user-approved fallback;
- task-based routing (e.g. coding, summarization, vision) only when capability and quality are validated;
- local-first preference;
- budget/latency-aware selection when trustworthy data exists.

Rules:
- Never silently send private data to another provider as a fallback.
- Show the actual provider and model used.
- Respect user allowlists and workspace policy.
- Do not claim automatic best-model selection without a transparent, testable policy.
- Cost estimates must be marked estimates and based on current provider pricing metadata; never invent prices.
- Fallback must preserve the user's intent and disclose any capability reduction.
- Do not route around a provider's safety, policy, or account restrictions.

---

# 9. MCP, skills, tools, and agent interoperability

Evaluate MCP and other documented interoperability protocols as integration surfaces, not as universal solutions.

- Determine whether OpenClone should expose an MCP server, connect as an MCP client, or both.
- Define narrowly scoped tools with typed input/output schemas.
- Require authentication for remote MCP endpoints.
- Apply tool-level authorization and workspace boundaries.
- Validate every tool argument.
- Minimize exposed filesystem and repository scope.
- Document transport, authentication, permissions, and compatibility.
- Add protocol version and client compatibility tests.
- Avoid exposing secrets or unrestricted shell access through MCP.
- Keep skills and prompts portable where possible, with thin environment-specific wrappers.
- Investigate Agent Client Protocol (ACP), language-server/extension APIs, and other standards only when they solve a real interoperability problem.
- Do not add protocol support solely for marketing or checklist completion.

---

# 10. Global anti-AI-slop governance integration

The previously requested global anti-AI-slop governance upgrade remains mandatory and must apply to:
- adapter implementations;
- generated instruction files;
- provider integrations;
- model catalogs;
- chatbot UX and copy;
- documentation and setup guides;
- tests and sample projects;
- routing and agent workflows.

Enforce:
- no unnecessary adapters or duplicated implementations;
- no fake compatibility claims;
- no invented model capabilities, pricing, benchmarks, or provider status;
- no fake integrations that only create placeholder files;
- no generic, bloated chatbot features without user value;
- no needless abstractions or microservices;
- no security shortcuts;
- no silent provider fallback;
- no dark patterns or misleading subscription claims;
- no over-designed interface or decorative AI clichés;
- no undocumented configuration side effects.

Preserve and reuse the existing Taste Skill quality checks. Integrate global quality gates into the actual development lifecycle where practical. Do not claim subjective quality is fully automatable.

---

# 11. Documentation and user experience

Create or update documentation using the repository's existing documentation conventions.

Required documentation:
1. **Integration overview** — explain IDE adapters, model providers, and chatbot as separate layers.
2. **Supported environments matrix** — verified status, supported features, setup links, limitations, and last-verified date.
3. **Provider matrix** — official API route, auth method, supported capabilities, billing caveat, and setup guide.
4. **Quick start** — minimum path to use OpenClone in one supported IDE/agent.
5. **Adapter development guide** — how to add and test a new environment adapter.
6. **Provider development guide** — how to add a provider adapter and model metadata.
7. **Chat application guide** — setup, configuration, security, storage, and deployment, if the chat application exists or is approved within scope.
8. **Security and privacy guide** — credential handling, data flow, retention, tool permissions, and threat model.
9. **Troubleshooting guide** — authentication, unsupported features, rate limits, model discovery, MCP, and adapter installation.
10. **Migration guide** — existing OpenClone users and adapters.
11. **Compatibility verification process** — how to re-check integrations after upstream releases.

Documentation must distinguish:
- available now;
- implemented in this change;
- experimental;
- planned;
- unsupported.

Never use “supports all AI IDEs” or “works with every model” unless an exhaustive and defensible compatibility guarantee actually exists.

---

# 12. Testing and acceptance criteria

Build tests around actual contracts and user journeys.

### Adapter tests
- schema validation;
- generated output snapshots;
- idempotent installation;
- conflict detection;
- preservation of user-managed files;
- unsupported feature reporting;
- uninstall/rollback behavior where implemented;
- compatibility smoke tests against documented sample configurations.

### Provider tests
- configuration validation;
- model listing and manual model IDs;
- capability discovery;
- streaming and cancellation;
- normalized error handling;
- rate-limit handling;
- timeout behavior;
- safe fallback behavior;
- secret redaction;
- custom endpoint SSRF protections;
- mock-provider tests for CI.

Never make CI depend on paid live API calls. Live integration tests must be optional, explicitly configured, and cost-controlled.

### Chat tests, if applicable
- conversation lifecycle;
- model/provider switching;
- streaming;
- cancellation;
- attachment validation;
- access control and tenant isolation;
- export and deletion;
- responsive/accessibility checks;
- prompt injection and tool permission boundaries.

### Definition of done
The upgrade is complete only when:
- current repository baseline and ecosystem research are documented;
- each implemented adapter has an accurate manifest and verification evidence;
- at least one end-to-end environment integration is proven, not merely documented;
- provider adapter contracts are tested with mocks;
- no secret is exposed client-side or in logs;
- provider capability limitations are visible;
- existing OpenClone behavior and Taste Skill checks remain intact;
- generated instructions do not contradict canonical policies;
- documentation matches actual implementation;
- tests and relevant CI checks pass;
- limitations and unsupported integrations are explicitly reported.

Do not claim every candidate is implemented. Deliver a stable core and a prioritized roadmap for the remaining verified candidates.

---

# 13. Phased execution plan

Execute in this order, keeping each phase reviewable:

**Phase 0 — Repository and ecosystem audit**
- Inspect the current checkout and prior integrations.
- Research current IDE/agent and provider ecosystems using official sources.
- Create baseline and dated compatibility matrices.
- Identify architecture fit and scope.

**Phase 1 — Architecture and contracts**
- Define adapter manifest/schema.
- Define canonical instruction and skill distribution strategy.
- Define provider contract and capability model.
- Define security and data-flow boundaries.
- Record architecture decisions.

**Phase 2 — Shared integration foundation**
- Implement shared adapter tooling only where justified.
- Implement safe generation/installation and validation.
- Preserve existing adapters and user files.
- Add compatibility tests.

**Phase 3 — Priority IDE/agent adapters**
- Prioritize the environments already used or explicitly requested: Antigravity, Claude Code, Qwen Code, Kiro, Kilo Code, and Codex.
- Then add other high-value, verified environments based on usage, official support, and maintenance.
- Do not build all candidates at once.
- Provide an explicit reason for each selected adapter.

**Phase 4 — Provider foundation**
- Implement provider abstraction and capability discovery.
- Add mock provider and secure configuration.
- Add a small, high-value set of first-party providers first.
- Add gateway and local-runtime adapters after core correctness.
- Preserve native provider-specific features where useful.

**Phase 5 — Unified chat**
- Only if it fits the actual repository/product boundary.
- Upgrade an existing chat app or propose a separate optional package/app with clear architecture.
- Implement secure conversation lifecycle and streaming before advanced features.
- Integrate model selection and capability-aware behavior.

**Phase 6 — Interoperability and routing**
- Add MCP/ACP or other protocols only where verified and useful.
- Add explicit routing/fallback policies.
- Add observability, limits, and diagnostics.

**Phase 7 — Quality, security, and release readiness**
- Run the global anti-slop checks.
- Run adapter/provider/chat tests.
- Review dependency and license risks.
- Review data flow and threat model.
- Update all docs and compatibility dates.
- Produce final implementation report.

---

# 14. Scope and change control

- Do not rewrite the repository architecture without evidence.
- Do not replace the existing Taste Skill or anti-AI-slop system.
- Do not add a new database, framework, queue, vector database, or microservice unless the audit proves it is necessary.
- Do not add every possible provider or IDE in one release.
- Do not use undocumented private APIs, browser automation to impersonate users, reverse-engineered subscription endpoints, or credential extraction.
- Do not install global tools, alter global IDE settings, or modify files outside the repository without explicit user approval.
- Do not deploy, publish, release, commit, or push without explicit authorization.
- Preserve user changes and inspect `git status` before and after work.
- Use existing package managers and conventions.
- Pin or constrain dependencies according to repository policy; explain new dependencies.
- Keep secrets out of fixtures, screenshots, logs, and documentation.
- If an upstream product is renamed, retired, or replaced, document the current official name and migration path rather than perpetuating stale branding.

---

# 15. Final report format

At completion, report:

1. **Repository baseline** — what existed before.
2. **Ecosystem research date** — when compatibility was checked.
3. **Architecture decisions** — adapters, providers, chat boundary, MCP/ACP decisions.
4. **IDE/agent matrix** — each candidate's verified status and implemented features.
5. **Provider matrix** — each provider's status, auth approach, capabilities, and limitations.
6. **Files changed** — grouped by adapter, provider, chat, security, tests, docs.
7. **Implemented versus documented** — no ambiguity.
8. **Security review** — credential storage, tenancy, SSRF, tool permissions, retention.
9. **Test results** — commands run and actual pass/fail counts.
10. **Known limitations** — including unsupported environments and features.
11. **Remaining roadmap** — prioritized by value, feasibility, and risk.
12. **Git status** — confirm no unauthorized commit, push, deployment, or release occurred.

Use evidence and exact paths. Never report a test as passed unless it was run. Never report an integration as working unless it was tested in the relevant environment or clearly label it as unverified.

---

# 16. Start instruction

Begin with **Phase 0 only**: inspect the actual OpenClone checkout, existing architecture, current adapters, provider/chat implementation, and official ecosystem documentation. Produce the baseline report and dated compatibility matrix. Then proceed through the phases in order, making the smallest safe changes that satisfy the requirements.

The outcome should be a maintainable OpenClone ecosystem—not a giant checklist, not a collection of fake adapters, and not an unnecessary rewrite. Prioritize real interoperability, security, accurate capability reporting, user choice, and long-term maintainability.
