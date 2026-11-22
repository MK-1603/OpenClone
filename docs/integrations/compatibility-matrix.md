# Multi-Host IDE & Agent Compatibility Matrix
**Platform Verification & Conformance Registry**  
**Specification:** v1.0.0 | **Authority:** Conformance Registry | **Date:** 2026-11-22

---

## 1. Supported AI IDE & Coding Agent Hosts

OpenClone provides native adapters for all major agent environments using the Model Context Protocol (MCP) and platform-native configuration files.

| Host Surface | Adapter Path | Protocol / Transport | Supported Features | Conformance Status | Last Verified |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **Google Antigravity** | [`adapters/antigravity/`](file:///d:/New%20folder/OpenClone/adapters/antigravity) | MCP stdio / Native Plugin | Full Tools, Workflows, Sidecar UI, Slop Audit | **VERIFIED** | 2026-11-22 |
| **Claude Code** | [`adapters/claude-code/`](file:///d:/New%20folder/OpenClone/adapters/claude-code) | MCP stdio (`.mcp.json`) | Full Tools, Slash Commands, Subagents | **VERIFIED** | 2026-11-22 |
| **Cursor** | [`adapters/cursor/`](file:///d:/New%20folder/OpenClone/adapters/cursor) | MCP stdio (`.cursor/mcp.json`)| Full Tools, `.cursorrules`, Taste Governance | **VERIFIED** | 2026-11-22 |
| **OpenAI Codex** | [`adapters/codex/`](file:///d:/New%20folder/OpenClone/adapters/codex) | MCP stdio (`mcp.json`) | Full Tools, CLI Agents, Execution DAG | **VERIFIED** | 2026-11-22 |
| **ChatGPT** | [`adapters/chatgpt/`](file:///d:/New%20folder/OpenClone/adapters/chatgpt) | Remote MCP / HTTPS SSE | Remote Tools, Knowledge Search, Concept Explainer | **VERIFIED** | 2026-11-22 |
| **Qwen Code** | Planned | MCP stdio | CLI Agent Workflows | `SPECIFIED` | 2026-11-22 |
| **Kiro / Kilo Code** | Planned | MCP stdio | Steering files, Project Context | `SPECIFIED` | 2026-11-22 |

---

## 2. Model Provider Compatibility

| Provider / Route | Connection Type | Tool Calling | Streaming | Vision | Context Window | Verified Quota Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **OpenAI** (GPT-4o, o1, o3) | Direct API / Gateway | Yes | Yes | Yes | 128k | Commercial / Tiered |
| **Anthropic** (Claude 3.5 Sonnet) | Direct API | Yes | Yes | Yes | 200k | Commercial / Tiered |
| **Google Gemini** (Gemini 1.5/2.0) | AI Studio / Vertex AI | Yes | Yes | Yes | 1M - 2M | Free Tier & PayGo |
| **xAI** (Grok 2) | Direct API | Yes | Yes | Yes | 128k | Commercial |
| **DeepSeek** (V3, R1) | Direct API | Yes | Yes | No | 64k | PayGo |
| **Alibaba Qwen** (Qwen 2.5) | Model Studio / DashScope | Yes | Yes | Yes | 128k | PayGo |
| **Local Ollama** (Llama 3, Qwen) | Loopback HTTP | Yes | Yes | Optional | VRAM-dependent| Zero-Cost / Offline |
| **Local vLLM** | Loopback HTTP | Yes | Yes | Optional | Configurable | Zero-Cost / Self-Hosted |
