# Google Antigravity Adapter

# Google Antigravity Adapter

This adapter provides native Google Antigravity integration for OpenClone.

## Quick Install (Antigravity Plugin)
Install OpenClone directly into Antigravity with a single CLI command:

```bash
agy plugin install https://github.com/MK-1603/OpenClone
```

## Role in the 6-Phase Engineering Pipeline
In the OpenClone multi-AI workflow, Google Antigravity serves as the **Master Engineering Execution Engine**:
1. **Ingest Workspace:** The user opens the dedicated project folder extracted from the `.zip` specification package generated in Claude / ChatGPT.
2. **Execute Master Prompt:** The user pastes `BUILD_PROMPT.md` into Antigravity.
3. **Phased Engineering Execution:** Antigravity coordinates specialist agents through topological order:
   - **Scaffold:** Clean repository structure, configuration files, build scripts.
   - **Frontend UI:** Responsive components built with anti-slop tokens.
   - **Backend & APIs:** Type-safe endpoints, business validation, auth controllers.
   - **Database Connection:** Schemas, migrations, connection pools, and seed fixtures.
   - **AI / ML Layer (if applicable):** Dataset pipelines, model training/inference scripts, RAG connections.
4. **Testing & Security:** Executes 100% of test suites and enforces the 19-point SaaS security baseline.
5. **Deployment & Release:** Clears the release gate (`python aisdf.py gate`), containerizes the app, and publishes the production release.

## Packaging Options

- `workspace/`: copy `.agents/` into the root of the project opened in Antigravity. It provides an always-on AISDF rule and an on-demand `aisdf` skill.
- `plugin/`: versioned distributable plugin with `.antigravity-plugin/plugin.json`, skills, rules, and custom reviewer agent definitions.

Antigravity uses `.agents/skills/<skill-name>/SKILL.md` for workspace skills and `.agents/rules/*.md` for workspace rules. Plugin component directories remain at the plugin root. See the official [Rules](https://antigravity.google/docs/rules/), [Skills](https://antigravity.google/docs/skills), and [Build plugins](https://antigravity.google/docs/build-plugins/) documentation.

## Install workspace adapter

1. Copy the contents of `workspace/` into the target project root.
2. Open/reload the project in Antigravity.
3. Confirm the AISDF skill is discoverable; invoke `/aisdf` if manual invocation is supported by the installed version.
4. Ask the agent to explain the AISDF operating modes and show the files it read before making changes.

## Plugin

Run `agy plugin validate <path-to-plugin>` with a compatible Antigravity CLI before installing. This repository package has not run that host-specific command; plugin validation is therefore pending.
