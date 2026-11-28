"""OpenClone Agency Agents Integration — Domain Data Models.

Defines typed data structures for external Agency Agents, divisions,
execution contracts, team compositions, and upstream synchronization tracking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class AgentSource(str, Enum):
    """Source origin of specialist agents."""
    NATIVE_OPENCLONE = "native_openclone"
    EXTERNAL_AGENCY = "external_agency_agents"


class ExecutionStatus(str, Enum):
    """Execution status for agent tasks."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


@dataclass
class AgencyDivision:
    """A professional department/division from Agency Agents."""
    id: str
    label: str
    icon: str
    color: str
    description: str
    agent_count: int = 0


@dataclass
class AgencyAgentProfile:
    """Full unredacted specification and personality of an external specialist agent."""
    id: str
    name: str
    division: str
    description: str
    color: str = "#3B82F6"
    emoji: str = "🤖"
    vibe: str = ""
    source: AgentSource = AgentSource.EXTERNAL_AGENCY
    source_file: str = ""
    upstream_url: str = "https://github.com/msitarzewski/agency-agents"
    license: str = "MIT"
    revision_sha: str = "HEAD"
    imported_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # Preserved original personality & core sections
    identity_memory: str = ""
    mission: str = ""
    expertise: List[str] = field(default_factory=list)
    critical_rules: List[str] = field(default_factory=list)
    workflow_steps: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    communication_style: str = ""
    raw_content: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to serializable dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "division": self.division,
            "description": self.description,
            "color": self.color,
            "emoji": self.emoji,
            "vibe": self.vibe,
            "source": self.source.value,
            "source_file": self.source_file,
            "upstream_url": self.upstream_url,
            "license": self.license,
            "revision_sha": self.revision_sha,
            "imported_at": self.imported_at,
            "identity_memory": self.identity_memory,
            "mission": self.mission,
            "expertise": self.expertise,
            "critical_rules": self.critical_rules,
            "workflow_steps": self.workflow_steps,
            "deliverables": self.deliverables,
            "communication_style": self.communication_style,
        }


@dataclass
class ExecutionContract:
    """Governed execution parameters binding an external agent to OpenClone runtime."""
    contract_id: str
    task_id: str
    agent_id: str
    division: str
    prompt: str
    project_context: Dict[str, Any]
    allowed_actions: List[str] = field(default_factory=lambda: ["observe", "plan", "design"])
    denied_actions: List[str] = field(default_factory=lambda: ["unauthorized_exec", "raw_shell", "expose_secrets"])
    requires_approval: bool = False
    assigned_model: str = "gpt-6.2-sol"
    status: ExecutionStatus = ExecutionStatus.PENDING
    deliverables_received: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class TeamMember:
    """An individual specialist assigned to a team role."""
    role_name: str
    agent_id: str
    agent_name: str
    division: str
    responsibility: str
    depends_on: List[str] = field(default_factory=list)


@dataclass
class TeamComposition:
    """An assembled specialist team configured for project execution."""
    team_id: str
    name: str
    purpose: str
    members: List[TeamMember] = field(default_factory=list)
    execution_order: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "team_id": self.team_id,
            "name": self.name,
            "purpose": self.purpose,
            "execution_order": self.execution_order,
            "members": [
                {
                    "role_name": m.role_name,
                    "agent_id": m.agent_id,
                    "agent_name": m.agent_name,
                    "division": m.division,
                    "responsibility": m.responsibility,
                    "depends_on": m.depends_on,
                }
                for m in self.members
            ],
            "created_at": self.created_at,
        }


@dataclass
class SyncReport:
    """Audit report of external catalog synchronization against upstream."""
    synced_at: str
    upstream_url: str
    total_scanned: int
    new_agents: List[str] = field(default_factory=list)
    modified_agents: List[str] = field(default_factory=list)
    removed_agents: List[str] = field(default_factory=list)
    conflicts_detected: List[str] = field(default_factory=list)
    status: str = "SYNCED"
