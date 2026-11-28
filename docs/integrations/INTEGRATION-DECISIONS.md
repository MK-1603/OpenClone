# OpenClone Upstream Integration Decisions & Rationale

**Document ID:** `DEC-UPSTREAM-27-REPOSITORIES-v1.0.0`  
**Product:** OpenClone 2.0 Universal AI Software Engineering Platform  
**Standard:** AISDF Standard 1.0.0  
**Status:** `NORMATIVE INTEGRATION DECISIONS`  

---

## 1. Integration Decision Framework

To prevent AI slope, context bloat, and license contamination, OpenClone enforces 5 strict decision criteria:

1. **Smallest Maintainable Surface:** Never copy entire third-party codebases into OpenClone core. Extract only the essential specification, token, or adapter wrapper.
2. **Deterministic Governance Over LLM Fluff:** Replace vague advice with actionable checklists, schemas, and testable code.
3. **License Safety & Attribution:** Preserve upstream author attribution, respect copyleft boundaries, and reject repositories with missing or ambiguous licenses.
4. **Isolated Operational Boundaries:** External security scanners run as authorization-gated tools with target allowlists; never run unauthenticated dynamic scans against external systems.
5. **Context Budget Management:** Exhaustive reference materials are decoupled into on-demand modules or live MCP guidance (< 12 KB).

---

## 2. Detailed Upstream Repository Decisions

### 2.1 UI/UX and Frontend Design (11 Repositories)

#### UI-001: bergside/design-md-chrome (MIT)
- **What was useful:** Logic for extracting computed styles, fonts, and hex colors from live web pages into formatted Markdown.
- **What was reused:** The token extraction and Markdown rendering schema.
- **What was not reused:** The Chrome browser extension manifest and background service worker.
- **Why:** OpenClone operates inside IDEs and CLI environments, not as a browser popup.
- **Implementation Location:** [`integrations/adapters/design_token_adapter.py`](../../integrations/adapters/design_token_adapter.py).
- **Test:** `tests/integrations/test_upstream_integrations.py::test_design_token_adapter_ui001`.

#### UI-002: shadcn-ui/ui (MIT)
- **What was useful:** Accessible component primitives (Radix UI) and Tailwind CSS design tokens.
- **What was reused:** Architectural component patterns and theme tokens.
- **What was not reused:** Hundreds of generated React component files.
- **Why:** Application developers generate their own components; OpenClone provides the engineering governance.
- **Implementation Location:** [`domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md`](../../framework/domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md).
- **Test:** Taste Skill governance tests (`skills/taste-skill/tests/test-governance.mjs`).

#### UI-003: Dammyjay93/interface-design (MIT)
- **What was useful:** Consumer interface patterns and screen layouts.
- **What was reused:** Pattern classification references.
- **What was not reused:** Raw image assets and Figma links.
- **Why:** Reference material is incorporated into domain 05 without bloating the git repo.
- **Implementation Location:** `domains/05-UX-UI-ENGINEERING/`.

#### UI-004: Mohit-Raj-Singh/Unstop-UI (UNKNOWN LICENSE)
- **What was useful:** Dashboard component layouts.
- **What was reused:** None.
- **What was not reused:** All source code and assets.
- **Why:** No root LICENSE file exists. In accordance with Operating Contract Rule 2, reuse is marked `BLOCKED_LICENSE_REVIEW`.
- **Implementation Location:** Excluded from distribution.

#### UI-005: anthropics/skills/skills/frontend-design (Apache-2.0)
- **What was useful:** Spatial hierarchy, typography sizing, and art direction rules.
- **What was reused:** Prompt instructions and anti-slop guidelines.
- **What was not reused:** Unrelated skills in parent repository.
- **Why:** Bounded to the requested `skills/frontend-design` directory.
- **Implementation Location:** [`skills/taste-skill/`](../../framework/skills/taste-skill/).
- **Test:** Taste Skill instruction audit suite.

#### UI-006: Leonxlnx/taste-skill (MIT)
- **What was useful:** Complete anti-AI-slop design system, pre-build plan gates, and contrast verification.
- **What was reused:** Entire skill structure, token curves, and 13 automated tests.
- **What was not reused:** Decoupled 35.76 MB of heavy scene renders into optional module `mod-taste-skill-assets`.
- **Why:** Keeps default plugin installation under 350 KB while preserving 100% of governance rules.
- **Implementation Location:** `skills/taste-skill/`.
- **Test:** `node skills/taste-skill/tests/test-governance.mjs` (13 tests passing).

#### UI-007: nutlope/hallmark (MIT)
- **What was useful:** Frontend design critique vocabulary and automated evaluation criteria.
- **What was reused:** Defect criteria prohibiting neon gradients, centered card walls, and blurry drop shadows.
- **What was not reused:** Next.js benchmark application harness.
- **Why:** Evaluation criteria are synthesized into deterministic quality gates.
- **Implementation Location:** `domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md`.

