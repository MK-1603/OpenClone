# OpenClone — Repository Optimization & Public README Upgrade
## Antigravity Master Execution Prompt
**Version:** 1.0.0  
**Purpose:** Safely reorganize the existing OpenClone repository, simplify its top-level structure, clarify ownership, preserve all valuable capabilities, and redesign the root README as a clean, credible open-source project landing page.

---

# 1. ROLE AND EXECUTION EXPECTATIONS

Act as a principal software architect, repository maintainer, Python packaging engineer, documentation architect, open-source maintainer, and migration engineer.

You are working inside the **existing OpenClone repository**. Your task is to inspect the actual checkout, plan and execute a controlled repository optimization, and upgrade the global root `README.md`.

This is an implementation task, not a request to merely write recommendations.

You must work with the repository as it exists now. A previously shared repository tree may be useful as historical context, but it is not proof of the current checkout. Always inspect the actual files, Git state, imports, manifests, tests, and configuration before changing anything.

## Primary outcome

Make OpenClone feel like a well-maintained, approachable open-source software project:

- A clean and understandable root directory.
- Clear responsibility and ownership for every major folder.
- One canonical implementation for each runtime capability.
- Related resources grouped logically.
- Historical and superseded material separated from active resources.
- Existing engineering knowledge and capabilities preserved.
- A concise, polished, useful public-facing root README.
- Working imports, CLI, adapters, discovery, workflows, project generation, schemas, tests, and documentation links after migration.

**Optimize organization, not capability count. Do not achieve a smaller tree by deleting useful work.**

---

# 2. NON-NEGOTIABLE RULES

1. **Preserve before optimizing.** Do not delete, overwrite, or discard useful files merely to simplify the tree.
2. Do not assume the previous repository tree is current. Inspect the live checkout.
3. Do not blindly move folders based on their names. Read files and inspect references first.
4. Do not create duplicate implementations, registries, generators, schemas, or documentation systems.
5. Do not create empty placeholder directories or README files merely to make the tree look complete.
6. Do not rename stable IDs unless there is a compelling compatibility-safe reason and an explicit migration.
7. Preserve all 31 engineering domains and all 56 engine IDs if they are present in the current checkout. Verify the actual counts and identifiers rather than assuming.
8. Preserve workforce roles, teams, contracts, adapter integrations, workflows, templates, schemas, tests, examples, and licenses.
9. Preserve the complete Taste Skill package, including assets, references, scripts, tests, license, changelog, and attribution. Do not flatten, trim, or rewrite it unnecessarily.
10. Preserve all existing user changes. Inspect `git status` before editing. Never reset, clean, stash, or overwrite user work without authorization.
11. Do not remove a file because it appears old, redundant, or unused until references and purpose have been checked.
12. Do not claim tests passed unless you actually ran them and observed successful results.
13. Do not claim features are implemented based only on documentation.
14. Do not invent installation commands, CLI commands, badges, package names, links, supported integrations, model providers, capabilities, or compatibility claims.
15. Do not add dependencies unless required and justified.
16. Do not add infrastructure or technologies simply to make the project appear advanced.
17. Do not publish internal implementation details in the root README unless they are necessary for a new user to get started.
18. Keep security-sensitive files, credentials, local environment files, private notes, and internal-only data out of public documentation and Git tracking.
19. Do not change project identity, package identity, Git remote, license, or versioning policy without explicit authorization.
20. Use small, reviewable migration batches. Validate after every batch.
21. Prefer Git moves/renames where possible so history remains understandable.
22. If a migration is unsafe or ambiguous, leave the source in place, document the issue, and continue with safe work.
23. Do not turn this task into a broad feature-development project. Scope is repository organization, ownership clarity, documentation hierarchy, hygiene, and root README.
24. Avoid “AI slope”: no unnecessary frameworks, folders, abstraction layers, metadata systems, or ornamental README sections.

---

# 3. KNOWN REPOSITORY CONTEXT — VERIFY BEFORE USING

A previous repository tree snapshot showed the following categories. They are audit clues only, not guaranteed current state:

