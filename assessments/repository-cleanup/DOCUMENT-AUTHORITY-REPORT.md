# OpenClone — Document Authority & Single Source of Truth Register

**Audit Date:** 2026-11-23  
**Purpose:** Establish one clear, unambiguous single source of truth for every major functional area.  

---

## Authority Register

| Functional Subject | Authoritative Source of Truth | Subordinate / Supporting Documents | Deprecated / Archived Locations |
|---|---|---|---|
| **Core Governance Rules** | `domains/00-GOVERNANCE/OPENCLONE-RULEBOOK.md` | `AGENTS.md`, `GOVERNANCE.md` | `domains/00-GOVERNANCE/AISDF-RULEBOOK.md` (Forwarder) |
| **System Architecture** | `docs/architecture/OPENCLONE-2.0-ARCHITECTURE.md` | `TARGET_REPOSITORY_ARCHITECTURE.md` | `docs/archive/v4/ARCHITECTURE.md` |
| **Product Charter & Truth**| `PROJECT.md` | `OPENCLONE-MISSION-AND-SCOPE.md` | `AISDF-MISSION-AND-SCOPE.md` (Forwarder) |
| **Platform Operating Guide**| `docs/framework/OPERATING-GUIDE.md` | `docs/framework/RULES-AND-ENFORCEMENT.md` | `docs/archive/v4/OPERATING-GUIDE.md` |
| **UI/UX Anti-Slop Standard**| `domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md` | `skills/taste-skill/` | N/A |
| **Live MCP Guidance** | `docs/knowledge/*.md` (< 12 KB each) | `src/openclone/mcp/server.py` | `docs/archive/knowledge-drafts/` |
| **Master Encyclopedias** | `docs/knowledge-catalogues/*.md` | `modules/modules.manifest.json` | N/A |
| **Third-Party IP & Licensing**| `THIRD_PARTY_LICENSES.md`, `THIRD_PARTY_NOTICES.md` | `NOTICE`, `docs/legal/` | N/A |
| **Security Tooling Baseline** | `security/scanners.lock.json` | `docs/security/saas-security-baseline.md` | N/A |
| **Lifecycle & Verification** | `docs/engineering-lifecycle/22-PHASE-LIFECYCLE.md` | `tools/checklist_engine.py` | N/A |
