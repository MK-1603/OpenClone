# OpenClone — Catalogue to Product Capability Mapping
**Version:** 1.0.0  
**Scope:** Explicit mapping of concepts across UI (232), Backend (580), AI (1,095), and Motion (365) to OpenClone product implementation boundaries.

---

## 1. Classification Methodology

To prevent implementation bloat and maintain architectural discipline, every capability in the knowledge catalogues is assigned one of six distinct product classifications:

1. **`CORE_PRODUCT`**: Capabilities provided directly to end-users or executed by the OpenClone core platform (e.g. portable project generator, deterministic skill engine, MCP inspection tools).
2. **`INTERNAL_ENGINEERING`**: Mechanisms implemented internally to power OpenClone's governance, audit ledger, and security checks (e.g. SHA-256 approval binding, SQLite DAG, Taste Skill anti-slop scanner).
3. **`OPTIONAL_INTEGRATION`**: Capabilities supported via optional, user-enabled tools or plugins (e.g. Strix DAST pentest, external LLM routers, Playwright visual regression).
4. **`REFERENCE_KNOWLEDGE`**: Architectural patterns, design taxonomies, and best practices provided as guidance for AI agents and human architects during project planning (e.g. 86 visual styles, 580 backend topics).
5. **`FUTURE_RESEARCH`**: Emerging frontiers monitored for future roadmap consideration (e.g. Test-Time Compute scaling, Spiking Neural Networks).
6. **`OUT_OF_SCOPE`**: Deliberately excluded capabilities that contradict core principles (e.g. scraping proxies, unmonitored autonomous swarms, arbitrary shell bypasses).

---

## 2. Product Capability Mapping Table

| Domain / Concept Cluster | Source Catalogue | Product Classification | Implementation / Guidance Path | Handling Rationale |
|---|---|---|---|---|
| **Portable Specification Generator** | Core Architecture | `CORE_PRODUCT` | `templates/PROJECT.template.md`, `README.md` | Core zero-install workflow for application creators |
| **Deterministic Skill Engine** | Skill System | `CORE_PRODUCT` | `src/openclone/skills/engine.py`, `tools/skill_engine.py` | Eliminates skill amnesia; executes 8-stage lifecycle |
| **Shared MCP Service** | Tool Protocols | `CORE_PRODUCT` | `src/openclone/mcp/server.py` | Universal JSON-RPC 2.0 stdio/SSE server for multi-IDE integration |
| **Local Task DAG & Audit Ledger** | Control Plane | `INTERNAL_ENGINEERING` | `openclone.py`, `openclone.py` | Tamper-evident SQLite state machine and hash-chained log |
| **Taste Skill Anti-Slop Scanner** | UI Governance | `INTERNAL_ENGINEERING` | `skills/taste-skill/audit-slop.mjs` | AST-based static scanner blocking AI aesthetic clichés |
| **Design Plan Pre-Build Gate** | UI Governance | `INTERNAL_ENGINEERING` | `skills/taste-skill/plan-check.mjs` | Deterministic quality gate (Level 1 to Level 5) |
| **19-Point SaaS Security Baseline** | Security Controls | `INTERNAL_ENGINEERING` | `docs/security/saas-security-baseline.md` | Verification checklist and security gate criteria |
| **Scanner Lock & Hardening** | Supply-Chain Security | `INTERNAL_ENGINEERING` | `security/scanners.lock.json` | 12 scanners pinned to immutable 40-char commit SHAs |
| **Strix Dynamic AI Pentesting** | Security DAST | `OPTIONAL_INTEGRATION` | `docs/integrations/strix-dynamic-testing.md` | Gated dynamic testing requiring written owner authorization |
| **External LLM Routers (LiteLLM)** | AI Gateways | `OPTIONAL_INTEGRATION` | `docs/integrations/llm-router-comparison.md` | Optional fallback router for provider failover and rate limits |
| **Visual Regression Testing** | UI Quality | `OPTIONAL_INTEGRATION` | `docs/alternatives/UI_UX_AND_DESIGN_ALTERNATIVES.md` | Playwright screenshot diffing in CI pipelines |
| **86 Visual Design Directions** | UI Catalogue | `REFERENCE_KNOWLEDGE` | `docs/knowledge-catalogues/UI_DESIGN_CATALOGUE.md` | Reference styles selected during Stage B art direction |
| **232 UI Architecture Taxonomy** | UI Catalogue | `REFERENCE_KNOWLEDGE` | `docs/knowledge-catalogues/UI_DESIGN_CATALOGUE.md` | 8-layer component and container architectural taxonomy |
| **365 Animation & Motion Concepts** | Motion Catalogue | `REFERENCE_KNOWLEDGE` | `docs/knowledge-catalogues/ANIMATION_MOTION_CATALOGUE.md` | Physical spring tokens, 60fps rules, and reduced-motion standards |
| **580 Backend & System Topics** | Backend Catalogue | `REFERENCE_KNOWLEDGE` | `docs/knowledge-catalogues/BACKEND_SYSTEM_DESIGN_CATALOGUE.md` | Architecture, database, caching, queue, and scaling patterns |
| **1,095 AI Engineering Topics** | AI Catalogue | `REFERENCE_KNOWLEDGE` | `docs/knowledge-catalogues/AI_ENGINEERING_CATALOGUE.md` | LLM, RAG, agent, prompting, and token budgeting reference |
| **Test-Time Compute & MCTS** | AI Catalogue Domain 18 | `FUTURE_RESEARCH` | `docs/knowledge-catalogues/AI_ENGINEERING_CATALOGUE.md` | Emerging inference-time search research under evaluation |
| **Scraping / Free Web Routers** | Router Candidates | `OUT_OF_SCOPE` | `docs/alternatives/DEFERRED_AND_REJECTED_OPTIONS.md` | Violates provider TOS; severe security and reliability risk |
| **Unbounded Autonomous Swarms** | Agent Architecture | `OUT_OF_SCOPE` | `docs/alternatives/DEFERRED_AND_REJECTED_OPTIONS.md` | Causes infinite retry loops, runaway costs, and state chaos |