- `adapters/`
- `ASSESSMENT/`
- `blueprints/`
- `concepts/`
- `docs/`
- `domains/`
- `EGM-WORKFLOWS/`
- `engines/`
- `examples/`
- `memory/`
- `modes/`
- `prompts/`
- `reference/`
- `REFERENCE-PROJECTS/`
- `registries/`
- `runtime/`
- `schemas/`
- `security/`
- `security-operations/`
- `skills/`
- `src/`
- `standards/`
- `templates/`
- `tests/`
- `tools/`
- `workflows/`
- `workforce/`

The snapshot also showed root-level governance and project documents, Python packaging configuration, manifests, CLI entry files, and README files.

It included possible overlap between:
- `src/openclone/`
- `runtime/`
- `tools/aisdf_runtime/`

It also showed possible organizational overlap between:
- `domains/` and `standards/`
- `workflows/`, `modes/`, and `EGM-WORKFLOWS/`
- `prompts/` and adapter-specific instructions
- `registries/`, `schemas/`, and `workforce/registry/`
- `security/` and `security-operations/`
- `blueprints/`, `concepts/`, and `reference/`

Treat these as questions to investigate, not proof of duplication.

---

# 4. PHASE 0 — BASELINE AND SAFETY AUDIT

Before editing:

## 4.1 Inspect repository state

Run and record appropriate commands, including:

```bash
git status --short
git branch --show-current
git log -5 --oneline
git ls-files
```

Inspect:
- Root directory and nested tree.
- `.gitignore`.
- `pyproject.toml` and all packaging configuration.
- Python package source and CLI entry points.
- Runtime implementations.
- All manifests and registries.
- Test configuration and test files.
- Workflow and adapter discovery mechanisms.
- Documentation links and path references.
- License and third-party attribution files.

Do not expose secrets in audit output.

## 4.2 Build a file inventory

Create a temporary or documented audit inventory containing:

- Current path.
- File type.
- Responsibility.
- Active, historical, generated, or uncertain status.
- Referenced-by locations.
- Proposed destination, if any.
- Migration risk.
- Validation required.

Do not add a permanent inventory artifact unless it provides lasting maintenance value.

## 4.3 Establish the baseline

Run the existing test suite and repository validation commands that are discoverable from project configuration and documentation.

Record:
- Commands executed.
- Pass/fail/blocked status.
- Existing failures before migration.
- Environment limitations.

Do not fix unrelated pre-existing defects unless a migration depends on them. Clearly distinguish baseline failures from migration regressions.

## 4.4 Produce an ownership map

For each category, identify one canonical owner:

- Runtime/application code.
- CLI.
- Project generation.
- Workforce definitions and execution.
- Engineering domains.
- Engineering engines.
- Workflows and modes.
- Adapter-specific files.
- General prompts.
- Schemas.
- Templates.
- Security policies and procedures.
- Skills.
- Documentation.
- Tests.
- Examples.
- Historical design documents.
- Repository maintenance scripts.

A category may have multiple folders only when their responsibilities are genuinely different and explicitly documented.

---

# 5. TARGET ORGANIZATION

Use the following as the preferred destination architecture, not as a rigid instruction to force every file into it.

```text
OpenClone/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── adapters/
│   ├── antigravity/
│   ├── claude-code/
│   ├── codex/
│   ├── cursor/
│   └── README.md
│
├── src/
│   └── openclone/
│       ├── __init__.py
│       ├── cli/
│       ├── core/
│       ├── project/
│       ├── workforce/
│       ├── workflows/
│       └── integrations/
│
├── knowledge/
│   ├── domains/
│   ├── engines/
│   ├── concepts/
│   ├── standards/
│   └── registries/
│
├── workforce/
│   ├── contracts/
│   ├── registry/
│   ├── teams/
│   └── README.md
│
├── workflows/
│   ├── definitions/
│   ├── modes/
│   ├── design-review/
│   └── README.md
│
├── skills/
│   ├── taste-skill/
│   └── README.md
│
├── resources/
│   ├── prompts/
│   ├── templates/
│   ├── schemas/
│   └── memory/
│
├── security/
│   ├── policies/
│   ├── operations/
│   └── README.md
│
├── docs/
│   ├── getting-started/
│   ├── guides/
│   ├── architecture/
│   ├── integrations/
│   ├── development/
│   ├── reference/
│   └── README.md
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── fixtures/
│   └── README.md
│
├── scripts/
│   ├── validation/
│   ├── maintenance/
│   └── README.md
│
├── examples/
│   └── demo-project/
│
├── archive/
│   └── design-history/
│
├── AGENTS.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
├── SUPPORT.md
├── pyproject.toml
└── VERSION
```

