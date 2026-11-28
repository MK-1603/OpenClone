# OpenClone — Global Anti-AI-Slop Governance Upgrade
**Single master execution prompt for Antigravity | Version 1.0.0**

## Mission

Upgrade OpenClone's existing anti-AI-slop standards into a coherent, repository-wide quality governance system that prevents low-quality, generic, unnecessary, unverified, over-engineered, repetitive, insecure, or poorly finished AI-assisted work across the entire software lifecycle.

This is an upgrade of the existing system—not a greenfield rewrite.

The repository snapshot previously shared shows an existing design-focused foundation, including:

- `domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md`
- `domains/05-UX-UI-ENGINEERING/HUMAN-CRAFTED-DESIGN-SYSTEM.md`
- `domains/05-UX-UI-ENGINEERING/TASTE-SKILL-GUIDE.md`
- `skills/taste-skill/`
- `skills/taste-skill/skills/taste-skill/SKILL.md`
- `skills/taste-skill/skills/taste-skill/references/anti-slop-governance.md`
- `skills/taste-skill/skills/taste-skill/scripts/audit-slop.mjs`
- `skills/taste-skill/skills/taste-skill/scripts/gate.mjs`
- `skills/taste-skill/skills/taste-skill/scripts/instruction-audit.mjs`
- related consistency, copy-lint, plan-check, performance, and design-quality scripts
- governance, agent rules, workflows, domains, engines, workforce, adapters, tests, and documentation.

These paths are based on a previously supplied repository tree. Verify the current checkout and exact paths before acting. Do not assume the snapshot is current.

### Desired outcome

Create **one global Anti-AI-Slop governance policy**, supported by focused domain standards, practical agent instructions, and proportionate automated checks.

The system must work across:
- planning and requirements
- product decisions and feature scope
- architecture and system design
- frontend, backend, mobile, and API implementation
- UI/UX and visual design
- code quality and maintainability
- data and database engineering
- AI/ML, prompts, agents, and automation
- security, privacy, and compliance
- testing, verification, and debugging
- documentation and technical writing
- dependencies and technology selection
- DevOps, cloud, deployment, and operations
- repository organization and developer experience
- workflows, handoffs, reviews, and workforce collaboration
- context, memory, token, and compute usage.

Do not interpret “anti-AI-slop” as “avoid using AI.” The objective is to prevent low-quality outcomes regardless of whether a human or AI produced them.

---

## 1. Mandatory execution rules

1. Inspect the actual repository, current branch, Git status, tracked/untracked files, current governance documents, scripts, tests, manifests, and adapter configurations before modifying anything.
2. Read the full contents of every existing anti-slop-related source before proposing changes. At minimum inspect the files listed above if they exist.
3. Search the entire repository for related rules and enforcement, not just filenames containing `slop`.
4. Build an evidence-based inventory of current rules, checks, gates, references, and duplicates.
5. Preserve the existing Taste Skill as a complete, independently useful package. Do not delete, flatten, rename, or break its assets, references, scripts, examples, license, changelog, installation, or tests.
6. Reuse existing validators and scripts when they are correct. Extend them only where a real gap exists.
7. Do not create a second design-quality system that competes with Taste Skill. Keep design-specific expertise in Taste Skill and connect it to global governance through a clear contract.
8. Do not create hundreds of rules to make the system appear comprehensive. Prefer a small set of strong global principles, focused domain controls, and measurable acceptance criteria.
9. Do not turn subjective preferences into mandatory universal rules. Make context-dependent guidance conditional and explain when it applies.
10. Do not treat every AI-generated, unconventional, minimal, or visually simple output as slop. Judge outcomes against purpose, constraints, evidence, quality, and user needs.
11. No speculative feature additions, unnecessary frameworks, duplicated registries, excessive scripts, arbitrary score thresholds, or architecture rewrites.
12. Every new rule must have a unique ID, scope, rationale, severity, applicability, verification method, and owner/source of truth.
13. Every automated check must have tests, clear output, documented limitations, and a remediation path.
14. Never claim a check is automated if it is only an instruction or a manual review.
15. Never claim that a tool can reliably detect subjective quality from text patterns alone.
16. Do not delete or rewrite existing material until its purpose, references, ownership, and migration path are understood.
17. Do not commit, push, publish, tag, release, or deploy without explicit authorization.
18. Work in phases. Run relevant tests after each phase and report evidence, not assumptions.

