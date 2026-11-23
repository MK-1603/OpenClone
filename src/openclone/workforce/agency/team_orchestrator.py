"""OpenClone Agency Agents Integration — Specialist Team Orchestrator.

Assembles specialist teams from Agency Agents, configures handoffs,
and computes deterministic execution DAG orders.
"""

from __future__ import annotations

import uuid
from typing import Dict, List, Optional

from src.openclone.workforce.agency.catalog import AgencyCatalog
from src.openclone.workforce.agency.models import TeamComposition, TeamMember


class AgencyTeamOrchestrator:
    """Orchestrates specialist multi-agent team assembly and task coordination."""

    def __init__(self, catalog: Optional[AgencyCatalog] = None):
        self.catalog = catalog or AgencyCatalog()

    def assemble_ui_ux_team(self, project_name: str = "Web Interface") -> TeamComposition:
        """Assemble the authoritative 5-stage UX Pro specialist team workflow.

        Workflow order:
        UX Researcher -> UX Architect -> UI Designer -> Frontend Developer -> UI Finish-Gate Reviewer
        """
        members = [
            TeamMember(
                role_name="User Researcher",
                agent_id="ux-researcher",
                agent_name="UX Researcher",
                division="design",
                responsibility="Analyze user mental models, conduct heuristic audits, and define user problem statements.",
                depends_on=[],
            ),
            TeamMember(
                role_name="Information Architect",
                agent_id="ux-architect",
                agent_name="UX Architect",
                division="design",
                responsibility="Establish user flows, wireframe blocks, interaction paradigms, and navigation hierarchy.",
                depends_on=["ux-researcher"],
            ),
            TeamMember(
                role_name="Interface Designer",
                agent_id="ui-designer",
                agent_name="UI Designer",
                division="design",
                responsibility="Design component architecture, semantic design tokens, typography scales, and responsive layouts.",
                depends_on=["ux-architect"],
            ),
            TeamMember(
                role_name="Frontend Engineer",
                agent_id="frontend-developer",
                agent_name="Frontend Developer",
                division="engineering",
                responsibility="Implement production components, WCAG accessibility, and all 14 interaction states.",
                depends_on=["ui-designer"],
            ),
            TeamMember(
                role_name="Finish-Gate Reviewer",
                agent_id="ui-finish-gate-reviewer",
                agent_name="UI Finish-Gate Reviewer",
                division="design",
                responsibility="Inspect rendered layouts, verify WCAG 4.5:1 contrast, eliminate AI slop, and issue sign-off.",
                depends_on=["frontend-developer"],
            ),
        ]

        order = [m.agent_id for m in members]

        return TeamComposition(
            team_id=f"team_ux_{uuid.uuid4().hex[:8]}",
            name=f"{project_name} UX Pro Specialist Team",
            purpose="End-to-end user experience, interface design, frontend implementation, and finish-gate verification.",
            members=members,
            execution_order=order,
        )

    def assemble_website_development_team(self, project_name: str = "Website Build") -> TeamComposition:
        """Assemble a complete website engineering team."""
        members = [
            TeamMember(
                role_name="Project Coordinator",
                agent_id="project-shepherd",
                agent_name="Project Shepherd",
                division="project-management",
                responsibility="Coordinate milestone delivery, resolve dependencies, and track deliverables.",
                depends_on=[],
            ),
            TeamMember(
                role_name="User Researcher",
                agent_id="ux-researcher",
                agent_name="UX Researcher",
                division="design",
                responsibility="Understand user needs, target demographics, and primary conversion pathways.",
                depends_on=["project-shepherd"],
            ),
            TeamMember(
                role_name="Interface Designer",
                agent_id="ui-designer",
                agent_name="UI Designer",
                division="design",
                responsibility="Define visual hierarchy, design tokens, responsive breakpoints, and component states.",
                depends_on=["ux-researcher"],
            ),
            TeamMember(
                role_name="Backend Architect",
                agent_id="backend-architect",
                agent_name="Backend Architect",
                division="engineering",
                responsibility="Design scalable API endpoints, database schemas, and data pipelines.",
                depends_on=["project-shepherd"],
            ),
            TeamMember(
                role_name="Frontend Engineer",
                agent_id="frontend-developer",
                agent_name="Frontend Developer",
                division="engineering",
                responsibility="Build responsive web pages and components using approved tokens.",
                depends_on=["ui-designer", "backend-architect"],
            ),
            TeamMember(
                role_name="Reality Checker",
                agent_id="reality-checker",
                agent_name="Reality Checker",
                division="testing",
                responsibility="Stress-test assumptions, network resilience, edge cases, and failure modes.",
                depends_on=["frontend-developer"],
            ),
            TeamMember(
                role_name="Visual Quality Reviewer",
                agent_id="ui-finish-gate-reviewer",
                agent_name="UI Finish-Gate Reviewer",
                division="design",
                responsibility="Perform final visual QA, contrast audits, and pre-release sign-off.",
                depends_on=["reality-checker"],
            ),
        ]

        order = self.compute_execution_order(members)

        return TeamComposition(
            team_id=f"team_web_{uuid.uuid4().hex[:8]}",
            name=f"{project_name} Development Team",
            purpose="Complete website development from architecture and design to implementation and finish-gate QA.",
            members=members,
            execution_order=order,
        )

    def assemble_custom_team(
        self,
        team_name: str,
        purpose: str,
        agent_ids: List[str],
        dependencies: Optional[Dict[str, List[str]]] = None,
    ) -> TeamComposition:
        """Assemble an arbitrary specialist team by agent IDs with dependency resolution."""
        dep_map = dependencies or {}
        members: List[TeamMember] = []

        for aid in agent_ids:
            profile = self.catalog.get_agent(aid)
            name = profile.name if profile else aid.replace("-", " ").title()
            div = profile.division if profile else "specialized"
            members.append(
                TeamMember(
                    role_name=name,
                    agent_id=aid,
                    agent_name=name,
                    division=div,
                    responsibility=profile.description if profile else f"Execute {name} responsibilities.",
                    depends_on=dep_map.get(aid, []),
                )
            )

        order = self.compute_execution_order(members)

        return TeamComposition(
            team_id=f"team_custom_{uuid.uuid4().hex[:8]}",
            name=team_name,
            purpose=purpose,
            members=members,
            execution_order=order,
        )

    @staticmethod
    def compute_execution_order(members: List[TeamMember]) -> List[str]:
        """Compute deterministic topological ordering for team execution."""
        from collections import defaultdict, deque

        member_ids = {m.agent_id for m in members}
        indegree = {m.agent_id: 0 for m in members}
        adj = defaultdict(list)

        for m in members:
            for dep in m.depends_on:
                if dep in member_ids:
                    adj[dep].append(m.agent_id)
                    indegree[m.agent_id] += 1

        queue = deque(sorted([mid for mid, deg in indegree.items() if deg == 0]))
        order = []

        while queue:
            curr = queue.popleft()
            order.append(curr)
            for nxt in sorted(adj[curr]):
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)

        # If cycles or missing nodes remain, append remaining deterministically
        for m in members:
            if m.agent_id not in order:
                order.append(m.agent_id)

        return order
