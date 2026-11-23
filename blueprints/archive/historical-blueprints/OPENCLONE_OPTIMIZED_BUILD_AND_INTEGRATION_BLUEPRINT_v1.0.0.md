# OpenClone — Optimized Build & Integration Blueprint
**Engineering execution plan for the Multi-AI Gateway, IDE Adapters, and Security Toolchain**
**Version 1.0.0**

## 1. Product outcome

Build OpenClone as a modular, secure AI development platform with three independently usable capabilities:

1. **IDE and coding-agent adapters** — make OpenClone's canonical rules, skills, workflows, and tools available inside supported AI coding environments.
2. **Multi-provider AI gateway** — let users connect authorized model providers and local runtimes through one consistent configuration and routing layer.
3. **Security engineering toolchain** — orchestrate mature security tools through safe, optional profiles and produce traceable reports.

Do not turn OpenClone into a repository dump. OpenClone owns integration contracts, policy, configuration, orchestration, and user experience. Mature upstream tools remain independent dependencies or optional external services unless there is a compelling, license-compatible reason to vendor a small component.

## 2. The most important optimization decisions

| Decision | Recommended approach | Why |
|---|---|---|
| Repository integration | Clone candidates into a temporary research workspace; integrate selectively | Avoids source-tree bloat and supply-chain risk |
| LLM router | Select one primary router after an evidence-based comparison | Avoids competing routers and duplicated routing logic |
| Provider support | Thin provider adapters plus a normalized capability model | Keeps provider-specific behavior visible |
| IDE support | One canonical OpenClone source with thin native adapters | Prevents duplicated instructions and policy drift |
| Security tools | Invoke independent tools through a security orchestrator | Reuses mature scanners and keeps them optional |
| Execution | Profiles with least privilege, timeouts, and explicit approvals | Prevents every scan from becoming expensive or dangerous |
| Persistence | Reuse the existing database and storage architecture | Avoids needless infrastructure |
| Deployment | Start as a modular monolith or CLI/orchestrator; split services only with evidence | Reduces operational overhead |
| UI | Add only if an existing app/dashboard boundary supports it | Avoids turning a framework into an oversized SaaS product |
| CI | Mock provider tests; deterministic security checks; opt-in live tests | Prevents paid API calls and flaky builds |
| Quality | Keep global anti-AI-slop and Taste Skill gates active | Prevents scope creep and inconsistent standards |

## 3. Target system architecture

Adapt names and locations to the real repository. This diagram expresses boundaries, not a requirement to create every box as a separate service.

```text
                          OPENCLONE
                              |
             +----------------+----------------+
             |                |                |
          CORE            INTEGRATIONS      SECURITY
             |                |                |
      Canonical Policy    IDE/Agent Adapters   Profiles
      Skills & Workflows  Provider Adapters    Orchestrator
      Contracts           Router Adapter       Tool Adapters
      Quality Gates       MCP (when needed)    Findings
             |                |                |
             +----------------+----------------+
                              |
                      SHARED CONTROL PLANE
                              |
            Configuration / Permissions / Audit / Diagnostics
                              |
          +-------------------+--------------------+
          |                   |                    |
       IDE Agents         Model Gateway       Security Tools
          |                   |                    |
 Antigravity/Claude     OpenAI/Anthropic      Semgrep/Trivy
 Codex/Qwen/Kiro        Gemini/Qwen/Grok      TruffleHog
 Kilo/Cursor/etc.       Local runtimes        Nuclei/Strix*
                                              PyRIT*
```

`*` Dynamic testing and LLM red-team tools are opt-in, isolated, and target-authorized.

### Architectural boundaries

- Core policy must not import vendor-specific provider SDKs.
- IDE adapters must not implement their own copies of global governance.
- Provider adapters must not know about UI components.
- Security tool adapters must not bypass the orchestrator's permission and scope checks.
- The chat UI, if present, calls the server-side gateway; it never calls provider APIs with secret keys from the browser.
- A provider gateway must not automatically grant an agent permission to execute tools or edit files.
- All external operations must carry a request/run ID and record the effective provider/tool, scope, and outcome.

## 4. Repository organization strategy

First inspect the existing tree. Reuse current conventions. If no suitable structure exists, consider:

```text
openclone/
├── core/
│   ├── contracts/
│   ├── governance/
│   ├── policies/
│   └── orchestration/
├── integrations/
│   ├── ide-adapters/
│   ├── providers/
│   ├── llm-gateways/
│   └── security-tools/
├── security/
│   ├── profiles/
│   ├── policies/
│   ├── schemas/
│   └── threat-model/
├── configs/
│   ├── providers/
│   ├── routing/
│   └── security/
├── docs/
│   ├── architecture/
│   ├── integrations/
│   └── security/
└── tests/
    ├── contracts/
    ├── adapters/
    ├── providers/
    └── security/
```

