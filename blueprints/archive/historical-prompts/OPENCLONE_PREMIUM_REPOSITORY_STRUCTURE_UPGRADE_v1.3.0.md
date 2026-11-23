# OpenClone — Premium Repository Structure & Domain Consolidation Upgrade
## Antigravity in-place execution specification | v1.3.0

**Product:** OpenClone  
**Repository currently known:** `MK-1603/aisdf` (verify the actual remote and local workspace before acting)  
**Objective:** Restructure the existing OpenClone repository into a clean, premium, scalable architecture, with all 31 numbered domains (`00`–`30`) grouped under one canonical parent folder.

> This is a repository restructuring and quality upgrade—not a new project, not a second framework, and not a documentation-only exercise. Perform the work in the existing OpenClone repository and preserve its working capabilities.

---

# 1. What the user wants

The current repository has numbered domain folders such as `00-GOVERNANCE`, `01-METHODOLOGY`, through `30-AGENT-RULES-AND-VERIFICATION` at the repository root. The supplied project tree also shows separate top-level areas for adapters, assessment, blueprints, concepts, docs, engines, examples, memory, modes, prompts, registries, runtime, schemas, security, security-operations, skills, source, standards, templates, tests, tools, workflows, and workforce. fileciteturn153file0L4-L18 fileciteturn153file0L97-L138 fileciteturn153file0L353-L410 fileciteturn153file0L895-L924

The requested structural change is:

- Put **all 31 numbered domains (`00`–`30`) inside one parent folder**, recommended name: `domains/`.
- Keep their numbering, identity, scope, and internal content intact unless a verified audit justifies a correction.
- Reorganize the rest of the repository into a small number of clearly owned top-level areas.
- Make the structure understandable to developers, AI coding agents, contributors, and future maintainers.
- Upgrade root documentation, navigation, naming, consistency, and developer experience to a premium open-source project standard.
- Do not delete useful material merely to make the tree look smaller.

The `domains/` parent is the canonical home of the 31 domains. Do not leave duplicate numbered-domain folders at the root after migration.

---

# 2. Non-negotiable safety and change-control rules

1. Inspect the real local repository, current branch, current commit, and `git status` before editing.
2. Read `AGENTS.md`, root README, project/mission documents, governance rules, manifests, version file, architecture maps, and nested instructions.
3. Preserve uncommitted user work. Never run destructive reset/clean commands.
4. Create a dedicated local branch for the restructuring if Git is available and the working tree permits it. Do not push or merge without explicit authorization.
5. Do not delete, truncate, rewrite from memory, or replace existing specifications with generic placeholders.
6. Move files with Git-aware operations where possible so history can be followed.
7. Preserve stable IDs, engine IDs, schema identifiers, public CLI commands, workflow IDs, and compatibility contracts unless a migration is explicitly designed and tested.
8. Every move must have a traceable old-path → new-path mapping.
9. Update every affected link, import, test fixture, script, manifest, CI workflow, package configuration, adapter instruction, and example.
10. Do not leave two competing canonical copies of a document.
11. Do not create a new `UPGRADE/`, `V2/`, `NEW-OPENCLONE/`, or parallel repository.
12. If an operation is destructive, externally consequential, paid, or requires production credentials, stop and ask for approval.
13. Keep a rollback path until all validation passes.
14. Do not claim tests, integrations, or deployments passed unless executed and evidenced.

---

# 3. Target premium repository structure

Use this as the target organizational model. Adapt names only when the existing project conventions or executable dependencies require it. Keep the structure shallow, predictable, and easy to navigate.

