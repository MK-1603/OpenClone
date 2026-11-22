# OpenClone — Repository Alternatives Matrix
**Version:** 1.0.0  
**Scope:** Evaluation of the 27 external reference repositories with verified candidate alternatives.

---

## 1. UI / UX & Frontend Design Repositories (11)

| # | Reference Repo | Capability Role | OpenClone Recommendation | Candidate Alternative A | Candidate Alternative B | Decision & Fallback Strategy |
|---|---|---|---|---|---|---|
| 1 | `bergside/design-md-chrome` | Design extraction | `REFERENCE` | Chrome DevTools Protocol (CDP) | Playwright CSS Extractor | Use as Chrome extension reference; fallback to CDP extraction |
| 2 | `shadcn-ui/ui` | Accessible primitives | `PRIMARY` | Radix UI Primitives | Park UI / Zag.js | Copy-paste components into project; fallback to raw Radix primitives |
| 3 | `Dammyjay93/interface-design` | UI design patterns | `REFERENCE` | Refactoring UI (Wathan/Schoger) | Nielsen Norman Design System | Retain as reference; do not install as code dependency |
| 4 | `Mohit-Raj-Singh/Unstop-UI` | Enterprise dashboard | `REFERENCE` | Tailwind UI Application Shells | Tremor Dashboard Blocks | Reference for data-dense dashboard composition |
| 5 | `anthropics/skills/.../frontend` | Frontend skill prompt | `SPECIALIST` | OpenClone Taste Skill v2.6.0 | Custom `.cursorrules` / Claude rules | Use OpenClone native skill; fallback to Anthropic prompt |
| 6 | `Leonxlnx/taste-skill` | Anti-AI-slop & gate | `PRIMARY` | Stylelint custom AST rules | Biome linter rules | Maintained as active native governance engine in `skills/` |
| 7 | `Nutlope/hallmark` | Visual critique tool | `OPTIONAL` | Playwright screenshot diffing | Cypress Visual Regression | Optional post-build screenshot review tool |
| 8 | `nextlevelbuilder/...` | Design system skill | `REFERENCE` | OpenClone 86-Style UI Catalog | OpenUI Community Group | Integrated into `docs/knowledge/ui-ux-design-catalogue.md` |
| 9 | `flitzrrr/...` | Frontend skills bundle | `REFERENCE` | OpenClone Skill Engine | W3C Web Design Standards | Handled by `tools/skill_engine.py` |
| 10 | `pbakaus/impeccable` | Craft & polish review | `OPTIONAL` | Web Vitals CLI + Lighthouse | Axe-core Accessibility Engine | Usability audit reference; fallback to Lighthouse CI |
| 11 | `jpoindexter/typography-skills`| Typography rhythm | `PRIMARY` | Typescale.com modular scales | Tailwind Typography plugin | Integrated into typography standards in `docs/knowledge/` |

---

## 2. Security Engineering Repositories (12)

| # | Reference Repo | Capability Role | OpenClone Recommendation | Candidate Alternative A | Candidate Alternative B | Decision & Fallback Strategy |
|---|---|---|---|---|---|---|
| 12 | `usestrix/strix` | Dynamic pentesting | `SPECIALIST` | ProjectDiscovery Nuclei | OWASP ZAP (Baseline Scan) | Strictly bounded to Docker isolated local targets with consent |
| 13 | `projectdiscovery/nuclei` | Vulnerability scanner | `OPTIONAL` | Nikto Web Scanner | OWASP ZAP API Scanner | Template-based DAST; optional for staging environments |
| 14 | `openai/codex-security` | LLM code scanner | `REFERENCE` | Semgrep Security Rules | GitHub CodeQL | Reference for LLM-assisted code review patterns |
| 15 | `cloudflare/security-audit-skill`| Cloudflare audit | `SPECIALIST` | ScoutSuite (Multi-Cloud) | Prowler (Cloud Security) | Specialist skill for Cloudflare Workers/DNS hardening |
| 16 | `semgrep/semgrep` | Static analysis (SAST) | `PRIMARY` | CodeQL (GitHub Actions) | Bandit (Python) / ESLint Security | Primary pinned static scanner in `security/scanners.lock.json` |
| 17 | `anthropics/...security-review`| AI security review | `SPECIALIST` | OpenClone Security Reviewer | OWASP Top 10 Manual Checklist | Run as specialist agent role in clean isolated context |
| 18 | `aquasecurity/trivy` | Container / SCA scan | `PRIMARY` | Grype (Anchore) | Snyk CLI (Open Source) | Pinned container & dependency vulnerability scanner |
| 19 | `trufflesecurity/trufflehog` | Secret detection | `PRIMARY` | Gitleaks | detect-secrets (Yelp) | Primary entropy & pattern-based secret scanner |
| 20 | `NVIDIA/skillspector` | Skill permission audit | `OPTIONAL` | OpenClone Skill Engine Verify | OPA / Rego Policy Engine | Optional auditor for third-party skill manifests |
| 21 | `Cisco-Talos/clamav` | Malware scanning | `OPTIONAL` | VirusTotal API | YARA Rules Engine | Specialized for user upload pipelines; optional |
| 22 | `qybaihe/bla` | Binary analysis | `DEFERRED` | Ghidra OSS | Radare2 | Out of scope for standard web SaaS; deferred |
| 23 | `microsoft/pyrit` | AI Red Teaming | `SPECIALIST` | Garak (NVIDIA) | Promptfoo (Red Teaming) | Framework for testing AI prompt injection and jailbreaks |

---

## 3. Software Engineering Repositories (4)

| # | Reference Repo | Capability Role | OpenClone Recommendation | Candidate Alternative A | Candidate Alternative B | Decision & Fallback Strategy |
|---|---|---|---|---|---|---|
| 24 | `cloudera/hue` | Big data query UI | `REFERENCE` | Apache Superset | Metabase OSS | Reference for data-dense querying; not a core dependency |
| 25 | `obra/superpowers` | Agent tool expansion | `REFERENCE` | MCP Official Servers | LangChain Toolkits | Replaced by standard Model Context Protocol (MCP) servers |
| 26 | `shadcn/improve` | CLI refactoring tool | `REFERENCE` | OpenClone Skill Engine | ESLint / Prettier Automation | Incorporated into portable IDE build workflow prompts |
| 27 | `microsoft/TokenEconomizer` | Token optimization | `REFERENCE` | Structured Context Pruning | Prompt Compression (LLMLingua) | Native context budgeting rules in `docs/knowledge/` |