## 5.1 Target structure principles

- Aim for approximately 12–15 meaningful top-level directories, including standard project metadata directories such as `.github`.
- Keep `src/` for canonical executable application code.
- Keep `knowledge/` for reusable engineering knowledge and catalogs.
- Keep `workforce/` for worker definitions, contracts, teams, and workforce metadata.
- Keep `workflows/` for workflow definitions and mode-specific execution resources.
- Keep `adapters/` for external coding-tool integrations.
- Keep `skills/` for self-contained reusable skills.
- Keep `resources/` for reusable prompts, templates, schemas, and memory templates when those resources do not have a more natural canonical owner.
- Keep `security/` for security policy and operational security material.
- Keep `docs/` for human-facing documentation.
- Keep `tests/` for automated tests.
- Keep `scripts/` for repository maintenance and validation utilities.
- Keep `examples/` for demonstrable, safe examples.
- Keep `archive/` only for genuinely superseded or historical material that remains useful.

Do not create a folder if it would contain only one trivial file and would make navigation worse. Do not force this exact structure when the actual codebase demonstrates a better, simpler boundary.

## 5.2 Detailed migration guidance

Use this mapping as a starting point:

| Existing location | Candidate destination | Conditions |
|---|---|---|
| `domains/` | `knowledge/domains/` | Preserve all domain IDs, metadata, links, and discovery. |
| `engines/` | `knowledge/engines/` | Preserve all engine IDs, ordering, references, and loading behavior. |
| `concepts/` | `knowledge/concepts/` | Keep canonical concepts active; archive only verified superseded alternatives. |
| `standards/` | `knowledge/standards/` | Preserve standards and update references. |
| `registries/` | `knowledge/registries/` | Move only general catalogs; keep workforce-specific registries under workforce. |
| `modes/` | `workflows/modes/` | Preserve mode selection and entry behavior. |
| `EGM-WORKFLOWS/` | `workflows/design-review/` | Only if these are genuinely workflow resources and all references can be updated. |
| `workflows/` | `workflows/definitions/` | Preserve WF identifiers and runtime discovery. |
| `prompts/` | `resources/prompts/` | Keep adapter-specific instructions with their adapters. |
| `templates/` | `resources/templates/` | Preserve template names and generation references. |
| `schemas/` | `resources/schemas/` | Only if a single resource owner is appropriate; runtime-owned schemas may stay with their package. |
| `memory/` | `resources/memory/` | Preserve lifecycle behavior and templates. |
| `security-operations/` | `security/operations/` | Merge organizationally; preserve policy distinctions. |
| `blueprints/` | `archive/design-history/` | Archive only historical/superseded material. Move active specifications to their canonical owners. |
| `reference/` | `docs/reference/` | Preserve source attribution and links. |
| `REFERENCE-PROJECTS/` | `examples/` | Only if safe and intended for public distribution. |
| `ASSESSMENT/` | `docs/development/assessments/` | Preserve reports and distinguish historical assessments. |
| `tools/` | `scripts/` or `src/` | Inspect each file; scripts are not automatically runtime code. |
| `runtime/` | `src/openclone/` or another canonical runtime package | Only after import, packaging, and runtime ownership analysis. |
| root manifests | Root or canonical registry location | Keep only authoritative manifests and update all consumers. |

Do not move files merely to match this table. Record exceptions and explain why they are better left in place.

---

# 6. PHASE 1 — RESOLVE RUNTIME AND PACKAGE OWNERSHIP

This is a high-priority architecture task.

