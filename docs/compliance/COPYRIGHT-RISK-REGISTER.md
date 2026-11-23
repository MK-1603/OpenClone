# OpenClone Copyright & Intellectual Property Risk Register

**Document ID:** `RISK-IP-COMPLIANCE-v1.0.0`  
**Standard:** AISDF Standard 1.0.0  
**Status:** `ACTIVE RISK REGISTER`  

---

## 1. Risk Assessment Matrix

| Risk ID | Target Repository | License Category | Risk Scenario | Severity | Implemented Mitigation | Residual Risk |
|---|---|---|---|---|---|---|
| **RSK-01** | `UI-004` (Unstop-UI) | `NO IDENTIFIABLE LICENSE` | Unauthorized copying of unlicensed UI components. | **HIGH** | Excluded completely from distribution (`BLOCKED_LICENSE_REVIEW`). | **ZERO** |
| **RSK-02** | `SEC-005` (semgrep) | `WEAK COPYLEFT` (LGPL-2.1) | Direct linking causes copyleft infection of core. | **HIGH** | Invoked strictly as independent external CLI subprocess. | **ZERO** |
| **RSK-03** | `SEC-008` (trufflehog) | `STRONG COPYLEFT` (GPL-3.0) | Vendoring source forces viral license terms. | **HIGH** | Strictly isolated as external CLI; regex filters rewritten in native Python. | **ZERO** |
| **RSK-04** | `SEC-010` (clamav) | `STRONG COPYLEFT` (GPL-2.0) | Daemon code linkage causes GPL infection. | **HIGH** | Network socket / daemon interaction only. | **ZERO** |
| **RSK-05** | `UI-006` (taste-skill) | `PERMISSIVE` (MIT) | 35 MB of heavy 3D renders bloats core plugin. | **MEDIUM** | Decoupled into on-demand optional module `mod-taste-skill-assets`. | **ZERO** |
| **RSK-06** | All Permissive Repos | `PERMISSIVE` (MIT / Apache) | Missing author attribution in distribution. | **LOW** | Centralized `THIRD-PARTY-NOTICES.md` with explicit copyright preservation. | **ZERO** |

---

## 2. Copyleft Boundary Policy
- **No Static Linking:** No GPL or LGPL code is ever imported into the OpenClone Python package.
- **Independent Subprocesses:** Scanners communicate over standard pipes (`stdin`/`stdout`) or HTTP/sockets.
- **Clean Reimplementation:** Algorithms (such as token extraction or regex filtering) are clean-room reimplemented in native Python.