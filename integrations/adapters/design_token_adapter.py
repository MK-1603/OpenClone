"""
OpenClone Design Token Adapter (Derived from UI-001 design-md-chrome)
Extracts, normalizes, and generates design tokens in Markdown and JSON formats.
"""

import json
from typing import Dict, Any, List


class DesignTokenAdapter:
    """Adapter for web design token extraction and normalization."""

    def __init__(self, theme_name: str = "default"):
        self.theme_name = theme_name

    def normalize_tokens(self, raw_tokens: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw CSS/computed properties into standard design tokens."""
        colors = raw_tokens.get("colors", {})
        typography = raw_tokens.get("typography", {})
        spacing = raw_tokens.get("spacing", {})

        return {
            "version": "1.0.0",
            "theme": self.theme_name,
            "tokens": {
                "color": {
                    "background": colors.get("background", "#ffffff"),
                    "foreground": colors.get("foreground", "#0f172a"),
                    "primary": colors.get("primary", "#0284c7"),
                    "muted": colors.get("muted", "#64748b"),
                    "border": colors.get("border", "#e2e8f0"),
                },
                "typography": {
                    "font_family_sans": typography.get("font_family", "system-ui, -apple-system, sans-serif"),
                    "font_size_base": typography.get("font_size_base", "16px"),
                    "line_height_base": typography.get("line_height_base", "1.5"),
                },
                "spacing": spacing or {"unit": "4px", "scale": [0, 4, 8, 12, 16, 24, 32, 48, 64]},
            },
        }

    def to_markdown(self, tokens: Dict[str, Any]) -> str:
        """Render normalized tokens as Markdown documentation."""
        t = tokens.get("tokens", {})
        colors = t.get("color", {})
        typo = t.get("typography", {})

        md = [
            f"# Design Tokens: {tokens.get('theme', 'Default')}",
            "",
            "## Colors",
            "| Token | Value | Sample |",
            "|---|---|---|",
        ]
        for k, v in colors.items():
            md.append(f"| `color.{k}` | `{v}` | `{v}` |")

        md.extend([
            "",
            "## Typography",
            f"- **Font Family:** `{typo.get('font_family_sans')}`",
            f"- **Base Size:** `{typo.get('font_size_base')}`",
            f"- **Base Line Height:** `{typo.get('line_height_base')}`",
        ])
        return "\n".join(md)
