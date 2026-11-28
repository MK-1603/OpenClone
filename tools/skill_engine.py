#!/usr/bin/env python3
"""OpenClone Skill Engine CLI
Performs skill discovery, task classification, deterministic selection, loading, and report generation.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from src.openclone.skills.engine import (
    SkillRegistry,
    SkillSelector,
    SkillReportGenerator,
    ProjectArchetypeClassifier,
    ApplicationStateManager,
)


def main():
    parser = argparse.ArgumentParser(description="OpenClone Skill Engine CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    subparsers.add_parser("list", help="List all registered skills")

    # select
    sel_parser = subparsers.add_parser("select", help="Select skills for a task")
    sel_parser.add_argument("--task", required=True, help="Task description or prompt")
    sel_parser.add_argument("--task-id", default="TASK-001", help="Task identifier")
    sel_parser.add_argument("--env", default="all", help="Target IDE environment (antigravity, claude-code, cursor, codex)")
    sel_parser.add_argument("--archetype", default=None, help="Explicit project archetype override")
    sel_parser.add_argument("--discipline", default=None, help="Explicit discipline override")
    sel_parser.add_argument("--report", action="store_true", help="Output markdown selection report")

    # verify
    subparsers.add_parser("verify", help="Verify all registered skill manifests and paths")

    # load
    load_parser = subparsers.add_parser("load", help="Load and parse a skill definition from disk")
    load_parser.add_argument("--skill-id", required=True, help="Skill ID to load")

    # archetypes
    arch_parser = subparsers.add_parser("archetypes", help="Classify text into archetypes and application states")
    arch_parser.add_argument("--task", required=True, help="Task or project description")

    args = parser.parse_args()
    reg = SkillRegistry(root=ROOT)
    selector = SkillSelector(registry=reg)

    if args.command == "list":
        print(f"Registered OpenClone Skills ({len(reg.list_all())} total):")
        for s in reg.list_all():
            resolved = reg.resolve_path(s.id)
            status_flag = "VALID" if resolved else "PATH_ERROR"
            print(f" - [{s.id}] {s.name} (v{s.version}, prec={s.precedence}, mat={s.maturity}) [{status_flag}] -> {s.path}")

    elif args.command == "select":
        res = selector.select(args.task, environment=args.env, archetype=args.archetype, discipline=args.discipline)
        if args.report:
            print(SkillReportGenerator.generate_selection_report(args.task_id, res))
        else:
            print(f"Task: {args.task}")
            print(f"Archetypes: {', '.join(res.get('archetypes', []))}")
            print(f"Selected ({res['total_selected']}):")
            for s in res["selected_skills"]:
                print(f"  * [{s.id}] {s.name} (prec={s.precedence}, cat={s.category}, mat={s.maturity})")
            if res.get("dependencies_resolved"):
                print("Dependencies Resolved:")
                for dep in res["dependencies_resolved"]:
                    print(f"  + {dep['dependent_skill']} -> {dep['resolved_skill']} ({dep['reason']})")
            print(f"Skipped ({res['total_skipped']}):")
            for sk in res["skipped_skills"]:
                print(f"  - [{sk['skill_id']}] {sk['reason']}")

    elif args.command == "verify":
        errors = reg.validate_all()
        if errors:
            print(f"FAIL: {len(errors)} skill path errors found:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        else:
            print(f"PASS: All {len(reg.list_all())} registered skills have valid manifests and paths on disk.")

    elif args.command == "load":
        try:
            loaded = reg.load(args.skill_id)
            print(f"SUCCESS: Loaded skill '{loaded.skill_id}' from {loaded.resolved_path}")
            print(f"Maturity: {loaded.maturity}")
            print(f"Metadata keys: {list(loaded.metadata.keys())}")
            print(f"Content preview (first 200 chars):\n{loaded.body[:200]}...")
        except Exception as e:
            print(f"ERROR: Failed to load skill '{args.skill_id}': {e}")
            sys.exit(1)

    elif args.command == "archetypes":
        matched = ProjectArchetypeClassifier.classify(args.task)
        print(f"Task: {args.task}")
        print(f"Identified Archetypes: {matched}")
        states = ApplicationStateManager.get_recommended_states(matched[0] if matched else "web_application", feature=args.task)
        print(f"Mandatory Application States ({len(states)}): {states}")


if __name__ == "__main__":
    main()
