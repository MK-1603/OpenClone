# Upstream IP Compliance Report: clamav (SEC-010)

**Audit Number:** `REPO-AUDIT-21`  
**Repository ID:** `SEC-010`  
**Canonical URL:** [https://github.com/Cisco-Talos/clamav](https://github.com/Cisco-Talos/clamav)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `clamav`
- **Original Owner / Organization:** `Cisco-Talos`
- **Target URL:** https://github.com/Cisco-Talos/clamav
- **Local Maintainer Path:** `.openclone-dev\upstream\security\SEC-010`
- **Original Branch:** `main`
- **Pinned Commit SHA:** `cad7b18a3e6505195fe08db1412449a18fc9f012`
- **Commit Date:** `2026-11-22`
- **Description:** Open source antivirus engine for detecting trojans, viruses, malware and malicious threats.
- **Primary Languages:** C, Rust
- **Core Technologies:** ClamAV Daemon, Libclamav, Rust FFI

## 2. License Identification
- **Declared License:** `GPL-2.0`
- **License Category:** `STRONG COPYLEFT`
- **License File Location:** `SEC-010/LICENSE` or constituent file
- **SPDX Identifier:** `GPL-2.0`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (C) 2021-2026 Cisco Systems, Inc.`
- **Original Authors / Maintainers:** `Cisco-Talos` and community contributors.
- **Assertion of Ownership:** OpenClone asserts ZERO ownership over upstream intellectual property.

## 4. Relevant File-Level Licenses & Exceptions
- **Root License:** `GPL-2.0` applies across repository files unless explicitly overridden.
- **Exceptions:** COPYING/ directory with constituent licenses

## 5. Reusable Capabilities
- **Concepts:** Architecture design, technical patterns, workflow sequencing.
- **Functional Value:** Integrates with OpenClone capability framework without copying entire application codebases.

## 6. Reuse Restrictions
- **Code Reuse:** `PROHIBITED UNDER IDENTIFIED TERMS`
- **Documentation Reuse:** `ALLOWED WITH CONDITIONS`
- **Asset Reuse:** `NOT APPLICABLE`
- **Specific Conditions:** GPL-2.0: Direct source inclusion prohibited. Independent daemon/socket communication only.

## 7. Attribution Requirements
- Must preserve: `Copyright (C) 2021-2026 Cisco Systems, Inc.` in downstream notices.
- Must cite source URL: `https://github.com/Cisco-Talos/clamav`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `YES`
- **Skill Distribution:** `NO`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `YES`
- **Redistribution Terms:** `YES (GPL-2.0 BOUNDARY: DAEMON ONLY)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** C, Rust
- **Copyleft Contamination Risk:** HIGH (GPL/LGPL copyleft isolation required)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `GPL-2.0: Direct source inclusion prohibited. Independent daemon/socket communication only.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `cad7b18a3e6505195fe08db1412449a18fc9f012`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\security\SEC-010`
- License Manifest: `integrations/manifests/SEC-010.manifest.json`