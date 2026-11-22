# OpenClone — Provider, Model & Router Alternatives
**Version:** 1.0.0  
**Scope:** Model providers, external routing frameworks, and IDE host fallback strategies.

---

## 1. Model Provider Alternatives

| Provider / Model | Role | Key Strengths | Known Limitations | License / Privacy | Fallback Path |
|---|---|---|---|---|---|
| **Anthropic (Claude 3.5 / 3.7 Sonnet)** | `PRIMARY` | Nuanced reasoning, system design, architectural depth, low hallucination | Higher cost per million tokens; strict rate limits on Tier 1 | Commercial API; zero training on commercial data | OpenAI GPT-4o / o3-mini |
| **OpenAI (GPT-4o, o1, o3-mini)** | `FALLBACK` | High speed, extensive tool-calling ecosystem, strong coding synthesis | Occasional aesthetic slop in UI code; aggressive prompt caching | Commercial API; zero retention agreements available | Claude 3.5 Sonnet / DeepSeek |
| **Google Gemini (Gemini 1.5 Pro / Flash)** | `OPTIONAL` | Massive context window (2M tokens), multimodal processing, low cost | Can lose fine-grained instruction details across large contexts | Commercial API; Google Cloud enterprise terms | Anthropic Claude |
| **DeepSeek (DeepSeek-V3 / R1)** | `OPTIONAL` | Exceptional math and code reasoning; extremely low API cost; self-hostable | Variable API latency during peak hours; regional compliance considerations | Open Weights (MIT/DeepSeek) / Commercial API | Claude 3.5 Sonnet |
| **Ollama / Local Models (Llama 3.3, Qwen 2.5 Coder)** | `SPECIALIST` | 100% offline, zero data exfiltration, no API cost | High GPU hardware requirements; limited context window | Apache 2.0 / Open Weights | Commercial API Provider |

---

## 2. Evaluation of 8 Router Candidates

| Candidate Router | Upstream Repo | Architectural Fit | License | Maintenance / Security Risk | Recommendation |
|---|---|---|---|---|---|
| **LiteLLM** | `BerriAI/litellm` | High (100+ providers, standard OpenAI format) | MIT | Active, audited, strong community | **Recommended Production Router** |
| **Devansh-365/freellm** | `Devansh-365/freellm` | Low (Reverse-engineered free web endpoints) | Unclear | High risk of endpoint breakage, rate blocks, and TOS breach | `REJECTED` |
| **kaiser-data/free-llm-...** | `kaiser-data/free-llm-api...` | Low (Scraping proxy) | MIT | Fragile, security risk for enterprise tokens | `REJECTED` |
| **nabinkhadka/free-llm-api** | `nabinkhadka/free-llm-api` | Low (Reverse proxy) | GPL | High maintenance, TOS risk | `REJECTED` |
| **YeomanYe/free-llm-router** | `YeomanYe/free-llm-router` | Low (Experimental) | MIT | Stale commits, unverified reliability | `REJECTED` |
| **alienz-dev/llm-router** | `alienz-dev/llm-router` | Medium (Internal proxy) | Apache 2.0 | Low documentation, small ecosystem | `DEFERRED` |
| **MajidAsghariTabrizi/...** | `MajidAsghariTabrizi/...` | Low (Scraping wrapper) | MIT | Fragile upstream dependencies | `REJECTED` |
| **tashfeenahmed/freellmapi**| `tashfeenahmed/freellmapi` | Low (Experimental proxy) | MIT | High fragility | `REJECTED` |
| **Gmagl/omniroute** | `Gmagl/omniroute` | Medium (Multi-protocol proxy) | MIT | Maintained, but smaller than LiteLLM | `OPTIONAL_CANDIDATE` |

---

## 3. IDE Host Alternatives & Fallback Matrix

| IDE / Host Tool | Supported Instruction Files | Tool Interop Protocol | Context Loading Limits | Manual Fallback Workflow |
|---|---|---|---|---|
| **Google Antigravity** | `AGENTS.md`, `project.md`, `.antigravity/` | Native AGY Tools + Terminal Sandbox | Dynamic auto-compacting | Terminal CLI commands via PowerShell / bash |
| **Claude Code CLI** | `CLAUDE.md`, `AGENTS.md` | Model Context Protocol (`.mcp.json`) | 200k tokens | Direct CLI commands and bash prompts |
| **Cursor Composer** | `.cursorrules`, `.cursor/rules/`, `AGENTS.md` | MCP Server (`.cursor/mcp.json`) | Varies by model tier | File @-mentions and composer prompt chains |
| **OpenAI Codex / CLI** | `AGENTS.md`, `mcp.json` | JSON-RPC MCP Tools | 128k tokens | Standalone script execution |
| **ChatGPT Web UI** | Master Entry Prompt, `PROJECT.md` | Chat file attachment / Web upload | ~32k–128k tokens | Copy-paste generated markdown specification packages |
| **Zed / Windsurf** | Standard Markdown Rules | Native Language Servers + MCP | Standard context windows | Direct file editing and terminal integration |
