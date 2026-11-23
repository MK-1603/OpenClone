# OpenClone Dependency and Reference Map

**Document ID:** `MAP-DEPENDENCY-v2.0.0`  
**Status:** `VERIFIED REFERENCE MAP`  

---

## 1. Core Bidirectional Reference Map

```mermaid
graph TD
    AGENTS["AGENTS.md<br/>Operating Contract"] --> PROJ["PROJECT.md<br/>Project Specification"]
    PROJ --> DOM["domains/<br/>31 Domains"]
    DOM --> ENG["engines/<br/>56 Engines"]
    ENG --> WF["workflows/<br/>15 Workflows"]
    WF --> CAP["src/openclone/integrations/capabilities.py<br/>15 Canonical Capabilities"]
    CAP --> GW["src/openclone/integrations/gateway.py<br/>HMAC & Replay Defense"]
    GW --> MCP["src/openclone/mcp/server.py<br/>JSON-RPC Server"]
    MCP --> TESTS["tests/<br/>118 Passing Automated Tests"]
```

## 2. Integrity Guarantees
- No broken markdown references in tracked documentation.
- All engine specifications (`E-001` to `E-056`) and workflows (`WF-001` to `WF-015`) are cross-referenced in manifests.
