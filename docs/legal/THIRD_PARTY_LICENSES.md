# OpenClone — Third-Party Licenses Inventory

This document provides a comprehensive inventory of all licenses governing the 28 external upstream projects audited and integrated by OpenClone.

## Summary of License Distributions
- **Permissive (MIT):** 16 repositories
- **Permissive (Apache-2.0):** 7 repositories
- **Public Domain Dedication (CC0-1.0):** 1 repository
- **Weak Copyleft (LGPL-2.1):** 1 repository (`semgrep`) — quarantined to external CLI subprocess
- **Strong Copyleft (GPL-2.0 / GPL-3.0):** 2 repositories (`clamav`, `trufflehog`) — quarantined to external CLI/socket subprocess
- **Unverified / Missing License:** 1 repository (`Unstop-UI`) — quarantined, strictly prohibited from code reuse

---

## Detailed Repository License Matrix

| ID | Repository | Upstream URL | SPDX License | Ownership / Attribution | In OpenClone Core? |
|---|---|---|---|---|---|
| **UI-001** | `bergside/design-md-chrome` | `https://github.com/bergside/design-md-chrome` | `MIT` | Bergside | No (Optional Token Adapter) |
| **UI-002** | `shadcn-ui/ui` | `https://github.com/shadcn-ui/ui` | `MIT` | shadcn | No (Design Patterns Only) |
| **UI-003** | `Dammyjay93/interface-design` | `https://github.com/Dammyjay93/interface-design` | `MIT` | Dammyjay93 | No (Reference Only) |
| **UI-004** | `Mohit-Raj-Singh/Unstop-UI` | `https://github.com/Mohit-Raj-Singh/Unstop-UI` | `UNKNOWN` | Mohit-Raj-Singh | No (PROHIBITED FROM USE) |
| **UI-005** | `anthropics/skills` | `https://github.com/anthropics/skills` | `Apache-2.0` | Anthropic, PBC | No (Subdirectory Reference) |
| **UI-006** | `Leonxlnx/taste-skill` | `https://github.com/Leonxlnx/taste-skill` | `MIT` | Leonxlnx | Yes (Governance Skill in `skills/`) |
| **UI-007** | `nutlope/hallmark` | `https://github.com/nutlope/hallmark` | `MIT` | Hassan El Mghari | No (Reference Only) |
| **UI-008** | `nextlevelbuilder/ui-ux-pro-max-skill` | `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill` | `MIT` | nextlevelbuilder | No (Prompt Guideline Reference) |
| **UI-009** | `flitzrrr/frontend-design-skills` | `https://github.com/flitzrrr/frontend-design-skills` | `MIT` | flitzrrr | No (Design Patterns Only) |
| **UI-010** | `pbakaus/impeccable` | `https://github.com/pbakaus/impeccable` | `Apache-2.0` | Paul Bakaus | No (Design Rules Only) |
| **UI-011** | `jpoindexter/typography-skills` | `https://github.com/jpoindexter/typography-skills` | `MIT` | J. Poindexter | No (Type Token Reference) |
| **SEC-001** | `usestrix/strix` | `https://github.com/usestrix/strix` | `Apache-2.0` | Strix Security | No (External Docker Adapter) |
| **SEC-002** | `projectdiscovery/nuclei` | `https://github.com/projectdiscovery/nuclei` | `MIT` | ProjectDiscovery, Inc. | No (CLI Subprocess) |
| **SEC-003** | `openai/codex-security` | `https://github.com/openai/codex-security` | `Apache-2.0` | OpenAI | No (Reference Rules) |
| **SEC-004** | `cloudflare/security-audit-skill` | `https://github.com/cloudflare/security-audit-skill` | `MIT` | Cloudflare, Inc. | No (Reference Skill) |
| **SEC-005** | `semgrep/semgrep` | `https://github.com/semgrep/semgrep` | `LGPL-2.1` | Semgrep, Inc. | No (CLI Subprocess Only) |
| **SEC-006** | `anthropics/claude-code-security-review` | `https://github.com/anthropics/claude-code-security-review` | `MIT` | Anthropic, PBC | No (Review Prompt Reference) |
| **SEC-007** | `aquasecurity/trivy` | `https://github.com/aquasecurity/trivy` | `Apache-2.0` | Aqua Security Software Ltd. | No (CLI Subprocess Only) |
| **SEC-008** | `trufflesecurity/trufflehog` | `https://github.com/trufflesecurity/trufflehog` | `GPL-3.0` | Truffle Security Co. | No (CLI Subprocess Only) |
| **SEC-009** | `NVIDIA/skillspector` | `https://github.com/NVIDIA/skillspector` | `Apache-2.0` | NVIDIA Corporation | No (Subprocess Analyzer) |
| **SEC-010** | `Cisco-Talos/clamav` | `https://github.com/Cisco-Talos/clamav` | `GPL-2.0` | Cisco Systems, Inc. | No (External Socket/CLI Daemon) |
| **SEC-011** | `qybaihe/bla` | `https://github.com/qybaihe/bla` | `MIT` | qybaihe | No (CLI Scanner Adapter) |
| **SEC-012** | `microsoft/pyrit` | `https://github.com/microsoft/pyrit` | `MIT` | Microsoft Corporation | No (Optional PyRIT Adapter) |
| **ENG-001** | `cloudera/hue` | `https://github.com/cloudera/hue` | `Apache-2.0` | Cloudera, Inc. | No (Architecture Reference) |
| **ENG-002** | `obra/superpowers` | `https://github.com/obra/superpowers` | `MIT` | Jesse Vincent | No (Skill Patterns Reference) |
| **ENG-003** | `shadcn/improve` | `https://github.com/shadcn/improve` | `MIT` | shadcn | No (Code Review Pattern) |
| **ENG-004** | `microsoft/TokenEconomizer` | `https://github.com/microsoft/TokenEconomizer` | `MIT` | Microsoft Corporation | No (Prompt Optimization Formula) |
| **RES-001** | `codecrafters-io/build-your-own-x` | `https://github.com/codecrafters-io/build-your-own-x` | `CC0-1.0` | CodeCrafters, Inc. | No (Curated Tutorial Index) |

---

## Copyleft Isolation Boundary
OpenClone strictly enforces that copyleft software (`semgrep` under LGPL-2.1, `trufflehog` under GPL-3.0, and `clamav` under GPL-2.0) is NEVER linked into or vendored within the OpenClone Python runtime or distribution packages. All interactions are executed across clean process boundaries via external CLI arguments and standard POSIX/pipe streams.
