"""Command-line interface for the OpenClone Global Plugin installer."""

import argparse
import json
import sys
from pathlib import Path

from src.openclone.installer.detector import detect_hosts
from src.openclone.installer.engine import InstallerEngine, SUPPORTED_HOSTS


def main(args=None):
    parser = argparse.ArgumentParser(
        prog="openclone installer",
        description="OpenClone Global Plugin Installer and Host Manager",
    )
    subparsers = parser.add_subparsers(dest="action", help="Installer commands")

    # install
    p_install = subparsers.add_parser("install", help="Install a native host adapter")
    p_install.add_argument("host", nargs="?", default="all", help=f"Target host: {', '.join(sorted(SUPPORTED_HOSTS))} or 'all'")
    p_install.add_argument("--scope", choices=["user", "workspace"], default="workspace", help="Installation scope")
    p_install.add_argument("--target", type=str, default=None, help="Target directory (defaults to cwd)")
    p_install.add_argument("--dry-run", action="store_true", help="Simulate installation without writing")
    p_install.add_argument("--yes", "-y", action="store_true", help="Auto-confirm prompts")

    # uninstall
    p_uninst = subparsers.add_parser("uninstall", help="Uninstall a host adapter")
    p_uninst.add_argument("host", help=f"Host to uninstall: {', '.join(sorted(SUPPORTED_HOSTS))}")
    p_uninst.add_argument("--target", type=str, default=None, help="Target directory (defaults to cwd)")
    p_uninst.add_argument("--dry-run", action="store_true", help="Simulate uninstall without deleting")

    # update
    p_update = subparsers.add_parser("update", help="Update installed host adapter")
    p_update.add_argument("host", help=f"Host to update: {', '.join(sorted(SUPPORTED_HOSTS))}")
    p_update.add_argument("--target", type=str, default=None, help="Target directory (defaults to cwd)")

    # rollback
    p_rollback = subparsers.add_parser("rollback", help="Rollback adapter to prior backup")
    p_rollback.add_argument("host", help=f"Host to rollback: {', '.join(sorted(SUPPORTED_HOSTS))}")
    p_rollback.add_argument("--target", type=str, default=None, help="Target directory (defaults to cwd)")

    # status
    p_status = subparsers.add_parser("status", help="Show detected hosts and installation status")
    p_status.add_argument("--target", type=str, default=None, help="Target directory")
    p_status.add_argument("--json", action="store_true", help="Output as JSON")

    # doctor
    p_doctor = subparsers.add_parser("doctor", help="Run environmental diagnostics and fix hints")
    p_doctor.add_argument("--target", type=str, default=None, help="Target directory")
    p_doctor.add_argument("--json", action="store_true", help="Output as JSON")

    parsed = parser.parse_args(args)
    if not parsed.action:
        parser.print_help()
        return 0

    engine = InstallerEngine()
    target_path = Path(parsed.target) if getattr(parsed, "target", None) else None

    if parsed.action == "install":
        hosts_to_install = list(SUPPORTED_HOSTS) if parsed.host == "all" else [parsed.host]
        print(f"=== OpenClone Global Plugin Installer ===")
        print(f"Target Scope: {parsed.scope} | Target Dir: {target_path or Path.cwd()}")
        for h in hosts_to_install:
            try:
                res = engine.install(h, scope=parsed.scope, target_dir=target_path, dry_run=parsed.dry_run)
                if parsed.dry_run:
                    print(f"  [DRY-RUN] {h}: Would install {len(res['planned_files'])} files -> {res['planned_files']}")
                else:
                    print(f"  [PASS] {h}: Successfully installed {len(res['installed_files'])} files (backups: {res['backups_created']})")
            except Exception as e:
                print(f"  [FAIL] {h}: {e}")

    elif parsed.action == "uninstall":
        res = engine.uninstall(parsed.host, target_dir=target_path, dry_run=parsed.dry_run)
        if parsed.dry_run:
            print(f"  [DRY-RUN] Would remove: {res.get('files_to_remove')} | Would restore: {res.get('backups_to_restore')}")
        elif res.get("success"):
            print(f"  [PASS] Successfully uninstalled '{parsed.host}'. Removed: {res.get('files_removed')} (restored backups: {res.get('backups_restored')})")
        else:
            print(f"  [INFO] {res.get('message')}")

    elif parsed.action == "update":
        res = engine.update(parsed.host, target_dir=target_path)
        print(f"  [PASS] Updated '{parsed.host}': {len(res['installed_files'])} files intact.")

    elif parsed.action == "rollback":
        res = engine.rollback(parsed.host, target_dir=target_path)
        print(f"  [PASS] Rolled back '{parsed.host}': {res}")

    elif parsed.action == "status":
        res = engine.status(target_dir=target_path)
        if parsed.json:
            print(json.dumps(res, indent=2))
        else:
            print("=== OpenClone Installation Status ===")
            print(f"Core Version:   {res['core_version']}")
            print(f"Workspace:      {res['workspace_root']}\n")
            print("Installed Adapters:")
            if not res["installed_adapters"]:
                print("  (None installed in this workspace)")
            for hid, info in res["installed_adapters"].items():
                integ = info["integrity"]
                status_str = "INTACT" if integ.get("intact") else f"MODIFIED ({len(integ.get('modified', []))} files)"
                print(f"  - {hid} [Scope: {info['scope']}] — Status: {status_str} ({integ.get('total_files', 0)} files)")
            print("\nDetected AI Coding Hosts:")
            for hid, det in res["detected_hosts"].items():
                flag = "DETECTED" if det["detected"] else "NOT DETECTED"
                print(f"  - {det['name']:<22}: {flag:<12} (Confidence: {det['confidence']*100:.0f}%, CLI: {'YES' if det['cli_found'] else 'NO'})")

    elif parsed.action == "doctor":
        res = engine.doctor(target_dir=target_path)
        if parsed.json:
            print(json.dumps(res, indent=2))
        else:
            print("=== OpenClone Environmental Doctor ===")
            for c in res["checks"]:
                mark = "[PASS]" if c["passed"] else "[FAIL]"
                print(f"  {mark:<6} {c['name']:<28}: {c['detail']}")
                if not c["passed"]:
                    print(f"         └─ Fix Hint: {c['fix_hint']}")
            print(f"\nResult: {res['summary']} — {'System healthy.' if res['all_healthy'] else 'Issues detected.'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
