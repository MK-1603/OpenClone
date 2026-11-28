#!/usr/bin/env python3
"""OpenClone Engineering Lifecycle & Independent Verification CLI.

Usage:
    python tools/checklist_engine.py generate [--project-id ID] [--type TYPE] [--features FEATS]
    python tools/checklist_engine.py list [--phase PHASE] [--status STATUS]
    python tools/checklist_engine.py status
    python tools/checklist_engine.py transition --item-id ID --status STATUS [--waiver REASON]
    python tools/checklist_engine.py attach-evidence --item-id ID --type TYPE --ref REF --desc DESC
    python tools/checklist_engine.py verify --item-id ID
    python tools/checklist_engine.py gate --phase PHASE
    python tools/checklist_engine.py handoff --task-id ID
    python tools/checklist_engine.py report [--output PATH]
"""
import argparse
import json
import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.openclone.lifecycle.engine import LifecycleEngine
from src.openclone.lifecycle.schema import ProjectType, ItemStatus, Priority

STATE_FILE = ROOT / ".openclone" / "lifecycle_checklist.json"


def load_engine() -> LifecycleEngine:
    engine = LifecycleEngine(project_id="openclone-default", repo_root=ROOT)
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            engine.project_id = data.get("project_id", "openclone-default")
            engine.project_type = ProjectType(data.get("project_type", "WEB_SAAS"))
            engine.features = data.get("features", [])
            engine.generate_checklist(
                project_type=engine.project_type,
                features=engine.features,
            )
            # Restore item statuses and evidence
            for item_data in data.get("items", []):
                item_id = item_data.get("id")
                if item_id in engine.items:
                    it = engine.items[item_id]
                    it.status = ItemStatus(item_data.get("status", "NOT_STARTED"))
                    it.waiver_reason = item_data.get("waiver_reason")
                    it.completed_at = item_data.get("completed_at")
                    it.verified_at = item_data.get("verified_at")
                    for ev in item_data.get("evidence_refs", []):
                        engine.attach_evidence(
                            item_id=item_id,
                            evidence_type=ev.get("evidence_type", "code_diff"),
                            ref=ev.get("ref", ""),
                            description=ev.get("description", ""),
                            produced_by=ev.get("produced_by", "user"),
                        )
        except Exception as e:
            print(f"Warning: Failed to load previous state: {e}", file=sys.stderr)
    return engine