---

## 2. Phase 0 — Repository audit and baseline

### 2.1 Locate all relevant material

Search for:
- AI slop, anti-slop, slop audit, human-crafted, quality gate, quality assurance
- simplicity, scope control, over-engineering, unnecessary abstraction
- instruction governance, prompt quality, agent rules
- hallucination, evidence, provenance, verification, source quality
- copy lint, accessibility, performance, security, dependency governance
- token budgets, context loading, memory lifecycle, cost governance
- definition of done, completion reports, phase gates, review contracts.

Inspect:
- all relevant `domains/` documents
- `00-GOVERNANCE/` or its current equivalent
- `30-AGENT-RULES-AND-VERIFICATION/` or its current equivalent
- `AGENTS.md` and root instructions
- all relevant workflows and engines
- `skills/taste-skill/` in full
- all adapter-specific rules and skills
- existing scripts and test suites
- policy precedence and exception registers
- root README and documentation indexes.

### 2.2 Establish a baseline inventory

Produce a machine-readable and human-readable inventory containing:

| Field | Meaning |
|---|---|
| Rule ID | Existing ID or `UNASSIGNED` |
| Rule title | Short descriptive name |
| Source file | Canonical current path |
| Domain | Global or specialist domain |
| Rule type | Principle, requirement, recommendation, check, gate |
| Severity | Critical, high, medium, low, advisory |
| Applicability | Always, conditional, domain-specific |
| Enforcement | Automated, human review, instruction-only, none |
| Test coverage | Existing test reference or missing |
| Duplicate/conflict | Related rule IDs |
| Disposition | Keep, merge, revise, split, deprecate, archive |

Count actual unique rules only after reading and normalizing their contents. Do not infer rule counts from filenames or headings. Report separately:
- source documents
- unique normative rules
- advisory guidelines
- automated checks
- human-review checks
- gates
- duplicates
- conflicts
- untested controls.

Do not count one rule repeatedly merely because it is copied into several adapters.

### 2.3 Baseline quality report

Record:
- what currently works
- what is design-only
- what already applies globally
- what is merely advisory
- which scripts are genuinely executable
- test status
- gaps and false-positive risks
- rule conflicts and unclear authority
- duplicated content and maintenance burden.

Do not modify files in Phase 0.

---

## 3. Target governance architecture

Adapt this conceptual architecture to the existing repository. Do not force a new folder structure if an equivalent canonical structure already exists.

```text
GLOBAL ANTI-AI-SLOP GOVERNANCE
│
├── 1. Global policy and principles
│
├── 2. Domain standards
│   ├── Product and scope
│   ├── Requirements and planning
│   ├── Architecture and engineering
│   ├── Code and implementation
│   ├── UI/UX and visual design
│   ├── AI, prompts and agents
│   ├── Security and privacy
│   ├── Data and integrations
│   ├── Testing and verification
│   ├── Documentation and communication
│   ├── Dependencies and technology
│   ├── DevOps and operations
│   ├── Repository and developer experience
│   └── Context, tokens and resource efficiency
│
├── 3. Enforcement and review
│   ├── Preflight checks
│   ├── Planning gates
│   ├── Implementation checks
│   ├── Review gates
│   └── Completion verification
│
├── 4. Tooling
│   ├── Static validators
│   ├── Domain-specific audits
│   ├── Human-review checklists
│   └── Reports and evidence
│
└── 5. Integrations
    ├── Antigravity
    ├── Claude Code
    ├── Codex
    ├── Cursor
    └── Other supported hosts
```

### Source-of-truth principle

- One canonical global policy.
- One canonical rule registry, if a registry is justified by the existing architecture.
- Domain standards contain specialist details and reference global rules.
- Taste Skill remains the canonical specialist design-quality package.
- Adapters contain only host-specific instructions and links/references to canonical policies where possible.
- Do not copy the full global policy into every agent, skill, workflow, or adapter.
- Define precedence and conflict resolution using the repository's existing governance model.

---

## 4. Global principles to formalize

Audit existing principles first. Merge or revise rather than duplicating them.

