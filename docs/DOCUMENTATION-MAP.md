# OpenClone Canonical Documentation Map
## Single Source of Authority & Documentation Precedence

**Version:** 1.0.0  
**Standard:** AISDF Standard 1.0.0 / OpenClone Platform 1.0.0  
**Status:** `NORMATIVE AND CANONICAL`

---

## 1. Documentation Authority & Precedence

To eliminate conflicting specifications, overlapping rules, and contradictory requirements, OpenClone establishes a strict documentation precedence order:

1. **Platform / Tool Constraints:** Host execution boundaries, sandbox security rules, and user-approved permissions.
2. **Repository Operating Contract ([`AGENTS.md`](../AGENTS.md)):** Core operating rules for AI coding agents and human engineers.
3. **Active Project Specification ([`PROJECT.md`](../PROJECT.md)):** Current approved requirements, architecture, and scope for the active project.
4. **Normative Framework Standards:** Domain rules, security baselines, and quality gates in `domains/` and `standards/`.
5. **Runtime Specifications:** Deterministic engine contracts in `src/openclone/`, `engines/`, and `schemas/`.
6. **Architecture Decisions & Alternatives:** Trade-off records in `docs/alternatives/` and `docs/upgrade/`.
7. **Reference Knowledge & Encyclopedias:** Deep catalogues in `docs/knowledge-catalogues/` and `docs/knowledge/`.
8. **Historical Archive:** Superseded blueprints, upgrade prompts, and legacy notes in `blueprints/` and `docs/archive/`.

---

## 2. Master Authority Matrix by Subject

| Engineering Area | Canonical Authority Document | Scope / Role | Subordinate / Supporting Docs |
|---|---|---|---|
| **Repository Operating Contract** | [`AGENTS.md`](../AGENTS.md) | Single operating ruleset for all AI agents | `rules/*.md`, `adapters/*/rules` |
| **Product & Framework Standard** | [`openclone.manifest.json`](../openclone.manifest.json) | Version, runtime capabilities, scanner lock | `openclone.manifest.json`, `VERSION` |
| **Anti-AI-Slop Governance** | [`domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md`](../framework/domains/05-UX-UI-ENGINEERING/ANTI-AI-SLOP-STANDARDS.md) | Normative design rules, tokens, and contrast gates | `docs/knowledge/ui-ux-design-catalogue.md` |
| **SaaS Security Baseline** | [`docs/security/saas-security-baseline.md`](security/saas-security-baseline.md) | 19-point SaaS security standard | `security/scanners.lock.json`, `docs/security/THREAT-MODEL.md` |
| **22-Phase Lifecycle** | [`docs/engineering-lifecycle/MASTER_LIFECYCLE_CATALOGUE.md`](engineering-lifecycle/MASTER_LIFECYCLE_CATALOGUE.md) | Canonical 22-phase lifecycle and quality gates | `tools/checklist_engine.py` |
| **V0–V5 Evidence Verification** | [`docs/engineering-lifecycle/VERIFICATION_AND_EVIDENCE.md`](engineering-lifecycle/VERIFICATION_AND_EVIDENCE.md) | Observable evidence requirements & Goldfish protocol | `src/openclone/integrations/capabilities.py` |
| **Canonical Capabilities (15)** | [`src/openclone/integrations/capabilities.py`](../src/openclone/integrations/capabilities.py) | Python implementation, schemas, and risk tiers | `docs/integrations/CAPABILITY_REGISTRY.md` |
| **Gateway & Approvals** | [`src/openclone/integrations/gateway.py`](../src/openclone/integrations/gateway.py) | Cryptographic human approval & policy engine | `docs/integrations/SECURITY_AND_APPROVALS.md` |
| **Shared MCP Service** | [`src/openclone/mcp/server.py`](../src/openclone/mcp/server.py) | JSON-RPC 2.0 stdio/SSE MCP protocol implementation | `docs/integrations/MCP_SERVER.md` |
| **OpenClone 2.0 Architecture** | [`docs/architecture/OPENCLONE-2.0-ARCHITECTURE.md`](architecture/OPENCLONE-2.0-ARCHITECTURE.md) | Component boundaries, ADRs, modular distribution | `docs/architecture/REPOSITORY-AND-DISTRIBUTION-ARCHITECTURE.md` |
| **Host Compatibility** | [`docs/../global/docs/HOST-COMPATIBILITY.md`](../global/docs/HOST-COMPATIBILITY.md) | Multi-host extension format & conformance matrix | `docs/integrations/HOST_COMPATIBILITY_MATRIX.md` |
| **Global Plugin Installer** | [`src/openclone/installer/engine.py`](../src/openclone/installer/engine.py) | Multi-host transactional installer, doctor, status | `docs/installation/GLOBAL-PLUGIN-INSTALLATION.md`, `docs/installation/INSTALLATION-AND-MODULES.md` |
| **UI Design Styles (86)** | [`docs/reference/UI_DESIGN_CATALOGUE.md`](reference/UI_DESIGN_CATALOGUE.md) | Exhaustive 86-style visual catalog and architecture | `docs/knowledge/ui-ux-design-catalogue.md` |
| **Backend System Topics (580)** | [`docs/reference/BACKEND_SYSTEM_DESIGN_CATALOGUE.md`](reference/BACKEND_SYSTEM_DESIGN_CATALOGUE.md) | Exhaustive 580 backend & distributed system topics | `docs/knowledge/backend-system-design-catalogue.md` |
| **AI Engineering Topics (1,095)**| [`docs/reference/AI_ENGINEERING_CATALOGUE.md`](reference/AI_ENGINEERING_CATALOGUE.md) | LLM, RAG, agent, prompting, token budgeting topics | `docs/knowledge/ai-engineering-catalogue.md` |
| **Animation Tokens (365)** | [`docs/reference/ANIMATION_MOTION_CATALOGUE.md`](reference/ANIMATION_MOTION_CATALOGUE.md) | Physical spring easing tokens, 60fps rules | `docs/knowledge/motion-and-animation.md` |
| **Workforce Roles (72)** | [`workforce/registry/workers/`](../framework/workforce/registry/workers/) | 72 JSON worker role definitions | `workforce/teams/` |
| **Capability Engines (56)** | [`engines/`](../framework/engines/) | 56 engine execution specifications (E-001..E-056) | `docs/engineering-coverage/CATALOGUE.md` |
| **Workflows (15)** | [`workflows/`](../framework/workflows/) | 15 executable workflow definitions (WF-001..WF-015) | `openclone.manifest.json` |
| **Universal Project Intelligence** | [`docs/intelligence/README.md`](intelligence/README.md) | Universal taxonomy (12 families), multi-label classifier, router, 14 blueprints | `framework/registries/project-taxonomy.json`, `blueprints/README.md` |

