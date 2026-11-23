# OpenClone — External LLM Router & Security Toolchain Integration
**Master repository acquisition, audit, integration, and verification prompt for Antigravity**
**Version 1.0.0**

## Mission

Upgrade the existing **OpenClone** repository by evaluating and integrating the user-provided open-source projects for:

1. Multi-provider LLM routing and fallback, including free-tier and local model endpoints.
2. Application, repository, dependency, secret, container, cloud, and AI-agent security.
3. AI-generated code review, vulnerability discovery, and AI red teaming.

The requested repositories are research and integration candidates—not a mandate to paste 20+ entire codebases into OpenClone. Clone every accessible candidate into a **temporary isolated research workspace**, inspect it, verify its license and supply-chain posture, and then integrate the appropriate projects using the safest maintainable method.

**Do not blindly vendor all repositories, merge unrelated codebases, execute unknown setup scripts, or claim that a tool is integrated just because its README was copied.**

OpenClone should own the orchestration, configuration, policies, adapter contracts, documentation, and user experience. Mature specialist tools should remain independently versioned and isolated where appropriate.

---

# 1. User-provided repository inventory

Preserve the exact repository identities below and verify each URL before cloning.

## A. LLM routing and free-model gateway candidates (8)

1. `Devansh-365/freellm` — https://github.com/Devansh-365/freellm
2. `kaiser-data/free-llm-proxy-router` — https://github.com/kaiser-data/free-llm-proxy-router
3. `nabinkhadka/free-llm-api` — https://github.com/nabinkhadka/free-llm-api
4. `YeomanYe/free-llm-router` — https://github.com/YeomanYe/free-llm-router
5. `alienz-dev/llm-router` — https://github.com/alienz-dev/llm-router
6. `MajidAsghariTabrizi/free-best-router` — https://github.com/MajidAsghariTabrizi/free-best-router
7. `tashfeenahmed/freellmapi` — https://github.com/tashfeenahmed/freellmapi
8. `Gmagl/omniroute` — https://github.com/Gmagl/omniroute

Evaluate these as alternative implementations or sources of design ideas. Several solve overlapping gateway/routing problems. Do not run multiple routers in production by default. Select one primary integration strategy after comparing architecture, license, security, provider support, streaming, tool calling, routing correctness, maintenance, resource use, and compatibility with OpenClone.

## B. Security, code review, and AI red-team candidates (12)

1. Strix — https://github.com/usestrix/strix
2. Cloudflare Security Audit Skill — https://github.com/cloudflare/security-audit-skill
3. Trivy — https://github.com/aquasecurity/trivy
4. Nuclei — https://github.com/projectdiscovery/nuclei
5. TruffleHog — https://github.com/trufflesecurity/trufflehog
6. NVIDIA SkillSpector — https://github.com/NVIDIA/skillspector
7. Semgrep — https://github.com/semgrep/semgrep
8. OpenAI Codex Security — https://github.com/openai/codex-security
9. ClamAV — https://github.com/Cisco-Talos/clamav
10. Claude Code Security Review — https://github.com/anthropics/claude-code-security-review
11. BLA (Blind LLM Agents) — https://github.com/qybaihe/bla
12. Microsoft PyRIT — https://github.com/microsoft/pyrit

The supplied list contains 20 repositories total. If a URL is missing, moved, private, renamed, archived, or not the expected project, record that fact and investigate the official successor only when evidence supports it. Do not silently substitute a different repository.

---

# 2. Non-negotiable safety and acquisition rules

## 2.1 Isolated acquisition

1. Inspect the actual OpenClone checkout and Git state first.
2. Create a temporary research directory outside the tracked OpenClone product tree, for example `.tmp/openclone-integration-research/` only if that directory is safely ignored; otherwise use an OS temporary directory.
3. Clone each accessible repository into its own directory. Use shallow clones for initial inspection where appropriate, but fetch tags/history when required for license, release, provenance, or maintenance review.
4. Record source URL, resolved default branch, commit SHA, tag/release, acquisition date, license file, and repository status.
5. Do not initialize or update arbitrary nested submodules until their URLs and contents are reviewed.
6. Do not run `install`, `build`, `test`, `setup`, Docker, Make, shell, Python, Node, or other project scripts during initial inspection.
7. Do not provide provider API keys, GitHub tokens, SSH credentials, cloud credentials, or personal data to candidate projects.
8. Do not modify the user's global IDE settings, shell profile, PATH, global packages, Docker daemon configuration, or machine-wide services.
9. Do not commit, push, publish, deploy, release, or create external resources.

