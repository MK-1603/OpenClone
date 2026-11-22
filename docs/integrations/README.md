# Integrations Architecture & Subsystem Index

## Overview

OpenClone provides an adapter-first integration architecture designed to connect the deterministic OpenClone control plane with AI coding IDEs, external model routers, and security analysis toolchains.

Integration components adhere to three fundamental constraints:
1. **Host-Neutral Core**: Core governance, task validation, and security policies never import vendor-specific SDKs.
2. **Deterministic Mediation**: External model calls and scanner invocations must pass through strictly typed schemas, least-privilege permission gates, and execution sandboxes.
3. **Evidence Integrity**: All tool runs produce immutable, hash-verified execution evidence with credentials automatically redacted.

---

## Directory Contents

| Document | Purpose | Authority |
| :--- | :--- | :--- |
| [`llm-router-comparison.md`](file:///d:/New%20folder/OpenClone/docs/integrations/llm-router-comparison.md) | Technical comparison of 8 external open-source LLM routers and gateway architectures | Evaluative Architecture Record |
| [`security-toolchain.md`](file:///d:/New%20folder/OpenClone/docs/integrations/security-toolchain.md) | Classification, execution boundaries, and integration tiers for 12 security engines | Security Standard |
| [`compatibility-matrix.md`](file:///d:/New%20folder/OpenClone/docs/integrations/compatibility-matrix.md) | Multi-host IDE and model provider conformance verification matrix | Conformance Registry |
| [`adding-a-router.md`](file:///d:/New%20folder/OpenClone/docs/integrations/adding-a-router.md) | Contributor specification for implementing a new LLM router or gateway adapter | Implementation Guide |
| [`adding-a-security-tool.md`](file:///d:/New%20folder/OpenClone/docs/integrations/adding-a-security-tool.md) | Contributor specification for adding a static or dynamic scanner adapter | Implementation Guide |

---

## Target Host Surfaces

OpenClone maintains first-class native adapters in [`adapters/`](file:///d:/New%20folder/OpenClone/adapters):
- **Antigravity**: Native IDE plugin with contextual sidecar tools.
- **Claude Code**: Native `.mcp.json` toolchain registration.
- **Cursor**: Native `.cursor/mcp.json` integration with anti-slop rules.
- **Codex**: Native `mcp.json` developer agent configuration.
- **ChatGPT**: Remote HTTPS SSE / Model Context Protocol bridge.
