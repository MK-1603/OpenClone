# Claude Code Adapter

This adapter provides a Claude Code skill and a `CLAUDE.md` bridge template.

# Claude Code Adapter

This adapter provides Claude Code skills, MCP server registration, and a `CLAUDE.md` bridge template.

## Quick Install (MCP Plugin)
Install OpenClone without cloning the repository and register it as an MCP plugin in Claude Code:

```bash
pip install git+https://github.com/MK-1603/OpenClone.git
claude mcp add openclone python -m openclone.mcp.server
```

## Role in the 6-Phase Engineering Pipeline
In the OpenClone multi-AI workflow, Claude serves as the **Lead Architect & Specification Bundler**:
1. **Phase 1 (PIA Sets A, B, C, D):** Interacts with the user to analyze the idea, detect edge cases/gaps, design solutions, and produce master specifications (`PROJECT.md`, `Features-List.md`, `Solution-Blueprint.md`, etc.).
2. **Phase 2 (Branding & Metadata):** Validates anti-slop design tokens, environment configurations, and authors the master `BUILD_PROMPT.md`.
3. **Phase 3 (Bundling as .zip):** Packages the entire blueprint, design assets, and prompts into a downloadable `.zip` archive to be extracted into a dedicated project folder for Google Antigravity.

## Workspace Template Install
1. Review the target repository's existing `CLAUDE.md`, `AGENTS.md`, and `.claude/` files.
2. Copy/merge `.claude/skills/aisdf/SKILL.md` into the target repository's `.claude/skills/aisdf/SKILL.md`.
3. Use `CLAUDE.template.md` as a starting point for a root `CLAUDE.md`; it references the shared `AGENTS.md` contract.
4. Keep the target project's own `PROJECT.md` and `AGENTS.md` as canonical project/agent files.
5. Verify the skill and project instructions are visible in the installed Claude Code version.

Do not overwrite existing instructions. This package is an adapter template, not live certification.
