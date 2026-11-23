# OpenClone Optimized Repository Structure

**Document ID:** `STRUCT-OPTIMIZED-v2.0.0`  
**Status:** `CANONICAL DIRECTORY TOPOLOGY`  

---

## 1. Directory Structure & Responsibilities

```text
OpenClone/
├── adapters/           # Native host adapters (Antigravity, Claude Code, Cursor, Codex)
├── assessments/        # Master repository audit & release readiness assessments
├── blueprints/         # Historical architecture blueprints (Immutable Archive)
├── docs/               # Comprehensive documentation, guides, and reports
│   ├── architecture/   # System architecture and modular distribution specs
│   ├── compatibility/  # Multi-host conformance matrices
│   ├── installation/   # Global plugin installation guides
│   ├── integrations/   # Upstream registry, decisions, and update policy
│   ├── ip-compliance/  # Complete IP, copyright, and SBOM documentation
│   ├── knowledge/      # Fast live MCP guidance (< 12 KB per file)
│   ├── reports/        # Master upgrade and audit reports
│   └── security/       # Threat model, SaaS security baseline
├── domains/            # 31 engineering domain specifications (00-30)
├── engines/            # 56 capability engine execution contracts (E-001..E-056)
├── integrations/       # 27 upstream repository registry, manifests, and adapters
├── modules/            # On-demand capability pack manifests (mod-taste-skill-assets)
├── prompts/            # Reusable prompt scaffolds and role instructions
├── schemas/            # JSON Schema definitions for lifecycle and manifests
├── security/           # Pinned scanners lockfile (scanners.lock.json)
├── skills/             # Design governance skills (taste-skill)
├── src/openclone/      # Canonical Python runtime, gateway, installer, and MCP server
├── templates/          # Portable project templates (PROJECT.md, HANDOFF.md)
├── tests/              # 118 automated tests (100% pass rate)
├── tools/              # Repository validators, engines, and CLI utilities
└── workflows/          # 15 executable engineering workflows (WF-001..WF-015)
```
