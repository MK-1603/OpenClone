# OpenClone Final Repository Structure
**Version:** 2.0.0  
**Architecture:** Modular Universal AI Software Engineering Platform  

---

```text
OpenClone/
├── .github/workflows/          # Deterministic CI/CD pipelines
├── adapters/                   # Multi-IDE host adapters (Antigravity, Cursor, Claude Code, Codex)
├── agents/                     # IDE agent configuration and rules (.cursorrules, CLAUDE.md)
├── assessments/
│   ├── README.md               # Assessments directory overview
│   ├── current/                # Single source of truth for active platform assessments
│   │   ├── REPOSITORY-HEALTH.md
│   │   ├── SECURITY-STATUS.md
│   │   └── RELEASE-READINESS.md
│   └── archive/                # Immutable historical assessment records
│       └── historical-assessments/
│           ├── cleanup-audit/
│           ├── maturity-rubric/
│           ├── repository-optimization/
│           └── requirements/
├── blueprints/
│   ├── README.md               # Authoritative blueprints index
│   ├── AISDF-METHODOLOGY-REFERENCE.md
│   ├── EXAMPLE-AI-SAAS-PROJECT.md
│   ├── OPENCLONE-MASTER-BLUEPRINT.md
│   └── archive/                # Preserved historical blueprints and prompts
│       ├── historical-blueprints/
│       └── historical-prompts/
├── concepts/                   # 10 unified architectural specifications (01..10)
│   ├── 01-GOVERNANCE-AND-AUTHORITY.md
│   ├── ...
│   ├── 10-MULTI-TOOL-ADAPTER-ECOSYSTEM.md
│   └── README.md
├── docs/                       # Comprehensive platform documentation
│   ├── README.md
│   ├── DOCUMENTATION-MAP.md
│   ├── alternatives/
│   ├── architecture/
│   ├── archive/
│   ├── compatibility/
│   ├── demo/
│   ├── engineering-coverage/
│   ├── engineering-lifecycle/
│   ├── installation/
│   ├── integrations/
│   ├── ip-compliance/
│   ├── knowledge/              # Tier 2: Live MCP Guidance Profiles (<12KB)
│   ├── knowledge-catalogues/   # Tier 1: Master Encyclopedias (~85KB)
│   ├── legal/                  # Third-party compliance and copyleft policy
│   ├── reports/                # Milestone reports
│   └── security/               # Threat models and security baselines
├── domains/                    # 31 software engineering knowledge domains (00..30)
├── engines/                    # 56 execution engine specifications (E-001..E-056)
├── integrations/               # Declarative metadata for 28 upstream repos
│   ├── manifests/
│   └── registry/
├── modules/                    # Modular distribution manifest (modules.manifest.json)
├── runtime/
│   ├── openclone_runtime/      # Primary deterministic execution engine & ledger
│   └── aisdf_runtime/          # Backward-compatibility forwarding layer
├── schemas/                    # JSON Schema draft 2020-12 specifications
├── security/                   # Pinned scanner toolchain lock (scanners.lock.json)
├── src/openclone/              # Modular v2.0 plugin platform (CLI, MCP, Skills, Installer)
├── tests/                      # 108 automated unit and integration tests
├── tools/                      # Deterministic CLI utilities and repository quality gate
├── workforce/                  # 72 specialist role contracts across 12 teams
├── AGENTS.md                   # Repository Operating Contract
├── CHANGELOG.md                # Release version history
├── LICENSE                     # MIT License
├── NOTICE                      # Upstream copyright attributions
├── PROJECT.md                  # Canonical project specification
├── README.md                   # Repository landing page
├── THIRD_PARTY_LICENSES.md     # Upstream license inventory
├── THIRD_PARTY_NOTICES.md      # Detailed attribution and modifications log
└── VERSION                     # Canonical release version (2.0.0)
```
