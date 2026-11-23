# OpenClone — Semantic & Near-Duplicate Documents Report

**Audit Date:** 2026-11-23  
**Scope:** Markdown Specifications, Prompts, Blueprints, and Knowledge Catalogues  

---

## 1. Verified Semantic Clusters

### Cluster A: Root Specification Forwarders & Canonical Targets
- **Primary Canonical Targets:**
  - `OPENCLONE-CORE-PRINCIPLES.md` (Authoritative)
  - `OPENCLONE-FUNCTIONAL-MAP.md` (Authoritative)
  - `OPENCLONE-LIFECYCLE-OVERVIEW.md` (Authoritative)
  - `OPENCLONE-MISSION-AND-SCOPE.md` (Authoritative)
- **Forwarding Stubs:**
  - `OPENCLONE-CORE-PRINCIPLES.md` (Forwarding stub to preserve external links)
  - `OPENCLONE-FUNCTIONAL-MAP.md` (Forwarding stub)
  - `OPENCLONE-LIFECYCLE-OVERVIEW.md` (Forwarding stub)
  - `OPENCLONE-MISSION-AND-SCOPE.md` (Forwarding stub)
- **Verdict:** `PRESERVE` forwarding stubs to guarantee backward-compatibility for external bookmarks and existing automation; no content duplication exists because stubs contain only forwarding notices.

### Cluster B: Knowledge Catalogues (Live MCP vs Master Encyclopedias)
- **Live MCP Guidance (`docs/knowledge/`):** 5 concise documents (< 12 KB each) optimized for fast LLM context injection during MCP tool calls.
- **Master Encyclopedias (`docs/knowledge-catalogues/`):** Exhaustive master taxonomies (16–19 KB each) packaged as on-demand modules.
- **Verdict:** `PRESERVE DUAL-TIER`. Not duplicate implementations; they fulfill distinct latency and context-window requirements.

### Cluster C: Governance Rulebook
- **Primary Canonical:** `domains/00-GOVERNANCE/OPENCLONE-RULEBOOK.md`
- **Forwarding Stub:** `domains/00-GOVERNANCE/OPENCLONE-RULEBOOK.md`
- **Verdict:** `PRESERVE`. Forwarding stub resolves backward-compatibility while establishing single source of truth.

### Cluster D: Concept Specifications (Standard vs Alternate)
- **Standard Specifications:** `concepts/01-GOVERNANCE-AND-AUTHORITY.md` to `10-MULTI-TOOL-ADAPTER-ECOSYSTEM.md`
- **Alternate Specifications:** `concepts/01-GOVERNANCE-AND-AUTHORITY.alternate.md` to `10-MULTI-TOOL-ADAPTER-ECOSYSTEM.alternate.md`
- **Verdict:** `PRESERVE`. Semantic analysis confirms alternate specifications document the explicit *Agile Self-Sovereign Developer Mode* for solo developer spikes.
