"""
OpenClone Memory Context Builder.
Prepares bounded, token-budgeted, role-tailored context packages for agents.
"""

from __future__ import annotations
import uuid
from typing import List, Optional, Dict, Any
from openclone.memory.models import MemoryRecord, MemoryScope, MemoryType, MemoryStatus
from openclone.memory.retrieval.engine import MemoryRetrievalEngine
from openclone.memory.security.guardrails import MemorySecurityGuard


class MemoryContextPackage:
    """Bounded, traceable context package delivered to an executing agent."""

    def __init__(
        self,
        context_id: str,
        project_id: str,
        task_id: str,
        agent_id: str,
        memories: List[Dict[str, Any]],
        approved_decisions: List[Dict[str, Any]],
        project_constraints: List[str],
        token_budget_allocated: int,
        token_budget_used: int,
        omissions: List[str]
    ):
        self.context_id = context_id
        self.project_id = project_id
        self.task_id = task_id
        self.agent_id = agent_id
        self.memories = memories
        self.approved_decisions = approved_decisions
        self.project_constraints = project_constraints
        self.token_budget = {
            "allocated": token_budget_allocated,
            "used": token_budget_used
        }
        self.omissions = omissions

    def to_dict(self) -> Dict[str, Any]:
        return {
            "context_id": self.context_id,
            "project_id": self.project_id,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "memories": self.memories,
            "approved_decisions": self.approved_decisions,
            "project_constraints": self.project_constraints,
            "token_budget": self.token_budget,
            "omissions": self.omissions,
        }


class MemoryContextBuilder:
    """
    Constructs bounded memory context packages for OpenClone agents.
    Rules:
    - Enforces hard token budget limits (approx 4 chars/token).
    - Goldfish Isolation: Independent Verifier receives ONLY explicit requirements, ZERO drafting memories.
    - Role tailoring: Database agent gets database decisions; Frontend agent gets UI/token decisions.
    - Frames memory records in untrusted data delimiters.
    """

    ROLE_TYPE_AFFINITIES = {
        "openclone-backend-agent": ["decision", "project_fact", "lesson"],
        "openclone-database-agent": ["decision", "project_fact"],
        "openclone-frontend-agent": ["decision", "project_fact", "preference"],
        "openclone-ui-design-agent": ["preference", "decision"],
        "openclone-security-agent": ["decision", "lesson", "project_fact"],
        "openclone-independent-verifier-agent": ["decision"],  # Strictly restricted Goldfish boundary
    }

    def __init__(self, retrieval_engine: MemoryRetrievalEngine):
        self.retrieval_engine = retrieval_engine

    def build_context(
        self,
        query: str,
        scope: MemoryScope,
        agent_id: str,
        task_id: str,
        token_budget: int = 4000
    ) -> MemoryContextPackage:
        context_id = f"CTX-{uuid.uuid4().hex[:6].upper()}"

        # Goldfish Principle check
        is_verifier = "verifier" in agent_id.lower() or agent_id == "openclone-independent-verifier-agent"

        # Query retrieval engine
        retrieval_results = self.retrieval_engine.retrieve(
            query=query,
            scope=scope,
            limit=20,
            include_superseded=False
        )

        allowed_types = self.ROLE_TYPE_AFFINITIES.get(agent_id, ["decision", "project_fact", "lesson", "session_checkpoint"])
        memories = []
        approved_decisions = []
        project_constraints = []
        omissions = []

        total_chars_budget = token_budget * 4
        current_chars = 0

        for res in retrieval_results:
            rec = res.record

            # Goldfish boundary: If verifier, suppress all working/session/unverified memories
            if is_verifier:
                if rec.memory_type != MemoryType.DECISION or rec.authority.value == "unverified":
                    continue

            # Role affinity filter
            if rec.memory_type.value not in allowed_types:
                continue

            entry_text = f"[{rec.id}] {rec.title}: {rec.statement}"
            if rec.details:
                entry_text += f" | {rec.details}"

            entry_chars = len(entry_text)
            if current_chars + entry_chars > total_chars_budget:
                omissions.append(f"Omitted record {rec.id} ({rec.title}) due to token budget constraint.")
                continue

            current_chars += entry_chars
            sanitized_statement = MemorySecurityGuard.sanitize_untrusted_memory(rec.statement)

            rec_dict = {
                "id": rec.id,
                "title": rec.title,
                "type": rec.memory_type.value,
                "statement": sanitized_statement,
                "authority": rec.authority.value,
                "score": res.score,
                "source_refs": [s.to_dict() if hasattr(s, "to_dict") else s for s in rec.source_refs]
            }

            if rec.memory_type == MemoryType.DECISION:
                approved_decisions.append(rec_dict)
            else:
                memories.append(rec_dict)

            if "constraint" in rec.title.lower() or "limit" in rec.title.lower():
                project_constraints.append(rec.statement)

        used_tokens = current_chars // 4

        return MemoryContextPackage(
            context_id=context_id,
            project_id=scope.project_id,
            task_id=task_id,
            agent_id=agent_id,
            memories=memories,
            approved_decisions=approved_decisions,
            project_constraints=project_constraints,
            token_budget_allocated=token_budget,
            token_budget_used=used_tokens,
            omissions=omissions
        )
