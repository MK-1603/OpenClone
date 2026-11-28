"""OpenClone Module Management Engine.

Provides explicit lifecycle states, dynamic module discovery, dependency validation,
activation, and failure rollback.
"""
from __future__ import annotations

import enum
import importlib
import logging
import pkgutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger("openclone.core.modules")


class ModuleState(str, enum.Enum):
    DISCOVERED = "DISCOVERED"
    VALIDATED = "VALIDATED"
    REGISTERED = "REGISTERED"
    INITIALIZED = "INITIALIZED"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    DEACTIVATED = "DEACTIVATED"


@dataclass
class ModuleMetadata:
    module_id: str
    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = "OpenClone Contributors"
    dependencies: List[str] = field(default_factory=list)
    optional_dependencies: List[str] = field(default_factory=list)
    capabilities_provided: List[str] = field(default_factory=list)
    state: ModuleState = ModuleState.DISCOVERED
    error_message: Optional[str] = None
    package_path: Optional[str] = None
    entrypoint: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module_id": self.module_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "dependencies": self.dependencies,
            "capabilities_provided": self.capabilities_provided,
            "state": self.state.value,
            "error_message": self.error_message,
        }


class ModuleManager:
    """Manages the lifecycle of OpenClone modular subsystems."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = Path(workspace_root or Path.cwd()).resolve()
        self.modules: Dict[str, ModuleMetadata] = {}
        self.active_instances: Dict[str, Any] = {}
        self._register_known_internal_modules()

    def _register_known_internal_modules(self) -> None:
        """Register the authoritative canonical modules of OpenClone."""
        known = [
            ModuleMetadata(
                module_id="openclone.core",
                name="OpenClone Core System",
                version="1.0.0",
                description="Core application lifecycle, module engine, and event coordination",
                capabilities_provided=["core.lifecycle", "core.events", "core.modules"],
                state=ModuleState.ACTIVE,
            ),
            ModuleMetadata(
                module_id="openclone.planning",
                name="Planning & Architecture Engine",
                version="1.0.0",
                description="OpenClone Planning Agent, Socratic Clarification, and PlanBuilder",
                dependencies=["openclone.core", "openclone.intelligence"],
                capabilities_provided=["planning.orchestration", "planning.dag", "planning.clarification"],
                state=ModuleState.ACTIVE,
            ),
            ModuleMetadata(
                module_id="openclone.intelligence",
                name="Project Intelligence Architect",
                version="1.0.0",
                description="Four-Set Intelligence (Sets A, B, C, D) and project discovery",
                dependencies=["openclone.core"],
                capabilities_provided=["intelligence.discovery", "intelligence.architecture", "intelligence.sets_a_to_d"],
                state=ModuleState.ACTIVE,
            ),
            ModuleMetadata(
                module_id="openclone.engineering",
                name="Engineering Intelligence System",
                version="2.0.0",
                description="23 Engineering Domains, Knowledge Graph, Role Registry, and EPSE",
                dependencies=["openclone.core"],
                capabilities_provided=["engineering.graph", "engineering.domains", "engineering.problem_solving"],
                state=ModuleState.ACTIVE,
            ),
            ModuleMetadata(
                module_id="openclone.connectors",
                name="Universal AI Assistant Connector",
                version="1.0.0",
                description="7 Platform Adapters (ChatGPT, Claude, Gemini, Z.ai, Mistral, WebUI, LibreChat)",
                dependencies=["openclone.core", "openclone.integrations"],
                capabilities_provided=["connectors.mcp_http", "connectors.mcp_sse", "connectors.function_calling"],
                state=ModuleState.ACTIVE,
            ),
            ModuleMetadata(
                module_id="openclone.reverse_engineering",
                name="Reverse Engineering Intelligence",
                version="1.0.0",
                description="Static polyglot repository inspection, AST analysis, and technical debt scoring",
                dependencies=["openclone.core"],
                capabilities_provided=["reverse_engineering.ast", "reverse_engineering.inspectors"],
                state=ModuleState.ACTIVE,
            ),
            ModuleMetadata(
                module_id="openclone.system_design",
                name="System Design & Capacity Engine",
                version="1.0.0",
                description="Quantitative capacity modeling, C4 Mermaid diagrams, and architectural decisions",
                dependencies=["openclone.core"],
                capabilities_provided=["system_design.capacity", "system_design.c4_diagrams", "system_design.decisions"],
                state=ModuleState.ACTIVE,
            ),
            ModuleMetadata(
                module_id="openclone.memory",
                name="Memory Intelligence System (OMIS)",
                version="1.0.0",
                description="Dual-tier SQLite audit ledger and Markdown vault storage with semantic retrieval",
                dependencies=["openclone.core"],
                capabilities_provided=["memory.sqlite", "memory.vault", "memory.retrieval"],
                state=ModuleState.ACTIVE,
            ),
            ModuleMetadata(
                module_id="openclone.runtime",
                name="Workforce Runtime & Ledger",
                version="1.0.0",
                description="73-worker role control plane, topological DAG sort, and tamper-evident ledger",
                dependencies=["openclone.core"],
                capabilities_provided=["runtime.workforce", "runtime.ledger", "runtime.gates"],
                state=ModuleState.ACTIVE,
            ),
            ModuleMetadata(
                module_id="openclone.security",
                name="Security & Governance Engine",
                version="1.0.0",
                description="Loopback network firewall, STRIDE threat modeling, and secret redaction",
                dependencies=["openclone.core"],
                capabilities_provided=["security.firewall", "security.redaction", "security.governance"],
                state=ModuleState.ACTIVE,
            ),
        ]
        for meta in known:
            self.modules[meta.module_id] = meta

    def discover_modules(self) -> List[ModuleMetadata]:
        """Discover modules in the openclone namespace."""
        import openclone
        discovered: List[ModuleMetadata] = []

        if hasattr(openclone, "__path__"):
            for _, name, is_pkg in pkgutil.iter_modules(openclone.__path__):
                mod_id = f"openclone.{name}"
                if mod_id not in self.modules:
                    meta = ModuleMetadata(
                        module_id=mod_id,
                        name=f"OpenClone {name.replace('_', ' ').title()}",
                        state=ModuleState.DISCOVERED,
                        package_path=str(self.workspace_root / "src" / "openclone" / name),
                    )
                    self.modules[mod_id] = meta
                    discovered.append(meta)

        return list(self.modules.values())

    def validate_module(self, module_id: str) -> bool:
        """Validate module requirements and dependencies."""
        if module_id not in self.modules:
            logger.error(f"Cannot validate unknown module {module_id}")
            return False

        meta = self.modules[module_id]
        missing_deps = [dep for dep in meta.dependencies if dep not in self.modules]
        if missing_deps:
            meta.state = ModuleState.FAILED
            meta.error_message = f"Missing required dependencies: {', '.join(missing_deps)}"
            return False

        meta.state = ModuleState.VALIDATED
        return True

    def initialize_module(self, module_id: str) -> bool:
        """Initialize a validated module."""
        if module_id not in self.modules:
            return False
        meta = self.modules[module_id]

        if meta.state not in (ModuleState.VALIDATED, ModuleState.REGISTERED, ModuleState.ACTIVE):
            if not self.validate_module(module_id):
                return False

        try:
            # Try importing package
            importlib.import_module(module_id)
            meta.state = ModuleState.INITIALIZED
            return True
        except Exception as e:
            meta.state = ModuleState.FAILED
            meta.error_message = f"Initialization import failed: {e}"
            return False

    def activate_module(self, module_id: str) -> bool:
        """Activate initialized module for runtime consumption."""
        if module_id not in self.modules:
            return False
        meta = self.modules[module_id]

        if meta.state != ModuleState.INITIALIZED and meta.state != ModuleState.ACTIVE:
            if not self.initialize_module(module_id):
                return False

        meta.state = ModuleState.ACTIVE
        return True

    def rollback_module(self, module_id: str) -> None:
        """Rollback module to safe state upon failure."""
        if module_id in self.modules:
            meta = self.modules[module_id]
            meta.state = ModuleState.ROLLED_BACK
            logger.warning(f"Module {module_id} rolled back")

    def list_modules(self, state: Optional[ModuleState] = None) -> List[ModuleMetadata]:
        if state:
            return [m for m in self.modules.values() if m.state == state]
        return list(self.modules.values())

    def health_check(self) -> Dict[str, Any]:
        total = len(self.modules)
        active = sum(1 for m in self.modules.values() if m.state == ModuleState.ACTIVE)
        failed = sum(1 for m in self.modules.values() if m.state == ModuleState.FAILED)
        return {
            "status": "HEALTHY" if failed == 0 else "DEGRADED",
            "total_modules": total,
            "active_modules": active,
            "failed_modules": failed,
        }
