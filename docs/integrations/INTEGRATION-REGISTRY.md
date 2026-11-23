# OpenClone 27 Upstream Repositories Master Registry

**Document ID:** `REG-UPSTREAM-27-REPOSITORIES-v1.0.0`  
**Standard:** AISDF Standard 1.0.0 / OpenClone Platform 2.0.0  
**Machine-Readable Authority:** [`integrations/registry/upstream_registry.json`](../../integrations/registry/upstream_registry.json)  
**Status:** `ACTIVE REGISTRY · 27 ENTRIES RECORDED`  

---

## 1. Registry Architecture & Governance

The OpenClone Upstream Integration Registry governs all 27 external repositories. Each upstream repository is managed through a multi-tier lifecycle:

```text
UPSTREAM REPOSITORY
        │
        ▼ (Phase B)
    [ CLONED ]  ──────> Stored in maintainer workspace (.openclone-dev/upstream/)
        │
        ▼ (Phase C & D)
   [ REGISTERED ] ────> Tracked in upstream_registry.json & individual manifests
        │
        ▼ (Phase E & F)
    [ AUDITED ]  ─────> License, dependencies, and risks evaluated
        │
        ▼
   [ INTEGRATED ] ────> Connected via thin adapter or canonical OpenClone rule
        │
        ▼ (Phase I)
   [ AVAILABLE ]  ────> Invoked through OpenClone workflow or on-demand module
```

### Safety Rules
1. **Zero Unreviewed Default Inclusions:** No upstream repository is included in the default end-user plugin bundle (`included_by_default: false`).
2. **Immutable Commit Pinning:** Every integration is pinned to a specific verified Git commit SHA.
3. **No Upstream Mutation:** OpenClone never writes to or alters upstream Git checkouts.

---

## 2. Complete Upstream Registry Table