Inspect all executable Python files and determine:
- Which code is imported by the CLI.
- Which code is packaged and installed.
- Which code is called by tests.
- Which code is a prototype or legacy implementation.
- Which files are actual runtime services.
- Which files are scripts or maintenance utilities.
- Whether there are duplicated functions or divergent implementations.

The prior tree suggested possible overlap among:

```text
src/openclone/
runtime/
tools/aisdf_runtime/
```

Verify this in the live repository.

## Required outcome

Establish one canonical package implementation for each real capability.

A possible package organization is:

```text
src/openclone/
├── __init__.py
├── cli/
├── core/
├── project/
├── workforce/
├── workflows/
└── integrations/
```

This is illustrative. Derive the final package boundaries from existing responsibilities and imports.

### Rules

- Do not create empty packages to satisfy the diagram.
- Do not move scripts into the runtime merely because they are Python.
- Do not retain two implementations with one merely forwarding to the other unless a compatibility shim is necessary.
- If a compatibility shim is required, document its deprecation plan.
- Preserve public CLI behavior unless a change is explicitly justified.
- Preserve package import compatibility where feasible.
- Update `pyproject.toml`, entry points, package discovery, tests, and documentation.
- Verify clean installation in an isolated environment if feasible.
- Avoid changing the project's package name or import namespace without explicit authorization.

---

# 7. PHASE 2 — CONSOLIDATE KNOWLEDGE AND RESOURCE OWNERSHIP

## 7.1 Domains and engines

If the current repository contains the known domain and engine collections:

- Preserve every domain and engine.
- Preserve stable identifiers and filenames unless a compatibility-safe migration is necessary.
- Ensure each domain and engine has one canonical location.
- Ensure the root and category indexes point to the correct locations.
- Ensure discovery and selection logic still works.
- Ensure OpenClone loads only relevant resources for a task rather than indiscriminately loading every domain and engine.

## 7.2 Registries

Audit every registry and identify:
- Data owner.
- Schema.
- Consumer.
- Validation mechanism.
- Whether it duplicates another catalog.
- Whether it is generated or manually maintained.

Do not merge registries with different responsibilities merely because both contain JSON or Markdown.

A worker catalog is not automatically the same thing as an engine registry or technology registry.

## 7.3 Prompts and adapter instructions

Separate:
- General reusable prompts.
- Workflow-specific prompts.
- Role instructions.
- Tool-specific adapter instructions.
- Generated project instructions.

Keep tool-specific instructions with the adapter when that makes installation and maintenance clearer.

Avoid maintaining duplicate prompt text across adapters. Where safe, use a canonical source and generate or package tool-specific forms through a documented mechanism. Do not introduce a generator if direct maintenance is simpler.

## 7.4 Schemas and templates

Every schema and template must have:
- One canonical owner.
- A clear consumer.
- A validation or test path where appropriate.
- Updated references after migration.

Do not relocate a schema away from its runtime package if package-local ownership is the cleaner design.

## 7.5 Workflows and modes

Clarify the distinction:

- A **mode** selects the kind of user journey or operating context.
- A **workflow** defines a repeatable sequence of work.
- A **design-review workflow** is a specialized workflow category, not automatically a separate orchestration system.

Preserve existing behavior and identifiers.

## 7.6 Historical design documents

For every candidate historical file:
- Search for inbound links and references.
- Check whether it defines a still-active rule or requirement.
- Compare it with the current canonical document.
- Preserve unique information.
- Archive only when its historical status is clear.
- Add an archive index explaining the archive's purpose and the status of its contents.

Do not create an archive containing active specifications.

---

# 8. PHASE 3 — REPOSITORY HYGIENE

Inspect and improve repository hygiene.

## 8.1 Ignore generated and local files

Update `.gitignore` based on the actual stack. At minimum, evaluate:

```gitignore
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/
.venv/
venv/
.env
.env.*
!.env.example
dist/
build/
*.egg-info/
.DS_Store
Thumbs.db
```

Add language/tool-specific entries only when relevant.

Do not ignore source files, lockfiles, fixtures, or examples required for reproducible builds.

Audit tracked generated cache files. Remove generated cache artifacts from Git tracking only after verifying they are reproducible and not user data.

## 8.2 Root file discipline