```text
OpenClone/
│
├── domains/                         # THE single home for all numbered domains
│   ├── 00-governance/
│   ├── 01-methodology/
│   ├── 02-project-intelligence/
│   ├── 03-requirements-engineering/
│   ├── 04-product-engineering/
│   ├── 05-ux-ui-engineering/
│   ├── 06-technology-intelligence/
│   ├── 07-engineering-knowledge/
│   ├── 08-software-architecture/
│   ├── 09-platform-engineering/
│   ├── 10-ai-and-model-engineering/
│   ├── 11-agent-engineering/
│   ├── 12-orchestration-and-context/
│   ├── 13-harness-and-execution/
│   ├── 14-security-and-privacy/
│   ├── 15-data-and-database-engineering/
│   ├── 16-api-and-integration-engineering/
│   ├── 17-testing-and-verification/
│   ├── 18-devops-and-cloud-engineering/
│   ├── 19-deployment-and-operations/
│   ├── 20-reliability-and-observability/
│   ├── 21-distributed-systems-and-scalability/
│   ├── 22-cost-and-resource-governance/
│   ├── 23-legal-and-compliance/
│   ├── 24-product-analytics-and-support/
│   ├── 25-framework-maintenance/
│   ├── 26-distribution-and-extensions/
│   ├── 27-standards-and-compatibility/
│   ├── 28-templates-and-examples/
│   ├── 29-benchmarks-and-evaluation/
│   ├── 30-agent-rules-and-verification/
│   └── README.md
│
├── core/                            # Shared OpenClone runtime and contracts
│   ├── src/                         # Move existing src/ here only after import audit
│   ├── runtime/                     # Move existing runtime/ here only after import audit
│   ├── schemas/                     # Canonical machine-readable contracts
│   └── README.md
│
├── integrations/                    # External AI platforms and provider adapters
│   ├── mcp/
│   ├── platforms/
│   │   ├── chatgpt/
│   │   ├── claude/
│   │   ├── codex/
│   │   └── gemini/
│   ├── providers/
│   ├── connectors/
│   ├── registries/
│   └── README.md
│
├── workforce/                       # Existing specialist/agent workforce
│   ├── contracts/
│   ├── registry/
│   ├── teams/
│   └── README.md
│
├── engineering/                     # Execution workflows and engineering assets
│   ├── engines/
│   ├── workflows/
│   ├── modes/
│   ├── prompts/
│   ├── skills/
│   ├── tools/
│   ├── standards/
│   └── README.md
│
├── knowledge/                       # Reference and durable knowledge
│   ├── concepts/
│   ├── blueprints/
│   ├── memory/
│   ├── reference/
│   └── README.md
│
├── quality/                         # Tests, assessments, benchmarks, assurance
│   ├── tests/
│   ├── assessment/
│   ├── benchmarks/
│   ├── security/
│   └── README.md
│
├── delivery/                        # Build, release, deployment and operations
│   ├── ci/
│   ├── deployment/
│   ├── operations/
│   ├── release/
│   └── README.md
│
├── docs/                            # User-facing docs and project guides
│   ├── getting-started/
│   ├── architecture/
│   ├── guides/
│   ├── examples/
│   ├── migration/
│   ├── release-history/
│   └── README.md
│
├── templates/                       # Reusable project and report templates
├── examples/                        # Runnable end-to-end examples
├── adapters/                        # Keep only if these are distinct IDE/agent packaging adapters
├── .github/                          # CI, issue templates, PR templates, workflows
│
├── AGENTS.md
├── README.md
├── QUICK-START.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── SUPPORT.md
├── LICENSE
├── VERSION
├── CHANGELOG.md
├── pyproject.toml
├── requirements-dev.txt
└── manifests/                        # Canonical product/package manifests if supported
```

## Important architecture note

This is a target organization, not permission to move every folder mechanically. Some existing folders may already be referenced by Python imports, CLI entry points, skill installers, agent clients, GitHub workflows, documentation URLs, or external users. Inspect dependencies first.

If a proposed move would create more risk than value, keep the folder where it is for this release and record the reason. The mandatory requirement is that all numbered domains live under one `domains/` parent. Other top-level grouping can be staged safely.

Avoid needless nesting. Do not move root project configuration files into arbitrary folders. Keep conventional root entry points (`README.md`, `pyproject.toml`, `AGENTS.md`, `LICENSE`, `VERSION`, etc.) at the root unless a tool requires otherwise.

---

# 4. Domain consolidation requirements

## 4.1 All 31 domains

Move the existing numbered directories `00` through `30` into `domains/`. Preserve the numeric prefixes and domain names. Normalize case and hyphenation only if every reference is updated and the change is documented.

