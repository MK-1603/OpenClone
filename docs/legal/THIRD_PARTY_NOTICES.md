# OpenClone — Third-Party Notices & Attribution Register

OpenClone respects and acknowledges all third-party intellectual property, copyright notices, and license obligations. This document provides complete provenance, upstream commit SHAs, copyright notices, and integration details for all 28 integrated/audited external repositories.

---

## 1. UI & UX Design Repositories (UI-001 to UI-011)

### UI-001: design-md-chrome
- **Repository:** https://github.com/bergside/design-md-chrome
- **Commit SHA:** `8e07614fb1` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 Bergside
- **OpenClone Integration:** Integrated via `integrations/adapters/design_token_adapter.py` for design token parsing and markdown formatting. No upstream source files are vendored.

### UI-002: shadcn/ui
- **Repository:** https://github.com/shadcn-ui/ui
- **Commit SHA:** `bfa64ff4d1` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2023 shadcn
- **OpenClone Integration:** Architecture and design token conventions referenced in `domains/05-UI-UX-DESIGN/`.

### UI-003: interface-design
- **Repository:** https://github.com/Dammyjay93/interface-design
- **Commit SHA:** `2f9be32068` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 Dammyjay93
- **OpenClone Integration:** Conceptual reference for component layouts.

### UI-004: Unstop-UI
- **Repository:** https://github.com/Mohit-Raj-Singh/Unstop-UI
- **Commit SHA:** `09da6d2088` (branch `master`)
- **License:** **UNKNOWN / MISSING**
- **Copyright:** Mohit-Raj-Singh
- **Status:** **BLOCKED_LICENSE_REVIEW**. Strictly prohibited from code reuse, copying, or bundling into OpenClone.

### UI-005: anthropic-frontend-design (from anthropics/skills)
- **Repository:** https://github.com/anthropics/skills/tree/main/skills/frontend-design
- **Commit SHA:** `e4bb5d960d` (branch `main`)
- **License:** Apache License 2.0
- **Copyright:** Copyright (c) 2024 Anthropic, PBC
- **OpenClone Integration:** Prompt heuristics and frontend design evaluation rules.

### UI-006: taste-skill
- **Repository:** https://github.com/Leonxlnx/taste-skill
- **Commit SHA:** `f6b76575f9` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 Leonxlnx
- **OpenClone Integration:** Governed design system skill in `skills/taste-skill/` with 13 automated node anti-slop verification tests. Original MIT license preserved in `skills/taste-skill/LICENSE`.

### UI-007: hallmark
- **Repository:** https://github.com/nutlope/hallmark
- **Commit SHA:** `04977e15f3` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 Hassan El Mghari
- **OpenClone Integration:** AI UI generation patterns and visual review guidelines.

### UI-008: ui-ux-pro-max-skill
- **Repository:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- **Commit SHA:** `6ec2bb5833` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 nextlevelbuilder
- **OpenClone Integration:** Design system prompts and multi-variant component checklists.

### UI-009: frontend-design-skills
- **Repository:** https://github.com/flitzrrr/frontend-design-skills
- **Commit SHA:** `d607ba305b` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 flitzrrr
- **OpenClone Integration:** Frontend design patterns and layout tokens.

### UI-010: impeccable
- **Repository:** https://github.com/pbakaus/impeccable
- **Commit SHA:** `b49177d327` (branch `main`)
- **License:** Apache License 2.0
- **Copyright:** Copyright (c) 2024 Paul Bakaus
- **OpenClone Integration:** Accessibility benchmarks and contrast ratio rules.

### UI-011: typography-skills
- **Repository:** https://github.com/jpoindexter/typography-skills
- **Commit SHA:** `615006a142` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 J. Poindexter
- **OpenClone Integration:** Typographic scale and responsive viewport font formulas.

---

## 2. Security Scanners, Toolchains & Agents (SEC-001 to SEC-012)

### SEC-001: strix
- **Repository:** https://github.com/usestrix/strix
- **Commit SHA:** `a1ccf777d8` (branch `main`)
- **License:** Apache License 2.0
- **Copyright:** Copyright (c) 2024 Strix Security
- **OpenClone Integration:** Integrated via `integrations/adapters/strix_adapter.py`. Dynamic pentesting runner with strict target allowlists.