Keep essential project metadata at the root:
- `README.md`
- `LICENSE`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `SUPPORT.md`, if useful and maintained
- `pyproject.toml`
- `VERSION`, if it is the actual version source
- `AGENTS.md`, if it is the active repository-wide agent instruction file
- Other essential package/build configuration

Do not keep every internal planning document at the root.

Do not remove root-level files required by GitHub, package tooling, or project governance.

## 8.3 Naming consistency

Adopt consistent naming without mass-renaming stable files:
- Lowercase kebab-case for new directory and file names where appropriate.
- Preserve established IDs such as `E-001` and `WF-001`.
- Preserve external tool conventions such as `AGENTS.md`, `CLAUDE.md`, or editor-specific filenames.
- Avoid renaming files when the benefit is merely cosmetic and reference risk is high.

---

# 9. PHASE 4 — DOCUMENTATION ARCHITECTURE

Organize documentation into three reader journeys.

## 9.1 Public landing page

Root `README.md` is for people discovering the project.

It should answer:
- What is OpenClone?
- Why might I use it?
- What can I do with it today?
- How do I get started?
- Where can I learn more?
- How can I contribute?

It must not become an internal engineering encyclopedia.

## 9.2 User documentation

Organize user-facing guides in a simple structure such as:

```text
docs/
├── getting-started/
├── guides/
├── integrations/
└── reference/
```

Include only categories with actual content.

## 9.3 Developer documentation

Organize contributor and maintainer documentation such as:

```text
docs/
├── architecture/
├── development/
├── engineering/
└── maintenance/
```

Do not create duplicate documentation. Move or link existing authoritative documents instead.

## 9.4 README hierarchy

Nested README files should have a distinct purpose:
- Root README: project introduction and first steps.
- `docs/README.md`: documentation index.
- Category README: explain the category, its contents, and how to extend it.
- Component README: explain how to use or maintain that component.

Remove redundant repetition only after preserving useful information and checking inbound links.

---

# 10. PHASE 5 — ROOT README REDESIGN

Rewrite the global root `README.md` as a polished, minimal, credible open-source landing page.

## 10.1 Tone and visual direction

The README should feel:
- Simple.
- Professional.
- Confident.
- Open and welcoming.
- Easy to scan.
- Developer-friendly.
- Maintained by a serious open-source project.

Avoid:
- Excessive emojis.
- Marketing hype.
- Unsupported superlatives.
- Long paragraphs.
- Huge architecture diagrams.
- Large folder trees.
- Internal engineering jargon.
- Internal implementation inventories.
- Roadmap promises presented as completed features.
- Excessive badges.
- Repeated calls to action.
- Generic AI-generated marketing phrases.

Use a restrained, consistent Markdown style.

## 10.2 Project description must be evidence-based

Inspect:
- Actual source code.
- Current CLI behavior.
- Existing workflows.
- Supported adapters.
- Installation and packaging.
- Current examples.
- Tests and validation.

Describe only capabilities that are implemented and demonstrable.

Clearly distinguish:
- Available now.
- Experimental.
- Planned.

Do not call a documented concept an implemented feature.

Do not invent model providers, model names, API integrations, supported tools, or deployment capabilities.

## 10.3 Suggested README outline

Use this as a guide and adapt it to verified project reality:

```markdown
<div align="center">

# OpenClone

A concise, accurate one-line description of the project.

[Getting Started] · [Documentation] · [Contributing]

</div>

---

## Overview

A short explanation of what OpenClone does and who it is for.

## Features

A concise list of verified capabilities.

## Getting Started

The simplest supported path to try OpenClone.

## Installation

Only verified installation instructions.

## Usage

A small working example using real commands and actual output expectations.

## Documentation

Links to user and developer documentation.

## Contributing

A short invitation and link to CONTRIBUTING.md.

## License

The exact license and link to LICENSE.
```

Do not copy illustrative text as factual content without verification.

## 10.4 Badges

Use only useful, working badges supported by actual repository configuration:
- License.
- Current CI status, if CI exists and the badge URL is correct.
- Latest release, if releases exist.
- Package version, if a real package is published.
- Supported Python version, only if verified.

Do not add broken, decorative, or invented badges.

