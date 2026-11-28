# OpenClone — Target Repository Architecture

```mermaid
graph TD
    CLI["openclone CLI / openclone.py"] --> MCP["Model Context Protocol (src/openclone/mcp/)"]
    CLI --> INST["Global Installer (src/openclone/installer/)"]
    CLI --> RT["Local Control Plane (runtime/openclone_runtime/)"]
    
    RT --> DB[(.openclone/workforce.sqlite3)]
    RT --> LEDGER["Audit Ledger & Release Gate"]
    
    MCP --> KNOWLEDGE["Knowledge Engine (docs/knowledge/)"]
    MCP --> ENGINES["56 Capability Engines (engines/)"]
    
    INTEG["Integrations Gateway (integrations/)"] --> EXT_SEC["12 Security Scanners (Subprocess)"]
    INTEG --> EXT_UX["11 UI/UX Adapters"]
    
    DOMAINS["31 Engineering Domains (domains/)"] --> GOV["Governance & Rulebook (domains/00-GOVERNANCE/)"]
```

## Architectural Layers
1. **Presentation & Interoperability:** `src/openclone/cli.py`, `src/openclone/mcp/server.py`, `adapters/`.
2. **Deterministic Control Plane:** `runtime/openclone_runtime/` (Python stdlib + SQLite).
3. **Integration Gateway:** `integrations/adapters/`, `integrations/manifests/`, `integrations/registry/`.
4. **Engineering Knowledge Engine:** `domains/` (31 domains), `engines/` (56 engine specs), `docs/knowledge/`.
5. **Quality & Anti-Slop Governance:** `skills/taste-skill/`, `security/`, `tests/`.