## 2.2 Trust and supply-chain review

Before executing any candidate:
- inspect license and notices;
- inspect dependency manifests and lockfiles;
- inspect install scripts, lifecycle hooks, postinstall scripts, Makefiles, Dockerfiles, entrypoints, and CI workflows;
- inspect network destinations and telemetry behavior;
- inspect credential handling and secret storage;
- inspect filesystem access, shell execution, subprocess use, privilege requirements, and persistence mechanisms;
- inspect release provenance and maintainer activity;
- scan source and dependencies with appropriate tools once the scanning tools themselves are safely installed and validated;
- check for known vulnerabilities and malicious packages;
- identify unpinned dependencies, install-time downloads, opaque binaries, and suspicious obfuscation.

Do not treat a clean scanner report as proof of safety. Do not execute untrusted code simply to test whether it is malicious.

## 2.3 Licensing

Record each project's exact SPDX license identifier, copyright notices, attribution obligations, source-distribution requirements, and compatibility with OpenClone's license.

- Do not copy code into OpenClone until license compatibility is reviewed.
- Preserve upstream license and notice files for any approved vendored code.
- If a license is absent, unclear, or incompatible, do not vendor the code. Prefer a documented external installation/integration, or exclude it.
- Do not assume that public GitHub availability means permission to relicense or redistribute.
- Keep a third-party notices/SBOM record for included components.

---

# 3. Repository and product audit

Before implementation, inspect:
- OpenClone's root tree, Git status, branch, package/workspace structure, lockfiles, build/test commands, CI, license, and contribution rules.
- Existing IDE adapters, model/provider adapters, router abstractions, chat application, API, CLI, MCP integrations, skills, hooks, and agent workflows.
- Existing global anti-AI-slop governance and Taste Skill checks; preserve them.
- Existing security policies, threat models, dependency scanning, secret scanning, and release workflows.
- Existing environment configuration, secrets handling, authentication, tenant/workspace boundaries, logs, and deployment architecture.

Determine whether OpenClone is a framework repository, application repository, monorepo, or combination. Do not assume the architecture from a previous tree snapshot.

Create a baseline before editing:
- current capabilities;
- existing tools and overlaps;
- gaps;
- architecture fit;
- security risks;
- current tests;
- paths likely to change;
- user changes that must be preserved.

---

# 4. Candidate evaluation and selection

Create a comparison matrix for all 20 candidates. Use current repository content and official documentation, not marketing copy alone.

For every repository record:
- availability and current status;
- exact license;
- latest release and last meaningful commit;
- language/runtime;
- installation and deployment model;
- primary purpose;
- supported OS/platforms;
- dependency footprint;
- security posture and permissions;
- credential/data handling;
- API/CLI/MCP/CI integration surfaces;
- maintenance and issue activity;
- overlapping OpenClone features;
- integration effort;
- recommendation: `integrate`, `optional external tool`, `adapter only`, `research only`, `reject`, or `blocked pending review`.

## 4.1 Router comparison dimensions

For all eight LLM routers, evaluate:
- direct provider support and official API usage;
- free-tier eligibility verification and freshness;
- model catalog discovery and metadata quality;
- model capability detection;
- routing strategies and deterministic behavior;
- quota/rate-limit tracking;
- retries, cooldowns, circuit breakers, and key rotation;
- streaming behavior and time-to-first-token;
- tool/function calling preservation;
- structured output support;
- vision and multimodal support;
- context-window handling;
- provider-specific error fidelity;
- model identity and route transparency;
- privacy, telemetry, prompt retention, and data egress;
- authentication and gateway security;
- dashboard/observability;
- local model support;
- concurrency and resource consumption;
- deployment, upgrade, and rollback;
- tests and CI;
- license and dependency risk.

**Important:** “Free” does not mean unlimited, guaranteed, or suitable for production. Free provider quotas, model availability, regions, and terms change. Do not promise unlimited coding or automatic quota resets. Do not encourage creating multiple accounts or rotating identities to bypass provider limits. Key rotation must only support legitimate keys/accounts and must respect each provider's terms.

## 4.2 Security tool comparison dimensions

