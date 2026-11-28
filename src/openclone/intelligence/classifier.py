"""OpenClone Multi-Label Project Classifier.

Implements versioned, machine-readable multi-label classification across 14 primary
engineering categories (ENG-01 through ENG-14), independent project archetypes,
and independent dimensions (complexity, delivery targets, deployment model,
AI dependency, data sensitivity, and reliability tier).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from src.openclone.intelligence.taxonomy import TaxonomyRegistry


@dataclass
class ProjectComplexity:
    level: str  # MINI, SMALL, MEDIUM, LARGE, ENTERPRISE, RESEARCH_EXPERIMENTAL
    rationale: str


@dataclass
class ProjectProfile:
    project_id: str
    project_name: str
    primary_family: str
    primary_type: str
    secondary_types: List[str] = field(default_factory=list)
    supporting_types: List[str] = field(default_factory=list)
    supporting_disciplines: List[str] = field(default_factory=list)  # ENG-01 .. ENG-14
    classification_confidence: float = 1.0
    classification_rationale: str = ""
    ambiguity_flags: List[str] = field(default_factory=list)
    complexity: ProjectComplexity = field(default_factory=lambda: ProjectComplexity("MEDIUM", "Standard modular scope"))
    delivery_targets: List[str] = field(default_factory=lambda: ["web_browser"])
    deployment_model: str = "cloud"  # local, cloud, hybrid, on_premises, edge
    ai_dependency: str = "none"  # none, optional, required
    data_sensitivity: str = "internal"  # public, internal, confidential, restricted
    reliability_tier: str = "standard_99_0"  # standard_99_0, high_99_9, mission_critical_99_99
    unresolved_questions: List[str] = field(default_factory=list)
    conditional_profiles: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "primary_family": self.primary_family,
            "primary_type": self.primary_type,
            "secondary_types": self.secondary_types,
            "supporting_types": self.supporting_types,
            "supporting_disciplines": self.supporting_disciplines,
            "classification_confidence": round(self.classification_confidence, 2),
            "classification_rationale": self.classification_rationale,
            "ambiguity_flags": self.ambiguity_flags,
            "complexity": {
                "level": self.complexity.level,
                "rationale": self.complexity.rationale,
            },
            "delivery_targets": self.delivery_targets,
            "deployment_model": self.deployment_model,
            "ai_dependency": self.ai_dependency,
            "data_sensitivity": self.data_sensitivity,
            "reliability_tier": self.reliability_tier,
            "unresolved_questions": self.unresolved_questions,
            "conditional_profiles": self.conditional_profiles,
        }


class ProjectClassifier:
    """Classifies natural language requirements and repository files into a multi-label ProjectProfile."""

    FAMILY_SIGNATURES: Dict[str, Dict[str, List[str]]] = {
        "operating_systems_and_systems": {
            "linux_distribution": ["linux distro", "linux distribution", "custom linux", "initramfs", "bootable iso", "kernel image", "rootfs", "busybox", "chroot", "grub", "systemd"],
            "kernel_driver_module": ["kernel module", "device driver", "ioctl", "character device", "pci driver", "dmesg", "kernel panic", "v4l2", "kbuild"],
        },
        "embedded_hardware_and_robotics": {
            "rtos_firmware": ["freertos", "zephyr", "stm32", "esp32", "microcontroller", "firmware", "embedded c", "spi", "i2c", "uart", "gpio", "watchdog"],
            "robotics_platform": ["ros 2", "ros2", "robotics", "sensor fusion", "lidar", "motor controller", "kinematics", "slam", "actuator"],
        },
        "mobile_engineering": {
            "cross_platform_mobile": ["flutter", "react native", "react-native", "expo", "dart mobile", "mobile app", "cross-platform mobile"],
            "native_android": ["android", "kotlin android", "jetpack compose", "android sdk", "apk", "aab", "gradle android"],
            "native_ios": ["swift", "swiftui", "ios app", "xcode", "cocoapods", "coredata", "apple watch"],
        },
        "desktop_engineering": {
            "cross_platform_desktop": ["tauri", "electron", "desktop app", "system tray", "window management", "gtk", "qt desktop"],
            "native_desktop_tool": ["windows desktop", "macos desktop", "win32", "cocoa app", "wpf"],
        },
        "ai_engineering": {
            "rag_knowledge_system": ["rag", "retrieval augmented", "vector database", "embeddings", "chroma", "pinecone", "qdrant", "weaviate", "semantic search"],
            "autonomous_agent_system": ["agentic", "ai agent", "multi-agent", "tool calling", "function calling", "autonomous agent", "langchain", "crewai", "autogen"],
        },
        "machine_learning": {
            "classical_ml_pipeline": ["scikit-learn", "xgboost", "lightgbm", "tabular", "feature engineering", "cross-validation", "random forest", "logistic regression"],
            "deep_learning_cv_nlp": ["pytorch", "tensorflow", "transformer", "huggingface", "computer vision", "object detection", "yolo", "whisper", "fine-tuning"],
        },
        "data_engineering_and_data_science": {
            "etl_pipeline": ["etl", "elt", "airflow", "dbt", "spark", "kafka", "data pipeline", "lakehouse", "snowflake", "bigquery", "databricks"],
            "data_science_study": ["eda", "exploratory data", "statistical analysis", "hypothesis testing", "jupyter", "pandas analysis", "data science"],
        },
        "game_and_simulation": {
            "game_application": ["game", "game engine", "unity", "unreal", "godot", "phaser", "pixijs", "game loop", "ecs", "2d game", "3d game", "physics engine"],
        },
        "developer_tools_and_languages": {
            "cli_developer_tool": ["cli tool", "command-line", "command line tool", "terminal utility", "argparse", "click", "clap rust", "cobra go", "sdk library"],
            "compiler_toolchain": ["compiler", "interpreter", "ast parser", "lexer", "llvm", "bytecode", "type checker", "transpiler"],
        },
        "research_and_scientific_computing": {
            "computational_model": ["scientific computing", "numerical simulation", "differential equations", "bioinformatics", "geospatial", "finite element", "scipy", "numpy simulation"],
        },
        "backend_and_distributed_systems": {
            "microservices_platform": ["microservices", "grpc", "distributed system", "api gateway", "service mesh", "consul", "envoy"],
            "event_driven_stream": ["event-driven", "message queue", "rabbitmq", "nats", "websocket server", "real-time stream"],
        },
        "web_engineering": {
            "mini_website": ["landing page", "mini website", "portfolio", "documentation site", "marketing site", "static site", "astro", "next.js landing"],
            "saas_web_app": ["saas", "web app", "web application", "dashboard", "billing", "multi-tenant", "full-stack", "next.js", "remix"],
            "enterprise_platform": ["enterprise platform", "portal", "internal tool", "compliance platform", "erp", "crm", "hrms"],
        },
    }

    # Mapping of types to primary engineering discipline
    TYPE_TO_DISCIPLINE: Dict[str, str] = {
        "rag_knowledge_system": "ENG-01",
        "autonomous_agent_system": "ENG-01",
        "classical_ml_pipeline": "ENG-02",
        "deep_learning_cv_nlp": "ENG-02",
        "data_science_study": "ENG-03",
        "etl_pipeline": "ENG-03",
        "mini_website": "ENG-05",
        "cross_platform_mobile": "ENG-05",
        "native_android": "ENG-05",
        "native_ios": "ENG-05",
        "cross_platform_desktop": "ENG-05",
        "native_desktop_tool": "ENG-05",
        "cli_developer_tool": "ENG-05",
        "microservices_platform": "ENG-06",
        "event_driven_stream": "ENG-06",
        "enterprise_platform": "ENG-07",
        "saas_web_app": "ENG-08",
        "linux_distribution": "ENG-12",
        "kernel_driver_module": "ENG-12",
        "rtos_firmware": "ENG-12",
        "robotics_platform": "ENG-12",
        "game_application": "ENG-12",
        "compiler_toolchain": "ENG-12",
        "computational_model": "ENG-12",
    }

    def __init__(self, taxonomy: Optional[TaxonomyRegistry] = None):
        self.taxonomy = taxonomy or TaxonomyRegistry()

    def classify_text(self, text: str, project_name: str = "project") -> ProjectProfile:
        lower = text.lower()
        slug_id = re.sub(r"[^a-z0-9_-]", "-", project_name.lower()).strip("-") or "project-001"

        matched_types: List[str] = []
        family_scores: Dict[str, int] = {}

        for fam_id, type_sigs in self.FAMILY_SIGNATURES.items():
            for t_id, keywords in type_sigs.items():
                for kw in keywords:
                    if re.search(r"\b" + re.escape(kw) + r"\b", lower):
                        if t_id not in matched_types:
                            matched_types.append(t_id)
                        family_scores[fam_id] = family_scores.get(fam_id, 0) + 1

        unresolved_questions: List[str] = []

        # If no keywords matched
        if not matched_types:
            primary_family = "web_engineering"
            primary_type = "saas_web_app"
            confidence = 0.4
            rationale = "No specialized domain keywords detected; default modular profile suggested pending domain clarification."
            ambiguity_flags = ["no_explicit_domain_keywords_detected"]
            unresolved_questions.append("Project domain and platform requirements not detected; please specify target platform (web, mobile, desktop, embedded, or systems).")
        else:
            # First matched type is primary unless high-scoring family indicates otherwise
            best_family = max(family_scores.keys(), key=lambda k: family_scores[k])
            best_type = next((t for t in matched_types if self.taxonomy.get_family_for_type(t) == best_family), matched_types[0])
            primary_type = best_type
            primary_family = best_family
            confidence = min(0.95, 0.65 + 0.1 * len(matched_types))
            rationale = f"Matched {len(matched_types)} domain keywords across {len(family_scores)} project families."
            ambiguity_flags = [] if len(matched_types) <= 3 else ["multi_domain_hybrid_project"]

        secondary = [t for t in matched_types if t != primary_type][:3]
        supporting = [t for t in matched_types if t != primary_type and t not in secondary]

        # Determine supporting engineering disciplines (ENG-01 to ENG-14)
        supporting_disciplines_set: Set[str] = set()
        for t in matched_types:
            disc = self.TYPE_TO_DISCIPLINE.get(t)
            if disc:
                supporting_disciplines_set.add(disc)

        # Baseline disciplines: Quality (ENG-13), Security (ENG-11)
        supporting_disciplines_set.add("ENG-11")  # Cybersecurity Engineering
        supporting_disciplines_set.add("ENG-13")  # Quality Engineering

        if "web_browser" in lower or "ui" in lower or "frontend" in lower or primary_family in ("web_engineering", "mobile_engineering", "desktop_engineering"):
            supporting_disciplines_set.add("ENG-14")  # UI/UX & Product Engineering

        if "cloud" in lower or "devops" in lower or "ci/cd" in lower or "docker" in lower:
            supporting_disciplines_set.add("ENG-09")  # DevOps & Cloud Engineering

        supporting_disciplines = sorted(list(supporting_disciplines_set))

        # Determine delivery targets
        delivery_targets: Set[str] = set()
        primary_def = self.taxonomy.get_type(primary_type)
        if primary_def and primary_def.typical_delivery_targets:
            delivery_targets.update(primary_def.typical_delivery_targets)
        for s in secondary:
            s_def = self.taxonomy.get_type(s)
            if s_def and s_def.typical_delivery_targets:
                delivery_targets.update(s_def.typical_delivery_targets)

        if not delivery_targets:
            delivery_targets.add("web_browser")

        # Determine AI dependency
        if any(k in lower for k in ["rag", "agent", "llm", "gpt", "gemini", "claude", "neural", "vision model", "model training", "inference"]):
            ai_dependency = "required"
        elif any(k in lower for k in ["smart", "analytics", "predictive", "recommendation", "automation"]):
            ai_dependency = "optional"
        else:
            ai_dependency = "none"

        # Determine Deployment Model
        if "mobile" in primary_family or "cross_platform_mobile" in matched_types or "native_android" in matched_types or "native_ios" in matched_types:
            deployment_model = "hybrid"
        elif any(k in lower for k in ["local only", "embedded", "firmware", "desktop only", "offline only"]):
            deployment_model = "local"
        elif any(k in lower for k in ["on-prem", "on-premises", "private cloud", "air-gapped"]):
            deployment_model = "on_premises"
        elif any(k in lower for k in ["hybrid", "edge"]):
            deployment_model = "hybrid"
        else:
            deployment_model = "cloud"

        # Determine Data Sensitivity
        if any(k in lower for k in ["hipaa", "pci", "credit card", "medical", "secret", "financial", "biometric"]):
            data_sensitivity = "restricted"
        elif any(k in lower for k in ["auth", "user account", "password", "customer", "billing"]):
            data_sensitivity = "confidential"
        elif any(k in lower for k in ["internal", "employee", "intranet"]):
            data_sensitivity = "internal"
        else:
            data_sensitivity = "public" if primary_type == "mini_website" else "internal"

        # Determine Reliability Tier
        if any(k in lower for k in ["mission critical", "life safety", "high frequency", "99.99"]):
            reliability_tier = "mission_critical_99_99"
        elif any(k in lower for k in ["high availability", "enterprise", "sla", "99.9"]):
            reliability_tier = "high_99_9"
        else:
            reliability_tier = "standard_99_0"

        # Determine complexity
        complexity = self._derive_complexity(lower, primary_family, len(matched_types))

        # Build conditional profiles
        conditional_profiles = self._build_conditional_profiles(primary_family, matched_types, lower)

        return ProjectProfile(
            project_id=slug_id,
            project_name=project_name,
            primary_family=primary_family,
            primary_type=primary_type,
            secondary_types=secondary,
            supporting_types=supporting,
            supporting_disciplines=supporting_disciplines,
            classification_confidence=confidence,
            classification_rationale=rationale,
            ambiguity_flags=ambiguity_flags,
            complexity=complexity,
            delivery_targets=sorted(list(delivery_targets)),
            deployment_model=deployment_model,
            ai_dependency=ai_dependency,
            data_sensitivity=data_sensitivity,
            reliability_tier=reliability_tier,
            unresolved_questions=unresolved_questions,
            conditional_profiles=conditional_profiles,
        )

    def classify_repository(self, repo_path: Path, project_name: Optional[str] = None) -> ProjectProfile:
        repo_path = Path(repo_path)
        name = project_name or repo_path.name
        detected_text = []

        # Inspect package manifests and files
        checks = {
            "package.json": "web_app nodejs javascript typescript",
            "pubspec.yaml": "flutter mobile app cross-platform",
            "Cargo.toml": "rust systems tool cli desktop",
            "requirements.txt": "python backend data ml",
            "pyproject.toml": "python application tool",
            "Dockerfile": "containers_cloud docker deployment",
            "Makefile": "systems build tool",
            "CMakeLists.txt": "c++ native systems embedded desktop",
            "pom.xml": "java enterprise backend",
            "go.mod": "golang microservices backend distributed",
        }

        for fname, desc in checks.items():
            if (repo_path / fname).exists():
                detected_text.append(desc)

        # Inspect key directory structures
        if (repo_path / "android").exists() or (repo_path / "ios").exists():
            detected_text.append("mobile application native android ios")
        if (repo_path / "kernel").exists() or (repo_path / "drivers").exists():
            detected_text.append("linux distribution kernel module device driver")
        if (repo_path / "firmware").exists() or (repo_path / "embedded").exists():
            detected_text.append("freertos firmware microcontroller embedded")

        text_corpus = " ".join(detected_text) or name
        return self.classify_text(text_corpus, project_name=name)

    def _derive_complexity(self, text: str, family: str, matched_types_count: int) -> ProjectComplexity:
        if family in ("operating_systems_and_systems", "embedded_hardware_and_robotics"):
            return ProjectComplexity("LARGE", "Low-level hardware/kernel engineering requires deep verification and isolation")
        if re.search(r"\bmini\b|\blanding\b|\bportfolio\b", text):
            return ProjectComplexity("MINI", "Focused landing page or mini-site with minimal state")
        if matched_types_count >= 3:
            return ProjectComplexity("LARGE", "Multi-discipline hybrid project spanning multiple platform types")
        if "enterprise" in text or "distributed" in text or "compliance" in text:
            return ProjectComplexity("ENTERPRISE", "Enterprise regulatory, security, and scalability requirements")
        if "research" in text or "simulation" in text:
            return ProjectComplexity("RESEARCH_EXPERIMENTAL", "Experimental algorithm exploration and numerical verification")
        return ProjectComplexity("MEDIUM", "Standard modular application scope")

    def _build_conditional_profiles(self, primary_family: str, matched_types: List[str], text: str) -> Dict[str, Any]:
        profiles: Dict[str, Any] = {}
        all_types = set(matched_types)

        if "rag_knowledge_system" in all_types or "autonomous_agent_system" in all_types or "ai" in text:
            profiles["ai"] = {
                "model_family": "gpt-6",
                "rag_enabled": "rag" in text or "rag_knowledge_system" in all_types,
                "agentic_tools": "agent" in text or "autonomous_agent_system" in all_types,
                "safety_evaluations": ["prompt_injection_eval", "citation_groundedness"],
            }

        if "classical_ml_pipeline" in all_types or "deep_learning_cv_nlp" in all_types or "ml" in text:
            profiles["ml"] = {
                "target_variable": "predictive_target",
                "data_provenance": "verified_dataset_split",
                "leakage_controls": True,
                "baseline_model": "heuristic_or_linear_baseline",
                "drift_monitoring": True,
            }

        if "data_science_study" in all_types:
            profiles["data_science"] = {
                "hypothesis": "exploratory_correlation_hypothesis",
                "statistical_methods": ["t_test", "pearson_correlation"],
                "eda_visualizations": True,
                "reproducibility_seed": 42,
            }

        if "etl_pipeline" in all_types:
            profiles["data_engineering"] = {
                "pipeline_type": "hybrid",
                "source_connectors": ["relational_db", "event_stream"],
                "storage_layer": "lakehouse_parquet",
                "idempotency_guarantee": True,
            }

        if "linux_distribution" in all_types or "kernel_driver_module" in all_types:
            profiles["os_systems"] = {
                "target_arch": "x86_64",
                "kernel_base": "linux-lts",
                "bootloader": "grub",
                "init_system": "systemd",
                "build_environment": "containerized_chroot",
            }

        if "rtos_firmware" in all_types or "robotics_platform" in all_types:
            profiles["embedded_hardware"] = {
                "target_mcu": "arm_cortex_m4",
                "rtos": "freertos",
                "memory_limit_kb": 256,
                "firmware_update_strategy": "dual_bank_ota",
            }

        if "cross_platform_mobile" in all_types or "native_android" in all_types or "native_ios" in all_types:
            profiles["mobile"] = {
                "platforms": ["android", "ios"],
                "offline_storage": True,
                "push_notifications": True,
                "deep_linking": True,
            }

        if "cross_platform_desktop" in all_types or "native_desktop_tool" in all_types:
            profiles["desktop"] = {
                "framework": "tauri",
                "auto_update": True,
                "code_signing": True,
            }

        return profiles
