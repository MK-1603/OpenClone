"""OpenClone Reverse Engineering Data Models and Contracts."""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ExecutionLevel(str, Enum):
    LEVEL_1_STATIC = "LEVEL_1_STATIC"
    LEVEL_2_RUNTIME = "LEVEL_2_RUNTIME"
    LEVEL_3_DEEP = "LEVEL_3_DEEP"


class EvidenceType(str, Enum):
    SOURCE_CODE_EVIDENCE = "SOURCE_CODE_EVIDENCE"
    AST_ANALYSIS = "AST_ANALYSIS"
    DEPENDENCY_MANIFEST = "DEPENDENCY_MANIFEST"
    SCHEMA_EVIDENCE = "SCHEMA_EVIDENCE"
    CONFIGURATION_EVIDENCE = "CONFIGURATION_EVIDENCE"
    DOCUMENTATION_EVIDENCE = "DOCUMENTATION_EVIDENCE"
    TEST_EVIDENCE = "TEST_EVIDENCE"
    RUNTIME_TRACE = "RUNTIME_TRACE"
    LOG_EVIDENCE = "LOG_EVIDENCE"
    HUMAN_CONFIRMED = "HUMAN_CONFIRMED"


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"


class FindingStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    INFERRED = "INFERRED"
    NOT_FOUND = "NOT_FOUND"
    NOT_VERIFIED = "NOT_VERIFIED"
    BLOCKED = "BLOCKED"


class CoverageStatus(str, Enum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    NOT_SUPPORTED = "NOT_SUPPORTED"
    NOT_EXECUTED = "NOT_EXECUTED"


@dataclass
class EvidenceRef:
    evidence_type: EvidenceType
    path: str
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    description: str = ""
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


@dataclass
class DependencyItem:
    name: str
    version_constraint: str
    ecosystem: str  # python, npm, cargo, go, maven
    is_direct: bool = True
    is_dev: bool = False
    vulnerability_warning: Optional[str] = None
    evidence: Optional[EvidenceRef] = None


@dataclass
class SymbolInfo:
    name: str
    symbol_type: str  # class, function, method, interface
    path: str
    line_start: int
    line_end: int
    complexity: int = 1
    parameters: List[str] = field(default_factory=list)
    docstring: Optional[str] = None


@dataclass
class EntityModel:
    name: str
    columns: List[str] = field(default_factory=list)
    primary_key: Optional[str] = None
    foreign_keys: List[Dict[str, str]] = field(default_factory=list)
    relationships: List[Dict[str, str]] = field(default_factory=list)
    source_path: str = ""
    orm_type: Optional[str] = None  # sqlalchemy, django, prisma, raw_sql


@dataclass
class ApiEndpoint:
    method: str
    path: str
    handler_name: str
    auth_required: bool = False
    line_number: int = 0
    source_path: str = ""


@dataclass
class WorkflowItem:
    name: str
    entrypoint: str
    trigger_type: str  # http, cli, cron, event, queue
    description: str = ""


@dataclass
class QualityMetrics:
    total_test_files: int = 0
    test_frameworks: List[str] = field(default_factory=list)
    has_ci_config: bool = False
    untested_critical_paths: List[str] = field(default_factory=list)


@dataclass
class SecurityFinding:
    finding_id: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    description: str
    path: str
    line: int
    is_confirmed_vulnerability: bool = False
    evidence_type: EvidenceType = EvidenceType.SOURCE_CODE_EVIDENCE


@dataclass
class TechnicalDebtItem:
    debt_id: str
    category: str
    title: str
    description: str
    severity: str
    loc_or_file: str


@dataclass
class CoverageReport:
    python_analysis: CoverageStatus = CoverageStatus.NOT_EXECUTED
    typescript_javascript_analysis: CoverageStatus = CoverageStatus.NOT_EXECUTED
    sql_analysis: CoverageStatus = CoverageStatus.NOT_EXECUTED
    dependency_analysis: CoverageStatus = CoverageStatus.NOT_EXECUTED
    api_extraction: CoverageStatus = CoverageStatus.NOT_EXECUTED
    runtime_analysis: CoverageStatus = CoverageStatus.NOT_EXECUTED
    security_analysis: CoverageStatus = CoverageStatus.NOT_EXECUTED

    def to_dict(self) -> Dict[str, str]:
        return {
            "python_analysis": self.python_analysis.value,
            "typescript_javascript_analysis": self.typescript_javascript_analysis.value,
            "sql_analysis": self.sql_analysis.value,
            "dependency_analysis": self.dependency_analysis.value,
            "api_extraction": self.api_extraction.value,
            "runtime_analysis": self.runtime_analysis.value,
            "security_analysis": self.security_analysis.value,
        }


@dataclass
class AsIsArchitectureReport:
    project_name: str
    root_path: str
    analyzed_at: str
    execution_level: ExecutionLevel
    confidence: ConfidenceLevel
    total_files: int
    total_loc: int
    languages: Dict[str, int]
    detected_frameworks: List[str]
    architecture_pattern: str
    dependencies: List[DependencyItem] = field(default_factory=list)
    symbols: List[SymbolInfo] = field(default_factory=list)
    entities: List[EntityModel] = field(default_factory=list)
    endpoints: List[ApiEndpoint] = field(default_factory=list)
    workflows: List[WorkflowItem] = field(default_factory=list)
    quality: QualityMetrics = field(default_factory=QualityMetrics)
    security_findings: List[SecurityFinding] = field(default_factory=list)
    technical_debt: List[TechnicalDebtItem] = field(default_factory=list)
    coverage: CoverageReport = field(default_factory=CoverageReport)
    c4_diagram: str = ""
    evidence_chain: List[EvidenceRef] = field(default_factory=list)
    unknowns_and_limitations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "root_path": self.root_path,
            "analyzed_at": self.analyzed_at,
            "execution_level": self.execution_level.value,
            "confidence": self.confidence.value,
            "total_files": self.total_files,
            "total_loc": self.total_loc,
            "languages": self.languages,
            "detected_frameworks": self.detected_frameworks,
            "architecture_pattern": self.architecture_pattern,
            "dependencies_count": len(self.dependencies),
            "symbols_count": len(self.symbols),
            "entities_count": len(self.entities),
            "endpoints_count": len(self.endpoints),
            "workflows_count": len(self.workflows),
            "technical_debt_count": len(self.technical_debt),
            "security_findings_count": len(self.security_findings),
            "coverage": self.coverage.to_dict(),
            "unknowns_and_limitations": self.unknowns_and_limitations,
        }
