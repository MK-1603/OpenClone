# OpenClone Adapter Registry

This registry tracks the status and capability contracts for AI platforms, IDE coding agents, and application deployment providers. In accordance with OpenClone truthfulness invariants, unverified external integrations remain explicitly marked as `SPECIFIED` or `NOT_VERIFIED` until live conformance evidence is recorded.

---

## 1. AI Platform Adapters (Shared Tool Surface)

| Adapter ID | Platform | Transport / Protocol | Integration Model | Status |
|---|---|---|---|---|
| `adapter-chatgpt` | OpenAI ChatGPT | Custom Action / MCP | Shared tool schema envelope | `SPECIFIED` |
| `adapter-claude` | Anthropic Claude | Model Context Protocol (MCP) | OpenClone MCP Gateway | `SPECIFIED` |
| `adapter-codex` | OpenAI Codex / CLI | Tool Gateway / Stdio | Structured tool calls | `SPECIFIED` |
| `adapter-gemini` | Google Gemini | Function Calling / Tool API | Google Antigravity / API | `SPECIFIED` |

---

## 2. Coding Agent & IDE Adapters

| Adapter ID | Environment | Contract File | Support Level | Status |
|---|---|---|---|---|
| `adapter-antigravity` | Google Antigravity (AGY) | `adapters/antigravity.md` | Native skill & tool execution | `INTEGRATED` |
| `adapter-cursor` | Cursor IDE | `adapters/cursor.md` | `.cursorrules` + MCP server | `SPECIFIED` |
| `adapter-claudecode` | Claude Code CLI | `adapters/claude-code.md` | REPL Stop hooks & tool calls | `SPECIFIED` |
| `adapter-openhands` | OpenHands | `adapters/openhands.md` | Container runtime harness | `SPECIFIED` |

---

## 3. Application Deployment Provider Adapters

| Adapter ID | Provider | Target Workload | Preview Mechanism | Status |
|---|---|---|---|---|
| `deploy-cloudflare` | Cloudflare Pages / Workers | Static Web & Edge APIs | Automatic branch deployments | `SPECIFIED` |
| `deploy-vercel` | Vercel | Next.js / Serverless Frontend | Preview deployment aliases | `SPECIFIED` |
| `deploy-render` | Render | Web Services & Databases | Ephemeral PR environments | `SPECIFIED` |
| `deploy-railway` | Railway | Full-stack Containers | Dynamic branch environments | `SPECIFIED` |
| `deploy-flyio` | Fly.io | Global Container Machines | Staging machine instances | `SPECIFIED` |
| `deploy-local` | Docker / Local Preview | Localhost container test | Port-mapped preview container | `IMPLEMENTED` |

---

## 4. Conformance Standards
Every external adapter must conform to `schemas/tool-capability-profile.schema.json` and declare its authentication scopes, failure modes, and rate limits.