| ID | Name | Category | Pinned Commit | Branch | License | Decision | Status | Operational Role |
|---|---|---|---|---|---|---|---|---|
| **UI-001** | [design-md-chrome](https://github.com/bergside/design-md-chrome) | `ui-ux` | `8e07614f` | `main` | MIT | `ADAPTED` | `INTEGRATED` | Web design token extraction to Markdown |
| **UI-002** | [shadcn-ui](https://github.com/shadcn-ui/ui) | `ui-ux` | `bfa64ff4` | `main` | MIT | `REFERENCED` | `AVAILABLE` | Accessible React component primitives |
| **UI-003** | [interface-design](https://github.com/Dammyjay93/interface-design) | `ui-ux` | `2f9be320` | `main` | MIT | `REFERENCED` | `AVAILABLE` | Consumer UI patterns and layout references |
| **UI-004** | [Unstop-UI](https://github.com/Mohit-Raj-Singh/Unstop-UI) | `ui-ux` | `09da6d20` | `master` | UNKNOWN | `BLOCKED_LICENSE_REVIEW` | `CLONED` | Component reference (Blocked pending license) |
| **UI-005** | [anthropic-frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | `ui-ux` | `e4bb5d96` | `main` | Apache-2.0 | `ADOPTED` | `INTEGRATED` | Claude frontend design skill & spatial rules |
| **UI-006** | [taste-skill](https://github.com/Leonxlnx/taste-skill) | `ui-ux` | `f6b76575` | `main` | MIT | `ADOPTED` | `INTEGRATED` | Core anti-AI-slop tokens & governance gates |
| **UI-007** | [hallmark](https://github.com/nutlope/hallmark) | `ui-ux` | `04977e15` | `main` | MIT | `ADAPTED` | `INTEGRATED` | Design critique rules preventing AI clichés |
| **UI-008** | [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `ui-ux` | `6ec2bb58` | `main` | MIT | `ADAPTED` | `INTEGRATED` | 67-domain design system rules for SaaS |
| **UI-009** | [frontend-design-skills](https://github.com/flitzrrr/frontend-design-skills) | `ui-ux` | `d607ba30` | `main` | MIT | `REFERENCED` | `AVAILABLE` | Cross-assistant prompt rules (Claude, Cursor) |
| **UI-010** | [impeccable](https://github.com/pbakaus/impeccable) | `ui-ux` | `b49177d3` | `main` | Apache-2.0 | `ADAPTED` | `INTEGRATED` | Design critique vocabulary and quality audit |
| **UI-011** | [typography-skills](https://github.com/jpoindexter/typography-skills) | `ui-ux` | `615006a1` | `main` | MIT | `ADOPTED` | `INTEGRATED` | Major Third type scale, fluid typography |
| **SEC-001** | [strix](https://github.com/usestrix/strix) | `security` | `a1ccf777` | `main` | Apache-2.0 | `OPTIONAL_ADAPTER` | `INTEGRATED` | Dynamic AI pentesting in Docker sandbox |
| **SEC-002** | [nuclei](https://github.com/projectdiscovery/nuclei) | `security` | `e169d3bb` | `dev` | MIT | `OPTIONAL_ADAPTER` | `AVAILABLE` | Template-based vulnerability scanner |
| **SEC-003** | [codex-security](https://github.com/openai/codex-security) | `security` | `35373239` | `main` | Apache-2.0 | `REFERENCED` | `AVAILABLE` | AI automated vulnerability triage patterns |
| **SEC-004** | [security-audit-skill](https://github.com/cloudflare/security-audit-skill) | `security` | `c1c8a8c1` | `main` | MIT | `ADAPTED` | `INTEGRATED` | Agent-driven codebase security audit checklists |
| **SEC-005** | [semgrep](https://github.com/semgrep/semgrep) | `security` | `c4dbe9ee` | `develop` | GPL-2.0 | `OPTIONAL_ADAPTER` | `AVAILABLE` | Multi-language static code analysis (SAST) |
| **SEC-006** | [claude-code-security-review](https://github.com/anthropics/claude-code-security-review) | `security` | `0c6a49f1` | `main` | MIT | `ADAPTED` | `INTEGRATED` | Pull request security review checklists |
| **SEC-007** | [trivy](https://github.com/aquasecurity/trivy) | `security` | `edf9f5c1` | `main` | Apache-2.0 | `OPTIONAL_ADAPTER` | `AVAILABLE` | Container, IaC, and dependency CVE scanner |
| **SEC-008** | [trufflehog](https://github.com/trufflesecurity/trufflehog) | `security` | `4ef51f69` | `main` | GPL-3.0 | `OPTIONAL_ADAPTER` | `AVAILABLE` | High-entropy secret and credential detector |
| **SEC-009** | [skillspector](https://github.com/NVIDIA/skillspector) | `security` | `f9bb13dd` | `main` | Apache-2.0 | `ADAPTED` | `INTEGRATED` | AI agent skill security & prompt tool audit |
| **SEC-010** | [clamav](https://github.com/Cisco-Talos/clamav) | `security` | `cad7b18a` | `main` | GPL-2.0 | `OPTIONAL_ADAPTER` | `AVAILABLE` | Antivirus scanner for user file uploads |
| **SEC-011** | [bla](https://github.com/qybaihe/bla) | `security` | `2b7a7c4f` | `main` | MIT | `REFERENCED` | `AVAILABLE` | LLM agent behavioral security analyzer |
| **SEC-012** | [pyrit](https://github.com/microsoft/pyrit) | `security` | `81752345` | `main` | MIT | `OPTIONAL_ADAPTER` | `AVAILABLE` | Microsoft generative AI red-teaming framework |
| **ENG-001** | [hue](https://github.com/cloudera/hue) | `software-engineering` | `7ad92b18` | `master` | Apache-2.0 | `REFERENCED` | `AVAILABLE` | SQL assistant & schema tree navigation UX |
| **ENG-002** | [superpowers](https://github.com/obra/superpowers) | `software-engineering` | `22f0b463` | `main` | MIT | `ADAPTED` | `INTEGRATED` | Core agent engineering: TDD, debug, milestones |
| **ENG-003** | [improve](https://github.com/shadcn/improve) | `software-engineering` | `cac56e1e` | `main` | MIT | `REFERENCED` | `AVAILABLE` | Brownfield codebase improvement workflows |
| **ENG-004** | [TokenEconomizer](https://github.com/microsoft/TokenEconomizer) | `software-engineering` | `1bfeccdc` | `main` | MIT | `ADAPTED` | `INTEGRATED` | Context budget optimization & prompt dedup |

---

## 3. Individual Manifest Directory

Every entry has an individual declarative JSON manifest located in [`integrations/manifests/`](../../integrations/manifests/):
- `UI-001.manifest.json` through `UI-011.manifest.json`
- `SEC-001.manifest.json` through `SEC-012.manifest.json`
- `ENG-001.manifest.json` through `ENG-004.manifest.json`
