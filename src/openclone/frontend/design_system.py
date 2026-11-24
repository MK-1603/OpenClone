"""Design System Engineering & Token Management Engine.

Manages 3-tier token hierarchy (Primitive -> Semantic -> Component)
and theme mode persistence (Light / Dark / System).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class TokenHierarchy(str, Enum):
    PRIMITIVE = "primitive"
    SEMANTIC = "semantic"
    COMPONENT = "component"


class ThemeMode(str, Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


@dataclass
class DesignToken:
    name: str
    hierarchy: TokenHierarchy
    value: str
    referenced_token: Optional[str] = None
    description: str = ""


class DesignTokenManager:
    """Validates and resolves design token architectures."""

    def __init__(self):
        self.primitives: Dict[str, DesignToken] = {}
        self.semantics: Dict[str, DesignToken] = {}
        self.components: Dict[str, DesignToken] = {}

    def register_primitive(self, name: str, value: str, description: str = "") -> DesignToken:
        token = DesignToken(name=name, hierarchy=TokenHierarchy.PRIMITIVE, value=value, description=description)
        self.primitives[name] = token
        return token

    def register_semantic(self, name: str, referenced_primitive: str, fallback_value: str = "", description: str = "") -> DesignToken:
        value = self.primitives[referenced_primitive].value if referenced_primitive in self.primitives else fallback_value
        token = DesignToken(
            name=name,
            hierarchy=TokenHierarchy.SEMANTIC,
            value=value,
            referenced_token=referenced_primitive,
            description=description,
        )
        self.semantics[name] = token
        return token

    def register_component_token(self, name: str, referenced_semantic: str, fallback_value: str = "", description: str = "") -> DesignToken:
        value = self.semantics[referenced_semantic].value if referenced_semantic in self.semantics else fallback_value
        token = DesignToken(
            name=name,
            hierarchy=TokenHierarchy.COMPONENT,
            value=value,
            referenced_token=referenced_semantic,
            description=description,
        )
        self.components[name] = token
        return token

    def validate_architecture(self) -> Dict[str, Any]:
        """Audits token architecture for broken references or bypasses."""
        unresolved_semantics = [t.name for t in self.semantics.values() if t.referenced_token not in self.primitives]
        unresolved_components = [t.name for t in self.components.values() if t.referenced_token not in self.semantics]

        is_valid = len(unresolved_semantics) == 0 and len(unresolved_components) == 0

        return {
            "primitive_count": len(self.primitives),
            "semantic_count": len(self.semantics),
            "component_count": len(self.components),
            "is_valid": is_valid,
            "unresolved_semantics": unresolved_semantics,
            "unresolved_components": unresolved_components,
        }