The global policy should cover the following outcomes.

### 4.1 Purpose and user-value discipline
- Every feature, abstraction, document, and automation must serve a defined user or engineering need.
- Do not add features because they are easy to generate or sound impressive.
- Prefer the smallest complete solution that satisfies acceptance criteria.
- Identify non-goals and explicit exclusions.
- Challenge assumptions before expanding scope.

### 4.2 Evidence and truthfulness
- Do not invent APIs, package behavior, benchmarks, test results, citations, integrations, or implementation status.
- Distinguish verified facts, assumptions, estimates, proposals, and unknowns.
- Verify external technical claims against appropriate current sources when required.
- Never report a command, test, deployment, or action as completed unless it actually ran successfully.
- Preserve traceability from requirements to implementation and tests where appropriate.

### 4.3 Simplicity and proportionality
- Avoid unnecessary abstraction, wrappers, services, patterns, dependencies, configuration, and indirection.
- Do not introduce distributed systems, queues, caches, microservices, or databases without demonstrated need.
- Prefer existing project conventions and supported dependencies.
- Do not rewrite working code merely to match personal preferences.
- Complexity must be justified by measurable requirements or material risk reduction.

### 4.4 Engineering quality
- Generated code must be understandable, maintainable, tested, and consistent with the repository.
- Avoid placeholder implementations, dead code, fake integrations, empty handlers, broad exception swallowing, unsafe defaults, and duplicated logic.
- Handle errors, validation, resource limits, and edge cases proportionately.
- Do not confuse code volume with engineering completeness.

### 4.5 Design and communication quality
- Preserve user needs, accessibility, usability, hierarchy, and product identity.
- Avoid generic templates, decorative effects without purpose, meaningless animations, empty marketing claims, repetitive copy, and fabricated testimonials.
- Use Taste Skill for its established design-specific audits and standards.
- Do not impose one aesthetic style on every product; quality is contextual.

### 4.6 Security and privacy
- No insecure shortcuts, exposed secrets, excessive permissions, unvalidated input, or unsafe execution.
- Apply least privilege, safe defaults, and threat-aware design.
- Security exceptions require explicit justification, risk ownership, and documented approval.

### 4.7 Resource and context efficiency
- Avoid loading entire repositories or knowledge bases when targeted context is sufficient.
- Avoid repeated tool calls, redundant summaries, unnecessary model calls, and unbounded outputs.
- Use the smallest adequate model/tool/resource for the task, without compromising correctness or safety.
- Do not optimize token usage by omitting necessary evidence, tests, or safety checks.
- Record meaningful cost/resource constraints only where they can be measured.

### 4.8 Completion integrity
- Define done through observable acceptance criteria.
- Verify changed behavior with relevant tests and checks.
- Report what changed, what was tested, what failed, and what remains unverified.
- No fake execution, fake completion, or unsubstantiated quality claims.

---

## 5. Domain-specific coverage

Create or update specialist standards only where the audit identifies a real gap. Each domain should contain concrete anti-patterns, positive alternatives, and verification guidance.

1. **Product and feature scope**
   - feature inflation, speculative requirements, unnecessary dashboards/settings, solving nonexistent problems.
2. **Requirements and planning**
   - vague requirements, untestable acceptance criteria, oversized plans, invented user needs, premature implementation.
3. **Architecture**
   - over-engineering, pattern worship, unnecessary services, needless abstraction, premature scaling, architecture astronautics.
4. **Code and implementation**
   - duplicated code, dead code, placeholder logic, unsafe shortcuts, unnecessary dependencies, unreadable generated code.
5. **UI/UX and visual design**
   - generic AI aesthetics, meaningless gradients/glass effects, template-like layouts, poor hierarchy, inaccessible interactions, decorative clutter.
   - Reuse Taste Skill rather than duplicating its design library.
6. **AI, prompts and agents**
   - vague prompts, role inflation, excessive agent delegation, circular agent conversations, redundant tools, fabricated tool results, unbounded loops.
7. **Security and privacy**
   - unsafe defaults, overprivileged tools, secret leakage, untrusted input, missing authorization, prompt-injection exposure.
8. **Data and integrations**
   - unnecessary data collection, schema bloat, brittle integrations, invented API assumptions, missing idempotency or validation where needed.
