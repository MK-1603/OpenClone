# OpenClone Quick Start Guide

OpenClone supports two distinct operating modes:
1. **The Portable Project Workflow (Zero-Install, No Clone Required):** For developers and teams building software applications with AI assistance.
2. **The Local Control Plane & Maintainer Environment (Optional):** For teams running the self-hosted deterministic SQLite ledger, MCP server, or developing OpenClone itself.

---

# Part 1: The Portable Project Workflow (Recommended)
> **You do NOT need to clone, install, or run OpenClone to build your applications.**  
> OpenClone is an open engineering standard and project-generation methodology. The generated project package lives in your own application repository and is executed by your preferred AI coding IDE.

### Step 1: Prepare your `PROJECT.md`
Create a `PROJECT.md` file in your project directory (or use our [starter template](../project/PROJECT.md.template)). Describe:
- The problem your application solves and target users.
- Core features and workflows.
- Preferred technology stack (languages, frameworks, databases).
- Any known constraints or security requirements.

### Step 2: Open ChatGPT or Claude
1. Open a new chat in [ChatGPT](https://chatgpt.com) or [Claude](https://claude.ai).
2. Copy and paste the [OpenClone Portable Project Intelligence Master Prompt](../framework/prompts/PORTABLE-PROJECT-INTELLIGENCE-MASTER-PROMPT.md).
3. Paste or attach your `PROJECT.md` file.

### Step 3: Clarify and Approve
- The AI assistant analyzes your specification, detects gaps, checks for feasibility, and asks 3–5 targeted clarification questions.
- Answer the questions and confirm key decisions (authentication method, database type, hosting target).

### Step 4: Generate Your Portable Project Package
The assistant generates 6 self-contained markdown documents. Save them directly into your project root:
- `PROJECT.md` — Normalized specification with stable requirement IDs (`FR-001`, `NFR-001`).
- `BUILD_PROMPT.md` — Master prompt provided to your AI coding IDE.
- `AGENT_INSTRUCTIONS.md` — Coding standards, least-privilege rules, and verification requirements.
- `IMPLEMENTATION_PLAN.md` — Milestone roadmap with dependency-ordered tasks.
- `SECURITY_PLAN.md` — Threat model, secret handling, and static scan baselines.
- `ACCEPTANCE_MATRIX.md` — Requirements mapped to test cases and verification commands.

### Step 5: Build in Your AI Coding IDE
1. Open your project folder in your chosen AI coding IDE:
   - **Google Antigravity**
   - **Claude Code** (`claude` in your project folder)
   - **Cursor**
   - **OpenAI Codex**
2. Paste the contents of `BUILD_PROMPT.md` into the IDE agent chat.
3. The IDE agent:
   - Inspects your real codebase and Git repository.
   - Builds features in small, testable vertical slices (M1 → M2 → M3...).
   - Runs automated tests after every modification.
   - Updates `PROGRESS.md` and `HANDOFF.md` to preserve context.
4. When finished, inspect the final diff and review verification evidence in `ACCEPTANCE_MATRIX.md`.

---

# Part 2: Local Control Plane & Maintainer Environment (Optional)
> Use this section only if you want to run OpenClone's deterministic local control plane (`openclone.py`), launch the shared MCP service, or contribute to OpenClone development.

### Requirements
- Python 3.10+
- Git
- Zero mandatory external pip packages for core runtime.

### 1. Clone and Validate OpenClone
```bash
# Clone the OpenClone repository
git clone https://github.com/MK-1603/OpenClone.git
cd OpenClone

# Run structural validation and tests
python tools/validate_repository.py
python -m unittest discover -s tests -v
node skills/taste-skill/tests/test-governance.mjs
```

### 2. Launch the Shared MCP Server
```bash
# Start OpenClone MCP server (JSON-RPC 2.0 stdio)
python openclone.py mcp
```

### 3. Initialize a Governed Workspace
```bash
# Initialize a governed project with a cryptographic SQLite ledger
python openclone.py init --project ../my-app --name "My App" --owner "Lead Architect"
```

### 4. Human Approval & Release Gates
```bash
# Approve a task with SHA-256 digest binding
python openclone.py approve --project ../my-app --task-id TASK-001 --approver "Lead Architect"

# Transition to READY (verifies approval hash & dependencies)
python openclone.py transition --project ../my-app --task-id TASK-001 --to READY

# Verify release gate before deployment
python openclone.py gate --project ../my-app
```
