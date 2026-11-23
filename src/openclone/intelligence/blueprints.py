"""OpenClone Project Family Blueprint Manager."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parents[3]
BLUEPRINTS_DIR = ROOT / "blueprints"


class BlueprintManager:
    """Discovers, parses, and provides project-family engineering blueprints."""

    BLUEPRINT_INDEX: Dict[str, Dict[str, str]] = {
        "01-MINI-WEBSITE": {
            "title": "Mini Website & Landing Page Blueprint",
            "family": "web_engineering",
            "file": "01-MINI-WEBSITE.md",
            "description": "High-performance marketing, documentation, and portfolio sites with minimal complexity.",
        },
        "02-SAAS-WEB-APP": {
            "title": "SaaS Web Application Blueprint",
            "family": "web_engineering",
            "file": "02-SAAS-WEB-APP.md",
            "description": "Multi-tenant web products with authentication, database persistence, billing, and APIs.",
        },
        "03-MOBILE-APP": {
            "title": "Mobile Application Blueprint",
            "family": "mobile_engineering",
            "file": "03-MOBILE-APP.md",
            "description": "Native and cross-platform mobile apps for Android and iOS with offline-first state.",
        },
        "04-DESKTOP-APP": {
            "title": "Desktop Application Blueprint",
            "family": "desktop_engineering",
            "file": "04-DESKTOP-APP.md",
            "description": "Tauri/Electron/Native desktop software with local filesystem access and code signing.",
        },
        "05-AI-AGENT-RAG": {
            "title": "AI Agent & RAG System Blueprint",
            "family": "ai_engineering",
            "file": "05-AI-AGENT-RAG.md",
            "description": "Retrieval-Augmented Generation, vector embeddings, prompt safety, and tool-calling agents.",
        },
        "06-MACHINE-LEARNING": {
            "title": "Machine Learning Engineering Blueprint",
            "family": "machine_learning",
            "file": "06-MACHINE-LEARNING.md",
            "description": "Feature engineering, reproducible training pipelines, model validation, and MLOps serving.",
        },
        "07-DATA-SCIENCE": {
            "title": "Data Science & Statistical Analysis Blueprint",
            "family": "data_engineering_and_data_science",
            "file": "07-DATA-SCIENCE.md",
            "description": "Exploratory data analysis, statistical hypotheses, reproducible notebooks, and insights.",
        },
        "08-DATA-ENGINEERING": {
            "title": "Data Engineering & Pipeline Blueprint",
            "family": "data_engineering_and_data_science",
            "file": "08-DATA-ENGINEERING.md",
            "description": "Idempotent ETL/ELT pipelines, schema evolution, dead-letter queues, and lakehouses.",
        },
        "09-BACKEND-DISTRIBUTED": {
            "title": "Backend & Distributed Systems Blueprint",
            "family": "backend_and_distributed_systems",
            "file": "09-BACKEND-DISTRIBUTED.md",
            "description": "High-throughput APIs, event-driven streaming, microservices, and distributed tracing.",
        },
        "10-LINUX-OS": {
            "title": "Linux Distribution & Systems Engineering Blueprint",
            "family": "operating_systems_and_systems",
            "file": "10-LINUX-OS.md",
            "description": "Kernel modules, device drivers, initramfs, package management, and bootable ISO builds.",
        },
        "11-EMBEDDED-IOT": {
            "title": "Embedded Systems, Firmware & Robotics Blueprint",
            "family": "embedded_hardware_and_robotics",
            "file": "11-EMBEDDED-IOT.md",
            "description": "RTOS firmware, bare-metal C/Rust, sensor bus communication, and robotics control loops.",
        },
        "12-GAME-SIMULATION": {
            "title": "Game & Simulation Engineering Blueprint",
            "family": "game_and_simulation",
            "file": "12-GAME-SIMULATION.md",
            "description": "2D/3D games, entity-component systems, physics simulations, and graphics asset pipelines.",
        },
        "13-DEVELOPER-TOOLS-COMPILER": {
            "title": "Developer Tools, CLI & Compiler Blueprint",
            "family": "developer_tools_and_languages",
            "file": "13-DEVELOPER-TOOLS-COMPILER.md",
            "description": "Terminal CLI tools, language toolchains, AST parsers, SDK libraries, and conformance suites.",
        },
        "14-RESEARCH-SCIENTIFIC": {
            "title": "Research & Scientific Software Blueprint",
            "family": "research_and_scientific_computing",
            "file": "14-RESEARCH-SCIENTIFIC.md",
            "description": "Computational physics, numerical precision, differential solvers, and scientific data platforms.",
        },
    }

    def __init__(self, blueprints_dir: Optional[Path] = None):
        self.blueprints_dir = blueprints_dir or BLUEPRINTS_DIR

    def list_blueprints(self) -> List[Dict[str, Any]]:
        res = []
        for bp_id, meta in self.BLUEPRINT_INDEX.items():
            path = self.blueprints_dir / meta["file"]
            res.append({
                "id": bp_id,
                "title": meta["title"],
                "family": meta["family"],
                "file": meta["file"],
                "description": meta["description"],
                "exists": path.exists(),
            })
        return res

    def get_blueprint(self, bp_id_or_file: str) -> Optional[str]:
        # Direct lookup by ID
        if bp_id_or_file in self.BLUEPRINT_INDEX:
            path = self.blueprints_dir / self.BLUEPRINT_INDEX[bp_id_or_file]["file"]
            if path.exists():
                return path.read_text(encoding="utf-8")
        # Direct lookup by filename
        path = self.blueprints_dir / bp_id_or_file
        if path.exists():
            return path.read_text(encoding="utf-8")
        return None
