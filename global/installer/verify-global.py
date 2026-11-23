#!/usr/bin/env python3
"""OpenClone Global Installation Verification Utility."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys


def get_default_home() -> Path:
    home_env = os.environ.get("OPENCLONE_HOME")
    if home_env:
        return Path(home_env).resolve()
    user_profile = os.environ.get("USERPROFILE") or os.environ.get("HOME")
    if user_profile:
        return Path(user_profile).resolve() / ".openclone"
    return Path.home().resolve() / ".openclone"


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def verify_installation(home_dir: Path, dry_run: bool = False) -> int:
    registry_file = home_dir / "registry" / "installed.json"
    print(f"Checking OpenClone Global Home: {home_dir}")

    if dry_run:
        print("[DRY-RUN] Verification simulated. Target path exists:", home_dir.exists())
        return 0

    if not registry_file.exists():
        print(f"ERROR: Registry file not found: {registry_file}", file=sys.stderr)
        return 1

    try:
        data = json.loads(registry_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: Failed to parse registry file: {e}", file=sys.stderr)
        return 1

    installed_files = data.get("installed_files", {})
    if not installed_files:
        print("WARNING: Registry contains no installed files.", file=sys.stderr)
        return 0

    mismatches = 0
    missing = 0
    verified = 0

    for rel_path, expected_hash in installed_files.items():
        target = home_dir / rel_path
        if not target.exists():
            print(f"MISSING: {target}")
            missing += 1
            continue
        actual_hash = compute_sha256(target)
        if actual_hash != expected_hash:
            print(f"CHECKSUM MISMATCH: {target} (expected {expected_hash[:8]}, got {actual_hash[:8]})")
            mismatches += 1
        else:
            verified += 1

    print(f"Verification Results: {verified} verified, {missing} missing, {mismatches} mismatches.")
    if missing > 0 or mismatches > 0:
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description="Verify OpenClone global installation.")
    parser.add_argument("--home", type=str, default=None, help="Custom OpenClone home directory")
    parser.add_argument("--dry-run", action="store_true", help="Simulate verification without failing on missing registry")
    args = parser.parse_args()

    home = Path(args.home).resolve() if args.home else get_default_home()
    sys.exit(verify_installation(home, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