The domain list must be checked against the actual repository, not just this proposed tree. Verify:
- No number is missing.
- No duplicate domain number exists.
- No two domains claim the same ownership without an explicit boundary.
- Every domain has a useful README with purpose, scope, non-goals, owner, dependencies, key documents, and links.
- README headings match the actual domain name.
- Domain map, functional map, manifests, indexes, and engine references resolve.
- Cross-domain dependencies are explicit rather than circular or hidden.

## 4.2 Domain landing page

Create `domains/README.md` as the canonical domain index:
- Purpose of the domain system.
- All 31 domains in numeric order.
- One-sentence scope for each.
- Primary inputs/outputs and ownership.
- Links to each domain README.
- Cross-domain dependency overview.
- Guidance on where new capabilities belong.
- Rule that new domains require an ADR and governance approval.

## 4.3 No duplicate domain homes

After migration:
- No `00-*` through `30-*` numbered domain directories should remain at repository root.
- Do not copy the domains and leave the originals as stale duplicates.
- If compatibility shims are required for one release, make them explicit, minimal, tested, and scheduled for removal. Prefer redirects/links or import compatibility modules over duplicated documents.

---

# 5. Reorganize the remaining repository areas

Map every existing top-level folder to one canonical destination. The following mapping is a starting proposal, not a blind command:

| Current area | Preferred destination | Notes |
|---|---|---|
| `engines/` | `engineering/engines/` | Preserve E-001…E-056 IDs and registry |
| `workflows/` | `engineering/workflows/` | Update workflow references |
| `modes/` | `engineering/modes/` | Keep stable mode identifiers |
| `prompts/` | `engineering/prompts/` | Preserve role prompts and entry prompts |
| `skills/` | `engineering/skills/` | Preserve skill metadata, license, assets, tests |
| `tools/` | `engineering/tools/` | Update executable paths and docs |
| `standards/` | `engineering/standards/` or relevant domain | Avoid duplicated standards |
| `concepts/` | `knowledge/concepts/` | Preserve primary/alternate distinction |
| `blueprints/` | `knowledge/blueprints/` | Mark historical vs canonical clearly |
| `memory/` | `knowledge/memory/` | Preserve vault template and governance |
| `reference/` | `knowledge/reference/` | Keep source provenance |
| `ASSESSMENT/` | `quality/assessment/` | Preserve historical assessment reports |
| `tests/` | `quality/tests/` | Update test discovery/configuration |
| `security/` | `quality/security/` or security domain | Keep machine policy paths consistent |
| `security-operations/` | `quality/security/operations/` or domain 14 | Choose one canonical owner |
| `runtime/` | `core/runtime/` | Check Python imports and entry points |
| `src/` | `core/src/` only if packaging supports it | Do not break package discovery |
| `schemas/` | `core/schemas/` | Keep schema IDs and references stable |
| `registries/` | Split by ownership into `integrations/registries/`, `engineering/`, or `core/` | Avoid a generic registry dump |
| `adapters/` | `integrations/platforms/` only for actual AI platform adapters; keep IDE-specific adapters distinct if needed | Do not conflate IDE and AI chat platform adapters |
| `EGM-WORKFLOWS/` | `engineering/workflows/egm/` or domain 17/30 ownership | Preserve schemas and templates |
| `docs/` | `docs/` | Reorganize internal docs, preserve demo assets and release history |
| `REFERENCE-PROJECTS/` | `examples/reference-projects/` | Preserve runnable project examples |
| `templates/` | `templates/` | Keep reusable templates easy to find |
| `examples/` | `examples/` | Keep runnable examples and fixtures distinct |
| `workforce/` | `workforce/` | Existing clear top-level bounded context |
| `adapters/` | `integrations/` or retain for IDE adapters | Decide after inventory |
| root manifests | `manifests/` only if tooling supports it | Keep compatibility entry points if required |

Where a folder has multiple responsibilities, split by ownership only after dependency mapping. Do not move an entire folder into one destination if its contents belong to different domains.

---

# 6. Premium repository quality standard

“Premium” means professional, coherent, navigable, consistent, maintainable, and easy to contribute to—not merely more folders or decorative README badges.

## 6.1 Naming and consistency

