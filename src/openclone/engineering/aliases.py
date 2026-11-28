"""OpenClone Engineering Domain Aliases & Bridge Registry.

Maps legacy framework directories (31 folders), EIS master sectors (17 sectors),
and classifier signatures (12 families) cleanly into the 23 Canonical Engineering Domains.
"""
from __future__ import annotations

from typing import Dict, List, Optional
from src.openclone.engineering.taxonomy import EngineeringDomain


class EngineeringDomainBridge:
    """Bidirectional bridge mapping legacy, filesystem, and external sector definitions."""

    # 31 Framework directories mapping (framework/domains/xx-*)
    FRAMEWORK_FOLDER_TO_DOMAIN: Dict[str, EngineeringDomain] = {
        "00-GOVERNANCE": EngineeringDomain.DOMAIN_23_GOVERNANCE,
        "01-METHODOLOGY": EngineeringDomain.DOMAIN_21_PROJECT_DELIVERY,
        "02-PROJECT-INTELLIGENCE": EngineeringDomain.DOMAIN_03_RESEARCH,
        "03-REQUIREMENTS-ENGINEERING": EngineeringDomain.DOMAIN_02_REQUIREMENTS,
        "04-PRODUCT-ENGINEERING": EngineeringDomain.DOMAIN_01_PRODUCT,
        "05-UX-UI-ENGINEERING": EngineeringDomain.DOMAIN_04_UX_UI,
        "06-TECHNOLOGY-INTELLIGENCE": EngineeringDomain.DOMAIN_22_TECHNOLOGY_INTELLIGENCE,
        "07-ENGINEERING-KNOWLEDGE": EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE,
        "08-SOFTWARE-ARCHITECTURE": EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE,
        "09-PLATFORM-ENGINEERING": EngineeringDomain.DOMAIN_15_INFRASTRUCTURE,
        "10-AI-AND-MODEL-ENGINEERING": EngineeringDomain.DOMAIN_11_AI,
        "11-AGENT-ENGINEERING": EngineeringDomain.DOMAIN_11_AI,
        "12-ORCHESTRATION-AND-CONTEXT": EngineeringDomain.DOMAIN_11_AI,
        "13-HARNESS-AND-EXECUTION": EngineeringDomain.DOMAIN_18_HARNESS,
        "14-SECURITY-AND-PRIVACY": EngineeringDomain.DOMAIN_12_SECURITY,
        "15-DATA-AND-DATABASE-ENGINEERING": EngineeringDomain.DOMAIN_08_DATABASE,
        "16-API-AND-INTEGRATION-ENGINEERING": EngineeringDomain.DOMAIN_07_API,
        "17-TESTING-AND-VERIFICATION": EngineeringDomain.DOMAIN_16_QUALITY,
        "18-DEVOPS-AND-CLOUD-ENGINEERING": EngineeringDomain.DOMAIN_15_INFRASTRUCTURE,
        "19-DEPLOYMENT-AND-OPERATIONS": EngineeringDomain.DOMAIN_15_INFRASTRUCTURE,
        "20-RELIABILITY-AND-OBSERVABILITY": EngineeringDomain.DOMAIN_17_RELIABILITY,
        "21-DISTRIBUTED-SYSTEMS-AND-SCALABILITY": EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN,
        "22-COST-AND-RESOURCE-GOVERNANCE": EngineeringDomain.DOMAIN_21_PROJECT_DELIVERY,
        "23-LEGAL-AND-COMPLIANCE": EngineeringDomain.DOMAIN_23_GOVERNANCE,
        "24-PRODUCT-ANALYTICS-AND-SUPPORT": EngineeringDomain.DOMAIN_01_PRODUCT,
        "25-FRAMEWORK-MAINTENANCE": EngineeringDomain.DOMAIN_21_PROJECT_DELIVERY,
        "26-DISTRIBUTION-AND-EXTENSIONS": EngineeringDomain.DOMAIN_15_INFRASTRUCTURE,
        "27-STANDARDS-AND-COMPATIBILITY": EngineeringDomain.DOMAIN_23_GOVERNANCE,
        "28-TEMPLATES-AND-EXAMPLES": EngineeringDomain.DOMAIN_01_PRODUCT,
        "29-BENCHMARKS-AND-EVALUATION": EngineeringDomain.DOMAIN_16_QUALITY,
        "30-AGENT-RULES-AND-VERIFICATION": EngineeringDomain.DOMAIN_23_GOVERNANCE,
    }

    # 17 EIS Master Sectors mapping (EIS-01 to EIS-17)
    EIS_SECTOR_TO_DOMAIN: Dict[str, EngineeringDomain] = {
        "EIS-01": EngineeringDomain.DOMAIN_02_REQUIREMENTS,
        "EIS-02": EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN,
        "EIS-03": EngineeringDomain.DOMAIN_06_BACKEND,
        "EIS-04": EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE,
        "EIS-05": EngineeringDomain.DOMAIN_11_AI,
        "EIS-06": EngineeringDomain.DOMAIN_11_AI,
        "EIS-07": EngineeringDomain.DOMAIN_08_DATABASE,
        "EIS-08": EngineeringDomain.DOMAIN_08_DATABASE,
        "EIS-09": EngineeringDomain.DOMAIN_15_INFRASTRUCTURE,
        "EIS-10": EngineeringDomain.DOMAIN_15_INFRASTRUCTURE,
        "EIS-11": EngineeringDomain.DOMAIN_12_SECURITY,
        "EIS-12": EngineeringDomain.DOMAIN_16_QUALITY,
        "EIS-13": EngineeringDomain.DOMAIN_17_RELIABILITY,
        "EIS-14": EngineeringDomain.DOMAIN_07_API,
        "EIS-15": EngineeringDomain.DOMAIN_04_UX_UI,
        "EIS-16": EngineeringDomain.DOMAIN_23_GOVERNANCE,
        "EIS-17": EngineeringDomain.DOMAIN_03_RESEARCH,
    }

    # 12 Classifier Family Signatures mapping
    CLASSIFIER_FAMILY_TO_DOMAIN: Dict[str, List[EngineeringDomain]] = {
        "operating_systems_and_systems": [EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN, EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE],
        "embedded_hardware_and_robotics": [EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN, EngineeringDomain.DOMAIN_18_HARNESS],
        "mobile_engineering": [EngineeringDomain.DOMAIN_13_MOBILE, EngineeringDomain.DOMAIN_04_UX_UI],
        "desktop_engineering": [EngineeringDomain.DOMAIN_14_DESKTOP, EngineeringDomain.DOMAIN_04_UX_UI],
        "ai_engineering": [EngineeringDomain.DOMAIN_11_AI, EngineeringDomain.DOMAIN_08_DATABASE],
        "machine_learning": [EngineeringDomain.DOMAIN_11_AI, EngineeringDomain.DOMAIN_08_DATABASE],
        "data_engineering_and_data_science": [EngineeringDomain.DOMAIN_08_DATABASE, EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN],
        "game_and_simulation": [EngineeringDomain.DOMAIN_14_DESKTOP, EngineeringDomain.DOMAIN_04_UX_UI],
        "developer_tools_and_languages": [EngineeringDomain.DOMAIN_15_INFRASTRUCTURE, EngineeringDomain.DOMAIN_16_QUALITY],
        "research_and_scientific_computing": [EngineeringDomain.DOMAIN_03_RESEARCH, EngineeringDomain.DOMAIN_11_AI],
        "backend_and_distributed_systems": [EngineeringDomain.DOMAIN_06_BACKEND, EngineeringDomain.DOMAIN_07_API, EngineeringDomain.DOMAIN_10_SYSTEM_DESIGN],
        "web_engineering": [EngineeringDomain.DOMAIN_05_FRONTEND, EngineeringDomain.DOMAIN_06_BACKEND, EngineeringDomain.DOMAIN_01_PRODUCT],
    }

    @classmethod
    def resolve_folder(cls, folder_name: str) -> Optional[EngineeringDomain]:
        cleaned = folder_name.strip().upper()
        return cls.FRAMEWORK_FOLDER_TO_DOMAIN.get(cleaned)

    @classmethod
    def resolve_eis_sector(cls, sector_id: str) -> Optional[EngineeringDomain]:
        cleaned = sector_id.strip().upper()
        return cls.EIS_SECTOR_TO_DOMAIN.get(cleaned)

    @classmethod
    def resolve_classifier_family(cls, family_name: str) -> List[EngineeringDomain]:
        return cls.CLASSIFIER_FAMILY_TO_DOMAIN.get(family_name.strip().lower(), [])