Do not create empty folders just to match this diagram. Create a path only when it contains a real implementation or useful documentation.

### Third-party source handling

Use one of these methods per candidate:

1. **External tool installation** — preferred for mature CLIs such as scanners.
2. **Documented API/SDK adapter** — preferred for gateways and hosted services.
3. **Optional container** — for heavyweight or isolated tools.
4. **Pinned submodule** — only when a source-level dependency is necessary and maintainable.
5. **Vendored code** — last resort, only after license, provenance, and security review.

Keep a machine-readable inventory containing repository URL, commit SHA or version, license, integration method, update owner, and verification date.

## 5. Build sequence — do not parallelize the wrong work

### Phase 0 — Protect and understand the current project

**Actions**
- Check `git status`, current branch, recent commits, package manifests, lockfiles, and existing tests.
- Identify user modifications and never overwrite them.
- Read root docs, architecture, governance, agent rules, existing adapters, Taste Skill, and anti-AI-slop standards.
- Identify current runtime, language, build system, database, auth, secrets, CI, and deployment.
- Map current functionality against the requested features.

**Exit gate**
- Baseline architecture and capability report exists.
- Current tests and quality checks are recorded.
- No source changes have been made.
- All 20 candidate URLs have a recorded reachability result.

### Phase 1 — Acquire and inspect candidates safely

**Actions**
- Clone the eight router candidates and twelve security candidates into a temporary directory outside the production source tree.
- Record exact resolved repository, branch, commit SHA, release, license, and acquisition date.
- Inspect README, license, manifests, lockfiles, install scripts, Dockerfiles, CI, permissions, network calls, secrets handling, and relevant source.
- Do not run project scripts or install dependencies during initial static review.
- Check maintenance and official documentation.

**Exit gate**
- Candidate comparison matrix is complete.
- License and security status are recorded.
- Blocked, missing, archived, or renamed repositories are identified.
- No candidate has been executed without review.

### Phase 2 — Make architecture decisions before coding

Create short Architecture Decision Records for:
1. Primary router selection.
2. Provider abstraction and model capability representation.
3. IDE adapter contract and generated configuration approach.
4. Security orchestration and execution boundary.
5. Secret storage and provider data-egress policy.
6. Optional chat UI/API boundary, if applicable.
7. Third-party dependency and update strategy.

**Exit gate**
- Each decision includes context, options, choice, trade-offs, security implications, and rollback path.
- No new database, queue, microservice, or framework is introduced without demonstrated need.

### Phase 3 — Build the shared contracts and configuration

Implement only the shared contracts needed by selected integrations:

**IDE adapter manifest**
- Stable ID and product category.
- Verified integration surfaces.
- Project/global config paths.
- Capabilities and limitations.
- Version compatibility and evidence.
- Install, validate, and uninstall behavior.

**Provider manifest**
- Provider ID and API mode.
- Authentication method.
- Model discovery method.
- Capability metadata.
- Streaming and tool-call support.
- Rate-limit/error normalization.
- Data handling and endpoint policy.

**Security tool manifest**
- Tool ID and version constraint.
- Supported platforms.
- Scan categories.
- Required permissions.
- Network access requirements.
- Input/output formats.
- Safe execution mode.
- Timeout/resource defaults.

**Configuration principles**
- Schema-validate all configuration.
- Separate defaults from user overrides.
- Never commit secrets.
- Never overwrite user-owned IDE configuration silently.
- Make install and update operations idempotent.
- Support dry-run and diagnostics.

**Exit gate**
- Contracts have unit tests and example fixtures.
- Invalid configuration fails clearly.
- User configuration preservation is tested.

### Phase 4 — Implement one vertical slice end to end

Do not build all adapters and providers at once. Prove the architecture with one complete, useful path.

Recommended first vertical slice:

```text
OpenClone configuration
        |
Selected router adapter
        |
One official provider + one optional local/provider route
        |
One supported coding agent
        |
Streaming response + cancellation
        |
Provider identity + error/usage metadata
        |
Tests + setup documentation
```

Select the first coding agent based on the user's actual environment and official compatibility. Antigravity, Claude Code, Codex, and Qwen Code are high-priority candidates, but verify the currently documented integration surface before implementation.

**Exit gate**
- A real request works in a disposable sample project.
- The effective model/provider is visible.
- Streaming, cancellation, errors, and unsupported features behave correctly.
- No credentials are exposed.
- No silent fallback occurs.

### Phase 5 — Expand the provider and IDE matrix

Add integrations in ranked batches, not one giant release.

**Suggested order**
1. Antigravity
2. Claude Code
3. Codex
4. Qwen Code
5. Kiro
6. Kilo Code
7. Cursor
8. OpenCode
9. Other verified high-value environments

