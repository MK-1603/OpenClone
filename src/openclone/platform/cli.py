"""CLI dispatcher for OpenClone platform management commands."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from src.openclone.platform.config.manager import ConfigurationManager
from src.openclone.platform.diagnostics.doctor import PlatformDoctor
from src.openclone.platform.installation.detector import detect_installation_mode
from src.openclone.platform.installation.manager import PlatformInstallationManager
from src.openclone.platform.runtime.manager import RuntimeManager
from src.openclone.platform.updates.engine import UpdateEngine


def handle_doctor(args: List[str]) -> int:
    """Handle 'openclone doctor' command."""
    parser = argparse.ArgumentParser(prog="openclone doctor", description="Environmental and platform health checks")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    parser.add_argument("--project", type=str, default=None, help="Project directory to inspect")
    parsed = parser.parse_args(args)
    doc = PlatformDoctor(workspace_root=Path(parsed.project) if parsed.project else None)
    return doc.render_report(json_output=parsed.json)


def handle_config(args: List[str]) -> int:
    """Handle 'openclone config' command."""
    parser = argparse.ArgumentParser(prog="openclone config", description="User configuration management")
    sub = parser.add_subparsers(dest="action")
    sub.add_parser("show", help="Show current configuration")
    p_get = sub.add_parser("get", help="Get setting by key path")
    p_get.add_argument("key", help="Key path (e.g. 'update.channel')")
    p_set = sub.add_parser("set", help="Set setting by key path")
    p_set.add_argument("key", help="Key path")
    p_set.add_argument("value", help="Value to set")

    parsed = parser.parse_args(args)
    mgr = ConfigurationManager()

    if parsed.action in (None, "show"):
        cfg = mgr.load_config()
        print(json.dumps(cfg.to_dict(), indent=2))
        return 0
    elif parsed.action == "get":
        val = mgr.get_setting(parsed.key)
        print(val)
        return 0
    elif parsed.action == "set":
        # Attempt type inference for booleans / numbers
        v = parsed.value
        if v.lower() == "true":
            val: Any = True
        elif v.lower() == "false":
            val = False
        else:
            try:
                val = int(v)
            except ValueError:
                val = v
        mgr.set_setting(parsed.key, val)
        print(f"Setting '{parsed.key}' updated to: {val}")
        return 0
    return 0


def handle_runtime(args: List[str]) -> int:
    """Handle 'openclone runtime' command."""
    parser = argparse.ArgumentParser(prog="openclone runtime", description="Runtime environment management")
    sub = parser.add_subparsers(dest="action")
    sub.add_parser("info", help="Display active runtime information")
    sub.add_parser("check", help="Check developer toolchains")

    parsed = parser.parse_args(args)
    rt = RuntimeManager()

    if parsed.action in (None, "info"):
        info = rt.get_python_info()
        print("=== OpenClone Runtime Profile ===")
        for k, v in info.items():
            print(f"  {k:18} : {v}")
        return 0
    elif parsed.action == "check":
        tools = rt.check_toolchains()
        print("=== OpenClone Toolchain Availability ===")
        for k, s in tools.items():
            badge = "[PASS]" if s.available else ("[WARN]" if not s.required else "[FAIL]")
            print(f"  {badge} {s.name:12} : {s.path or 'not found'} ({s.version or s.error_message or 'ok'})")
        return 0
    return 0


def handle_update(args: List[str]) -> int:
    """Handle 'openclone update' platform lifecycle command."""
    parser = argparse.ArgumentParser(prog="openclone update", description="Platform update manager")
    sub = parser.add_subparsers(dest="action")
    sub.add_parser("check", help="Check for available platform updates")
    sub.add_parser("apply", help="Apply available platform update")
    p_chan = sub.add_parser("channel", help="View or set release channel")
    p_chan.add_argument("--set", dest="channel_name", choices=["stable", "beta", "nightly"], help="Switch channel")
    sub.add_parser("rollback", help="Roll back to previous snapshot")

    parsed = parser.parse_args(args)
    engine = UpdateEngine()

    if parsed.action in (None, "check"):
        print(f"Checking for updates on channel '{engine.get_channel().value}'...")
        res = engine.check_for_updates()
        print(f"Current Version : {res.current_version}")
        print(f"Latest Version  : {res.latest_version}")
        print(f"Channel         : {res.channel}")
        print(f"Status          : {res.message}")
        if res.update_available:
            print(f"Action          : Run 'openclone update apply' to upgrade.")
        return 0
    elif parsed.action == "apply":
        res = engine.check_for_updates()
        if not res.update_available:
            print("System is already up to date.")
            return 0
        print(f"Applying update to {res.latest_version}...")
        applied = engine.apply_update(res)
        print(applied.get("message", "Update complete."))
        return 0 if applied.get("success") else 1
    elif parsed.action == "channel":
        if parsed.channel_name:
            new_ch = engine.set_channel(parsed.channel_name)
            print(f"Release channel updated to: {new_ch.value}")
        else:
            print(f"Current release channel: {engine.get_channel().value}")
        return 0
    elif parsed.action == "rollback":
        from src.openclone.platform.rollback.manager import RollbackManager
        rb = RollbackManager()
        res = rb.restore_latest_snapshot()
        print(res.get("message"))
        return 0 if res.get("success") else 1
    return 0


def handle_components(args: List[str]) -> int:
    """Handle 'openclone components' command."""
    parser = argparse.ArgumentParser(prog="openclone components", description="Component and extension management")
    sub = parser.add_subparsers(dest="action")
    sub.add_parser("list", help="List installed components")
    p_ins = sub.add_parser("inspect", help="Inspect component manifest")
    p_ins.add_argument("component_id", help="Component ID")
    p_install = sub.add_parser("install", help="Install component from directory")
    p_install.add_argument("source_dir", help="Directory containing component.json")
    p_en = sub.add_parser("enable", help="Enable component")
    p_en.add_argument("component_id", help="Component ID")
    p_dis = sub.add_parser("disable", help="Disable component")
    p_dis.add_argument("component_id", help="Component ID")
    p_rm = sub.add_parser("remove", help="Remove component")
    p_rm.add_argument("component_id", help="Component ID")

    parsed = parser.parse_args(args)
    from src.openclone.platform.components.manager import ComponentManager
    cm = ComponentManager()

    if parsed.action in (None, "list"):
        items = cm.list_components()
        print(f"=== Installed OpenClone Components ({len(items)}) ===")
        for c in items:
            state = "[ENABLED]" if c["enabled"] else "[DISABLED]"
            print(f"  {state} {c['id']:22} (v{c['version']}) [{c['category']}] - {c['name']}")
        return 0
    elif parsed.action == "inspect":
        item = cm.inspect_component(parsed.component_id)
        if not item:
            print(f"Component '{parsed.component_id}' not found.")
            return 1
        print(json.dumps(item.__dict__, indent=2))
        return 0
    elif parsed.action == "install":
        res = cm.install_from_dir(Path(parsed.source_dir))
        print(res.get("message"))
        return 0 if res.get("success") else 1
    elif parsed.action == "enable":
        ok = cm.set_enabled(parsed.component_id, True)
        print(f"Component '{parsed.component_id}' enabled." if ok else "Component not found.")
        return 0 if ok else 1
    elif parsed.action == "disable":
        ok = cm.set_enabled(parsed.component_id, False)
        print(f"Component '{parsed.component_id}' disabled." if ok else "Component not found.")
        return 0 if ok else 1
    elif parsed.action == "remove":
        ok = cm.remove_component(parsed.component_id)
        print(f"Component '{parsed.component_id}' removed." if ok else "Component not found.")
        return 0 if ok else 1
    return 0