### SEC-002: nuclei
- **Repository:** https://github.com/projectdiscovery/nuclei
- **Commit SHA:** `e169d3bb5d` (branch `dev`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 ProjectDiscovery, Inc.
- **OpenClone Integration:** Automated scanning templates coordinated via `integrations/adapters/scanner_gateway.py`.

### SEC-003: codex-security
- **Repository:** https://github.com/openai/codex-security
- **Commit SHA:** `35373239d9` (branch `main`)
- **License:** Apache License 2.0
- **Copyright:** Copyright (c) 2024 OpenAI
- **OpenClone Integration:** Heuristic rules for identifying sensitive tokens and insecure API usage.

### SEC-004: security-audit-skill
- **Repository:** https://github.com/cloudflare/security-audit-skill
- **Commit SHA:** `c1c8a8c147` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 Cloudflare, Inc.
- **OpenClone Integration:** Cloud security review and DNS/WAF rule auditing patterns.

### SEC-005: semgrep
- **Repository:** https://github.com/semgrep/semgrep
- **Commit SHA:** `c4dbe9ee2f` (branch `develop`)
- **License:** LGPL-2.1
- **Copyright:** Copyright (c) 2024 Semgrep, Inc.
- **OpenClone Integration:** External subprocess invocation via `ScannerGatewayAdapter`. Zero code vendored; strict process boundary.

### SEC-006: claude-code-security-review
- **Repository:** https://github.com/anthropics/claude-code-security-review
- **Commit SHA:** `0c6a49f1fa` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 Anthropic, PBC
- **OpenClone Integration:** Multi-stage security review prompts.

### SEC-007: trivy
- **Repository:** https://github.com/aquasecurity/trivy
- **Commit SHA:** `edf9f5c13d` (branch `main`)
- **License:** Apache License 2.0
- **Copyright:** Copyright (c) 2024 Aqua Security Software Ltd.
- **OpenClone Integration:** External CLI container/filesystem vulnerability and SBOM scanner.

### SEC-008: trufflehog
- **Repository:** https://github.com/trufflesecurity/trufflehog
- **Commit SHA:** `4ef51f69ca` (branch `main`)
- **License:** GPL-3.0
- **Copyright:** Copyright (c) 2024 Truffle Security Co.
- **OpenClone Integration:** External CLI secret detection scanner. Strict process boundary; zero vendored code.

### SEC-009: skillspector
- **Repository:** https://github.com/NVIDIA/skillspector
- **Commit SHA:** `f9bb13dd16` (branch `main`)
- **License:** Apache License 2.0
- **Copyright:** Copyright (c) 2024 NVIDIA Corporation
- **OpenClone Integration:** Agent safety and prompt compliance verification.

### SEC-010: clamav
- **Repository:** https://github.com/Cisco-Talos/clamav
- **Commit SHA:** `cad7b18a3e` (branch `main`)
- **License:** GPL-2.0
- **Copyright:** Copyright (c) 2024 Cisco Systems, Inc.
- **OpenClone Integration:** Daemon/socket scanner for workspace file inspection. Zero vendoring; strict socket boundary.

### SEC-011: bla (Binary Level Analysis)
- **Repository:** https://github.com/qybaihe/bla
- **Commit SHA:** `2b7a7c4f2a` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 qybaihe
- **OpenClone Integration:** Binary dependency and symbol safety checks.

### SEC-012: pyrit (Python Risk Identification Toolkit)
- **Repository:** https://github.com/microsoft/pyrit
- **Commit SHA:** `8175234584` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 Microsoft Corporation
- **OpenClone Integration:** Integrated via `integrations/adapters/pyrit_adapter.py` for AI red-teaming and prompt injection detection.

---

## 3. Software Engineering Capabilities (ENG-001 to ENG-004)

### ENG-001: hue
- **Repository:** https://github.com/cloudera/hue
- **Commit SHA:** `7ad92b1820` (branch `master`)
- **License:** Apache License 2.0
- **Copyright:** Copyright (c) 2024 Cloudera, Inc.
- **OpenClone Integration:** Architecture design patterns for SQL query execution and database tooling.

### ENG-002: superpowers
- **Repository:** https://github.com/obra/superpowers
- **Commit SHA:** `22f0b463e7` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 Jesse Vincent
- **OpenClone Integration:** Agent shell tool execution and developer workflow primitives.

### ENG-003: improve
- **Repository:** https://github.com/shadcn/improve
- **Commit SHA:** `cac56e1ebd` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 shadcn
- **OpenClone Integration:** Heuristics for codebase refactoring, code health, and minimal diff editing.

### ENG-004: TokenEconomizer
- **Repository:** https://github.com/microsoft/TokenEconomizer
- **Commit SHA:** `1bfeccdcec` (branch `main`)
- **License:** MIT License
- **Copyright:** Copyright (c) 2024 Microsoft Corporation
- **OpenClone Integration:** Prompt token optimization, context compression, and budget enforcement.

---

## 4. Engineering Knowledge Resources (RES-001)

### RES-001: build-your-own-x
- **Repository:** https://github.com/codecrafters-io/build-your-own-x
- **Commit SHA:** `94e4be4102` (branch `master`)
- **License:** CC0-1.0 Universal Public Domain Dedication
- **Copyright:** CodeCrafters, Inc. has waived copyright rights to this index.
- **OpenClone Integration:** Reference curriculum index for from-scratch system building tutorials. Linked external resources possess separate independent terms.
