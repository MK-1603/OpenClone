# OpenClone — Strix Feasibility, Integration & Project Completion Upgrade
**Master upgrade specification and Antigravity execution prompt**
**Version 1.0.0**

---

# PART A — STRIX: WHAT IT DOES AND WHETHER IT FITS OPENCLONE

## 1. Executive verdict

**Strix is feasible and valuable as an optional dynamic application-security testing engine in OpenClone.** It should be integrated into the existing Project Execution Engine and Security Orchestrator—not treated as a replacement for the other security tools, and not copied wholesale into OpenClone's core source.

Recommended integration:

- Keep Strix as an independently versioned upstream tool.
- Add an OpenClone Strix adapter/runner, configuration schema, execution policy, result importer, and project workflow.
- Expose Strix through the security orchestration layer and, where useful, through a coding-agent skill.
- Run source-code review and live application penetration tests as distinct modes.
- Require explicit target authorization, bounded budget, isolated execution, and user approval for live/dynamic testing.
- Feed findings into the same project issue/remediation/verification workflow used by other security tools.
- Re-run the relevant test after remediation and preserve the before/after evidence.

Official project: [usestrix/strix](https://github.com/usestrix/strix)

## 2. What Strix actually provides

Strix describes itself as an open-source autonomous AI penetration-testing tool. Its agents can inspect and dynamically test applications, use a security testing toolkit, validate vulnerabilities with proof-of-concept evidence, and produce reports. It supports local source targets, web applications, APIs, and multiple targets. It also documents agent skills, a local CLI, CI integration, and a managed cloud offering.

Capabilities described by the project include:
- reconnaissance and attack-surface mapping;
- web and API testing;
- authentication and authorization weaknesses;
- IDOR and broken access control;
- SQL/NoSQL/command injection and server-side template injection;
- XSS, CSRF, SSRF, and related web weaknesses;
- business-logic and race-condition testing;
- infrastructure/cloud misconfiguration checks;
- proof-of-concept validation and remediation guidance;
- multi-agent coordination;
- local result viewer and structured reports;
- coding-agent skills for running tests, fixing findings, and CI integration.

These are upstream project claims and capabilities; OpenClone must still verify the exact installed version, enabled mode, and target-specific coverage. A scan does not prove that an application is secure.

## 3. Strix operating modes

| Mode | Where it runs | Typical use | Key consideration |
|---|---|---|---|
| Open-source CLI | User's machine/runner, using Docker sandbox and a configured LLM provider | Local development, source review, controlled CI | Requires Docker and an LLM provider/API key; model usage may cost money |
| Managed Strix Cloud | Strix-hosted platform via CLI/API | Centralized scans, team workflows, hosted execution | Source/target data is sent to the managed service; account, scope, credits, and plan limits apply |
| Enterprise/self-hosted offerings | According to the vendor's current offering | Organization-level controls and deployment needs | Verify commercial terms, availability, and deployment details directly |

Do not assume the managed cloud is free, that local CLI means zero cost, or that a ChatGPT/Claude consumer subscription automatically grants API access. The current Strix documentation describes supported authentication options; OpenClone must follow the documented route for the installed release.

## 4. Local CLI prerequisites and safe setup

The current upstream quick-start describes:
- Docker running;
- Strix CLI installed;
- an LLM provider/model configured;
- an API key or another currently documented authentication method;
- first-run download of the Strix sandbox image.

The upstream README currently documents a standalone installer and Python package-manager alternatives. Do not execute a remote install script automatically from OpenClone. Prefer a reviewed, pinned installation procedure and verify the official instructions at setup time.

Illustrative upstream-style environment configuration:

```bash
export STRIX_LLM="openrouter/provider/model"
export LLM_API_KEY="YOUR_KEY"
```

Keep real keys in an OS secret store, protected environment variables, or approved CI secrets. Never put them in `PROJECT.md`, `AGENT.md`, committed `.env` files, logs, test fixtures, or browser storage.

The upstream agent skill documents a headless local source scan similar to:

```bash
strix -n -t ./ --scan-mode standard --max-budget 10
```

Treat this as an example only. Verify the exact flags and scan-mode values against the installed Strix version before generating commands. Always set an explicit budget cap for agent-driven scans.

## 5. Agent skill integration

The upstream project documents installing its coding-agent skills using:

```bash
npx skills add usestrix/strix
```

The documented skill set includes workflows for:
- penetration testing;
- managed pentesting;
- fixing security vulnerabilities and re-testing;
- CI security scanning;
- application security testing;
- web application penetration testing.

The exact number and names of skills may change by release. Inspect the upstream skill directory and license at the pinned commit before adopting them.

**OpenClone recommendation:** do not blindly install skills into every IDE globally. Add an OpenClone-managed, opt-in Strix skill adapter:
1. Pin and inspect the upstream skill source.
2. Verify its license and files.
3. Copy or link only approved skill content into the OpenClone project-local skill location, preserving attribution.
4. Generate environment-native references only for verified IDE adapters.
5. Keep the canonical OpenClone security policy authoritative.
6. Require approval before the skill invokes dynamic scans or changes code.

Strix skills are a workflow layer; the Strix CLI/cloud service is the execution engine. They are not interchangeable.

## 6. Feasibility assessment

| Area | Feasibility | Recommendation |
|---|---|---|
| Add Strix as optional CLI tool | High | Implement first |
| Add project-local Strix configuration | High | Implement with schema validation |
| Invoke headless local source scan | High, subject to Docker/LLM prerequisites | Support as an opt-in profile |
| Import Strix JSON/SARIF/report output | High if output schema is confirmed for pinned version | Build version-aware importer |
| Add coding-agent skills | High | Pin, audit, and install project-locally |
| Add Strix to project completion gates | High | Make risk-based, not unconditional |
| Run on every small code change | Technically possible, usually inefficient | Do not make default |
| Run on every pull request | Feasible with cost and runtime controls | Optional quick profile; test CI behavior |
| Test a live staging application | Feasible | Explicit authorization and allowlisted target required |
| Test production automatically | High risk | Manual approval, approved window, defined scope; disabled by default |
| Run without Docker in local OSS mode | Not supported by the documented local path | Use documented managed mode or another supported setup |
| Use without an LLM cost | Not guaranteed for local CLI | Verify provider pricing and current Strix options |
| Treat Strix as complete security coverage | Not feasible | Combine with SAST, SCA, secrets, configuration, and human review |
| Clone all Strix source into OpenClone core | Not recommended | Keep upstream separate; integrate through adapter |
| Make Strix mandatory for every project | Not recommended | Applicability and risk-based gate |

### Final verdict

**Integrate Strix as a first-class optional security adapter. Do not make it a hard dependency of OpenClone or every generated project.**

It adds dynamic, exploit-oriented testing that complements static analysis and dependency/secret scanners. Its execution is more expensive and potentially disruptive than ordinary static checks, so it belongs at selected project milestones and release gates.

---

# PART B — HOW STRIX FITS INTO THE OPENCLONE PROJECT LIFECYCLE

## 7. The upgraded end-to-end workflow

```text
                 USER PROJECT.md
                        |
                        v
              OPENCLONE PROJECT INTAKE
                        |
                        v
             REPOSITORY + REQUIREMENTS AUDIT
                        |
                        v
             SELECT RELEVANT OPENCLONE RULES
                        |
                        v
            PROJECT PACKAGE + EXECUTION PLAN
             PROJECT.md / AGENT.md / PLAN
                        |
                        v
                 READINESS GATE
                        |
                        v
               BUILD PROJECT IN SLICES
                        |
             +----------+-----------+
             |                      |
             v                      v
        TESTING GATES          SECURITY GATES
       Unit/Integration       Semgrep / Trivy
       E2E / Type / Build     TruffleHog / etc.
             |                      |
             +----------+-----------+
                        |
                        v
             STRIX DYNAMIC SECURITY GATE
           Local source / isolated test app
           or explicitly authorized staging
                        |
                        v
                TRIAGE FINDINGS
          Confirmed / Potential / Informational
                        |
                        v
               FIX ROOT CAUSE
                        |
                        v
             REGRESSION + STRIX RETEST
                        |
                        v
             SECURITY ACCEPTANCE GATE
                        |
                        v
             RELEASE READINESS REVIEW
                        |
                        v
              PROJECT COMPLETION REPORT
```

Strix is not the first thing that runs and should not be run on every trivial task. Run cheap deterministic checks continuously; run Strix when the project has enough implementation to test meaningfully.

## 8. Recommended security checkpoints

| Project stage | Security checks | Strix use |
|---|---|---|
| P0 — Intake | Identify data sensitivity, exposure, auth, roles, integrations, attack surface | No scan; determine applicability and authorization |
| P1 — Architecture | Threat model, trust boundaries, auth/data-flow review | Usually no scan; prepare test scope |
| P2 — Foundation | Secret scan, dependency scan, SAST, config checks | Optional baseline source review after runnable code exists |
| P3 — Core features | Tests, SAST, dependency checks, authorization tests | Focused local source scan for meaningful attack surfaces |
| P4 — API/authentication | AuthZ tests, input validation, secrets, API contract checks | High-value checkpoint for auth, IDOR, injection, and API behavior |
| P5 — Feature complete | Full relevant static and dynamic test suite | Standard source-assisted assessment |
| P6 — Staging | DAST and integration tests | Authorized staging test, allowlisted host and account |
| P7 — Release candidate | Full security profile, regression, dependency and secret checks | Final scoped assessment; budget and time cap |
| P8 — Post-fix | Regression tests and static checks | Re-test findings and verify remediation |
| P9 — Production | Monitoring, incident and vulnerability process | No automatic production scan unless separately approved |

## 9. Security profiles

Create OpenClone profiles that users can choose:
- `quick-local`: Fast local checks (secrets + SAST).
- `project-security`: Relevant SAST, dependency, secrets, and configuration checks.
- `api-auth-security`: API/authentication-focused tests using test credentials only.
- `staging-pentest`: Authorized staging pentest against allowlisted hosts with budget and time caps.
- `release-security`: Release candidate security validation.
- `remediation-verification`: Reproduce, fix, run unit/regression tests, and targeted retest.

---

# PART C — STRIX INTEGRATION DESIGN INSIDE OPENCLONE

## 10. Unified security finding model

OpenClone normalizes findings from Strix, Semgrep, Trivy, and TruffleHog while preserving source evidence:
- `finding_id`
- `source_tool` (`strix`)
- `source_finding_id`
- `category`
- `severity_original`
- `severity_normalized`
- `confidence`
- `file_path` / `endpoint`
- `evidence`
- `proof_of_concept_reference`
- `remediation_guidance`
- `status` (`new`, `confirmed`, `fix_in_progress`, `verified_fixed`, `accepted_risk`)

## 11. Finding-to-fix lifecycle

```text
STRIX FINDING -> TRIAGE -> TASK -> AGENT FIX -> REGRESSION TEST -> TARGETED RETEST -> VERIFIED FIXED
```
