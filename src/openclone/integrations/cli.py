"""CLI Command Handlers for Platforms and Integrations."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from src.openclone.integrations.manager import IntegrationManager


def handle_platforms(args: List[str]) -> int:
    """Handle 'oc platforms' or 'openclone platforms' CLI commands."""
    parser = argparse.ArgumentParser(
        prog="openclone platforms",
        description="Inspect and manage host IDE and platform discovery",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Platform commands")

    # discover
    subparsers.add_parser("discover", help="Probe host machine for installed development environments")

    # list
    subparsers.add_parser("list", help="List all supported platform descriptors and maturity levels")

    # inspect <platform>
    inspect_p = subparsers.add_parser("inspect", help="Deep inspection of platform configuration")
    inspect_p.add_argument("platform_id", help="Platform ID (e.g. antigravity, vscode, cursor, jetbrains, zed)")

    # connect <platform>
    connect_p = subparsers.add_parser("connect", help="Configure connection to specified platform")
    connect_p.add_argument("platform_id", help="Platform ID (e.g. antigravity, vscode, cursor, jetbrains, zed)")
    connect_p.add_argument("--global", "-g", dest="is_global", action="store_true", help="Install globally in user profile")

    # status
    subparsers.add_parser("status", help="Show overview of connected platforms in current workspace")

    parsed = parser.parse_args(args)
    manager = IntegrationManager()

    if parsed.subcommand == "discover":
        results = manager.discover_platforms()
        print("\n=== Discovered Platforms on Host System ===")
        print(f"{'Platform ID':<15} {'Name':<30} {'Installed':<12} {'Configured':<12} {'Compatibility'}")
        print("-" * 85)
        for p in results:
            inst = "YES" if p["is_installed"] else "NO"
            conf = "YES" if p["is_configured"] else "NO"
            print(f"{p['platform_id']:<15} {p['display_name']:<30} {inst:<12} {conf:<12} {p['compatibility']}")
        print()
        return 0

    elif parsed.subcommand == "list":
        descriptors = manager.list_all_platforms() if hasattr(manager, "list_all_platforms") else manager.list_platforms()
        print("\n=== Supported Platform Registry ===")
        print(f"{'Platform ID':<15} {'Name':<32} {'Maturity':<15} {'Protocols'}")
        print("-" * 80)
        for d in descriptors:
            protos = ", ".join(d["supported_protocols"])
            print(f"{d['platform_id']:<15} {d['display_name']:<32} {d['maturity']:<15} {protos}")
        print()
        return 0

    elif parsed.subcommand == "inspect":
        try:
            info = manager.inspect_platform(parsed.platform_id)
            print(f"\n=== Platform Inspection: {parsed.platform_id} ===")
            print(json.dumps(info, indent=2))
            return 0
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif parsed.subcommand == "connect":
        try:
            is_glob = getattr(parsed, "is_global", False)
            res = manager.connect_platform(parsed.platform_id, is_global=is_glob)
            print(f"\n[SUCCESS] Connected {parsed.platform_id} (Global: {is_glob})!")
            print(json.dumps(res, indent=2))
            return 0
        except Exception as e:
            print(f"Error connecting platform '{parsed.platform_id}': {e}", file=sys.stderr)
            return 1

    elif parsed.subcommand == "status":
        status = manager.get_status()
        print("\n=== OpenClone Ecosystem Integration Status ===")
        print(f"Workspace Root: {status['workspace_root']}")
        print(f"Total Supported: {status['total_supported']}")
        print(f"Configured in Workspace: {status['total_configured']}\n")
        print(f"{'Platform ID':<15} {'Name':<30} {'Installed':<12} {'Configured'}")
        print("-" * 70)
        for p in status["platforms"]:
            inst = "YES" if p["is_installed"] else "NO"
            conf = "YES" if p["is_configured"] else "NO"
            print(f"{p['platform_id']:<15} {p['display_name']:<30} {inst:<12} {conf}")
        print()
        return 0

    else:
        parser.print_help()
        return 0


def handle_integrations(args: List[str]) -> int:
    """Handle 'oc integrations' or 'openclone integrations' CLI commands."""
    parser = argparse.ArgumentParser(
        prog="openclone integrations",
        description="Manage IDE and platform integration lifecycle",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Integration actions")

    # list
    subparsers.add_parser("list", help="List available and configured integrations")

    # install <platform>
    install_p = subparsers.add_parser("install", help="Install platform integration")
    install_p.add_argument("platform_id", help="Platform ID (e.g. antigravity, vscode, cursor, jetbrains, zed)")
    install_p.add_argument("--global", "-g", dest="is_global", action="store_true", help="Install globally in user profile")

    # remove <platform>
    remove_p = subparsers.add_parser("remove", help="Remove platform integration")
    remove_p.add_argument("platform_id", help="Platform ID (e.g. antigravity, vscode, cursor, jetbrains, zed)")
    remove_p.add_argument("--global", "-g", dest="is_global", action="store_true", help="Remove globally installed integration")

    parsed = parser.parse_args(args)
    manager = IntegrationManager()

    if parsed.subcommand == "list":
        status = manager.get_status()
        print("\n=== Configured Platform Integrations ===")
        for p in status["platforms"]:
            mark = "[ACTIVE]" if p["is_configured"] else "[AVAILABLE]"
            print(f"{mark:<12} {p['platform_id']:<15} {p['display_name']}")
        print()
        return 0

    elif parsed.subcommand == "install":
        try:
            is_glob = getattr(parsed, "is_global", False)
            res = manager.install_integration(parsed.platform_id, is_global=is_glob)
            print(f"[SUCCESS] Installed integration for '{parsed.platform_id}' (Global: {is_glob}):")
            print(json.dumps(res, indent=2))
            return 0
        except Exception as e:
            print(f"Error installing integration '{parsed.platform_id}': {e}", file=sys.stderr)
            return 1

    elif parsed.subcommand == "remove":
        try:
            is_glob = getattr(parsed, "is_global", False)
            res = manager.remove_integration(parsed.platform_id, is_global=is_glob)
            print(f"[SUCCESS] Removed integration for '{parsed.platform_id}' (Global: {is_glob}):")
            print(json.dumps(res, indent=2))
            return 0
        except Exception as e:
            print(f"Error removing integration '{parsed.platform_id}': {e}", file=sys.stderr)
            return 1

    else:
        parser.print_help()
        return 0
