# Google Stitch Skills Integration for OpenClone

This package integrates Google's **Stitch Skills** ecosystem (`https://github.com/google-labs-code/stitch-skills`) directly into OpenClone as a first-class external skill provider.

---

## Architecture Overview

```text
OpenClone Framework
      │
      ├── UI/UX Engineering Engine (`src/openclone/skills/ui_ux_engineering.py`)
      │        │
      │        ▼
      ├── Stitch Integration Adapter (`integrations/stitch/adapter/`)
      │        ├── discovery.py       (Skill discovery & cataloging)
      │        ├── loader.py          (Upstream markdown & resource loader)
      │        ├── compatibility.py   (Dual-identifier & tool mapping)
      │        ├── dependencies.py    (Environment & tool prereqs)
      │        ├── mcp_client.py      (Google Stitch MCP Client & health checks)
      │        ├── orchestration.py   (UI/UX to Stitch pipeline coordinator)
      │        └── registry.py        (Registration into OpenClone SkillRegistry)
      │
      └── Upstream Skills Tree (`integrations/stitch/`)
               ├── design/skills/     (6 Design skills)
               ├── build/skills/      (5 Code generation skills)
               └── utilities/skills/  (5 Supporting & spec skills)
```

---

## Prerequisites & Setup

### 1. Google Stitch MCP Server

Stitch skills require the Stitch MCP server for live screen generation, retrieval, and updates:
- Setup Guide: https://stitch.withgoogle.com/docs/mcp/setup/
- Environment Variable: Set `STITCH_API_KEY` (or `GEMINI_API_KEY`):
  ```bash
  # PowerShell
  $env:STITCH_API_KEY = "your-api-key"
  ```
- Endpoint: Defaults to `https://stitch.googleapis.com` (configurable via `STITCH_MCP_ENDPOINT`).

> **Note on Offline / Mock Mode:** If no API key is configured, the integration gracefully reports `UNAVAILABLE` or operates in local token/design-system synthesis mode without pretending that remote generation succeeded.

---

## Supported Commands

In the OpenClone interactive shell (`oc`):

| Command | Action |
|---|---|
| `/stitch status` | Inspect Stitch MCP connection status and API key configuration. |
| `/stitch skills` | List all 16 registered Stitch skills and their availability. |
| `/stitch tools` | List Stitch MCP tools exposed by the server. |
| `/stitch connect` | Verify handshake with the Google Stitch MCP endpoint. |
| `/stitch update` | Check upstream repository for new commits or skill updates. |

---

## Orchestrated UI/UX Pipeline

Stitch skills seamlessly orchestrate with OpenClone's UI/UX Engineering suite:

1. **Intake & Archetype Analysis:** OpenClone evaluates project requirements (e.g., Financial Dashboard, SaaS Admin, Developer Tool).
2. **Anti-Slop Audit:** Identifies and flags generic UI patterns (identical 4-card grids, unreadable glassmorphism).
3. **Design Spec Synthesis:** Generates or refines a structured `DESIGN.md` via `stitch-taste-design` or `stitch-design-md`.
4. **Stitch Generation / Editing:** Invokes `stitch::generate-design` or `stitch::manage-design-system` through the MCP client.
5. **Component Conversion:** Converts screens into modular React or React Native components using `stitch::react-components` or `stitch::react-native`.
6. **Visual QA:** Validates 10 visual quality dimensions (typography, layout density, contrast, responsiveness) across desktop, tablet, and mobile breakpoints.

---

## Upstream Attribution & License

- Source: `https://github.com/google-labs-code/stitch-skills`
- License: Apache License 2.0 (see [LICENSE](LICENSE))
- Canonical Commit SHA: `75f4696f162000fb69fca6a31489b5b21d47a506`