---

## 3. Knowledge Directory Roles: Fast Guidance vs. Master Encyclopedias

To maintain sub-second response times for AI coding assistants while preserving comprehensive reference taxonomies, OpenClone separates knowledge into two tiers:

1. **Live MCP Guidance (`docs/knowledge/`):**
   - **Role:** Fast, compact guidance files (4–12 KB each) optimized for LLM context injection during MCP tool calls (`openclone_get_guidance`).
   - **Characteristics:** High signal-to-noise ratio, concise tables, focused checklists.
   - **Files:** `ui-ux-design-catalogue.md`, `ui-ux-quality-audit.md`, `motion-and-animation.md`, `backend-system-design-catalogue.md`, `ai-engineering-catalogue.md`.

2. **Master Knowledge Encyclopedias (`docs/knowledge-catalogues/`):**
   - **Role:** Deep, exhaustive engineering catalogues detailing complete taxonomies, code examples, trade-offs, and academic research references.
   - **Characteristics:** Packaged as an on-demand capability pack (`mod-knowledge-catalogues`), loaded only when deep domain research is required.
   - **Files:** `UI_DESIGN_CATALOGUE.md`, `ANIMATION_MOTION_CATALOGUE.md`, `BACKEND_SYSTEM_DESIGN_CATALOGUE.md`, `AI_ENGINEERING_CATALOGUE.md`, `CATALOGUE_TO_PRODUCT_CAPABILITY_MAP.md`.

---

## 4. Historical Archive & Planning Artifacts

Historical master blueprints, older upgrade prompts, and transition specifications in `blueprints/` and `docs/upgrade/` serve as immutable reference provenance. They are:
- Retained in the source repository for development traceability.
- **Excluded from default end-user plugin installations.**
- Classified under `ARCHIVE` in `archive/README.md`.
