"""OpenClone System Design Engineering & Capacity Intelligence Engine.

Provides automated capacity calculations, architecture pattern evaluation,
ADR generation, and 20 real-world system design case studies.
"""
from __future__ import annotations

from src.openclone.system_design.capacity import (
    BandwidthEstimate,
    CacheEstimate,
    CapacityEstimator,
    ComprehensiveCapacityReport,
    QueueEstimate,
    StorageEstimate,
    TrafficProfile,
)
from src.openclone.system_design.case_studies import (
    CaseStudyArchitecture,
    SystemDesignCatalogue,
)
from src.openclone.system_design.decision_engine import (
    ADRGenerator,
    ArchitectureRecommendation,
    QualityAttributes,
    SystemDesignDecisionEngine,
    SystemRequirements,
)
from src.openclone.system_design.diagrams import SystemDiagramGenerator

__all__ = [
    "ADRGenerator",
    "ArchitectureRecommendation",
    "BandwidthEstimate",
    "CacheEstimate",
    "CapacityEstimator",
    "CaseStudyArchitecture",
    "ComprehensiveCapacityReport",
    "QualityAttributes",
    "QueueEstimate",
    "StorageEstimate",
    "SystemDesignCatalogue",
    "SystemDesignDecisionEngine",
    "SystemDiagramGenerator",
    "SystemRequirements",
    "TrafficProfile",
]
