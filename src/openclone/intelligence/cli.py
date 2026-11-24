"""OpenClone Universal Project Intelligence CLI."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.openclone.intelligence.blueprints import BlueprintManager
from src.openclone.intelligence.classifier import ProjectClassifier
from src.openclone.intelligence.generator import ProjectPackageGenerator
from src.openclone.intelligence.router import ProjectRouter
from src.openclone.intelligence.taxonomy import TaxonomyRegistry
from src.openclone.intelligence.technology import TechnologyIntelligenceEngine


def main():
    parser = argparse.ArgumentParser(
        prog="openclone intelligence",
        description="OpenClone Universal AI Engineering Intelligence: multi-label classification, routing, technology evaluation, and package generation.",
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

    # Technology Evaluation
    p_tech = sub.add_parser("tech-eval", help="Evaluate and recommend technology stack options")
    p_tech.add_argument("text", nargs="?", default="", help="Natural language requirements")
    p_tech.add_argument("--json", action="store_true", help="Emit raw JSON")

    # Generate Package
    p_gen = sub.add_parser("generate", help="Generate complete governed project package from prompt")
    p_gen.add_argument("prompt", help="Natural language project idea or PRD")
    p_gen.add_argument("--name", type=str, default="project", help="Project name")
    p_gen.add_argument("--out", type=str, default="", help="Output directory to write files")
    p_gen.add_argument("--json", action="store_true", help="Emit raw JSON")

    # Blueprint
    p_bp = sub.add_parser("blueprint", help="View or search project family blueprints")
    p_bp.add_argument("blueprint_id", nargs="?", default="", help="Blueprint ID (e.g. 01-MINI-WEBSITE, 10-LINUX-OS)")
    p_bp.add_argument("--list", action="store_true", help="List all 14 project family blueprints")

    args = parser.parse_args()

    tax = TaxonomyRegistry()
    bp_mgr = BlueprintManager()
    classifier = ProjectClassifier(tax)
    router = ProjectRouter(tax)
    tech_engine = TechnologyIntelligenceEngine()
    generator = ProjectPackageGenerator(tax, classifier, router, tech_engine)

    if args.subcommand in ("status", None):
        res = {
            "version": tax.version,
            "categories_count": len(tax.list_categories()),
            "categories": tax.list_categories(),
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
            print(f"Primary Engineering Categories: {len(tax.list_categories())} (ENG-01 to ENG-14)")
            print(f"Supported Families: {len(tax.families)} | Blueprints: {len(bp_mgr.list_blueprints())}")
            print("\nEngineering Categories:")
            for c in tax.list_categories():
                print(f"  - {c['id']}: {c['name']} ({c['subdisciplines_count']} subdisciplines)")
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
            if d['supporting_disciplines']:
                print(f"Supporting Disciplines: {', '.join(d['supporting_disciplines'])}")
            print(f"Confidence: {d['classification_confidence']} ({d['classification_rationale']})")
            print(f"Complexity: {d['complexity']['level']} ({d['complexity']['rationale']})")
            print(f"Delivery Targets: {', '.join(d['delivery_targets'])}")
            print(f"Deployment Model: {d['deployment_model']} | AI: {d['ai_dependency']}")

    elif args.subcommand == "tech-eval":
        if not args.text:
            print("Error: provide text requirements", file=sys.stderr)
            sys.exit(1)
        profile = classifier.classify_text(args.text, project_name="eval-project")
        decisions = tech_engine.evaluate(profile, requirements_text=args.text)
        res = [d.to_dict() for d in decisions]
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("Evaluated Technology Stack Decisions:")
            for d in decisions:
                print(f"\n- {d.category}: {d.selected_technology} ({d.version}) [{d.license}]")
                print(f"  Rationale: {d.selection_rationale}")
                print(f"  Alternatives: {', '.join(d.alternatives_evaluated)}")

    elif args.subcommand == "generate":
        out_dir = Path(args.out) if args.out else None
        pkg = generator.generate(args.prompt, project_name=args.name, output_dir=out_dir)
        if args.json:
            print(json.dumps(pkg, indent=2))
        else:
            print(f"Successfully generated project package for: {pkg['profile']['project_name']}")
            print(f"Primary Archetype: {pkg['profile']['primary_type']}")
            print(f"Generated Artifacts: {', '.join(pkg['artifacts'].keys())}")
            if out_dir:
                print(f"Written to directory: {out_dir.resolve()}")

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
            print(f"Routing Decision for: {decision.project_id}")
            print(f"Activated Domains: {len(decision.domains)}")
            print(f"Activated Capabilities: {len(decision.capabilities)}")
            print(f"Workforce Teams: {len(decision.workforce)}")

    elif args.subcommand == "blueprint":
        if args.list or not args.blueprint_id:
            bps = bp_mgr.list_blueprints()
            print(f"Available Project Blueprints ({len(bps)}):")
            for b in bps:
                print(f"  [{b['id']}] {b['title']} ({b['family']})")
        else:
            content = bp_mgr.get_blueprint_content(args.blueprint_id)
            if content:
                print(content)
            else:
                print(f"Blueprint not found: {args.blueprint_id}", file=sys.stderr)
                sys.exit(1)


if __name__ == "__main__":
    main()
