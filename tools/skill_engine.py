#!/usr/bin/env python3
"""OpenClone Skill Engine CLI
Performs skill discovery, task classification, deterministic selection, and report generation.
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

from src.openclone.skills.engine import SkillRegistry, SkillSelector, SkillReportGenerator

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
    sel_parser.add_argument("--report", action="store_true", help="Output markdown selection report")

    # verify
    subparsers.add_parser("verify", help="Verify all registered skill manifests and paths")

    args = parser.parse_args()
    reg = SkillRegistry(root=ROOT)
    selector = SkillSelector(registry=reg)

    if args.command == "list":
        print(f"Registered OpenClone Skills ({len(reg.list_all())} total):")
        for s in reg.list_all():
            print(f" - [{s.id}] {s.name} (v{s.version}, prec={s.precedence}) -> {s.path}")

    elif args.command == "select":
        res = selector.select(args.task, environment=args.env)
        if args.report:
            print(SkillReportGenerator.generate_selection_report(args.task_id, res))
        else:
            print(f"Task: {args.task}")
            print(f"Selected ({res['total_selected']}):")
            for s in res["selected_skills"]:
                print(f"  * [{s.id}] {s.name} (prec={s.precedence})")
            print(f"Skipped ({res['total_skipped']}):")
            for sk in res["skipped_skills"]:
                print(f"  - [{sk['skill_id']}] {sk['reason']}")

    elif args.command == "verify":
        errors = []
        for s in reg.list_all():
            if s.path:
                target = ROOT / s.path
                if not target.exists():
                    errors.append(f"Skill '{s.id}' points to missing path: {s.path}")
        if errors:
            print(f"FAIL: {len(errors)} skill path errors found:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        else:
            print(f"PASS: All {len(reg.list_all())} registered skills have valid manifests and paths.")

if __name__ == "__main__":
    main()