- Use one consistent directory naming convention.
- Use stable, predictable file names.
- Fix spelling errors, mismatched README headings, inconsistent capitalization, and broken relative links.
- Avoid vague names such as `misc`, `stuff`, `new`, `old2`, `final-final`.
- Separate canonical/current documents from historical/archived records.
- Add owner and status metadata only where it improves traceability.
- Keep stable IDs such as `E-001` through `E-056`; do not renumber for aesthetics.

## 6.2 Root README and navigation

Upgrade the root README into a premium project landing page with:
1. OpenClone identity and concise value proposition.
2. What OpenClone does and does not do.
3. Key capabilities.
4. Architecture overview.
5. Four AI platform integrations: ChatGPT, Claude, Codex, Gemini (label actual maturity honestly).
6. Quick start.
7. Repository map.
8. Documentation navigation.
9. Security and privacy summary.
10. Testing and verification commands.
11. Contribution guide.
12. License and project status.

Use accurate badges only. Do not add fake stars, downloads, coverage, build status, certification, or compatibility badges.

## 6.3 Contributor experience

Provide:
- A clear quick-start for a new contributor.
- Supported language/runtime/tool versions.
- Reproducible install and test commands.
- Code style and formatting rules.
- How to add a domain document, engine, skill, adapter, connector, schema, or test.
- Pull request checklist.
- Release process and version policy.
- Troubleshooting guide.
- Architecture decision record template.
- Changelog convention.

## 6.4 Documentation design

- Consistent headings, tables, callouts, diagrams, and metadata.
- Short landing pages with links to detailed specs.
- No duplicated full specifications across multiple files.
- A clear status label: `DRAFT`, `PROPOSED`, `APPROVED`, `IMPLEMENTED`, `VERIFIED`, `DEPRECATED`.
- Every cross-reference must resolve.
- Diagrams must match actual implementation and be labeled conceptual when not implemented.
- Use Mermaid where it improves understanding; do not add diagrams for decoration.

---

# 7. Integrations and platform adapters

During the restructuring, preserve and prepare a clean integration architecture for:
- ChatGPT
- Claude
- OpenAI Codex
- Google Gemini

These must use one shared OpenClone core and stable tool contracts. Do not duplicate core logic in each platform adapter. Keep MCP/tool gateway contracts, authentication, authorization, connector registry, and platform-specific setup clearly separated.

Do not mark a platform integration as complete merely because a folder or config file exists. Record the maturity state and evidence:
`SPECIFIED`, `IMPLEMENTED`, `UNIT_TESTED`, `CONTRACT_TESTED`, `LIVE_CONNECTED`, `END_TO_END_VERIFIED`.

Do not move existing Antigravity, Cursor, Claude Code, or Codex IDE instructions into the wrong category. Distinguish:
- AI chat platform integration,
- coding-agent/IDE adapter,
- MCP server,
- provider API adapter,
- local CLI integration.

---

# 8. Migration engineering — do not break the repository

Before moving files:
1. Generate a complete file inventory and path reference map.
2. Search for references to every old path in Markdown, Python, JSON, YAML, TOML, shell, JavaScript, TypeScript, CI, package files, and test fixtures.
3. Inspect dynamic path construction and runtime path assumptions.
4. Identify public URLs or external consumers that may depend on paths.
5. Design a move manifest with old path, new path, reason, references to update, and verification test.
6. Check packaging and import discovery before moving `src/`, `runtime/`, `schemas/`, or `tools/`.
7. Check skill installation scripts and relative asset paths before moving `skills/`.
8. Check adapter discovery and instruction paths before moving `adapters/`.
9. Check CI and GitHub workflows before moving tests or configuration.
10. Plan a reversible migration.

Implement in small batches:
- Batch A: numbered domains → `domains/`.
- Batch B: documentation and knowledge organization.
- Batch C: engineering engines/workflows/prompts/skills/tools.
- Batch D: core source/runtime/schemas only if packaging and tests support it.
- Batch E: quality/security/assessment.
- Batch F: integration adapters and registries.
- Batch G: docs, links, root navigation, manifests and release metadata.

After each batch, run the relevant validation. Do not proceed to the next batch if the previous batch breaks tests or critical references.

Create a machine-readable path migration map (JSON or YAML) and a human-readable migration report. Do not retain the map as an alternative source of truth; it is a migration record.