For providers, prioritize the direct APIs the project can securely support, then add gateways and local runtimes. The exact order should follow the candidate audit, official API quality, user demand, and maintenance burden.

For every added integration:
- implement the manifest;
- add generated/native configuration;
- test idempotence and conflict handling;
- document exact prerequisites;
- mark unsupported features;
- add a smoke test;
- record last verification date.

**Exit gate**
- No adapter is marked verified without evidence.
- No duplicate policy source exists.
- Existing integrations continue to work.

### Phase 6 — Integrate the security toolchain incrementally

Start with non-invasive, high-signal checks:

**First security batch**
- TruffleHog: secrets.
- Semgrep: SAST.
- Trivy: dependencies, filesystem, containers, IaC, and SBOM where relevant.
- NVIDIA SkillSpector: agent-skill/MCP supply-chain checks, if the current project and tool support the intended input.

**Second batch, when relevant**
- ClamAV: malware scanning for supported artifacts.
- Cloudflare Security Audit Skill: inspect its actual workflow and permissions before adding it.
- Claude Code Security Review and Codex Security: evaluate supported review workflows and licensing/access requirements.

**Restricted batch**
- Nuclei and Strix: authorized dynamic testing only, explicit target allowlist, isolated environment.
- Microsoft PyRIT: controlled LLM red-team evaluation against a test system.
- BLA: research-only unless its maturity and fit justify more.

Each tool must be optional and independently runnable. Missing tools should produce `not installed` or `not run`, never a false `passed`.

**Exit gate**
- Quick local profile works without network-active scanners.
- PR profile returns structured findings.
- Dynamic profiles reject unapproved targets.
- Tool failures are distinguished from clean scans.

### Phase 7 — Add orchestration, reports, and CI

Implement a small orchestrator that:
- checks tool availability and versions;
- validates scope and permissions;
- constructs commands safely without shell-string injection;
- applies timeouts and resource limits;
- captures exit codes and structured output;
- normalizes findings while preserving source evidence and severity;
- emits JSON/Markdown and SARIF when supported;
- records scan profile, timestamp, tool version, and target scope.

Use CI gates proportionally:
- pull requests: secrets, SAST, dependency checks, relevant tests;
- scheduled: broader repository and dependency scans;
- release: SBOM, dependency review, secrets, and required security checks;
- dynamic testing: separate authorized workflow, never an unscoped default PR action.

**Exit gate**
- CI is deterministic and does not require paid model API calls.
- Scan errors do not appear as clean results.
- Reports are reproducible and traceable.

### Phase 8 — Optional chatbot and dashboard

Only do this if OpenClone already has a product UI/API boundary or the product scope explicitly includes one.

If applicable, implement in this order:
1. Secure server-side provider configuration.
2. Model/provider selector.
3. Conversation persistence and deletion.
4. Streaming and cancellation.
5. Error and rate-limit states.
6. Usage metadata where reliable.
7. Attachments and multimodal features only after provider capability validation.
8. Tool-enabled agent mode as a separate permissioned experience.

Do not build a ChatGPT clone merely to expose a gateway. A CLI and configuration layer may be the more optimized first release.

### Phase 9 — Hardening and release readiness

- Run all existing tests.
- Run adapter/provider/security contract tests.
- Run license and dependency checks.
- Review SSRF, tenant isolation, credential handling, prompt injection, and tool execution.
- Run anti-AI-slop and Taste Skill quality gates.
- Verify docs against the implementation.
- Verify installation, upgrade, rollback, and cleanup.
- Remove temporary research clones after the comparison evidence is safely recorded, unless the user explicitly wants to retain them.
- Produce a final report.

## 6. Routing behavior — optimize for correctness, not marketing

Use explicit routing modes:

| Mode | Behavior |
|---|---|
| Manual | User selects provider and model |
| Preferred + approved fallback | Try preferred route; fallback only to user-approved providers |
| Local only | Never send requests to cloud providers |
| Capability based | Select only models that meet declared feature requirements |
| Budget aware | Use current verified pricing/limits; estimates clearly labeled |
| Free-tier preference | Prefer currently eligible free routes, but never promise availability or unlimited use |

Rules:
- Never bypass provider quotas, account limits, or terms.
- Never rotate identities to evade limits.
- Never silently send code or prompts to a different provider.
- Do not treat free-tier access as production SLA.
- Preserve tool-call semantics when routing coding-agent requests.
- Do not route a vision request to a text-only model.
- Do not route a large-context request to a model whose verified context limit is insufficient.
- Expose the actual model ID returned by the provider/router.

## 7. Security profiles and default behavior