#### UI-008: nextlevelbuilder/ui-ux-pro-max-skill (MIT)
- **What was useful:** 67 domain-specific design system taxonomies for B2B SaaS, mobile, and dashboards.
- **What was reused:** Fast live MCP guidance topic `ui_ux_catalogue`.
- **What was not reused:** Massive multi-megabyte prompt files.
- **Why:** Prevents LLM context blowout by serving concise guidance via `openclone_get_guidance`.
- **Implementation Location:** [`docs/knowledge/ui-ux-design-catalogue.md`](../reference/guidance/ui-ux-design-catalogue.md).

#### UI-009: flitzrrr/frontend-design-skills (MIT)
- **What was useful:** Cross-IDE prompt conventions for Claude Code and Cursor.
- **What was reused:** Prompt scaffolding patterns.
- **What was not reused:** Duplicate prompt files overlapping with UI-005.
- **Why:** Unified under canonical OpenClone agent prompt format.
- **Implementation Location:** `templates/prompt_scaffolds/`.

#### UI-010: pbakaus/impeccable (Apache-2.0)
- **What was useful:** Rigorous design critique vocabulary and defect classification taxonomy.
- **What was reused:** Defect severity scoring and typography hierarchy rules.
- **What was not reused:** Marketing documentation.
- **Why:** Converted into live MCP guidance topic `ui_ux_quality`.
- **Implementation Location:** [`docs/knowledge/ui-ux-quality-audit.md`](../reference/guidance/ui-ux-quality-audit.md).

#### UI-011: jpoindexter/typography-skills (MIT)
- **What was useful:** Major Third typography scale (1.250), fluid clamp() calculations, optical line lengths (45–75 chars).
- **What was reused:** Mathematical type scale constants and CSS clamping formulas.
- **What was not reused:** Unrelated template files.
- **Why:** Directly integrated into OpenClone typography tokens.
- **Implementation Location:** `domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md`.

---

### 2.2 Security and Vulnerability Engineering (12 Repositories)

#### SEC-001: usestrix/strix (Apache-2.0)
- **What was useful:** Dynamic AI penetration testing workflows and automated vulnerability verification.
- **What was reused:** Bounded adapter architecture with strict target allowlists.
- **What was not reused:** Unchecked execution against arbitrary IP addresses.
- **Why:** Dynamic pentesting against unauthorized targets is strictly prohibited.
- **Implementation Location:** [`integrations/adapters/strix_adapter.py`](../../integrations/adapters/strix_adapter.py).
- **Test:** `tests/integrations/test_upstream_integrations.py::test_strix_security_adapter_sec001`.

#### SEC-002: projectdiscovery/nuclei (MIT)
- **What was useful:** Fast YAML template-based vulnerability scanning.
- **What was reused:** Integration gateway metadata and execution constraints.
- **What was not reused:** Complete Go binary vendoring.
- **Why:** Scanners are invoked as external tools managed via `security/scanners.lock.json`.
- **Implementation Location:** [`integrations/adapters/scanner_gateway.py`](../../integrations/adapters/scanner_gateway.py).

#### SEC-003: openai/codex-security (Apache-2.0)
- **What was useful:** AI vulnerability triage patterns and remediation verification.
- **What was reused:** Security triage rules and vulnerability classification rubrics.
- **What was not reused:** Proprietary training scripts.
- **Why:** Mapped to domain 14 security rules.
- **Implementation Location:** `domains/14-SECURITY-AND-PRIVACY/`.

#### SEC-004: cloudflare/security-audit-skill (MIT)
- **What was useful:** Agent-driven codebase security audit checklists.
- **What was reused:** Structured audit questions covering authentication, authorization, and data encryption.
- **What was not reused:** Generic prompt scaffolding.
- **Why:** Integrated into Phase 14 Security Architecture Review.
- **Implementation Location:** `domains/14-SECURITY-AND-PRIVACY/SECURITY-AUDIT-SKILL.md`.

#### SEC-005: semgrep/semgrep (LGPL-2.1)
- **What was useful:** Fast static code analysis (SAST) for Python, TypeScript, Go, Java, and C++.
- **What was reused:** Ruleset pinning and execution contract in scanner gateway.
- **What was not reused:** Monolithic OCaml/Python source tree.
- **Why:** Pinned in `security/scanners.lock.json` and executed externally to prevent license contamination.
- **Implementation Location:** [`integrations/adapters/scanner_gateway.py`](../../integrations/adapters/scanner_gateway.py).

#### SEC-006: anthropics/claude-code-security-review (MIT)
- **What was useful:** Pull request security review checklists and prompt rubrics.
- **What was reused:** Verification checklist for high-risk PR changes.
- **What was not reused:** Anthropic GitHub Action packaging.
- **Why:** Integrated into OpenClone Phase 18 Independent Verification gate.
- **Implementation Location:** `docs/engineering-lifecycle/VERIFICATION_AND_EVIDENCE.md`.