## 10.5 Hero links

Use relative links where appropriate:
- `docs/`
- `CONTRIBUTING.md`
- `LICENSE`
- Actual getting-started guide.

Use external links only when verified.

## 10.6 README quality gate

Before finalizing:
- Check all links.
- Check code fences.
- Check Markdown rendering.
- Verify every command against the actual CLI.
- Verify every feature claim.
- Ensure installation steps work or clearly state prerequisites.
- Ensure the README is concise and has no internal-only details.
- Ensure a new visitor can identify the next step quickly.

The root README should be a landing page, not a complete documentation replacement.

---

# 11. PHASE 6 — MIGRATION EXECUTION

Do not perform one giant move.

Execute small migration batches in this order, adapting to the actual dependency graph:

### Batch A — Hygiene and root organization
- Add or correct `.gitignore`.
- Identify root files that are essential versus internal planning material.
- Do not move essential metadata.
- Remove only verified generated artifacts from tracking.

### Batch B — Documentation and historical material
- Identify canonical documents.
- Separate historical blueprints and superseded alternatives.
- Consolidate documentation navigation.
- Update links.

### Batch C — Knowledge organization
- Move domains, engines, concepts, standards, and general registries into the agreed knowledge hierarchy if safe.
- Preserve IDs and discovery.
- Validate domain and engine counts.

### Batch D — Workflow and resource organization
- Consolidate modes and workflow definitions.
- Clarify design-review resources.
- Organize prompts, templates, schemas, and memory resources.
- Preserve adapter-specific files.

### Batch E — Security organization
- Consolidate security operations and policies without collapsing distinct responsibilities.
- Preserve security tooling configuration and release gates.

### Batch F — Runtime ownership
- Resolve duplicate or unclear runtime ownership.
- Establish one canonical implementation per capability.
- Update imports, package configuration, CLI, and tests.
- This batch requires especially careful validation.

### Batch G — Tests, examples, and scripts
- Organize test types only when it improves clarity and test discovery.
- Preserve fixtures.
- Separate maintenance scripts from runtime code.
- Preserve working examples.

### Batch H — Public README
- Rewrite root README after implementation facts are verified.
- Update documentation navigation.

After every batch:
1. Inspect `git diff --stat`.
2. Inspect `git status`.
3. Search for stale paths.
4. Run relevant tests and validation.
5. Fix migration regressions before continuing.
6. Record unresolved issues.

If the environment does not support a test or operation, report it as blocked rather than pretending it succeeded.

---

# 12. PHASE 7 — REFERENCE AND COMPATIBILITY UPDATES

Search the entire repository for references to old paths and names.

Check at least:
- Python imports.
- `pyproject.toml`.
- Console script entry points.
- Package discovery.
- JSON manifests.
- Registry paths.
- Schema references such as `$ref`.
- Workflow file paths.
- Adapter installation paths.
- Prompt and template paths.
- Test fixtures.
- Shell scripts.
- CI workflows.
- Documentation links.
- Relative image and asset paths.
- README links.
- Example commands.
- Any runtime resource loader.

Use repository-wide search tools and inspect all matches. Do not use blind global replacement for ambiguous path strings.

Preserve compatibility where external consumers may depend on existing paths. If a compatibility alias or shim is needed, document it and test it.

---

# 13. PHASE 8 — TESTING AND VERIFICATION

Run the existing test suite before and after migration.

Discover the correct commands from `pyproject.toml`, project documentation, and CI configuration. Do not assume a particular test runner or command.

At minimum, verify the following where the repository supports them:

## Repository integrity
- No accidental file loss.
- No broken internal links.
- No broken image or asset references.
- No stale references to old paths.
- No tracked Python cache files.
- No secrets or local environment files added.
- No duplicate canonical implementations introduced.

## Python packaging and runtime
- Package builds successfully.
- Package installs in a clean environment where feasible.
- Imports resolve.
- CLI entry points work.
- Existing CLI behavior is preserved.
- Runtime resource discovery works.