Evaluate the twelve security candidates by their real scope:
- static analysis / SAST;
- dependency and software supply-chain scanning;
- secrets detection;
- container, filesystem, IaC, and cloud configuration scanning;
- malware scanning;
- web/API vulnerability scanning;
- authorized dynamic penetration testing;
- AI agent skill and MCP package scanning;
- AI-generated code review;
- LLM application red teaming;
- research/prototype status versus production readiness;
- CI integration and machine-readable outputs;
- false-positive handling and evidence quality;
- required privileges, network access, and destructive potential.

Do not treat all tools as interchangeable. For example, a web penetration-testing tool is not a replacement for a dependency scanner, and an AI red-team research project is not automatically a production security gate.

---

# 5. Target OpenClone architecture

Adapt the following conceptual structure to the existing repository. Do not force these exact paths if equivalent conventions already exist.

```text
OpenClone
├── core/
│   ├── governance/
│   ├── policy/
│   ├── adapter-contracts/
│   └── orchestration/
│
├── integrations/
│   ├── ide-adapters/
│   ├── model-providers/
│   ├── llm-gateways/
│   ├── mcp/
│   └── security-tools/
│
├── security/
│   ├── profiles/
│   ├── policies/
│   ├── workflows/
│   ├── reports/
│   └── threat-model/
│
├── apps/                         # only if this already fits the repo
│   ├── api/
│   └── dashboard/
│
├── configs/
│   ├── providers/
│   ├── routing/
│   └── security/
│
├── docs/
│   ├── integrations/
│   ├── security/
│   ├── providers/
│   └── operations/
│
└── tests/
    ├── adapters/
    ├── providers/
    ├── security/
    └── integration/
```

The architecture must keep these concerns separate:
1. OpenClone core governance and agent framework.
2. Provider/model integration.
3. Optional LLM gateway.
4. Security tool orchestration.
5. User-facing configuration/reporting interface, if applicable.

Do not create microservices for every tool. Prefer local CLI integrations, stable APIs, optional containers, or documented external installations.

---

# 6. LLM router integration design

## 6.1 Select one primary router strategy

After comparison, select:
- one primary router to integrate or adapt;
- optional provider-native adapters for missing capabilities;
- optional alternative router profiles only if there is a real use case.

Avoid embedding multiple competing routers into the same request path.

Prefer one of these integration methods, in order:
1. Stable documented API/CLI integration.
2. Optional standalone service with health checks and a documented endpoint.
3. Maintained SDK/library integration where licensing and runtime fit.
4. Git submodule only when upstream contribution/version pinning makes it worthwhile.
5. Vendoring only a small, license-compatible component when no safer option exists.

Do not fork an entire router simply to change a few configuration values.

## 6.2 Normalized OpenClone provider contract

If OpenClone needs its own provider abstraction, define a thin contract that preserves upstream capabilities:

```text
ProviderAdapter
  - id
  - displayName
  - validateConfiguration()
  - listModels()
  - getCapabilities(model)
  - generate(request)
  - stream(request)
  - cancel(requestId)
  - normalizeError(error)
  - healthCheck()
  - getUsage(requestId)             [optional]
```

Represent capabilities as `supported`, `unsupported`, or `unknown`. Do not silently downgrade tool calling, streaming, vision, JSON output, or context requirements.

## 6.3 Routing policies

Support transparent policies where the chosen router permits:
- manual model/provider;
- coding;
- reasoning;
- fast/low-latency;
- long-context;
- economical/free-tier where currently verified;
- local-only;
- user-approved fallback.

Every response/trace should identify the actual provider and model. A fallback must not silently transmit sensitive data to another provider. Provide explicit provider allowlists and workspace policy controls.

## 6.4 Claude Code and other coding agent compatibility

If an upstream gateway exposes a documented OpenAI-compatible or Anthropic-compatible endpoint, configure coding agents only through their documented settings and supported environment variables.

- Verify the actual API compatibility required by each agent.
- Do not assume that OpenAI-compatible `/v1/chat/completions` is interchangeable with the Anthropic Messages API.
- Preserve tool-use, streaming, system prompt, and structured response semantics.
- Do not hijack private endpoints, browser sessions, consumer subscriptions, or undocumented auth.
- Do not claim that a gateway makes Claude models available without valid Claude API access.
- Clearly distinguish using a third-party model through a compatible endpoint from using the official Claude model/service.
- Test the actual coding-agent workflow in a safe sample repository before declaring support.

