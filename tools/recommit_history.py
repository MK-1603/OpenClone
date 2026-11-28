import subprocess
import sys
import os

os.chdir(r"d:\New folder\OpenClone")

def run(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if p.returncode != 0:
        print(f"FAILED: {cmd}")
        print("STDOUT:", p.stdout)
        print("STDERR:", p.stderr)
        sys.exit(1)
    return p.stdout.strip()

commits = [
    (
        [
            ".gitignore", ".github", ".agents", ".claude-plugin", ".env.example",
            "pyproject.toml", "requirements-dev.txt", "plugin.json",
            "openclone.manifest.json", "cliff.toml", "tools"
        ],
        "chore(scaffold): initialize enterprise repository scaffolding, build config, and manifests"
    ),
    (
        [
            "global", "AGENT.md", "AGENTS.md", "CONTRIBUTING.md", "GOVERNANCE.md",
            "CODE_OF_CONDUCT.md", "SECURITY.md", "SUPPORT.md", "LICENSE", "NOTICE",
            "VERSION", "PROJECT.md", "PROGRESS.md", "HANDOFF.md", "standards", "rules"
        ],
        "docs(standards): establish architectural governance, agent directives, and contributing standards"
    ),
    (
        [
            "framework/domains", "framework/agents", "agents", "framework/registries",
            "framework/engines", "reference", "runtime", "adapters", "modules",
            "assessments", "archive", "packaging", "scripts", "security", "openclone"
        ],
        "feat(framework): define 12-domain engineering taxonomy, specialist agents, and registries"
    ),
    (
        [
            "framework/schemas"
        ],
        "feat(schemas): establish deterministic JSON schemas for knowledge, memory, and blueprints"
    ),
    (
        [
            "src/openclone/core", "src/openclone/workflow", "src/openclone/security",
            "src/openclone/planning", "src/openclone/__init__.py"
        ],
        "feat(core): implement core orchestration engine, security boundaries, and workflow DAG"
    ),
    (
        [
            "src/openclone/intelligence", "src/openclone/reverse_engineering",
            "src/openclone/workforce", "skills/universal-project-intelligence",
            "skills/openclone-engineering", "plugins"
        ],
        "feat(intelligence): implement Phase 0 Project Intelligence Architect and universal ingestion"
    ),
    (
        [
            "src/openclone/engineering", "framework/engineering-intelligence",
            "framework/technology-intelligence"
        ],
        "feat(engineering): build universal engineering intelligence engine with 155 disciplines"
    ),
    (
        [
            "src/openclone/frontend", "src/openclone/system_design",
            "skills/design-system-engineering", "skills/frontend-engineering",
            "skills/responsive-engineering", "skills/taste-skill"
        ],
        "feat(design): implement design intelligence, typography, and responsive frontend systems"
    ),
    (
        [
            "src/openclone/branding", "src/openclone/identity"
        ],
        "feat(branding): implement Project Identity & Asset Generation System (PIAGS)"
    ),
    (
        [
            "src/openclone/blueprint", "blueprints"
        ],
        "feat(blueprints): introduce universal product blueprint generators and canonical blueprints"
    ),
    (
        [
            "src/openclone/devops", "src/openclone/connectors"
        ],
        "feat(devops): implement universal cloud, infrastructure, and deployment intelligence"
    ),
    (
        [
            "src/openclone/autonomous", "src/openclone/quality"
        ],
        "feat(autonomous): implement autonomous self-evolution, mutation, and mathematical quality gates"
    ),
    (
        [
            "src/openclone/integrations", "integrations", "extensions"
        ],
        "feat(integrations): build multi-IDE gateway adapter and native VS Code extension engine"
    ),
    (
        [
            "src/openclone/memory", "memory"
        ],
        "feat(memory): implement persistent episodic memory vault and immutable audit ledger"
    ),
    (
        [
            "assets"
        ],
        "assets(branding): integrate master vector logos, multi-dpi app icons, and social previews"
    ),
    (
        [
            "tests", "examples"
        ],
        "test(suite): establish 727 comprehensive regression, unit, and end-to-end test suites"
    ),
]

for idx, (paths, msg) in enumerate(commits, 1):
    existing = [p for p in paths if os.path.exists(p)]
    if existing:
        run(f"git add {' '.join(existing)}")
        status = run("git status --porcelain")
        staged = [line for line in status.splitlines() if line and line[0] in "MADRC"]
        if staged:
            run(f'git commit -m "{msg}"')
            print(f"[{idx}/{len(commits)+1}] Committed: {msg}")

# Final commit for remaining documentation and release artifacts
run("git add .")
status = run("git status --porcelain")
staged = [line for line in status.splitlines() if line and line[0] in "MADRC"]
if staged:
    final_msg = "docs(release): release OpenClone v2.0.0 documentation, architecture guides, and release notes"
    run(f'git commit -m "{final_msg}"')
    print(f"[{len(commits)+1}/{len(commits)+1}] Committed: {final_msg}")

print("All commits completed successfully!")
