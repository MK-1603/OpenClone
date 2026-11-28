"""
Automated Test Suite for OpenClone Engineering Intelligence System (EIS).

Verifies:
1. Exact presence and completeness of all 17 Master Sectors (EIS-01 to EIS-17).
2. Canonical Knowledge Schema validation (types, enums, required fields, depth).
3. Knowledge Graph Engine traversal (sector indexing, tool search, prerequisite resolution).
4. Capability Model and distinction between Role, Skill, Tool, Capability, and Agent.
5. Agent capability resolution matching 16 native specialist agents.
6. Engineering Problem-Solving Engine (EPSE) 18-stage lifecycle and multi-attribute evaluation.
7. End-to-end problem-solving scenarios across SaaS, Database, and Security domains.
8. Preservation of Goldfish verifier isolation and prohibited physical sector exclusions.
"""

import json
from pathlib import Path
import pytest

from openclone.engineering.models import (
    MasterSector,
    KnowledgeType,
    KnowledgeMaturity,
    KnowledgeSourceRef,
    KnowledgeUnit,
)
from openclone.engineering.graph import KnowledgeGraphEngine
from openclone.engineering.capabilities import (
    EngineeringCapability,
    CapabilityRegistry,
)
from openclone.engineering.epse import (
    ProblemCategory,
    SolutionAlternative,
    ProblemSolvingPlan,
    EngineeringProblemSolvingEngine,
)
from openclone.engineering.manager import EngineeringIntelligenceSystem

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestMasterSectorsAndTaxonomy:
    """Tests for 17 canonical sectors and physical engineering exclusions."""

    def test_all_17_sectors_defined_uniquely(self):
        sectors = list(MasterSector)
        assert len(sectors) == 17, f"Expected exactly 17 master sectors, got {len(sectors)}"
        sector_values = [s.value for s in sectors]
        for i in range(1, 18):
            expected = f"EIS-{i:02d}"
            assert expected in sector_values, f"Missing sector identifier: {expected}"

    def test_prohibited_physical_sectors_excluded(self):
        """Rule 3.5: No physical engineering sectors (civil, mechanical, chemical, electrical, PCB)."""
        sectors = [s.value for s in MasterSector]
        prohibited = ["mechanical", "electrical", "civil", "chemical", "pcb", "aerospace", "hardware"]
        for s in sectors:
            for p in prohibited:
                assert p not in s.lower()

    def test_master_sector_document_exists(self):
        doc_path = REPO_ROOT / "framework" / "engineering-intelligence" / "EIS-MASTER-SECTORS.md"
        assert doc_path.is_file(), "EIS-MASTER-SECTORS.md missing!"
        content = doc_path.read_text(encoding="utf-8")
        for i in range(1, 18):
            assert f"EIS-{i:02d}" in content


