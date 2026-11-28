"""Frontend Typography Intelligence & Font Registry Engine.

Manages font family registries, verified open-source / commercial licensing metadata,
modular type scales (Major Third 1.250), semantic typography tokens, fluid clamp() formulas,
and cross-platform system fallback stacks.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class FontCategory(str, Enum):
    """Broad typographic classifications."""
    NEO_GROTESQUE = "neo-grotesque"
    GEOMETRIC_SANS = "geometric-sans"
    HUMANIST_SANS = "humanist-sans"
    MONOSPACE = "monospace"
    SERIF = "serif"
    DISPLAY = "display"


class FontAvailability(str, Enum):
    """Runtime availability status of a typeface."""
    SYSTEM_LOCAL = "system_local"      # Built into OS (Apple, Windows, Android)
    LOADABLE_WEB = "loadable_web"      # Permissive Google Font or self-hosted WOFF2
    PROPRIETARY = "proprietary"        # Requires licensed commercial binary


@dataclass
class FontEntry:
    """Detailed font registry record with explicit licensing and embedding rules."""
    family: str
    category: FontCategory
    source: str
    available_weights: List[int]
    license_name: str
    license_verified: bool
    commercial_usable: bool
    embedding_restrictions: str
    availability_status: FontAvailability
    fallback_stack: str


class FontRegistry:
    """Curates, verifies, and resolves fonts with explicit licensing tracking."""

    def __init__(self):
        self.fonts: Dict[str, FontEntry] = {}
        self._populate_canonical_fonts()

    def _populate_canonical_fonts(self):
        """Register canonical verified fonts for software interfaces."""
        # 1. Plus Jakarta Sans (Geometric Neo-Grotesque)
        self.register_font(
            family="Plus Jakarta Sans",
            category=FontCategory.GEOMETRIC_SANS,
            source="Google Fonts / GitHub (Tokotype)",
            available_weights=[400, 500, 600, 700, 800],
            license_name="SIL Open Font License 1.1",
            license_verified=True,
            commercial_usable=True,
            embedding_restrictions="None (OFL permissive commercial web and desktop use)",
            availability_status=FontAvailability.LOADABLE_WEB,
            fallback_stack="'Plus Jakarta Sans', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        )

        # 2. Inter (Neo-Grotesque Screen Standard)
        self.register_font(
            family="Inter",
            category=FontCategory.NEO_GROTESQUE,
            source="Rasmus Andersson / Google Fonts",
            available_weights=[300, 400, 500, 600, 700, 800, 900],
            license_name="SIL Open Font License 1.1",
            license_verified=True,
            commercial_usable=True,
            embedding_restrictions="None (OFL permissive commercial use)",
            availability_status=FontAvailability.LOADABLE_WEB,
            fallback_stack="'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif",
        )

        # 3. JetBrains Mono (Engineered Technical Monospace)
        self.register_font(
            family="JetBrains Mono",
            category=FontCategory.MONOSPACE,
            source="JetBrains",
            available_weights=[400, 500, 700, 800],
            license_name="OFL 1.1 / Apache 2.0",
            license_verified=True,
            commercial_usable=True,
            embedding_restrictions="None (Permissive open source)",
            availability_status=FontAvailability.LOADABLE_WEB,
            fallback_stack="'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
        )

        # 4. Fira Code (Monospace with Programming Ligatures)
        self.register_font(
            family="Fira Code",
            category=FontCategory.MONOSPACE,
            source="Nikita Prokopov / Mozilla",
            available_weights=[400, 500, 600, 700],
            license_name="SIL Open Font License 1.1",
            license_verified=True,
            commercial_usable=True,
            embedding_restrictions="None (OFL permissive)",
            availability_status=FontAvailability.LOADABLE_WEB,
            fallback_stack="'Fira Code', 'Cascadia Code', ui-monospace, monospace",
        )

        # 5. System UI Sans (Zero Latency Native Stack)
        self.register_font(
            family="system-ui",
            category=FontCategory.NEO_GROTESQUE,
            source="Host Operating System",
            available_weights=[400, 500, 600, 700],
            license_name="Host OS Native Runtime",
            license_verified=True,
            commercial_usable=True,
            embedding_restrictions="None (Native system resource)",
            availability_status=FontAvailability.SYSTEM_LOCAL,
            fallback_stack="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
        )

    def register_font(
        self,
        family: str,
        category: FontCategory,
        source: str,
        available_weights: List[int],
        license_name: str,
        license_verified: bool,
        commercial_usable: bool,
        embedding_restrictions: str,
        availability_status: FontAvailability,
        fallback_stack: str,
    ) -> FontEntry:
        """Register a font family with audited licensing constraints."""
        entry = FontEntry(
            family=family,
            category=category,
            source=source,
            available_weights=available_weights,
            license_name=license_name,
            license_verified=license_verified,
            commercial_usable=commercial_usable,
            embedding_restrictions=embedding_restrictions,
            availability_status=availability_status,
            fallback_stack=fallback_stack,
        )
        self.fonts[family.lower()] = entry
        return entry

    def get_font(self, family: str) -> Optional[FontEntry]:
        """Lookup font entry by name case-insensitively."""
        return self.fonts.get(family.lower())


class TypographyIntelligenceEngine:
    """Derives modular scales, semantic typography tokens, and fluid clamp() styles."""

    SCALE_RATIOS = {
        "minor_second": 1.067,
        "major_second": 1.125,
        "minor_third": 1.200,
        "major_third": 1.250,   # Standard for B2B SaaS and technical dashboards
        "perfect_fourth": 1.333, # For high-contrast editorial and marketing
        "golden_ratio": 1.618,
    }

    @classmethod
    def generate_modular_scale(
        cls,
        base_px: float = 16.0,
        scale_name: str = "major_third",
        steps_up: int = 5,
        steps_down: int = 2,
    ) -> Dict[str, Dict[str, Any]]:
        """Calculate exact rem and px sizes along a mathematical modular scale."""
        ratio = cls.SCALE_RATIOS.get(scale_name, 1.250)
        tokens: Dict[str, Dict[str, Any]] = {}

        # Downward steps (e.g. caption, small)
        for i in range(steps_down, 0, -1):
            val_px = round(base_px / math.pow(ratio, i), 1)
            rem = round(val_px / 16.0, 3)
            key = f"step_down_{i}"
            tokens[key] = {"px": val_px, "rem": f"{rem}rem", "ratio": ratio}

        # Base step
        tokens["step_0_base"] = {"px": base_px, "rem": "1.0rem", "ratio": 1.0}

        # Upward steps (headings, titles)
        for i in range(1, steps_up + 1):
            val_px = round(base_px * math.pow(ratio, i), 1)
            rem = round(val_px / 16.0, 3)
            key = f"step_up_{i}"
            tokens[key] = {"px": val_px, "rem": f"{rem}rem", "ratio": ratio}

        return tokens

    @classmethod
    def generate_semantic_tokens(cls) -> Dict[str, Dict[str, str]]:
        """Produce standard semantic typography tokens mapped to responsive variables."""
        return {
            "text-display": {
                "font_size": "clamp(2.25rem, 1.8rem + 2.5vw, 3.25rem)",
                "font_weight": "800",
                "line_height": "1.15",
                "letter_spacing": "-0.03em",
                "role": "Large hero statements and marketing display",
            },
            "text-heading-1": {
                "font_size": "clamp(1.75rem, 1.5rem + 1.5vw, 2.25rem)",
                "font_weight": "800",
                "line_height": "1.20",
                "letter_spacing": "-0.025em",
                "role": "Primary page title (H1)",
            },
            "text-heading-2": {
                "font_size": "clamp(1.5rem, 1.3rem + 1.0vw, 1.875rem)",
                "font_weight": "700",
                "line_height": "1.25",
                "letter_spacing": "-0.02em",
                "role": "Section header (H2)",
            },
            "text-heading-3": {
                "font_size": "clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)",
                "font_weight": "600",
                "line_height": "1.30",
                "letter_spacing": "-0.015em",
                "role": "Subsection header (H3) and card headings",
            },
            "text-body": {
                "font_size": "1.0rem",
                "font_weight": "400",
                "line_height": "1.50",
                "letter_spacing": "0.0em",
                "role": "Standard body copy and input field values",
            },
            "text-body-small": {
                "font_size": "0.875rem",
                "font_weight": "400",
                "line_height": "1.40",
                "letter_spacing": "0.0em",
                "role": "Secondary description and table cell text",
            },
            "text-caption": {
                "font_size": "0.75rem",
                "font_weight": "500",
                "line_height": "1.35",
                "letter_spacing": "+0.02em",
                "role": "Metadata, timestamps, and badge tags",
            },
            "text-code": {
                "font_size": "0.875rem",
                "font_weight": "500",
                "line_height": "1.45",
                "letter_spacing": "0.0em",
                "role": "Code snippets, telemetry, and tabular numbers",
            },
        }

    @staticmethod
    def generate_fluid_clamp(min_px: float, max_px: float, min_vw: float = 375.0, max_vw: float = 1440.0) -> str:
        """Derive pure mathematical CSS clamp() formula between two viewport bounds."""
        min_rem = round(min_px / 16.0, 3)
        max_rem = round(max_px / 16.0, 3)

        slope = (max_px - min_px) / (max_vw - min_vw)
        y_intercept = min_px - (slope * min_vw)
        y_intercept_rem = round(y_intercept / 16.0, 3)
        slope_vw = round(slope * 100.0, 2)

        return f"clamp({min_rem}rem, {y_intercept_rem}rem + {slope_vw}vw, {max_rem}rem)"