The same honesty applies to Codex, Qwen Code, Antigravity, Kiro, Kilo Code, Cursor, and other IDE/agent integrations.

---

# 7. Security toolchain integration

Build an optional, layered security workflow rather than one giant mandatory scan.

## 7.1 Recommended security layers

| Layer | Candidate tools | Intended purpose |
|---|---|---|
| Agent skill / MCP supply-chain | NVIDIA SkillSpector | Inspect agent skills and MCP packages before installation |
| Secrets | TruffleHog | Detect exposed credentials and secrets |
| SAST / code patterns | Semgrep | Static code analysis and security rules |
| Dependency / SBOM / container / IaC | Trivy | Vulnerability and misconfiguration scanning |
| Malware | ClamAV | Scan files/artifacts where appropriate |
| Web/API dynamic testing | Nuclei | Authorized scanning of explicitly scoped targets |
| AI-assisted pentest | Strix | Authorized dynamic testing in an isolated target environment |
| Cloud security audit skill | Cloudflare Security Audit Skill | Agent-assisted security audit workflow; inspect exact skill permissions |
| AI code review | Claude Code Security Review | Review diffs/PRs using its supported workflow |
| AI vulnerability discovery | OpenAI Codex Security | Repository vulnerability analysis and remediation workflow |
| LLM red-team testing | Microsoft PyRIT | Evaluate LLM systems for security risks |
| Research | BLA | Evaluate research applicability; do not make a production dependency without evidence |

This is a starting mapping, not a claim that every tool is installed or appropriate for every project.

## 7.2 Profiles

Create configurable profiles:
- `quick-local`: fast, non-invasive checks for developer feedback.
- `pull-request`: secrets, dependency, SAST, and relevant diff checks.
- `full-repository`: broader SAST, dependency, container, IaC, and malware checks.
- `agent-supply-chain`: scan skills, MCP servers, agent configuration, and third-party prompts before installation.
- `authorized-dynamic`: Nuclei/Strix only against explicitly approved owned targets.
- `llm-red-team`: PyRIT and related evaluations against explicitly configured test systems.
- `release`: required release checks, SBOM/provenance and security report.

Profiles must be configurable by repository language and project type. Do not run irrelevant scans on every commit.

## 7.3 Safe execution boundaries

- Dynamic scanners must be disabled by default.
- Require explicit target allowlists and written authorization before Nuclei or Strix execution.
- Never scan arbitrary public IPs, domains, or third-party services.
- Use a disposable sandbox/container for tools that execute payloads, spawn agents, or interact with targets.
- Restrict network egress and filesystem mounts.
- Use non-root execution where feasible.
- Set CPU, memory, process, file-size, and time limits.
- Do not mount the user's home directory or credential directories into scanners.
- Do not pass production secrets to scanners or LLM agents.
- Require confirmation before applying automated fixes or modifying files.
- Store scan artifacts with access controls and retention limits.
- Separate findings from verified vulnerabilities; include evidence and confidence.
- Never let an AI agent mark its own unverified finding as confirmed.

---

# 8. Orchestration and reporting

Create one OpenClone security/tool orchestration layer only if the existing project can support it cleanly.

It should:
- check whether a tool is installed and identify its version;
- validate configuration and prerequisites;
- run selected profiles;
- pass only required paths/targets;
- enforce timeouts and safe execution constraints;
- capture exit codes and structured outputs;
- normalize findings into a common schema without discarding original evidence;
- deduplicate findings carefully;
- preserve source tool, rule ID, severity, confidence, file/line/target, evidence, remediation, and timestamp;
- distinguish `confirmed`, `potential`, `informational`, `suppressed`, and `not-run`;
- support SARIF where tools provide it, plus JSON/Markdown summaries;
- make reports reproducible and auditable.

Never invent a unified severity score that hides the source tool's severity. Preserve original severity and show any OpenClone-normalized severity separately.

### Suggested normalized finding fields

```text
findingId
sourceTool
sourceRuleId
category
title
description
severityOriginal
severityNormalized
confidence
status
repository
filePath
lineStart
lineEnd
target
evidence
remediation
references
firstSeenAt
lastSeenAt
scanProfile
scanRunId
```

Use the existing repository's schema conventions where possible.

---

# 9. Security of the LLM gateway itself

