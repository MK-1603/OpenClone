"""CLI dispatcher for OpenClone Autonomous Engineering Execution Engine."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.openclone.autonomous.engine import AutonomousExecutionEngine
from src.openclone.autonomous.models import ExecutionMode


def handle_autonomous(argv: list[str]) -> int:
    """Handle 'openclone autonomous' commands."""
    parser = argparse.ArgumentParser(
        prog="openclone autonomous",
        description="OpenClone Autonomous Engineering Execution Engine",
    )
    parser.add_argument("prompt", nargs="?", help="Engineering prompt or task description to execute")
    parser.add_argument(
        "--mode",
        choices=["instant", "fast", "standard", "deep", "autonomous"],
        default="standard",
        help="Execution mode (default: standard)",
    )
    parser.add_argument(
        "--workspace",
        default=".",
        help="Target workspace root directory",
    )

    args = parser.parse_args(argv)

    if not args.prompt:
        parser.print_help()
        return 0

    mode = ExecutionMode(args.mode)
    engine = AutonomousExecutionEngine(workspace_root=Path(args.workspace))

    print(f"=== OpenClone Autonomous Execution [{mode.value.upper()}] ===")
    print(f"Request: {args.prompt}")
    print(f"Target Workspace: {Path(args.workspace).resolve()}\n")

    report = engine.run(prompt=args.prompt, mode=mode)
    print(report.to_markdown())

    return 0 if report.status == "COMPLETED" else 1