def save_engine(engine: LifecycleEngine):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "project_id": engine.project_id,
        "project_type": engine.project_type.value,
        "features": engine.features,
        "items": [it.to_dict() for it in engine.items.values()],
    }
    STATE_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="OpenClone Lifecycle & Verification Engine")
    subparsers = parser.add_subparsers(dest="command")

    # generate
    gen_p = subparsers.add_parser("generate", help="Generate project checklist")
    gen_p.add_argument("--project-id", default="openclone-project")
    gen_p.add_argument("--type", default="WEB_SAAS", choices=[pt.value for pt in ProjectType])
    gen_p.add_argument("--features", default="")

    # list
    list_p = subparsers.add_parser("list", help="List checklist items")
    list_p.add_argument("--phase", default=None)
    list_p.add_argument("--status", default=None)

    # status
    subparsers.add_parser("status", help="Calculate verified engineering progress")

    # transition
    trans_p = subparsers.add_parser("transition", help="Transition item state")
    trans_p.add_argument("--item-id", required=True)
    trans_p.add_argument("--status", required=True, choices=[s.value for s in ItemStatus])
    trans_p.add_argument("--waiver", default=None)

    # attach-evidence
    ev_p = subparsers.add_parser("attach-evidence", help="Attach evidence to an item")
    ev_p.add_argument("--item-id", required=True)
    ev_p.add_argument("--type", default="code_diff")
    ev_p.add_argument("--ref", required=True)
    ev_p.add_argument("--desc", default="Implementation artifact")

    # verify
    ver_p = subparsers.add_parser("verify", help="Run independent verification")
    ver_p.add_argument("--item-id", required=True)

    # gate
    gate_p = subparsers.add_parser("gate", help="Evaluate phase quality gate")
    gate_p.add_argument("--phase", required=True)

    # handoff
    hand_p = subparsers.add_parser("handoff", help="Generate AI IDE handoff package")
    hand_p.add_argument("--task-id", required=True)

    # report
    rep_p = subparsers.add_parser("report", help="Export markdown report")
    rep_p.add_argument("--output", default=None)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    engine = load_engine()

    if args.command == "generate":
        feats = [f.strip() for f in args.features.split(",") if f.strip()]
        engine.project_id = args.project_id
        engine.generate_checklist(
            project_type=ProjectType(args.type),
            features=feats,
        )
        save_engine(engine)
        progress = engine.calculate_progress()
        print(f"Generated {len(engine.items)} checklist items for project '{args.project_id}' ({args.type}).")
        print(f"Applicable tasks: {progress['applicable_tasks']} | Not applicable: {progress['not_applicable_tasks']}")

    elif args.command == "list":
        for it in engine.items.values():
            if it.type.value == "PHASE":
                continue
            if args.phase and it.phase_id != args.phase:
                continue
            if args.status and it.status.value != args.status:
                continue
            print(f"[{it.status.value}] {it.id} ({it.priority.value}): {it.title}")

    elif args.command == "status":
        p = engine.calculate_progress()
        print("=== OpenClone Engineering Lifecycle Status ===")
        print(f"Project ID:             {engine.project_id} ({engine.project_type.value})")
        print(f"Total Tasks:            {p['total_tasks']}")
        print(f"Applicable Tasks:       {p['applicable_tasks']}")
        print(f"Planning Coverage:      {p['planning_coverage_pct']}%")
        print(f"Implementation Progress:{p['implementation_progress_pct']}% ({p['implemented_tasks']} implemented)")
        print(f"Verified Progress:      {p['verified_progress_pct']}% ({p['verified_tasks']} verified)")
        print(f"Waived with Approval:   {p['waived_tasks']}")
        print(f"Not Applicable:         {p['not_applicable_tasks']}")

    elif args.command == "attach-evidence":
        ev = engine.attach_evidence(
            item_id=args.item_id,
            evidence_type=args.type,
            ref=args.ref,
            description=args.desc,
        )
        save_engine(engine)
        print(f"Attached evidence '{ev.id}' to '{args.item_id}'. Status: {engine.items[args.item_id].status.value}")

    elif args.command == "transition":
        try:
            it = engine.transition_item(
                item_id=args.item_id,
                target_status=ItemStatus(args.status),
                waiver_reason=args.waiver,
            )
            save_engine(engine)
            print(f"Transitioned '{args.item_id}' to {it.status.value}.")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "verify":
        outcome, msg = engine.run_independent_verification(item_id=args.item_id)
        save_engine(engine)
        print(f"Verification outcome for '{args.item_id}': [{outcome.value}] {msg}")

    elif args.command == "gate":
        gate = engine.evaluate_quality_gate(phase_id=args.phase)
        print(f"=== Quality Gate: {gate.phase_name} ({gate.phase_id}) ===")
        print(f"Status: {gate.status}")
        if gate.blockers:
            print(f"Blockers ({len(gate.blockers)}):")
            for b in gate.blockers:
                print(f"  - [X] {b}")
        else:
            print("  ✓ Gate PASSED: All mandatory tasks verified and defect-free.")

    elif args.command == "handoff":
        pkg = engine.generate_ide_handoff_package(task_id=args.task_id)
        print(pkg)

    elif args.command == "report":
        p = engine.calculate_progress()
        lines = [
            f"# OpenClone Project Verification Report",
            f"**Project:** `{engine.project_id}` | **Type:** `{engine.project_type.value}`",
            f"**Implementation:** {p['implementation_progress_pct']}% | **Verified:** {p['verified_progress_pct']}%",
            "",
            "## Quality Gate Summary",
        ]
        for phase_id in engine.gates:
            gate = engine.evaluate_quality_gate(phase_id)
            lines.append(f"- **{gate.phase_name}:** `{gate.status}` ({len(gate.blockers)} blockers)")

        report_content = "\n".join(lines) + "\n"
        if args.output:
            Path(args.output).write_text(report_content, encoding="utf-8")
            print(f"Report written to {args.output}")
        else:
            print(report_content)


if __name__ == "__main__":
    main()