---

# 9. Required automated validation

Add or upgrade repository validation so it checks:

### Structure
- Exactly one canonical `domains/` directory.
- All 31 numbered domains exist under `domains/`.
- No numbered domain directories remain at root.
- No duplicate domain IDs.
- Every domain has a README.
- Every domain index entry resolves.
- No accidental empty or abandoned directories.
- No stale duplicate documents.

### References and configuration
- Markdown relative links.
- Internal file references.
- Python imports and package discovery.
- CLI entry points.
- JSON/YAML/TOML validity.
- Schema references and fixtures.
- Skill asset references and install scripts.
- Adapter discovery paths.
- CI workflow paths.
- Manifest file paths.
- Documentation examples and commands.

### Quality and security
- Formatting and lint.
- Type checks where relevant.
- Unit and integration tests.
- Secret scanning.
- Dependency/security checks where tools are available.
- License/attribution inventory for third-party skills and assets.
- No generated bytecode/cache files committed unless intentionally required.

### Build and release
- Reproducible local install.
- Build/package checks.
- CLI smoke test.
- Example workflow smoke test.
- Release manifest/version consistency.
- Clean final diff.

For every command, record exact invocation, environment, exit code, and result. Distinguish `PASS`, `FAIL`, `SKIPPED`, and `BLOCKED`. Do not convert skipped tests into passes.

---

# 10. Required deliverables inside the existing repository

Update existing canonical locations. Do not create a detached upgrade folder.

1. `domains/README.md` — complete 31-domain index.
2. Updated root `README.md`.
3. Updated `AGENTS.md` with the new canonical paths and repository navigation rules.
4. Updated `DOMAIN-MAP.md`, `OPENCLONE-FUNCTIONAL-MAP.md`, lifecycle overview, mission/scope docs, and relevant governance docs.
5. Updated engine, adapter, skill, workflow, and technology registries.
6. Machine-readable path migration map.
7. Human-readable structure migration report.
8. Updated contributor and quick-start documentation.
9. Updated CI/test/validation configuration.
10. Updated manifests and package metadata.
11. Updated changelog and migration notes.
12. Final repository assessment and release readiness report.

If a named document does not exist in the actual repository, do not invent a historical claim; create it only if it is genuinely needed and approved by the existing governance.

---

# 11. Versioning and release

- Inspect the existing `VERSION`, manifests, changelog, tags, and release policy first.
- Propose a semantic version bump based on actual compatibility impact.
- A folder-only move may be breaking if users, tools, scripts, or external links consume old paths.
- Preserve compatibility shims for a documented transition period when needed.
- Update migration instructions and deprecation schedule.
- Do not tag, push, publish, deploy, or merge without explicit authorization.
- Produce a local release candidate and clear owner instructions.

---

# 12. Final completion report

The final report must state:

1. Starting commit SHA and branch.
2. Final commit SHA (if locally committed) and branch.
3. Whether the working tree is clean.
4. Final version proposal.
5. Final top-level directory tree.
6. Confirmation that all 31 domains are under `domains/`.
7. Count and identity of the 31 domains.
8. Complete old-path → new-path migration summary.
9. Files moved, modified, added, deprecated, or retained with reasons.
10. Link/import/configuration repair results.
11. Test commands and exact results.
12. Packaging/build/CLI smoke-test results.
13. Security and license review results.
14. Compatibility risks and migration steps.
15. Blocked or unverified items.
16. Exact commands for the owner to reproduce checks.

Use honest statuses: `COMPLETE`, `PARTIALLY COMPLETE`, `BLOCKED`, `NOT IMPLEMENTED`, `NOT VERIFIED`.

**Do not call the work complete if any domain is missing, references are broken, core tests fail, or the migration has not been independently reviewed.**

---

# 13. Start instruction

Start by auditing the current repository and producing the proposed final tree plus path-migration manifest. Confirm the exact 31 domain directories and map every current top-level folder. Then implement the migration in small reversible batches, validate each batch, and finish with a tested local release candidate.

**The required outcome is a premium, clean, maintainable OpenClone repository where all 31 numbered domains live under one `domains/` folder, the rest of the structure has clear ownership, and the existing framework still works.**
