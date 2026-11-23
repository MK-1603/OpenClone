"""OpenClone Universal Project Intelligence CLI."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.openclone.intelligence.blueprints import BlueprintManager
from src.openclone.intelligence.classifier import ProjectClassifier
from src.openclone.intelligence.router import ProjectRouter
from src.openclone.intelligence.taxonomy import TaxonomyRegistry


def main():
    parser = argparse.ArgumentParser(
        prog="openclone intelligence",
        description="OpenClone Universal AI Engineering Intelligence: multi-label classification, routing, and blueprints.",
    )
    sub = parser.add_subparsers(dest="subcommand", help="Intelligence subcommand")

    # Status / Taxonomy
    p_status = sub.add_parser("status", help="Display project taxonomy and blueprint inventory")
    p_status.add_argument("--json", action="store_true", help="Emit raw JSON")

    # Classify
    p_cls = sub.add_parser("classify", help="Classify natural language requirements or codebase")
    p_cls.add_argument("text", nargs="?", default="", help="Natural language description or requirements")
    p_cls.add_argument("--repo", type=str, default="", help="Path to repository to scan")
    p_cls.add_argument("--name", type=str, default="project", help="Project name")
    p_cls.add_argument("--json", action="store_true", help="Emit raw JSON")

    # Route
    p_route = sub.add_parser("route", help="Compute deterministic domain, capability, and workforce routing")
    p_route.add_argument("text", nargs="?", default="", help="Natural language requirements")
    p_route.add_argument("--repo", type=str, default="", help="Path to repository to scan")
    p_route.add_argument("--name", type=str, default="project", help="Project name")
    p_route.add_argument("--json", action="store_true", help="Emit raw JSON")

    # Blueprint
    p_bp = sub.add_parser("blueprint", help="View or search project family blueprints")
    p_bp.add_argument("blueprint_id", nargs="?", default="", help="Blueprint ID (e.g. 01-MINI-WEBSITE, 10-LINUX-OS)")
    p_bp.add_argument("--list", action="store_true", help="List all 14 project family blueprints")

    args = parser.parse_args()

    tax = TaxonomyRegistry()
    bp_mgr = BlueprintManager()
    classifier = ProjectClassifier(tax)
    router = ProjectRouter(tax)

    if args.subcommand in ("status", None):
        res = {
            "version": tax.version,
            "families_count": len(tax.families),
            "families": tax.list_families(),
            "complexity_levels": tax.complexity_levels,
            "delivery_targets": tax.delivery_targets,
            "blueprints_count": len(bp_mgr.list_blueprints()),
        }
        if getattr(args, "json", False):
            print(json.dumps(res, indent=2))
        else:
            print(f"OpenClone Universal Project Intelligence v{tax.version}")
            print(f"Supported Families: {len(tax.families)} | Blueprints: {len(bp_mgr.list_blueprints())}")
            print("\nProject Families:")
            for f in tax.list_families():
                print(f"  - {f['id']} ({f['name']}): {f['type_count']} types")
            print(f"\nComplexity Levels: {', '.join(tax.complexity_levels)}")
            print(f"Delivery Targets: {', '.join(tax.delivery_targets)}")

    elif args.subcommand == "classify":
        if args.repo:
            profile = classifier.classify_repository(Path(args.repo), project_name=args.name)
        elif args.text:
            profile = classifier.classify_text(args.text, project_name=args.name)
        else:
            print("Error: provide text argument or --repo path", file=sys.stderr)
            sys.exit(1)

        d = profile.to_dict()
        if args.json:
            print(json.dumps(d, indent=2))
        else:
            print(f"Project Classification: {d['project_name']} ({d['project_id']})")
            print(f"Primary Family: {d['primary_family']} -> {d['primary_type']}")
            if d['secondary_types']:
                print(f"Secondary Types: {', '.join(d['secondary_types'])}")
            if d['supporting_types']:
                print(f"Supporting Types: {', '.join(d['supporting_types'])}")
            print(f"Confidence: {d['classification_confidence']} ({d['classification_rationale']})")
            print(f"Complexity: {d['complexity']['level']} ({d['complexity']['rationale']})")
            print(f"Delivery Targets: {', '.join(d['delivery_targets'])}")
            if d['conditional_profiles']:
                print(f"Conditional Profiles: {list(d['conditional_profiles'].keys())}")

    elif args.subcommand == "route":
        if args.repo:
            profile = classifier.classify_repository(Path(args.repo), project_name=args.name)
        elif args.text:
            profile = classifier.classify_text(args.text, project_name=args.name)
        else:
            print("Error: provide text argument or --repo path", file=sys.stderr)
            sys.exit(1)

        decision = router.route(profile)
        d = decision.to_dict()
        if args.json:
            print(json.dumps(d, indent=2))
        else:
            print(f"Deterministic Routing Decision: {d['project_id']}")
            print(f"Mandatory Domains ({len(d['domains']['mandatory'])}): {', '.join(d['domains']['mandatory'])}")
            print(f"Capabilities ({len(d['capabilities'])}): {', '.join([c['engine_id'] for c in d['capabilities']])}")
            print(f"Native Workforce: {', '.join(d['workforce']['native_agents'])}")
            if d['workforce']['external_agents']:
                print(f"External Workforce: {', '.join(d['workforce']['external_agents'])}")
            print(f"Primary Model: {d['models']['primary_model']}")
            print(f"Workflows: {', '.join([w['workflow_id'] for w in d['workflows']])}")
            print(f"Approval Gates ({len(d['approval_gates'])}): {', '.join([g['gate_id'] for g in d['approval_gates']])}")

    elif args.subcommand == "blueprint":
        if args.list or not args.blueprint_id:
            print("Canonical Project-Family Blueprints (14 Families):")
            for bp in bp_mgr.list_blueprints():
                print(f"  - [{bp['id']}] {bp['title']} ({bp['family']})")
        else:
            content = bp_mgr.get_blueprint(args.blueprint_id)
            if not content:
                print(f"Error: Blueprint '{args.blueprint_id}' not found.", file=sys.stderr)
                sys.exit(1)
            print(content)


if __name__ == "__main__":
    main()
