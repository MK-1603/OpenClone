# OpenClone Agent Client Protocol (ACP) Interoperability Guide
## Investigation, Specification, and Adapter Implementation for ACP Clients

**Version:** 1.0.0  
**Target:** Zed Editor, Agent Client Protocol Implementations, and Streaming Context Hosts  
**Canonical Product:** OpenClone 2.0

---

## 1. Investigation: ACP vs MCP

### What is ACP?
The **Agent Client Protocol (ACP)** is a protocol designed for bidirectional, streaming communication between an IDE/editor client and an external AI agent service. Unlike MCP (which is primarily designed for tool exposure, static resources, and prompt templates over JSON-RPC), ACP focuses on:

1. **Session & Thread Management:** Creating, resuming, and archiving agent conversation threads.
2. **Context Streaming:** Streaming active file buffers, diagnostics, and cursor selections from editor to agent.
3. **Turn-Based Delta Delivery:** Streaming partial model responses, thought blocks, and proposed edits directly into editor diff buffers.
4. **Interactive Confirmation:** Inline permission prompts for file writes and shell execution.

### Protocol Direction & Role
- **Client (Host Editor):** Zed, IDE, or terminal UI.
- **Server/Agent:** OpenClone ACP Adapter.
- In Zed and compatible editors, the editor acts as the **ACP Client**, initiating sessions and sending editor events. OpenClone acts as the **ACP Agent Server**, receiving user intents and streaming structured execution lifecycle events.

---

## 2. OpenClone ACP Adapter Architecture

OpenClone provides an in-process and stdio-compatible ACP Adapter (`src/openclone/integrations/acp.py`) that bridges ACP message schemas with the OpenClone Autonomous Engineering Execution Engine:

```text
+--------------------+                       +---------------------------+
|    Zed / Editor    |  --- ACP JSON-RPC --> | OpenClone ACP Adapter     |
|    (ACP Client)    |                       | (src.openclone.integrat..) |
+--------------------+                       +---------------------------+
          ^                                                |
          |                                                v
          |                             +--------------------------------+
          |                             |   Autonomous Execution Engine  |
          +------- Streaming Events --- |   - Intent Understanding       |
                   (Progress/Deltas)    |   - Plan Generation            |
                                        |   - Governed Task Execution    |
                                        |   - Verification Results       |
                                        +--------------------------------+
```

---

## 3. Supported ACP Message Schemas

### 3.1. `session/create`
Initializes an engineering session with project context.
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "session/create",
  "params": {
    "workspace_root": "/path/to/project",
    "capabilities": ["diff_stream", "tool_confirmation"]
  }
}
```

### 3.2. `session/prompt`
Submits an engineering prompt to OpenClone.
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "session/prompt",
  "params": {
    "session_id": "sess-uuid",
    "text": "Add rate limiter unit test for backend API",
    "mode": "Standard"
  }
}
```

### 3.3. Streaming Notifications (`session/update`)
OpenClone streams execution progress back to the editor:
- `stage_changed`: Transition between 12 lifecycle stages.
- `plan_ready`: Plan node breakdown with risk assessment.
- `task_executed`: Status of individual worker execution.
- `verification_complete`: Test results and compliance status.
- `delivery`: Final report and changed files summary.

---

## 4. Zed Configuration Example

To connect Zed to OpenClone via ACP or context server, update `~/.config/zed/settings.json`:

```json
{
  "context_servers": {
    "openclone": {
      "command": "oc",
      "args": ["mcp"],
      "enabled": true
    }
  },
  "assistant": {
    "version": "2",
    "default_model": {
      "provider": "openclone",
      "model": "autonomous"
    }
  }
}
```
Or run the automated setup command:
```bash
oc platforms connect zed
```
