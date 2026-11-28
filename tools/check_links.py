#!/usr/bin/env python3
"""OpenClone Markdown Relative Link Verifier."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def verify_links() -> int:
    errors = []
    total_links = 0
    checked_files = 0

    for md in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in md.parts) or any(p in md.parts for p in ("node_modules", "dist", "build")):
            continue
        checked_files += 1
        try:
            txt = md.read_text(encoding="utf-8")
        except Exception:
            continue

        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', txt):
            t_clean = target.split('#', 1)[0].strip()
            if not t_clean or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', t_clean) or t_clean.startswith('#') or '{{' in t_clean or t_clean.startswith('file://'):
                continue
            total_links += 1
            rel_parts = t_clean.replace('\\', '/').split('/')
            curr = md.parent
            for part in rel_parts:
                if not part or part == '.':
                    continue
                if part == '..':
                    curr = curr.parent
                    continue
                matches = [x.name for x in curr.iterdir() if x.name.lower() == part.lower()]
                if not matches:
                    errors.append((str(md.relative_to(ROOT)), target))
                    break
                if matches[0] != part:
                    errors.append((str(md.relative_to(ROOT)), f"{target} (casing mismatch: disk has {matches[0]})"))
                    break
                curr = curr / matches[0]

    print(f"Scanned {checked_files} Markdown files, verified {total_links} relative links.")
    if errors:
        print(f"FAILED: Found {len(errors)} broken relative links:", file=sys.stderr)
        for f, t in errors:
            print(f"  {f} -> {t}", file=sys.stderr)
        return 1

    print("SUCCESS: 0 broken Markdown links found.")
    return 0

if __name__ == "__main__":
    sys.exit(verify_links())