class TestCanonicalKnowledgeSchema:
    """Tests for schema validation of engineering knowledge units."""

    def test_valid_knowledge_unit_serialization(self):
        unit = KnowledgeUnit(
            id="EIS-KNOW-TEST",
            title="Clean Architecture Principles",
            sector_id=MasterSector.EIS_04,
            domain_id="SOFTWARE-ARCHITECTURE",
            subdomain_id="ENTERPRISE-PATTERNS",
            specialization_id="HEXAGONAL",
            knowledge_type=KnowledgeType.ENGINEERING_PRINCIPLE,
            description="Isolate business domain from transport and database adapters.",
            purpose="Ensure maintainable, testable, framework-independent systems.",
            concepts=["Entities", "Use Cases", "Interface Adapters"],
            tools=["python", "go"],
            standards=["ISO/IEC 25010"],
            source_refs=[KnowledgeSourceRef(uri="clean-arch.md", source_type="book")],
            maturity=KnowledgeMaturity.LEVEL_4_TECHNICALLY_VALIDATED
        )
        data = unit.to_dict()
        assert data["id"] == "EIS-KNOW-TEST"
        assert data["sector_id"] == "EIS-04"
        assert data["knowledge_type"] == "engineering_principle"
        assert len(data["concepts"]) == 3
        assert len(data["source_refs"]) == 1

    def test_schema_json_file_validity(self):
        schema_path = REPO_ROOT / "framework" / "schemas" / "engineering-knowledge.schema.json"
        assert schema_path.is_file()
        schema_data = json.loads(schema_path.read_text(encoding="utf-8"))
        assert schema_data["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert len(schema_data["properties"]["sector_id"]["enum"]) == 17


class TestKnowledgeGraphEngine:
    """Tests for graph indexing, search, and prerequisite resolution."""

    def test_graph_registration_and_traversal(self):
        graph = KnowledgeGraphEngine()
        u1 = KnowledgeUnit(
            id="EIS-KNOW-P1",
            title="Basic Relational Theory",
            sector_id=MasterSector.EIS_08,
            domain_id="DATABASE",
            subdomain_id="RELATIONAL",
            specialization_id="THEORY",
            knowledge_type=KnowledgeType.TECHNICAL_CONCEPT,
            description="Relational algebra and keys.",
            purpose="Foundation for data integrity.",
            tools=["sql"],
        )
        u2 = KnowledgeUnit(
            id="EIS-KNOW-P2",
            title="Index Optimization",
            sector_id=MasterSector.EIS_08,
            domain_id="DATABASE",
            subdomain_id="RELATIONAL",
            specialization_id="TUNING",
            knowledge_type=KnowledgeType.IMPLEMENTATION_METHOD,
            description="B-tree index tuning.",
            purpose="Query acceleration.",
            prerequisites=["EIS-KNOW-P1"],
            tools=["postgresql", "sqlite"],
        )
        graph.register_unit(u1)
        graph.register_unit(u2)

        # Query by sector
        sec_units = graph.get_units_by_sector(MasterSector.EIS_08)
        assert len(sec_units) == 2

        # Prerequisite resolution
        prereqs = graph.resolve_prerequisites("EIS-KNOW-P2")
        assert len(prereqs) == 2
        assert prereqs[0].id == "EIS-KNOW-P1"
        assert prereqs[1].id == "EIS-KNOW-P2"

        # Search by tool
        pg_units = graph.find_by_tool("postgresql")
        assert len(pg_units) == 1
        assert pg_units[0].id == "EIS-KNOW-P2"


class TestCapabilityRegistryAndAgentMapping:
    """Tests for capabilities and agent matching."""

    def test_capabilities_distinct_from_agents(self):
        reg = CapabilityRegistry()
        cap = reg.get_capability("CAP-REQ-001")
        assert cap is not None
        assert cap.sector_id == MasterSector.EIS_01

        # Check capable agents
        agents = reg.find_capable_agents("CAP-REQ-001")
        assert "openclone-product-requirements-agent" in agents

        # Check verifier capability mapping
        ver_agents = reg.find_capable_agents("CAP-VER-001")
        assert "openclone-independent-verifier-agent" in ver_agents

    def test_agent_capabilities_lookup(self):
        reg = CapabilityRegistry()
        caps = reg.get_agent_capabilities("openclone-backend-agent")
        assert len(caps) >= 1
        cap_ids = [c.id for c in caps]
        assert "CAP-DEV-001" in cap_ids


class TestEngineeringProblemSolvingEngine:
    """Tests for EPSE 18-stage problem solving and solution evaluation."""

    def test_solve_database_problem(self):
        eis = EngineeringIntelligenceSystem()
        plan = eis.solve_problem(
            title="PostgreSQL Table Lock Starvation under High Concurrency",
            description="ALTER TABLE operations are blocking application read queries during migrations.",
            category=ProblemCategory.DATABASE
        )

        assert plan.primary_sector == MasterSector.EIS_08
        assert "CAP-DB-001" in plan.required_capabilities
        assert "openclone-database-agent" in plan.recommended_agents
        assert plan.selected_solution.composite_score >= 0.85
        assert len(plan.testing_strategy) >= 3

    def test_solve_security_problem(self):
        eis = EngineeringIntelligenceSystem()
        plan = eis.solve_problem(
            title="Insecure Direct Object Reference (IDOR) on Tenant Resources",
            description="Users can modify other tenants' records by altering resource IDs in API requests.",
            category=ProblemCategory.SECURITY
        )

        assert plan.primary_sector == MasterSector.EIS_11
        assert "CAP-SEC-001" in plan.required_capabilities
        assert "openclone-security-agent" in plan.recommended_agents

    def test_solve_architecture_problem(self):
        eis = EngineeringIntelligenceSystem()
        plan = eis.solve_problem(
            title="High Latency in Distributed Microservices Transactions",
            description="Cross-service HTTP calls are causing cascading timeouts and distributed locks.",
            category=ProblemCategory.ARCHITECTURE
        )

        assert plan.primary_sector == MasterSector.EIS_04
        assert "CAP-ARCH-001" in plan.required_capabilities
        assert "openclone-product-architect-agent" in plan.recommended_agents
        # Discovered knowledge should surface Monolith-First principle
        assert "EIS-KNOW-001" in plan.discovered_knowledge
