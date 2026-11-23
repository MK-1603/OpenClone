"""Command line interface for NoteDigest."""
import argparse
import sys
from pathlib import Path
from .engine import NoteDigestEngine


def main():
    parser = argparse.ArgumentParser(description="NoteDigest: AI & rule-assisted meeting digest generator.")
    parser.add_argument("input_file", nargs="?", help="Path to text or transcript file to digest.")
    parser.add_argument("--output", "-o", help="Optional output path for generated markdown digest.")
    parser.add_argument("--json", action="store_true", help="Output digest as JSON.")

    args = parser.parse_args()

    if not args.input_file:
        # Read from stdin if available
        if not sys.stdin.isatty():
            content = sys.stdin.read()
        else:
            parser.print_help()
            sys.exit(1)
    else:
        path = Path(args.input_file)
        if not path.is_file():
            print(f"Error: File not found: {args.input_file}", file=sys.stderr)
            sys.exit(1)
        content = path.read_text(encoding="utf-8")

    engine = NoteDigestEngine()
    result = engine.process(content)

    if args.json:
        import json
        out_str = json.dumps(engine.to_dict(result), indent=2)
    else:
        out_str = engine.format_markdown(result)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(out_str, encoding="utf-8")
        print(f"Digest successfully exported to: {out_path}")
    else:
        print(out_str)


if __name__ == "__main__":
    main()