| Profile | Default behavior | Network-active? |
|---|---|---|
| `quick-local` | Fast local checks and changed-file checks | No, unless tool requires explicit metadata access |
| `pull-request` | Secrets, SAST, dependency checks | Limited and controlled |
| `full-repository` | Broader code, dependency, container, IaC checks | Controlled |
| `agent-supply-chain` | Inspect skills, MCP servers, plugins, agent configs | Only when explicitly needed |
| `authorized-dynamic` | Nuclei/Strix against allowlisted owned targets | Yes, explicit authorization required |
| `llm-red-team` | PyRIT or approved evaluation against test models | Yes, explicit configuration required |
| `release` | Release-focused checks, SBOM, provenance | Controlled |

Default-deny:
- no public-target scanning;
- no arbitrary shell execution from chatbot output;
- no privileged containers by default;
- no host home-directory mounts;
- no production credentials in scan containers;
- no automated fixes without review/approval.

## 8. Performance and cost optimization

### Build and runtime
- Reuse existing package manager, lockfile, and runtime.
- Avoid duplicate dependencies and SDKs.
- Lazy-load optional integrations.
- Keep heavyweight scanners out of the default developer install.
- Cache tool version checks and model metadata with bounded TTLs.
- Do not cache secrets or sensitive prompts.
- Use bounded concurrency for scans and provider requests.
- Apply timeouts and cancellation to every external operation.
- Keep local quick checks fast; move expensive checks to scheduled or opt-in profiles.

### CI
- Use mock providers in regular CI.
- Avoid live paid model calls in pull requests.
- Cache dependencies safely.
- Pin scanner versions or image digests.
- Run only relevant language/tool checks where possible.
- Keep a scheduled full scan to catch drift.
- Record duration and resource usage to identify slow gates.

### Maintainability
- One primary router.
- One canonical policy source.
- One adapter contract per concern.
- One security finding schema.
- One documented integration lifecycle.
- No duplicated tool-specific orchestration scattered across IDE adapters.

## 9. Verification matrix

The project is not done until each applicable row is verified.

| Area | Required proof |
|---|---|
| Repository safety | Git status preserved; no user changes lost |
| Third-party review | URL, commit, license, provenance recorded |
| Router | Real request succeeds through documented route |
| Provider | Model/capability metadata and errors tested |
| Coding agent | End-to-end sample project test |
| Streaming | Partial response and cancellation verified |
| Fallback | Explicit, approved, visible, and tested |
| Credentials | No browser exposure or log leakage |
| SSRF | Custom endpoint validation and redirect protections tested |
| Security tools | Version checks, safe invocation, structured results |
| Dynamic scanning | Unapproved targets rejected |
| Reports | Source evidence, severity, and status preserved |
| IDE adapters | Idempotence and user-config conflict behavior tested |
| Quality | Existing tests, Taste Skill, anti-slop gates pass |
| Documentation | Setup matches current implementation |
| Cleanup | Temporary files/clones handled safely |

## 10. Antigravity execution instructions

You are the implementation engineer. Work directly in the actual OpenClone checkout.

1. Begin with the current Git status and repository audit.
2. Do not assume paths or stack from old conversations.
3. Clone all 20 candidate repositories into a temporary isolated research workspace.
4. Do not execute candidate code before static trust and license review.
5. Complete the comparison matrix and architecture decisions.
6. Select the smallest set of components that delivers the highest value.
7. Implement one vertical slice end to end before expanding.
8. Preserve existing architecture, adapters, governance, Taste Skill, and user changes.
9. Test every meaningful integration; do not substitute documentation for implementation.
10. Keep a running changelog of files changed, commands run, and results.
11. Stop before any destructive, externally visible, paid, global-machine, deployment, commit, or push action that requires user authorization.
12. At the end of each phase, report completed work, evidence, tests, risks, and next phase. Continue to the next safe phase without asking for unnecessary confirmation.

### Final deliverables

- Baseline architecture report.
- 20-repository acquisition and trust inventory.
- Router comparison and selection ADR.
- Security tool classification and selection ADR.
- IDE/provider/security adapter contracts.
- Working first vertical slice.
- Security profiles and orchestrator.
- Provider and IDE compatibility matrices.
- Threat model and data-flow documentation.
- Third-party notices/SBOM where applicable.
- Tests and CI updates.
- Final implementation and limitations report.

## 11. Definition of success

OpenClone should be easy to install, predictable to configure, safe by default, and simple to extend.

A developer should be able to:
- use OpenClone from a verified coding environment;
- select an authorized AI provider/model or local runtime;
- understand exactly where code and prompts are sent;
- switch models without breaking supported coding-agent workflows;
- run the right security checks for the current task;
- inspect evidence-backed findings in one consistent report;
- add another IDE, provider, or security tool without rewriting the core.

**Build a dependable integration platform—not a pile of cloned repositories.**
