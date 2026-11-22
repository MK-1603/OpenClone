# Universal Integration Architecture

## 1. Architectural Principles

OpenClone's Universal Integration Architecture is built upon five foundational tenets:

1. **One Canonical Implementation:** Core domain logic, state transitions, evidence verification, and anti-slop rules are implemented once in `src/openclone/integrations/` and shared across all hosts.
2. **Gateway-First Policy Enforcement:** Protocol adapters (MCP, HTTP REST, CLI) cannot bypass authentication, scoped authorization, rate limits, or human approval gates.
3. **Provider-Neutral Interoperability:** Model providers (Anthropic, OpenAI, Google) are decoupled from AI host tools (Claude Code, ChatGPT, Antigravity, Cursor).
4. **Least Privilege & Tenant Boundary:** Every capability specifies exact required scopes. Operations strictly enforce workspace/project isolation boundaries.
5. **Deterministic Auditability:** Every mutation and authorization decision generates an immutable audit event recorded in the tamper-evident ledger.

---

## 2. Layered Component Architecture

```
+-------------------------------------------------------------------+
|                     Multi-Host AI Surface                         |
|  ChatGPT Actions · Claude Desktop · Antigravity · Cursor · VS Code |
+-------------------------------------------------------------------+
                                  │
                                  ▼
+-------------------------------------------------------------------+
|                      Protocol Adapters Layer                      |
|  • MCP Server (stdio / SSE JSON-RPC 2.0)                          |
|  • HTTP / OpenAPI REST Dispatcher                                 |
|  • Local CLI Entry Point (openclone / aisdf)                      |
+-------------------------------------------------------------------+
                                  │
                                  ▼
+-------------------------------------------------------------------+
|               Integration Gateway & Policy Engine                 |
|  • OAuth 2.1 / OIDC Bearer Token & API Key Authentication         |
|  • Scoped Permission Authorization Check (e.g. tasks:write)       |
|  • Cross-Project / Tenant Boundary Validation                     |
|  • Human Cryptographic Approval Verification (SHA-256 Digest)     |
|  • Sensitive Credential & Secret Redaction Engine                 |
|  • Immutable Audit Event Logging                                  |
+-------------------------------------------------------------------+
                                  │
                                  ▼
+-------------------------------------------------------------------+
|                    Canonical Capability Layer                     |
|  • Project Discovery & Context (openclone_list_projects)          |
|  • 22-Phase Lifecycle Checklist (openclone_get_checklist)          |
|  • Evidence Attachment & Independent Verification (V0-V5)         |
|  • Defect & Quality Gate Evaluation                               |
|  • Scoped IDE Handoff Package Generation                          |
|  • Anti-AI-Slop Standards & Design Tokens (Taste Skill v2.6.0)     |
+-------------------------------------------------------------------+
```

---

## 3. Data Flow & Security Sequence

```
Host Client              Protocol Adapter            Integration Gateway          Canonical Core
     │                          │                             │                          │
     │── 1. Tool Call / REST ──>│                             │                          │
     │                          │── 2. Route with Token ─────>│                          │
     │                          │                             │── 3. Validate Token ────┐│
     │                          │                             │<── AuthContext Validated┘│
     │                          │                             │                          │
     │                          │                             │── 4. Verify Scopes ─────┐│
     │                          │                             │<── Scopes Authorized ───┘│
     │                          │                             │                          │
     │                          │                             │── 5. Check Approval Gate │
     │                          │                             │   (If Production Impact) │
     │                          │                             │                          │
     │                          │                             │── 6. Execute Capability ─>
     │                          │                             │<── Raw Result Returned ──│
     │                          │                             │                          │
     │                          │                             │── 7. Redact Secrets ────┐│
     │                          │                             │<── Clean Output ────────┘│
     │                          │                             │                          │
     │                          │<── 8. Formatted Response ───│                          │
     │<── 9. JSON-RPC / JSON ───│                             │                          │
```
