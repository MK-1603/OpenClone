# Gap and Conflict Register — OpenClone Requirements
## Audit of OpenClone Requirements Gaps, Ambiguities, and Mitigations

- **Framework Version:** `1.0.0`
- **Audit Date:** 2026-11-22
- **Status:** MONITORED & RESOLVED

---

## 1. Register of Identified Gaps

| Gap ID | Area | Description | Severity | Resolution Status | Mitigation / Evidence |
|---|---|---|---|---|---|
| `GAP-REQ-001` | Multi-IDE Integration | Need for unified shared MCP service across Claude Code, Cursor, Codex, Antigravity, and ChatGPT. | `MEDIUM` | **RESOLVED** | Implemented stdio/SSE `openclone_mcp` server with 7 core tools; adapter manifests generated in `adapters/`. |
| `GAP-REQ-002` | Root vs Generated Requirements | Potential ambiguity between OpenClone's framework requirements and generated application requirements. | `MEDIUM` | **RESOLVED** | Explicit separation: root `PROJECT.md` documents OpenClone; `templates/PROJECT.template.md` documents user projects. |
| `GAP-REQ-003` | Requirements Taxonomy | Absence of formal MUST/SHOULD/COULD/WONT and Knowledge State tagging in earlier draft specifications. | `LOW` | **RESOLVED** | Standardized taxonomy in `assessments/requirements/REQUIREMENTS-SYSTEM-AUDIT.md` and root `PROJECT.md`. |
| `GAP-REQ-004` | ChatGPT Surface Integration | Lack of dedicated remote MCP connection configuration and custom GPT instructions. | `LOW` | **RESOLVED** | Added `adapters/chatgpt/` with security architecture, endpoint guide, and custom GPT system instructions. |

---

## 2. Register of Historical Conflicts & Precedence Resolutions

1. **Naming & Identity Conflict:**
   - *Conflict:* Legacy specifications used `AISDF`, while the canonical product is `OpenClone`.
   - *Resolution:* Unified as `OpenClone` (product name) powered by `AISDF` (underlying universal engineering standard).
2. **Domain Hierarchy Conflict:**
   - *Conflict:* 31 numbered domains previously sat at root, conflicting with clean repository packaging.
   - *Resolution:* All 31 domains consolidated under [`domains/`](file:///domains) in commit `ba8d2a1`; zero numbered folders at root.
3. **Execution Sandbox vs Governed Subprocess:**
   - *Conflict:* Prose occasionally suggested OpenClone includes an OS-level kernel container.
   - *Resolution:* Truthful documentation asserts `openclone.py` / `workforce.py` provides deterministic process execution, argument validation, and env redaction; real container sandboxing requires Docker or VM.
