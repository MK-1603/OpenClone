"""OpenClone Multi-Label Project Classifier."""
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
    classification_confidence: float = 1.0
    classification_rationale: str = ""
    ambiguity_flags: List[str] = field(default_factory=list)
    complexity: ProjectComplexity = field(default_factory=lambda: ProjectComplexity("MEDIUM", "Standard modular scope"))
    delivery_targets: List[str] = field(default_factory=lambda: ["web_browser"])
    conditional_profiles: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "primary_family": self.primary_family,
            "primary_type": self.primary_type,
            "secondary_types": self.secondary_types,
            "supporting_types": self.supporting_types,
            "classification_confidence": round(self.classification_confidence, 2),
            "classification_rationale": self.classification_rationale,
            "ambiguity_flags": self.ambiguity_flags,
            "complexity": {
                "level": self.complexity.level,
                "rationale": self.complexity.rationale,
            },
            "delivery_targets": self.delivery_targets,
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
            "enterprise_platform": ["enterprise platform", "portal", "internal tool", "compliance platform"],
        },
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

        # Fallback if no keywords matched
        if not matched_types:
            primary_family = "web_engineering"
            primary_type = "saas_web_app"
            confidence = 0.5
            rationale = "No specialized keywords matched; default SaaS web application inferred."
            ambiguity_flags = ["no_explicit_domain_keywords_detected"]
        else:
            # First matched type is primary unless high-scoring family indicates otherwise
            best_family = max(family_scores.keys(), key=lambda k: family_scores[k])
            # Find first matched type belonging to best_family
            best_type = next((t for t in matched_types if self.taxonomy.get_family_for_type(t) == best_family), matched_types[0])
            primary_type = best_type
            primary_family = best_family
            confidence = min(0.95, 0.65 + 0.1 * len(matched_types))
            rationale = f"Matched {len(matched_types)} domain keywords across {len(family_scores)} project families."
            ambiguity_flags = [] if len(matched_types) <= 3 else ["multi_domain_hybrid_project"]

        secondary = [t for t in matched_types if t != primary_type][:3]
        supporting = [t for t in matched_types if t != primary_type and t not in secondary]

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
            classification_confidence=confidence,
            classification_rationale=rationale,
            ambiguity_flags=ambiguity_flags,
            complexity=complexity,
            delivery_targets=sorted(list(delivery_targets)),
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
        if "mini" in text or "landing page" in text or "portfolio" in text:
            return ProjectComplexity("MINI", "Focused landing page or mini-site with minimal state")
        if family in ("operating_systems_and_systems", "embedded_hardware_and_robotics"):
            return ProjectComplexity("LARGE", "Low-level hardware/kernel engineering requires deep verification and isolation")
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
