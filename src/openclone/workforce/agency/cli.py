"""OpenClone Agency Agents CLI.

Provides command-line interface for browsing divisions, searching agents,
inspecting specialist profiles, and assembling multi-agent teams.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from src.openclone.workforce.agency.catalog import AgencyCatalog
from src.openclone.workforce.agency.team_orchestrator import AgencyTeamOrchestrator


def build_agency_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openclone agency",
        description="OpenClone Agency Agents External Specialist Workforce CLI",
    )
    sub = parser.add_subparsers(dest="agency_cmd", required=True)

    # Divisions command
    sub.add_parser("divisions", help="List all discovered professional divisions")

    # List command
    list_p = sub.add_parser("list", help="List specialist agents")
    list_p.add_argument("--division", "-d", help="Filter by division")
    list_p.add_argument("--query", "-q", help="Search by keyword")

    # Show command
    show_p = sub.add_parser("show", help="View full profile and personality of an agent")
    show_p.add_argument("agent_id", help="Slug of the agent (e.g. ui-designer, backend-architect)")

    # Team command
    team_p = sub.add_parser("team", help="Assemble a specialist team")
    team_p.add_argument("--type", choices=["ui_ux", "website"], default="ui_ux", help="Team preset type")
    team_p.add_argument("--name", default="Project", help="Project name")
    team_p.add_argument("--json", action="store_true", help="Output team composition as JSON")

    # Sync command
    sub.add_parser("sync", help="Check upstream synchronization status")

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_agency_parser()
    args = parser.parse_args(argv)
    catalog = AgencyCatalog()
    orchestrator = AgencyTeamOrchestrator(catalog)

    if args.agency_cmd == "divisions":
        divisions = catalog.list_divisions()
        print(f"\nDiscovered {len(divisions)} Agency Agents Divisions:")
        print("-" * 65)
        for d in divisions:
            print(f"  [{d.id:<20}] {d.label:<25} ({d.agent_count} agents)")
        print()

    elif args.agency_cmd == "list":
        agents = catalog.search(args.query, division=args.division) if args.query else catalog.list_agents(args.division)
        div_label = f"in division '{args.division}'" if args.division else "across all divisions"
        print(f"\nSpecialist Agents ({len(agents)} found {div_label}):")
        print("-" * 75)
        for a in agents:
            print(f"  {a.emoji} {a.name:<28} [{a.division:<18}] {a.description[:40]}...")
        print()

    elif args.agency_cmd == "show":
        agent = catalog.get_agent(args.agent_id)
        if not agent:
            print(f"ERROR: Agent '{args.agent_id}' not found in catalog.", file=sys.stderr)
            sys.exit(1)
        print(f"\n{agent.emoji} {agent.name.upper()} ({agent.division.title()})")
        print("=" * 65)
        print(f"Description: {agent.description}")
        print(f"Vibe:        {agent.vibe}")
        print(f"License:     {agent.license} (Upstream: {agent.upstream_url})")
        print("\n--- Core Mission ---")
        print(agent.mission or "No explicit mission text.")
        if agent.critical_rules:
            print("\n--- Critical Rules ---")
            for r in agent.critical_rules:
                print(f"  * {r}")
        if agent.workflow_steps:
            print("\n--- Workflow Process ---")
            for i, s in enumerate(agent.workflow_steps, 1):
                print(f"  {i}. {s}")
        if agent.deliverables:
            print("\n--- Expected Deliverables ---")
            for d in agent.deliverables:
                print(f"  [+] {d}")
        print()

    elif args.agency_cmd == "team":
        if args.type == "ui_ux":
            team = orchestrator.assemble_ui_ux_team(args.name)
        else:
            team = orchestrator.assemble_website_development_team(args.name)

        if args.json:
            print(json.dumps(team.to_dict(), indent=2))
        else:
            print(f"\n{team.name}")
            print("=" * 65)
            print(f"Purpose: {team.purpose}\n")
            print("Specialist Handoff Chain & Responsibilities:")
            for i, mid in enumerate(team.execution_order, 1):
                m = next(x for x in team.members if x.agent_id == mid)
                deps = f"(depends on: {', '.join(m.depends_on)})" if m.depends_on else "(initial)"
                print(f"  {i}. [{m.role_name}] - {m.agent_name} ({m.division}) {deps}")
                print(f"     -> {m.responsibility}")
            print()

    elif args.agency_cmd == "sync":
        report = catalog.synchronize()
        print("\nAgency Agents Catalog Upstream Synchronization Status:")
        print("-" * 65)
        print(f"Upstream Repository: {report.upstream_url}")
        print(f"Total Scanned:       {report.total_scanned}")
        print(f"Status:              {report.status}")
        print(f"New Agents:          {len(report.new_agents)}")
        print(f"Modified Agents:     {len(report.modified_agents)}")
        print(f"Removed Agents:      {len(report.removed_agents)}")
        print()


if __name__ == "__main__":
    main()
