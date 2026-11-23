# OpenClone Architecture Baseline & Topology

**Document ID:** `ARCH-BASELINE-v2.0.0`  
**Standard:** AISDF Standard 1.0.0  
**Status:** `VERIFIED ARCHITECTURE BASELINE`  

---

## 1. System Layers & Component Topology

```text
Layer 1: Multi-Host Integration Layer
         (Google Antigravity, Claude Code, Cursor, Codex, Generic MCP)
                     │
                     ▼
Layer 2: Shared MCP Service & Gateway
         (src/openclone/mcp/server.py · src/openclone/integrations/gateway.py)
         - 15 Canonical Capabilities · JSON-RPC 2.0 stdio/SSE
         - Cryptographic Human Approval Verification (HMAC-SHA256 with Nonce Replay Defense)
         - Workspace Boundary Containment (_check_boundary)
                     │
                     ▼
Layer 3: Deterministic Execution Core
         (openclone.py / openclone.py · tools/validate_repository.py · tools/checklist_engine.py)
         - 22-Phase Lifecycle State Machine (V0-V5 Evidence Verification)
         - Cycle-Free Task Dependency DAG
                     │
                     ▼
Layer 4: External Integrations & Modular Capability Packs
         (integrations/ · modules/ · skills/ · domains/ · engines/ · workforce/)
         - 27 Audited Upstream Repositories
         - 31 Engineering Domains
         - 56 Capability Engines
         - 72 Specialist Agent Roles
```

## 2. Component Boundaries
- **Runtime Boundary:** Python standard library (zero required external Python packages).
- **Security Boundary:** All file modifications anchored within `project_root` via `os.path.realpath`.
- **Packaging Boundary:** Core plugin installation package is < 350 KB. Heavy assets load on demand.
