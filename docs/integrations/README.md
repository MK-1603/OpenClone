# Universal AI Tool Integration & Global Plugin Ecosystem

## Executive Directive

OpenClone capabilities are decoupled from any single AI provider, coding IDE, chat application, or plugin marketplace.

OpenClone provides **one governed capability platform exposed through multiple compatible integration surfaces**:

```text
                 OPENCLONE PLATFORM
                        |
       +----------------+----------------+
       |                |                |
 Project & SDLC     Engineering       Skills &
 Checklist          Verification      Knowledge
       |                |                |
       +----------------+----------------+
                        |
             Canonical Capability Layer
                        |
             Permission & Policy Engine
                        |
                Integration Gateway
                        |
      +-----------------+------------------+
      |                 |                  |
  MCP Adapter       HTTP/API Adapter    CLI/SDK Adapter
      |                 |                  |
      +-----------------+------------------+
                        |
             Host Compatibility Adapters
                        |
      +---------+---------+---------+---------+
      |         |         |         |         |
   ChatGPT    Claude    Gemini   Antigravity  Cursor
      |         |         |         |         |
      +---------+---------+---------+---------+
                        |
             Other supported AI hosts
```

---

## Documentation Suite Index

| Document | Purpose |
|---|---|
| [Universal Architecture](UNIVERSAL_INTEGRATION_ARCHITECTURE.md) | Single canonical core, multi-adapter design, gateway layers. |
| [Canonical Capability Registry](CAPABILITY_REGISTRY.md) | The 15 canonical capabilities, schemas, risk classes, and scopes. |
| [MCP Server Specification](MCP_SERVER.md) | Model Context Protocol implementation (Tools, Resources, Prompts). |
| [HTTP & OpenAPI Specification](HTTP_OPENAPI.md) | REST API endpoints, OpenAPI 3.1 schema, and webhook contracts. |
| [Authorization & Scopes](AUTHORIZATION_AND_SCOPES.md) | OAuth 2.1/OIDC token claims, scoped permissions, and tenant boundaries. |
| [Host Compatibility Matrix](HOST_COMPATIBILITY_MATRIX.md) | Verified compatibility across ChatGPT, Claude, Antigravity, Cursor, etc. |
| [Host Setup Guides](HOST_SETUP_GUIDES.md) | Copy-pasteable connection configs for all supported AI coding hosts. |
| [Skill Portability](SKILL_PORTABILITY.md) | Canonical skill package export, lifecycle states, and runtime loading. |
| [Security & Approvals](SECURITY_AND_APPROVALS.md) | Policy engine, risk classifications, and SHA-256 approval binding. |
| [Conformance Tests](CONFORMANCE_TESTS.md) | Automated test suite verifying schemas, isolation, and gateway rules. |
| [Migration Guide](MIGRATION_GUIDE.md) | Backward compatibility rules and migration paths for existing users. |
| [Implementation Report](IMPLEMENTATION_REPORT.md) | Final delivery audit, test evidence, and release acceptance. |
