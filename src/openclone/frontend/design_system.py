"""Design System Engineering & Token Management Engine.

Manages 3-tier token hierarchy (Primitive -> Semantic -> Component),
circular dependency detection, brand token ingestion, token compilation to CSS/Tailwind,
and theme mode persistence (Light / Dark / System).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class TokenHierarchy(str, Enum):
    """3-Tier Token Architecture."""
    PRIMITIVE = "primitive"
    SEMANTIC = "semantic"
    COMPONENT = "component"


class ThemeMode(str, Enum):
    """Supported theme modes."""
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class TokenStatus(str, Enum):
    """Lifecycle status of a design token."""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    EXPERIMENTAL = "experimental"


@dataclass
class DesignToken:
    """Canonical design token model with full metadata and lifecycle tracking."""
    name: str
    hierarchy: TokenHierarchy
    value: str
    referenced_token: Optional[str] = None
    description: str = ""
    category: str = "general"  # color, typography, spacing, radius, shadow, motion, z-index
    token_id: str = ""
    version: str = "1.0.0"
    status: TokenStatus = TokenStatus.ACTIVE
    deprecated_by: Optional[str] = None

    def __post_init__(self):
        if not self.token_id:
            clean_name = self.name.lstrip("-").replace("/", "-")
            self.token_id = f"tok-{self.hierarchy.value[:3]}-{clean_name}"


class DesignTokenManager:
    """Validates, resolves, compiles, and governs design token architectures."""

    def __init__(self):
        self.primitives: Dict[str, DesignToken] = {}
        self.semantics: Dict[str, DesignToken] = {}
        self.components: Dict[str, DesignToken] = {}
        self.theme_overrides: Dict[ThemeMode, Dict[str, str]] = {
            ThemeMode.LIGHT: {},
            ThemeMode.DARK: {},
            ThemeMode.SYSTEM: {},
        }

    # --- Registration Methods ---

    def register_primitive(
        self,
        name: str,
        value: str,
        description: str = "",
        category: str = "general",
    ) -> DesignToken:
        """Register a raw primitive value."""
        token = DesignToken(
            name=name,
            hierarchy=TokenHierarchy.PRIMITIVE,
            value=value,
            description=description,
            category=category,
        )
        self.primitives[name] = token
        return token

    def register_semantic(
        self,
        name: str,
        referenced_primitive: str,
        fallback_value: str = "",
        description: str = "",
        category: str = "general",
    ) -> DesignToken:
        """Register an intent-driven semantic token mapping to a primitive."""
        value = self.primitives[referenced_primitive].value if referenced_primitive in self.primitives else fallback_value
        token = DesignToken(
            name=name,
            hierarchy=TokenHierarchy.SEMANTIC,
            value=value,
            referenced_token=referenced_primitive,
            description=description,
            category=category,
        )
        self.semantics[name] = token
        return token

    def register_component_token(
        self,
        name: str,
        referenced_semantic: str,
        fallback_value: str = "",
        description: str = "",
        category: str = "component",
    ) -> DesignToken:
        """Register a scoped component-level token referencing a semantic token."""
        value = self.semantics[referenced_semantic].value if referenced_semantic in self.semantics else fallback_value
        token = DesignToken(
            name=name,
            hierarchy=TokenHierarchy.COMPONENT,
            value=value,
            referenced_token=referenced_semantic,
            description=description,
            category=category,
        )
        self.components[name] = token
        return token

    def deprecate_token(self, name: str, replacement_name: str) -> bool:
        """Mark an existing token as deprecated with an explicit successor."""
        for store in (self.components, self.semantics, self.primitives):
            if name in store:
                store[name].status = TokenStatus.DEPRECATED
                store[name].deprecated_by = replacement_name
                return True
        return False

    # --- Resolution & Circular Dependency Detection ---

    def resolve_token(self, name: str, visited: Optional[Set[str]] = None) -> Optional[str]:
        """Recursively resolve token value through references, detecting circular chains."""
        if visited is None:
            visited = set()

        if name in visited:
            raise RecursionError(f"Circular dependency detected in design token resolution chain: {name}")

        visited.add(name)

        # Lookup in component -> semantic -> primitive
        token = self.components.get(name) or self.semantics.get(name) or self.primitives.get(name)
        if not token:
            return None

        if token.referenced_token:
            resolved = self.resolve_token(token.referenced_token, visited)
            if resolved is not None:
                token.value = resolved
                return resolved

        return token.value

    def validate_architecture(self) -> Dict[str, Any]:
        """Audits token architecture for broken references, circularity, and completeness."""
        unresolved_semantics = [t.name for t in self.semantics.values() if t.referenced_token not in self.primitives]
        unresolved_components = [t.name for t in self.components.values() if t.referenced_token not in self.semantics]

        # Check for circular chains across all tokens
        has_circular = False
        circular_details = []
        for name in list(self.components.keys()) + list(self.semantics.keys()):
            try:
                self.resolve_token(name)
            except RecursionError as e:
                has_circular = True
                circular_details.append(str(e))

        is_valid = (
            len(unresolved_semantics) == 0
            and len(unresolved_components) == 0
            and not has_circular
        )

        return {
            "primitive_count": len(self.primitives),
            "semantic_count": len(self.semantics),
            "component_count": len(self.components),
            "is_valid": is_valid,
            "unresolved_semantics": unresolved_semantics,
            "unresolved_components": unresolved_components,
            "circular_dependencies": circular_details,
        }

    # --- Brand Token Ingestion ---

    def ingest_brand_tokens(self, brand_spec: Dict[str, Any]) -> None:
        """Ingest approved brand identity parameters (from LEBIS) without polluting product tokens."""
        colors = brand_spec.get("color", {})
        prim_hex = colors.get("primary_hex", "#2563EB")
        sec_hex = colors.get("secondary_hex", "#0F172A")
        acc_hex = colors.get("accent_hex", "#38BDF8")

        # Register brand primitives
        self.register_primitive("brand-color-primary", prim_hex, "Approved brand primary color", category="color")
        self.register_primitive("brand-color-secondary", sec_hex, "Approved brand secondary color", category="color")
        self.register_primitive("brand-color-accent", acc_hex, "Approved brand accent highlight", category="color")

        # Map to semantic brand tokens
        self.register_semantic("color-brand-primary", "brand-color-primary", prim_hex, "Brand primary action", category="color")
        self.register_semantic("color-brand-secondary", "brand-color-secondary", sec_hex, "Brand secondary background", category="color")
        self.register_semantic("color-brand-accent", "brand-color-accent", acc_hex, "Brand accent element", category="color")

    # --- Standard Token Set Population ---

    def populate_standard_tokens(self) -> None:
        """Populate the canonical OpenClone 8px spatial grid, surfaces, and typography tokens."""
        # 1. Spacing Primitives
        spacings = {
            "space-0": "0px",
            "space-1": "4px",
            "space-2": "8px",
            "space-3": "12px",
            "space-4": "16px",
            "space-6": "24px",
            "space-8": "32px",
            "space-12": "48px",
            "space-16": "64px",
            "space-24": "96px",
        }
        for k, v in spacings.items():
            self.register_primitive(k, v, f"Spatial grid unit {v}", category="spacing")

        # 2. Surface & Palette Primitives
        palettes = {
            "palette-obsidian-950": "#0B0F19",
            "palette-obsidian-900": "#12151B",
            "palette-obsidian-800": "#181C24",
            "palette-obsidian-700": "#202632",
            "palette-cobalt-600": "#2563EB",
            "palette-cobalt-500": "#3B82F6",
            "palette-cyan-400": "#38BDF8",
            "palette-emerald-500": "#10B981",
            "palette-amber-500": "#F59E0B",
            "palette-crimson-500": "#EF4444",
            "palette-slate-50": "#F8FAFC",
            "palette-slate-400": "#94A3B8",
            "palette-slate-600": "#475569",
            "palette-white": "#FFFFFF",
        }
        for k, v in palettes.items():
            self.register_primitive(k, v, f"Color primitive {k}", category="color")

        # 3. Semantic Surfaces & Text
        self.register_semantic("surface-base", "palette-obsidian-950", "#0B0F19", "Root background canvas ground", category="color")
        self.register_semantic("surface-1", "palette-obsidian-900", "#12151B", "Primary container card surface", category="color")
        self.register_semantic("surface-2", "palette-obsidian-800", "#181C24", "Secondary panel and table header", category="color")
        self.register_semantic("surface-elevated", "palette-obsidian-700", "#202632", "Raised cards and hover elevation", category="color")
        self.register_semantic("action-primary", "palette-cobalt-600", "#2563EB", "Primary call to action surface", category="color")
        self.register_semantic("focus-ring", "palette-cobalt-500", "#3B82F6", "Visible high-contrast focus ring", category="color")
        self.register_semantic("text-primary", "palette-slate-50", "#F8FAFC", "High-contrast primary body text", category="color")
        self.register_semantic("text-secondary", "palette-slate-400", "#94A3B8", "Subdued secondary copy and captions", category="color")
        self.register_semantic("status-success", "palette-emerald-500", "#10B981", "Affirmative confirmation state", category="color")
        self.register_semantic("status-warning", "palette-amber-500", "#F59E0B", "Cautionary alert notice", category="color")
        self.register_semantic("status-error", "palette-crimson-500", "#EF4444", "Error validation indicator", category="color")

        # 4. Component Tokens
        self.register_component_token("button-primary-bg", "action-primary", "#2563EB", "Background fill for primary button")
        self.register_component_token("input-focus-border", "focus-ring", "#3B82F6", "Border color on focused input")
        self.register_component_token("card-background", "surface-1", "#12151B", "Standard card container background")

        # 5. Tactile Micro-Interactions & Elevation Tokens (2028 Premium Standard)
        self.register_primitive("shadow-bevel-top", "inset 0 1px 0 0 rgba(255, 255, 255, 0.25)", "Specular light catch on top border", category="elevation")
        self.register_primitive("shadow-bevel-bottom", "inset 0 -1px 0 0 rgba(0, 0, 0, 0.35)", "Physical depression rim on bottom", category="elevation")
        self.register_primitive("shadow-button-glow", "0 0 0 1px #2563EB, 0 1px 2px 0 rgba(0, 0, 0, 0.4), 0 8px 24px -4px rgba(37, 99, 235, 0.45)", "Ambient photonic aura on primary action", category="elevation")
        self.register_primitive("shadow-glass-surface", "0 8px 32px 0 rgba(0, 0, 0, 0.36), inset 0 1px 0 0 rgba(255, 255, 255, 0.08)", "Deep frosted glass elevation with rim highlight", category="elevation")
        self.register_primitive("transition-tactile", "all 0.18s cubic-bezier(0.16, 1, 0.3, 1)", "High-fidelity micro-spring transition curve", category="motion")

    # --- Compiler & Exporters ---

    def export_css_variables(self, mode: ThemeMode = ThemeMode.DARK) -> str:
        """Compile active tokens into standard-compliant CSS Custom Properties."""
        lines = [":root {"]

        # 1. Primitives
        lines.append("  /* --- Primitive Tokens --- */")
        for name, tok in sorted(self.primitives.items()):
            lines.append(f"  --{name}: {tok.value};")

        # 2. Semantics
        lines.append("\n  /* --- Semantic Tokens --- */")
        for name, tok in sorted(self.semantics.items()):
            if tok.referenced_token:
                lines.append(f"  --{name}: var(--{tok.referenced_token});")
            else:
                lines.append(f"  --{name}: {tok.value};")

        # 3. Component Tokens
        lines.append("\n  /* --- Component Tokens --- */")
        for name, tok in sorted(self.components.items()):
            if tok.referenced_token:
                lines.append(f"  --{name}: var(--{tok.referenced_token});")
            else:
                lines.append(f"  --{name}: {tok.value};")

        lines.append("}")
        return "\n".join(lines)

    def export_tailwind_config(self) -> Dict[str, Any]:
        """Compile resolved semantic and primitive tokens into a Tailwind theme extension dictionary."""
        colors: Dict[str, str] = {}
        for name, tok in self.semantics.items():
            if tok.category == "color":
                colors[name.replace("color-", "")] = f"var(--{name})"

        spacing: Dict[str, str] = {}
        for name, tok in self.primitives.items():
            if tok.category == "spacing":
                key = name.replace("space-", "")
                spacing[key] = f"var(--{name})"

        return {
            "theme": {
                "extend": {
                    "colors": colors,
                    "spacing": spacing,
                }
            }
        }

    def export_token_dictionary(self) -> Dict[str, Any]:
        """Return the normalized dictionary containing all token tiers and metadata."""
        return {
            "primitives": {
                name: {
                    "token_id": t.token_id,
                    "value": t.value,
                    "category": t.category,
                    "description": t.description,
                    "status": t.status.value,
                }
                for name, t in self.primitives.items()
            },
            "semantics": {
                name: {
                    "token_id": t.token_id,
                    "value": t.value,
                    "referenced_token": t.referenced_token,
                    "category": t.category,
                    "description": t.description,
                    "status": t.status.value,
                }
                for name, t in self.semantics.items()
            },
            "components": {
                name: {
                    "token_id": t.token_id,
                    "value": t.value,
                    "referenced_token": t.referenced_token,
                    "category": t.category,
                    "description": t.description,
                    "status": t.status.value,
                }
                for name, t in self.components.items()
            },
        }

    def export_markdown_documentation(self) -> str:
        """Produce structured markdown documentation of all tokens."""
        lines = [
            "# OpenClone Design Tokens Catalogue",
            "**Governed Token Architecture:** Primitive -> Semantic -> Component",
            "",
            "## 1. Semantic Tokens",
            "| Token Name | Reference | Computed Value | Category | Description |",
            "|---|---|---|---|---|",
        ]
        for name, t in sorted(self.semantics.items()):
            ref = f"`--{t.referenced_token}`" if t.referenced_token else "—"
            lines.append(f"| `--{name}` | {ref} | `{t.value}` | `{t.category}` | {t.description} |")

        lines.extend([
            "",
            "## 2. Component Tokens",
            "| Component Token | Reference | Category | Description |",
            "|---|---|---|---|",
        ])
        for name, t in sorted(self.components.items()):
            ref = f"`--{t.referenced_token}`" if t.referenced_token else "—"
            lines.append(f"| `--{name}` | {ref} | `{t.category}` | {t.description} |")

        return "\n".join(lines)