9. **Testing and verification**
   - fake tests, snapshot-only confidence, untested critical paths, ignored failures, meaningless coverage targets.
10. **Documentation and communication**
    - repeated docs, huge root README, stale instructions, generic prose, fabricated badges, unsupported claims, docs that do not match code.
11. **Dependencies and technology**
    - dependency accumulation, fashionable stack choices, unverified compatibility, abandoned packages, unnecessary vendor lock-in.
12. **DevOps and operations**
    - needless infrastructure, excessive observability stacks, unsafe deployment automation, unbounded retention, unjustified Kubernetes.
13. **Repository and developer experience**
    - duplicate source-of-truth files, unclear ownership, confusing folder sprawl, committed generated artifacts, dead examples.
14. **Context and resource usage**
    - repeated context ingestion, oversized prompts, unnecessary model calls, verbose tool output, wasteful memory retention.

Do not create a separate file for every bullet. Group related rules into a maintainable number of standards.

---

## 6. Rule taxonomy and rule quality

Use a consistent rule schema. Adapt to existing registry conventions if present.

Each rule should include:

```yaml
id: AAS-<DOMAIN>-<NUMBER>
title: Short imperative title
scope: global | domain
domain: <domain>
severity: critical | high | medium | low | advisory
type: requirement | recommendation | prohibition
applicability: always | conditional
statement: Clear, testable rule
rationale: Why it matters
anti_patterns:
  - Observable failure example
preferred_approach: Practical alternative
verification:
  mode: automated | human_review | instruction_only
  method: How to verify
remediation: How to correct a finding
exceptions:
  allowed: true | false
  approval_required: true | false
references: []
```

### Rule writing standards
- One rule should express one primary obligation.
- Use clear, direct language.
- Avoid vague terms such as “good,” “clean,” “modern,” or “professional” unless defined.
- State conditions and exceptions.
- Do not make subjective criteria appear objectively machine-verifiable.
- Avoid duplicate rules with slightly different wording.
- Use stable IDs and preserve them across revisions.
- Document deprecated IDs and replacements; never silently recycle an ID.

### Severity semantics
- **Critical:** creates serious security, privacy, integrity, or destructive-operation risk.
- **High:** likely to cause material user harm, major defects, or unacceptable delivery risk.
- **Medium:** material quality or maintainability issue that should normally be fixed.
- **Low:** limited issue with a practical improvement.
- **Advisory:** contextual guidance, not a release blocker.

Do not assign high severity merely because a style preference is violated.

---

## 7. Enforcement model

Use layered enforcement rather than trying to automate every quality judgment.

### Layer A — Always-on instructions
- concise global principles in root agent instructions
- clear precedence and links to canonical standards
- host-specific instructions in adapters
- no massive policy copy-paste into every context.

### Layer B — Preflight
Before significant work:
- identify task type and affected domain
- inspect relevant project conventions
- understand existing functionality
- define expected outcome and non-goals
- identify risks and approval requirements
- select relevant standards only.

### Layer C — Plan review
Before implementation when task complexity warrants it:
- verify user value
- challenge scope
- compare simpler alternatives
- identify dependencies and architecture impact
- define acceptance criteria and test plan
- flag speculative work.

Do not force a heavyweight plan for trivial changes.

### Layer D — Implementation checks
- run relevant static checks
- validate schemas and contracts
- detect known unsafe patterns
- check dependency changes
- use Taste Skill for applicable design work
- inspect diffs for unrelated or generated changes.

### Layer E — Independent review
- verify requirements and acceptance criteria
- inspect correctness, security, performance, accessibility, maintainability, and scope
- distinguish blocking defects from advisory suggestions
- require evidence for findings.

### Layer F — Completion gate
- run appropriate tests
- verify actual outputs
- report failures and limitations
- ensure documentation reflects actual behavior
- do not claim full completion when material checks remain unverified.

---

## 8. Automated tooling upgrade

Audit the existing Taste Skill scripts before changing them.

### Existing scripts to inspect if present
- `audit-slop.mjs`
- `gate.mjs`
- `instruction-audit.mjs`
- `consistency.mjs`
- `copy-lint.mjs`
- `plan-check.mjs`
- `perf.mjs`
- any related tests and package scripts.

