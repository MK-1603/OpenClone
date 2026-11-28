"""OpenClone Core System Architecture.

Provides global lifecycle state management, event orchestration, and subsystem coordination.
"""
from __future__ import annotations

import enum
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

logger = logging.getLogger("openclone.core.system")


class SystemState(str, enum.Enum):
    BOOTSTRAP = "BOOTSTRAP"
    INITIALIZING = "INITIALIZING"
    READY = "READY"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    FAILED = "FAILED"


@dataclass
class SystemEvent:
    event_type: str
    source: str
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class EventBus:
    """Synchronous lightweight pub/sub event bus."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[SystemEvent], None]]] = {}

    def subscribe(self, event_type: str, callback: Callable[[SystemEvent], None]) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event: SystemEvent) -> None:
        listeners = self._subscribers.get(event.event_type, [])
        for cb in listeners:
            try:
                cb(event)
            except Exception as e:
                logger.error(f"Error dispatching event {event.event_type} to listener: {e}")

        # Also emit to wildcard subscribers
        for cb in self._subscribers.get("*", []):
            try:
                cb(event)
            except Exception as e:
                logger.error(f"Error dispatching wildcard event {event.event_type}: {e}")


class OpenCloneCore:
    """Central singleton coordinator for OpenClone platform runtime."""

    _instance: Optional["OpenCloneCore"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, workspace_root: Optional[Path] = None):
        if getattr(self, "_initialized", False):
            return
        self.workspace_root = Path(workspace_root or Path.cwd()).resolve()
        self.state = SystemState.BOOTSTRAP
        self.event_bus = EventBus()
        self.subsystems: Dict[str, Any] = {}
        self.start_time = time.time()
        self._initialized = True
        logger.info(f"OpenCloneCore initialized at {self.workspace_root}")

    def register_subsystem(self, name: str, instance: Any) -> None:
        """Register a core subsystem instance."""
        self.subsystems[name] = instance
        self.event_bus.publish(SystemEvent("subsystem:registered", "core", {"name": name}))

    def get_subsystem(self, name: str) -> Optional[Any]:
        return self.subsystems.get(name)

    def transition_state(self, new_state: SystemState, reason: str = "") -> None:
        """Transition system state and broadcast event."""
        old_state = self.state
        self.state = new_state
        logger.info(f"SystemState transition: {old_state.value} -> {new_state.value} ({reason})")
        self.event_bus.publish(
            SystemEvent(
                "system:state_changed",
                "core",
                {"from": old_state.value, "to": new_state.value, "reason": reason},
            )
        )

    def health_check(self) -> Dict[str, Any]:
        """Aggregate health check across all registered subsystems."""
        subsystem_health = {}
        all_healthy = True

        for name, sub in self.subsystems.items():
            if hasattr(sub, "health_check") and callable(sub.health_check):
                try:
                    res = sub.health_check()
                    subsystem_health[name] = res
                    if isinstance(res, dict) and res.get("status") in ("FAILED", "UNHEALTHY", "DEGRADED"):
                        all_healthy = False
                except Exception as e:
                    subsystem_health[name] = {"status": "ERROR", "error": str(e)}
                    all_healthy = False
            else:
                subsystem_health[name] = {"status": "REGISTERED", "type": type(sub).__name__}

        return {
            "status": "HEALTHY" if all_healthy else "DEGRADED",
            "system_state": self.state.value,
            "uptime_seconds": round(time.time() - self.start_time, 2),
            "workspace": str(self.workspace_root),
            "subsystems_count": len(self.subsystems),
            "subsystems": subsystem_health,
        }