## OpenClone capabilities
- Domain discovery works.
- Engine discovery works.
- Workforce registry loads and validates.
- Team and role definitions remain available.
- Workflow discovery works.
- Mode selection works.
- Adapter resources remain installable/discoverable.
- Templates and schemas load correctly.
- Project generation still creates the expected project files.
- Generated `PROJECT.md` and `AGENTS.md` behavior remains intact if implemented.
- Taste Skill remains complete and usable.

## Quality
- Unit tests.
- Integration tests.
- End-to-end tests.
- Repository validation.
- Schema validation.
- Documentation link checks, if available.

Do not fabricate a successful test result. Report exact commands and outcomes.

---

# 14. REQUIRED FINAL STRUCTURE REVIEW

At completion, produce the actual final repository tree to a useful depth.

Compare it with the baseline and report:

1. Previous top-level directory count.
2. New top-level directory count.
3. Directories consolidated.
4. Files moved.
5. Files archived.
6. Files removed, with justification.
7. Capabilities preserved.
8. Canonical runtime ownership decisions.
9. README changes.
10. Test and validation results.
11. Remaining risks and blocked items.

Do not optimize for a numerical reduction alone. A slightly larger structure is acceptable if it is more understandable and has clear ownership.

---

# 15. ACCEPTANCE CRITERIA

The task is complete only when all applicable criteria are satisfied:

- [ ] The actual repository was audited before modification.
- [ ] Existing Git changes were preserved.
- [ ] A clear ownership map exists.
- [ ] The top-level structure is simpler and easier to navigate.
- [ ] Related folders are consolidated where their responsibilities genuinely overlap.
- [ ] Runtime implementation ownership is clear.
- [ ] No duplicate generators or runtime systems were introduced.
- [ ] All existing valuable engineering resources remain available.
- [ ] All domain and engine identifiers are preserved.
- [ ] Workforce definitions, contracts, teams, and registries still work.
- [ ] Adapters remain usable.
- [ ] Workflows and modes remain discoverable.
- [ ] Schemas and templates remain accessible.
- [ ] Taste Skill is preserved intact.
- [ ] Historical documents are separated without losing unique knowledge.
- [ ] Python imports and package configuration are correct.
- [ ] CLI behavior remains functional.
- [ ] Project generation remains functional.
- [ ] Internal links and resource references are updated.
- [ ] Generated cache files are not tracked.
- [ ] Root README is concise, accurate, polished, and beginner-friendly.
- [ ] README installation and usage instructions are verified.
- [ ] Tests and repository validation have been run and accurately reported.
- [ ] No unsupported feature claims or invented commands appear in public documentation.

If a criterion cannot be met, explain why and identify the remaining work. Do not mark the task complete merely because files have been moved.

---

# 16. FINAL REPORT FORMAT

At the end, provide a concise but sufficiently detailed report:

## A. Summary
What changed and why.

## B. Final repository structure
Show the actual resulting tree, not the proposed template.

## C. Migration map
A table of old path → new path → reason → validation.

## D. Preservation report
Confirm which important assets and identifiers were preserved.

## E. Runtime ownership
Explain the canonical package boundaries and any compatibility shims.

## F. README upgrade
Summarize the new structure and the verified project claims used.

## G. Verification
List exact commands and their results:
- PASS
- FAIL
- BLOCKED
- NOT RUN

## H. Remaining issues
List unresolved risks, ambiguous files, and follow-up work.

## I. Git status
Report the final changed-file summary. Do not commit or push unless explicitly authorized.

---

# 17. START EXECUTION

Begin now:

1. Inspect the live repository and Git status.
2. Build the baseline inventory and ownership map.
3. Run baseline validation.
4. Identify safe, high-value consolidation opportunities.
5. Present the proposed migration map briefly before high-risk moves.
6. Execute safe migration batches with validation after each.
7. Resolve runtime ownership only with evidence from imports, package configuration, and tests.
8. Upgrade the root README using verified functionality.
9. Run final verification.
10. Produce the final report.

**Final instruction:** Make OpenClone easier to understand, maintain, contribute to, and use. Keep its valuable engineering depth. Remove organizational confusion, not capability. The root README should welcome the open-source community; the deeper documentation should serve users and maintainers; the source tree should make each responsibility obvious.
