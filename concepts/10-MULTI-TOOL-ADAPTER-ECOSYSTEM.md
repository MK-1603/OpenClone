# Concept 10: Multi-Tool Adapter Ecosystem (Primary Specification)

## 1. Core Principle
OpenClone is provider-neutral and IDE-agnostic. Work is orchestrated using standardized work-unit contracts (`schemas/work-unit.schema.json`) that bridge to external tools like Claude Code, Cursor, Antigravity, OpenHands, and OpenCode.

## 2. Invariants
1. **Tool Independence:** The core control plane operates purely on local files, state databases, and standard CLI calls.
2. **Adapter Contract:** Adapters translate OpenClone lifecycle events into native tool configurations without violating the root permission rules.

---

## 4. Architectural Alternatives & Operational Trade-Offs

## 1. Alternate Paradigm: Direct MCP Client-Server Streaming Protocol
As the industry converges around the Model Context Protocol (MCP), using file-based adapters can be supplemented by live protocol connections. The alternate model provides a **Native OpenClone MCP Server**.

## 2. How the Alternate Operates
1. **Embedded MCP Server:** OpenClone runs as an MCP server (`openclone serve-mcp`) exposing standard MCP tools (`plan_task`, `request_approval`, `record_evidence`, `get_rules`).
2. **Direct Agent Integration:** Tools like Claude Desktop, Cursor, Antigravity, and Zed connect directly to the OpenClone server over JSON-RPC.
3. **Real-Time Interactive Gating:** The agent receives immediate structured feedback and errors directly inside the active tool's interface without exiting to the terminal.

## 3. Trade-Off Analysis
* **Strengths:** Frictionless in-editor integration with any MCP-compatible coding tool.
* **Risks:** Requires running a background server process during development.
