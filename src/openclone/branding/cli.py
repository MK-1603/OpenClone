"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — CLI Interface."""

import argparse
import json
import sys
from pathlib import Path

from src.openclone.branding import BrandGuidelineGenerator, engineer_brand_identity


def main():
    parser = argparse.ArgumentParser(
        prog="openclone brand",
        description="OpenClone Logo Engineering & Brand Identity System (LEBIS)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. engineer command
    engineer_cmd = subparsers.add_parser("engineer", help="Engineer complete brand identity from brief")
    engineer_cmd.add_argument("--name", required=True, help="Brand or product name")
    engineer_cmd.add_argument("--category", default="Software Platform", help="Product domain category")
    engineer_cmd.add_argument("--tagline", default="", help="Brand positioning or tagline")
    engineer_cmd.add_argument("--primary-color", default="#2563EB", help="Primary brand hex color")
    engineer_cmd.add_argument("--out-dir", default="assets/branding", help="Directory to export vector assets")

    # 2. validate command
    validate_cmd = subparsers.add_parser("validate", help="Validate an SVG logo file against LEBIS QA rules")
    validate_cmd.add_argument("--svg", required=True, help="Path to SVG file")

    args = parser.parse_args()

    if args.command == "engineer":
        raw_brief = {
            "brand_name": args.name,
            "category": args.category,
            "positioning": args.tagline or f"Premium {args.category}",
            "primary_color": args.primary_color,
        }
        pkg = engineer_brand_identity(raw_brief)
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)

        for v in pkg.variants:
            fname = f"{v.variant_type.value.lower().replace('_', '-')}.svg"
            (out / fname).write_text(v.svg_content, encoding="utf-8")

        manual = BrandGuidelineGenerator.generate_markdown_manual(pkg)
        (out / "BRAND-GUIDELINES.md").write_text(manual, encoding="utf-8")

        print(f"Successfully engineered brand identity for '{args.name}'.")
        print(f"Exported {len(pkg.variants)} vector variants and BRAND-GUIDELINES.md to {out}/")
        print(f"QA Score: {pkg.qa_report.total_score}/100.0 (Passed: {pkg.qa_report.passed})")

    elif args.command == "validate":
        svg_path = Path(args.svg)
        if not svg_path.exists():
            print(f"Error: File not found: {args.svg}", file=sys.stderr)
            sys.exit(1)
        content = svg_path.read_text(encoding="utf-8", errors="replace")
        has_raster = "<image" in content.lower() or "data:image/" in content
        if has_raster:
            print("FAILED: Embedded raster images detected.", file=sys.stderr)
            sys.exit(1)
        print(f"PASSED: '{args.svg}' is valid pure vector SVG.")


if __name__ == "__main__":
    main()