#### SEC-007: aquasecurity/trivy (Apache-2.0)
- **What was useful:** Comprehensive CVE scanning for containers, OS packages, and dependencies.
- **What was reused:** Configuration contracts and scanner lockfile definitions.
- **What was not reused:** Go binary source code.
- **Why:** External scanner invoked via scanner gateway.
- **Implementation Location:** `security/scanners.lock.json`.

#### SEC-008: trufflesecurity/trufflehog (GPL-3.0)
- **What was useful:** High-entropy secret detection with live verification detectors.
- **What was reused:** Secret detection patterns and regexes in `src/openclone/integrations/gateway.py`.
- **What was not reused:** Monolithic Go binary.
- **Why:** Python-native regex redaction provides instant secret protection without external process dependencies.
- **Implementation Location:** `src/openclone/integrations/gateway.py`.

#### SEC-009: NVIDIA/skillspector (Apache-2.0)
- **What was useful:** Security audit methodology for AI skills and agent tool declarations.
- **What was reused:** Skill manifest validation invariants in `tools/skill_engine.py`.
- **What was not reused:** Standalone CLI wrappers.
- **Why:** Embedded directly into OpenClone's skill engine.
- **Implementation Location:** `tools/skill_engine.py`.

#### SEC-010: Cisco-Talos/clamav (GPL-2.0)
- **What was useful:** Antivirus scanning engine for uploaded user files in SaaS applications.
- **What was reused:** Execution contract and daemon socket interface.
- **What was not reused:** ClamAV C engine source code.
- **Why:** GPL copyleft boundary is preserved by treating ClamAV as an independent external service.
- **Implementation Location:** `docs/security/saas-security-baseline.md`.

#### SEC-011: qybaihe/bla (MIT)
- **What was useful:** Behavioral analysis rules for LLM security evaluation.
- **What was reused:** Research taxonomy on prompt exfiltration.
- **What was not reused:** Experimental test scripts.
- **Why:** Synthesized into domain 11 agent engineering rules.
- **Implementation Location:** `domains/11-AGENT-ENGINEERING/`.

#### SEC-012: microsoft/pyrit (MIT)
- **What was useful:** Python Risk Identification Tool for Generative AI red-teaming.
- **What was reused:** Bounded prompt evaluation adapter for jailbreak and prompt injection detection.
- **What was not reused:** Cloud-dependent orchestrators.
- **Why:** Encapsulated in lightweight, local adapter `integrations/adapters/pyrit_adapter.py`.
- **Implementation Location:** [`integrations/adapters/pyrit_adapter.py`](../../integrations/adapters/pyrit_adapter.py).
- **Test:** `tests/integrations/test_upstream_integrations.py::test_pyrit_security_adapter_sec012`.

---

### 2.3 Software Development & Engineering (4 Repositories)

#### ENG-001: cloudera/hue (Apache-2.0)
- **What was useful:** SQL editor assistance, schema tree exploration, and query optimization patterns.
- **What was reused:** Architectural guidelines for database query assistants.
- **What was not reused:** 10,000+ files of Django/Knockout.js legacy UI application.
- **Why:** Massive legacy application unsuitable for inclusion in lightweight developer tooling.
- **Implementation Location:** `domains/15-DATA-AND-DATABASE-ENGINEERING/`.

#### ENG-002: obra/superpowers (MIT)
- **What was useful:** Disciplined coding agent methodology: test-driven development, systematic debugging, milestone decomposition.
- **What was reused:** Core methodology rules and step-by-step milestone planning guidelines.
- **What was not reused:** Jesse Vincent's personal prompt scripts.
- **Why:** Synthesized into OpenClone canonical domain 01 methodology.
- **Implementation Location:** `domains/01-METHODOLOGY/MK-FRAMEWORK/`.

#### ENG-003: shadcn/improve (MIT)
- **What was useful:** Codebase assessment, architectural X-ray, and systematic improvement workflows.
- **What was reused:** Workflow methodology for brownfield codebases.
- **What was not reused:** CLI binary.
- **Why:** Incorporated into canonical Workflow WF-002 (Existing Project X-Ray).
- **Implementation Location:** `workflows/WF-002-EXISTING-PROJECT-XRAY.md`.

#### ENG-004: microsoft/TokenEconomizer (MIT)
- **What was useful:** Token budget management, prompt deduplication, and context compression techniques.
- **What was reused:** Dual-tier knowledge architecture (compact MCP guidance files vs master encyclopedias).
- **What was not reused:** Python client library wrappers.
- **Why:** Embedded natively in OpenClone MCP server and documentation structure.
- **Implementation Location:** `src/openclone/mcp/server.py` and `docs/DOCUMENTATION-MAP.md`.