The router is a high-value security boundary because it holds provider credentials and receives source code/prompts.

Required controls:
- bind local development gateway to loopback by default;
- require authentication for non-local access;
- never expose admin endpoints publicly by default;
- store provider keys in environment variables or a secure secret store, not committed YAML/JSON;
- encrypt persisted credentials if persistence is necessary;
- redact credentials and sensitive prompt data from logs;
- validate request sizes, model IDs, content types, and parameters;
- add per-user/workspace rate limits and quotas;
- prevent SSRF in custom base URLs, redirects, DNS resolution, and private-network access;
- use provider allowlists and explicit user consent for data egress;
- separate user and workspace credentials;
- enforce tenant isolation;
- add request IDs and audit events;
- configure safe timeouts, bounded retries, circuit breakers, and cancellation;
- never retry a non-idempotent tool action without safeguards;
- disclose which upstream provider receives each request;
- provide a local-only mode and clear data-retention settings;
- protect streaming endpoints and browser origins;
- do not allow arbitrary tools or shell commands through a chat endpoint.

---

# 10. User experience and configuration

If OpenClone has a dashboard/configuration UI, add a clean integration management area. If it does not, use documented config files and CLI diagnostics rather than inventing a large dashboard.

Potential sections:
- **Model Gateway:** router status, endpoint, selected routing profile, available models.
- **Providers:** provider connection state, configured model list, quota/health only when supported by upstream data.
- **Security Tools:** installed/available tools, versions, profiles, last scan, findings.
- **Integrations:** IDE/agent adapters and setup status.
- **Reports:** scan history and export.
- **Settings:** credentials configuration guidance, data egress, retention, allowlists, and permissions.

Never display a green “secure” state merely because a scan completed. Show coverage, tools not run, exclusions, errors, and residual risk.

Do not store API keys in browser localStorage or expose them to client code. Prefer server-side secret management. If local-only CLI operation is chosen, document OS environment variables or an appropriate local secret store.

---

# 11. Dependency, runtime, and deployment strategy

- Keep heavyweight security tools optional.
- Prefer official releases, signed artifacts, package registries, or verified container images.
- Pin versions or digests for reproducible CI and deployment.
- Verify checksums/signatures when upstream provides them.
- Avoid running `curl | sh` or equivalent unreviewed install pipelines.
- Do not bundle every security tool into the default OpenClone install.
- Use Docker Compose only if multiple services genuinely need orchestration.
- Do not introduce Kubernetes, Redis, a new database, or a queue unless the audit proves a need.
- Define CPU/memory/disk expectations for optional tools.
- Support graceful behavior when a tool is absent.
- Add version checks and upgrade guidance.
- Provide a cleanup process for temporary clones and generated artifacts.

---

# 12. Testing and verification

## LLM gateway
- provider configuration validation;
- model catalog parsing;
- routing determinism where expected;
- 429/5xx/timeout fallback;
- cooldown and circuit breaker behavior;
- streaming correctness;
- tool-call preservation;
- context/capability filtering;
- provider identity in response metadata;
- no silent provider substitution;
- no credential leakage;
- SSRF and URL validation;
- local-only binding and authentication;
- concurrency and resource limits.

Use mocks for CI. Do not require paid live API calls. Optional live tests must require explicit opt-in and have cost/time limits.

## Security orchestration
- missing tool handling;
- version detection;
- timeout handling;
- safe command construction (no shell injection);
- path and target allowlist enforcement;
- sandbox boundary tests;
- structured output parsing;
- SARIF handling;
- report normalization;
- finding deduplication;
- scan failure versus clean result distinction;
- confirmation gate for fixes;
- no unauthorized network target accepted.

## Regression
- run all existing OpenClone tests and quality gates;
- preserve existing IDE adapters and Taste Skill;
- preserve global anti-AI-slop governance;
- verify generated instructions do not conflict;
- verify install/uninstall and cleanup do not overwrite user files.

Never claim a test passed unless it was actually run.

---

# 13. Implementation phases

## Phase 0 — Baseline and safe acquisition
- Inspect OpenClone and Git state.
- Create isolated research workspace.
- Clone all 20 listed repositories that are accessible.
- Record commit SHA, license, release, status, and source URL.
- Do not execute candidate code.