### Required tooling principles

1. Preserve design-specific behavior in Taste Skill.
2. Do not turn a design scanner into a universal code-quality scanner.
3. Create a small global audit entry point only if it can orchestrate existing checks without duplicating their logic.
4. Use domain-specific adapters/plugins for checks where necessary.
5. Keep static checks deterministic and explainable.
6. Use configuration and allowlists for known legitimate exceptions.
7. Provide machine-readable JSON output and concise human-readable summaries.
8. Support changed-file or scoped audits so a small task does not require scanning everything.
9. Include stable finding IDs, source location, severity, explanation, confidence, and remediation.
10. Make exit codes meaningful for CI and local use.
11. Avoid network calls in ordinary local audits unless explicitly configured.
12. Never execute arbitrary project code during a static audit.
13. Bound CPU, memory, file sizes, recursion, and output.
14. Exclude generated files, vendor directories, build outputs, caches, and binary assets where appropriate.
15. Document false positives and known blind spots.

### Detection limitations

Static heuristics may flag suspicious patterns, but they cannot reliably determine:
- whether a feature is truly valuable
- whether an architecture is over-engineered in its business context
- whether a design feels original or appropriate
- whether prose is genuinely useful
- whether an abstraction is justified.

For these matters, produce review prompts/checklists and require human or contextual judgment. Do not claim automated detection where it does not exist.

### Suggested command interface

Follow existing package conventions. If a command surface is justified, prefer a simple interface such as:

```text
openclone quality audit
openclone quality audit --changed
openclone quality audit --domain architecture
openclone quality audit --format json
openclone quality explain <finding-id>
```

These are proposed command names only. Do not implement a new CLI if an existing interface can provide the same capability cleanly.

---

## 9. Scorecards and quality gates

Do not create one opaque “AI slop score” that pretends to measure all quality.

If a scorecard is useful, show separate dimensions:
- correctness and evidence
- user value and scope discipline
- engineering simplicity
- maintainability
- security and privacy
- usability and accessibility
- documentation accuracy
- verification completeness
- resource efficiency.

For each dimension:
- state what is measured
- identify evidence
- state whether the result is automated or reviewed
- show unknown/not-applicable distinctly
- avoid false precision.

A critical security or integrity violation must not be hidden by a high average score.

Use risk-based gates:
- Critical: block until resolved or explicitly handled under policy.
- High: normally block release or require accountable approval.
- Medium: fix before completion where practical, otherwise document accepted risk.
- Low/advisory: report without unnecessarily blocking delivery.

Do not create arbitrary percentage thresholds without baseline data and validation.

---

## 10. Integration into existing OpenClone lifecycle

Inspect the current lifecycle and connect anti-slop controls to existing workflows and engines instead of creating parallel processes.

Evaluate where relevant:
- project intake and mode selection
- problem and product validation
- requirements engineering
- feature prioritization and scope control
- architecture and technology selection
- execution planning and delegation
- context handoff and memory
- implementation and code review
- security and privacy review
- test strategy and execution
- independent verification
- release readiness
- maintenance and closeout.

For every integration point:
- identify the existing workflow/engine/agent responsible
- add a concise reference or check
- avoid duplicating its existing responsibility
- define the trigger and expected evidence
- test the integration where possible.

The system should be proportional:
- trivial change: lightweight checks
- normal feature: relevant domain checks
- high-risk or cross-cutting change: full review and approval gates.

---

## 11. Cross-platform adapter integration

Inspect current adapter support and update only what exists and is supported:
- Antigravity
- Claude Code
- Codex
- Cursor
- other adapters discovered in the repository.

Each adapter should:
- load concise global rules
- reference the canonical source of truth
- invoke available checks only when supported
- explain host limitations
- avoid copying a large global policy into every host configuration
- preserve host-native conventions.

Do not claim that a host can run a script, hook, plugin, or command unless verified.

---

## 12. Documentation deliverables

Create or update documentation in the repository's established location and naming conventions.

