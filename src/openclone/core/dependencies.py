"""OpenClone Dependency Graph Analyzer.

Validates internal and external dependencies, checks version constraints,
detects circular dependencies, and reports ecosystem health.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("openclone.core.dependencies")


class DependencyType(str, Enum):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"
    OPTIONAL = "OPTIONAL"


@dataclass
class DependencyNode:
    name: str
    version: str = "1.0.0"
    node_type: DependencyType = DependencyType.INTERNAL
    dependencies: List[str] = field(default_factory=list)


class DependencyGraphAnalyzer:
    """Analyzes and validates dependency graphs for cycles and missing components."""

    def __init__(self):
        self.nodes: Dict[str, DependencyNode] = {}

    def add_node(self, name: str, dependencies: Optional[List[str]] = None, version: str = "1.0.0", node_type: DependencyType = DependencyType.INTERNAL) -> None:
        self.nodes[name] = DependencyNode(
            name=name,
            version=version,
            node_type=node_type,
            dependencies=dependencies or [],
        )

    def detect_cycles(self) -> List[List[str]]:
        """Detect circular dependencies using DFS graph traversal."""
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        cycles: List[List[str]] = []

        def dfs(node_name: str, path: List[str]):
            visited.add(node_name)
            rec_stack.add(node_name)
            path.append(node_name)

            node = self.nodes.get(node_name)
            if node:
                for neighbor in node.dependencies:
                    if neighbor not in self.nodes:
                        continue
                    if neighbor not in visited:
                        dfs(neighbor, list(path))
                    elif neighbor in rec_stack:
                        cycle = path[path.index(neighbor):] + [neighbor]
                        cycles.append(cycle)

            rec_stack.remove(node_name)

        for name in self.nodes:
            if name not in visited:
                dfs(name, [])

        return cycles

    def find_missing_dependencies(self) -> Dict[str, List[str]]:
        """Identify undeclared or missing dependency targets."""
        missing: Dict[str, List[str]] = {}
        for name, node in self.nodes.items():
            unresolved = [dep for dep in node.dependencies if dep not in self.nodes]
            if unresolved:
                missing[name] = unresolved
        return missing

    def topological_order(self) -> List[str]:
        """Compute valid initialization order for nodes."""
        in_degree = {name: 0 for name in self.nodes}
        adj = {name: [] for name in self.nodes}

        for name, node in self.nodes.items():
            for dep in node.dependencies:
                if dep in self.nodes:
                    adj[dep].append(name)
                    in_degree[name] += 1

        queue = [name for name, deg in in_degree.items() if deg == 0]
        order = []

        while queue:
            curr = queue.pop(0)
            order.append(curr)
            for nxt in adj[curr]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    queue.append(nxt)

        if len(order) != len(self.nodes):
            logger.warning("Dependency cycle detected while computing topological order")
        return order

    def health_check(self) -> Dict[str, Any]:
        cycles = self.detect_cycles()
        missing = self.find_missing_dependencies()
        return {
            "status": "HEALTHY" if not cycles and not missing else "DEGRADED",
            "total_nodes": len(self.nodes),
            "cycles_detected": len(cycles),
            "cycles": cycles,
            "missing_dependencies_count": len(missing),
            "missing_dependencies": missing,
        }