## Phase 1 — Static audit and comparison
- Read READMEs, licenses, manifests, lockfiles, CI, Dockerfiles, install scripts, security policies, and relevant source.
- Compare the eight routers.
- Classify the twelve security tools.
- Identify overlaps, risks, integration options, and blocked candidates.
- Produce a decision matrix and recommended shortlist.

## Phase 2 — Architecture and decisions
- Record architecture decision records.
- Select primary router strategy.
- Define optional security profiles and tool adapters.
- Define data flow, secret boundaries, and permissions.
- Decide what remains an external dependency versus what belongs in OpenClone source.

## Phase 3 — Integrate the router
- Integrate the selected router using a stable supported interface.
- Add OpenClone configuration, health checks, diagnostics, and tests.
- Add model/provider capability metadata only where verified.
- Test one real coding-agent integration in a disposable sample project, with user-provided credentials only if available and explicitly authorized.

## Phase 4 — Integrate security tools
- Add the high-value non-invasive tools first: secrets, SAST, dependencies/SBOM, agent-skill scanning.
- Add optional malware/container/IaC checks as relevant.
- Add dynamic scanning only behind explicit authorization and isolated execution.
- Add AI red-team/research workflows as optional profiles, not mandatory CI gates.

## Phase 5 — Orchestration and reports
- Normalize outputs.
- Add reproducible profiles, reports, and CI hooks.
- Preserve original evidence and source severity.
- Add safe suppression and baseline mechanisms.

## Phase 6 — Documentation and release readiness
- Update architecture and setup docs.
- Add third-party notices and SBOM as appropriate.
- Document free-tier limitations and provider data handling.
- Run security and regression tests.
- Report exact implemented, external, experimental, and rejected integrations.

---

# 14. Acceptance criteria

The work is complete only when:

1. All 20 candidate URLs have a recorded acquisition result.
2. All successfully cloned repositories have a commit SHA and license/status record.
3. No candidate code was executed before the initial static trust review.
4. A comparison matrix explains which router was selected and why.
5. The selected router works through a documented OpenClone integration path.
6. Actual provider/model identity is visible; fallback is transparent.
7. Free-tier limits and data-sharing caveats are documented.
8. A coding-agent integration is verified in a disposable sample project, or clearly marked pending credentials/environment.
9. Security tools are categorized by purpose and integrated through optional, least-privilege adapters.
10. Dynamic testing is disabled by default and requires explicit authorized targets.
11. Credentials are not committed, logged, or exposed client-side.
12. Existing OpenClone architecture, adapters, Taste Skill, and global anti-AI-slop governance remain intact.
13. License notices and third-party attribution are correct.
14. Tests and quality gates pass, with exact commands and results reported.
15. No deployment, publication, commit, or push occurs without explicit authorization.

---

# 15. Required final deliverables

Create/update the following using existing repository conventions:

- `docs/integrations/llm-router-comparison.md`
- `docs/integrations/security-toolchain.md`
- `docs/integrations/compatibility-matrix.md`
- `docs/security/llm-gateway-threat-model.md`
- `docs/security/security-profiles.md`
- `docs/integrations/adding-a-router.md`
- `docs/integrations/adding-a-security-tool.md`
- `THIRD_PARTY_NOTICES.md` or the existing equivalent
- machine-readable tool/provider manifests if the repository uses them
- architecture decision records for major selections

Do not create duplicate documents if equivalent files already exist; update the canonical files instead.

### Final report

Provide:
1. baseline architecture and Git status;
2. acquisition result for each of the 20 repositories;
3. commit SHA, license, and status for each acquired repository;
4. router comparison and selected primary router;
5. security-tool integration matrix;
6. files added/changed;
7. tools actually integrated versus merely documented;
8. security review and threat-model findings;
9. tests run and exact pass/fail results;
10. known limitations and unverified items;
11. cleanup status of temporary clones;
12. confirmation that no commit, push, deployment, or release was performed.

---

# 16. Start now

Start with Phase 0. Inspect the actual OpenClone checkout and Git status, then safely clone the 20 listed repositories into an isolated temporary workspace. Verify every repository identity and record its commit and license. Do not run any candidate scripts or install dependencies yet.

Proceed to static audit and comparison. Only after the audit should you select and integrate the smallest, safest, highest-value set of components.

**The target is not to make OpenClone a dumping ground for 20 repositories. The target is to make OpenClone a clean control plane that can securely use the best router and security tools, with explicit boundaries, verified integrations, and maintainable upgrades.**