Required outcomes:
1. Global Anti-AI-Slop Governance policy.
2. Rule taxonomy and precedence.
3. Rule registry or inventory, if justified.
4. Domain standards or clear links to existing standards.
5. Enforcement lifecycle and gate guide.
6. Automated tooling usage and limitations.
7. Human-review checklist.
8. Exception and risk-acceptance process.
9. Adapter integration guide.
10. Audit report with baseline and post-upgrade status.
11. Root documentation index links.
12. Changelog entry.

Keep the root README concise. Do not turn it into an internal policy catalogue.

---

## 13. Migration and compatibility

- Preserve all existing rule IDs where possible.
- Map duplicate rules to one canonical rule.
- Record deprecated rules and replacements.
- Update inbound links, references, manifests, tests, and adapter files.
- Preserve Taste Skill's standalone installation and functionality.
- Keep existing CLI and script interfaces backward-compatible unless a justified breaking change is approved.
- If a breaking change is necessary, document migration steps.
- Do not remove old documents until their content is migrated, references updated, and history preserved.
- Avoid moving files merely for visual neatness.

---

## 14. Testing and acceptance criteria

Add tests for the actual controls introduced or modified.

At minimum verify:
1. Rule registry/schema validation.
2. Unique rule IDs.
3. Required rule metadata.
4. No unresolved duplicate IDs.
5. No broken policy references.
6. Policy precedence is unambiguous.
7. Existing Taste Skill tests still pass.
8. Existing audit scripts still work.
9. New audit entry point works for a small fixture repository.
10. Known anti-pattern fixtures produce expected findings.
11. Legitimate code/design fixtures do not trigger excessive false positives.
12. Scoped/changed-file mode behaves correctly.
13. JSON output conforms to a documented schema.
14. Exit codes match documented behavior.
15. Exceptions and allowlists are validated and auditable.
16. Existing OpenClone tests and repository validation still pass.
17. No unrelated generated files, secrets, caches, or binary artifacts are added.
18. Documentation commands match actual executable commands.

Report tests as **passed**, **failed**, or **not run**. Never label unexecuted checks as passed.

---

## 15. Execution phases

### Phase 0 — Audit
Read current sources, inventory rules, scripts, tests, duplicates, and gaps. Establish baseline counts. No edits.

### Phase 1 — Governance design
Define canonical policy ownership, taxonomy, rule schema, severity, precedence, and exception handling. Produce a migration map. Review for duplication and unnecessary complexity.

### Phase 2 — Policy consolidation
Upgrade the global policy and domain references. Preserve specialist Taste Skill content. Merge duplicate rules carefully and retain traceability.

### Phase 3 — Lifecycle integration
Connect concise checks to existing instructions, workflows, engines, review contracts, and adapters. Do not create parallel lifecycle machinery.

### Phase 4 — Tooling
Improve existing scripts and tests. Add a global orchestrator only if justified. Keep subjective evaluation human-reviewed.

### Phase 5 — Verification
Run all relevant tests, repository validation, rule registry checks, script checks, and regression tests.

### Phase 6 — Documentation and report
Update documentation and changelog. Produce baseline-versus-final inventory and implementation report.

After each phase:
- summarize changes
- show files touched
- report tests run
- report unresolved risks
- continue unless a real blocker requires clarification.

---

## 16. Final deliverable report

At the end, provide:

1. Baseline number of source documents.
2. Baseline number of unique rules.
3. Baseline number of automated checks.
4. Baseline number of human-review checks.
5. Duplicate/conflicting rules found.
6. Final canonical rule count, with counting method.
7. Domain coverage matrix.
8. Existing files reused and upgraded.
9. New files created and why each was necessary.
10. Scripts/tools changed and their real capabilities.
11. Taste Skill preservation/regression results.
12. Lifecycle and adapter integration status.
13. Tests passed, failed, and not run.
14. False-positive limitations and known gaps.
15. Exceptions or unresolved risks.
16. Exact commands to run audits locally and in CI.
17. Confirmation that no commit, push, release, publication, or deployment occurred.

## Definition of success

OpenClone has a maintainable, evidence-based global quality governance system that prevents low-quality AI-assisted outcomes without slowing down useful work, forcing unnecessary process, duplicating existing tools, or treating subjective taste as machine fact.

**Begin with Phase 0. Inspect the actual repository. Read the existing sources. Establish the baseline. Do not start by creating more rules or files.**
