"""OpenClone Core Architecture & Foundation.

Defines OpenCloneCore, ModuleManager, UnifiedCapabilityRegistry, and DependencyGraphAnalyzer.
"""
from __future__ import annotations

from src.openclone.core.system import OpenCloneCore, SystemState, SystemEvent, EventBus
from src.openclone.core.modules import ModuleManager, ModuleMetadata, ModuleState
from src.openclone.core.capabilities import UnifiedCapabilityRegistry, CoreCapability
from src.openclone.core.dependencies import DependencyGraphAnalyzer, DependencyNode, DependencyType

__all__ = [
    "OpenCloneCore",
    "SystemState",
    "SystemEvent",
    "EventBus",
    "ModuleManager",
    "ModuleMetadata",
    "ModuleState",
    "UnifiedCapabilityRegistry",
    "CoreCapability",
    "DependencyGraphAnalyzer",
    "DependencyNode",
    "DependencyType",
]
