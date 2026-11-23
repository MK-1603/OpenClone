# OpenClone Upstream License & Attribution Register

**Document ID:** `LIC-UPSTREAM-27-REPOSITORIES-v1.0.0`  
**Product:** OpenClone 2.0 Universal AI Software Engineering Platform  
**Standard:** AISDF Standard 1.0.0  
**Status:** `NORMATIVE ATTRIBUTION REGISTER`  

---

## 1. Upstream Licensing Policy & Legal Safeguards

OpenClone rigorously upholds open-source licensing, copyright attribution, and intellectual property boundaries:

1. **No Relicensing:** OpenClone does NOT relicense upstream third-party code. Upstream projects retain their original licenses and copyright notices.
2. **Copyleft Boundary Enforcement:** Tools licensed under strong copyleft (e.g., GPL-2.0, GPL-3.0, LGPL-2.1) are NEVER vendored or statically linked into the OpenClone distributable core. They are integrated strictly as external processes or independent service adapters.
3. **No Unlicensed Inclusions:** Repositories without explicit permissive or open-source licenses (e.g., `UI-004` Unstop-UI) are classified as `BLOCKED_LICENSE_REVIEW` and excluded from distribution.
4. **Attribution & Notice Preservation:** Upstream authors, projects, and original repository URLs are catalogued and cited across all documentation, manifests, and adapters.

---

## 2. Comprehensive License & Attribution Ledger

| ID | Project Name | Upstream Repository | Declared License | Copyright Holders / Authors | Copyleft Status | Review Verdict |
|---|---|---|---|---|---|---|
| **UI-001** | `design-md-chrome` | `bergside/design-md-chrome` | **MIT** | Bergside | Permissive | `APPROVED` |
| **UI-002** | `shadcn-ui` | `shadcn-ui/ui` | **MIT** | Shadcn & Contributors | Permissive | `APPROVED` |
| **UI-003** | `interface-design` | `Dammyjay93/interface-design` | **MIT** | Damilola Jerugba | Permissive | `APPROVED` |
| **UI-004** | `Unstop-UI` | `Mohit-Raj-Singh/Unstop-UI` | **UNKNOWN** | Mohit Raj Singh | Missing License | `BLOCKED_LICENSE_REVIEW` |
| **UI-005** | `anthropic-frontend-design` | `anthropics/skills` | **Apache-2.0** | Anthropic, PBC | Permissive with Patent Grant | `APPROVED` |
| **UI-006** | `taste-skill` | `Leonxlnx/taste-skill` | **MIT** | Leonxlnx & Contributors | Permissive | `APPROVED` |
| **UI-007** | `hallmark` | `nutlope/hallmark` | **MIT** | Hassan El Mghari | Permissive | `APPROVED` |
| **UI-008** | `ui-ux-pro-max-skill` | `nextlevelbuilder/ui-ux-pro-max-skill` | **MIT** | NextLevelBuilder | Permissive | `APPROVED` |
| **UI-009** | `frontend-design-skills` | `flitzrrr/frontend-design-skills` | **MIT** | Flitzrrr | Permissive | `APPROVED` |
| **UI-010** | `impeccable` | `pbakaus/impeccable` | **Apache-2.0** | Paul Bakaus | Permissive with Patent Grant | `APPROVED` |
| **UI-011** | `typography-skills` | `jpoindexter/typography-skills` | **MIT** | Jason Poindexter | Permissive | `APPROVED` |
| **SEC-001** | `strix` | `usestrix/strix` | **Apache-2.0** | Strix Team | Permissive with Patent Grant | `APPROVED` |
| **SEC-002** | `nuclei` | `projectdiscovery/nuclei` | **MIT** | ProjectDiscovery, Inc. | Permissive | `APPROVED` |
| **SEC-003** | `codex-security` | `openai/codex-security` | **Apache-2.0** | OpenAI | Permissive with Patent Grant | `APPROVED` |
| **SEC-004** | `security-audit-skill` | `cloudflare/security-audit-skill` | **MIT** | Cloudflare, Inc. | Permissive | `APPROVED` |
| **SEC-005** | `semgrep` | `semgrep/semgrep` | **LGPL-2.1** | Semgrep, Inc. | Weak Copyleft (External CLI only) | `APPROVED (EXTERNAL ONLY)` |
| **SEC-006** | `claude-code-security-review`| `anthropics/claude-code-security-review` | **MIT** | Anthropic, PBC | Permissive | `APPROVED` |
| **SEC-007** | `trivy` | `aquasecurity/trivy` | **Apache-2.0** | Aqua Security Software Ltd. | Permissive with Patent Grant | `APPROVED` |
| **SEC-008** | `trufflehog` | `trufflesecurity/trufflehog` | **GPL-3.0** | Truffle Security Co. | Strong Copyleft (External CLI only) | `APPROVED (EXTERNAL ONLY)` |
| **SEC-009** | `skillspector` | `NVIDIA/skillspector` | **Apache-2.0** | NVIDIA Corporation | Permissive with Patent Grant | `APPROVED` |
| **SEC-010** | `clamav` | `Cisco-Talos/clamav` | **GPL-2.0** | Cisco Systems, Inc. | Strong Copyleft (External CLI only) | `APPROVED (EXTERNAL ONLY)` |
| **SEC-011** | `bla` | `qybaihe/bla` | **MIT** | qybaihe | Permissive | `APPROVED` |
| **SEC-012** | `pyrit` | `microsoft/pyrit` | **MIT** | Microsoft Corporation | Permissive | `APPROVED` |
| **ENG-001** | `hue` | `cloudera/hue` | **Apache-2.0** | Cloudera, Inc. | Permissive with Patent Grant | `APPROVED` |
| **ENG-002** | `superpowers` | `obra/superpowers` | **MIT** | Jesse Vincent | Permissive | `APPROVED` |
| **ENG-003** | `improve` | `shadcn/improve` | **MIT** | Shadcn | Permissive | `APPROVED` |
| **ENG-004** | `TokenEconomizer` | `microsoft/TokenEconomizer` | **MIT** | Microsoft Corporation | Permissive | `APPROVED` |

---

## 3. License Distribution Summary

| License SPDX ID | Count | Percentage | Reusability in OpenClone Core |
|---|---:|---:|---|
| **MIT** | 16 | 59.3% | Fully reusable with attribution |
| **Apache-2.0** | 7 | 25.9% | Fully reusable with NOTICE preservation |
| **GPL-2.0** | 1 | 3.7% | External process boundary only |
| **GPL-3.0** | 1 | 3.7% | External process boundary only |
| **LGPL-2.1** | 1 | 3.7% | External process boundary only |
| **UNKNOWN** | 1 | 3.7% | Blocked pending license clarification |
| **Total** | **27** | **100.0%** | **100% Accounted For** |
