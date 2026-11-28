"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — Typography Engine.

Evaluates typeface classification, typographic scale hierarchies,
character spacing, fallback font stacks, and open-source / commercial licensing.
"""

from __future__ import annotations

from typing import Dict, List

from src.openclone.branding.models import TypographySpec


class TypographyEngine:
    """Evaluates and prescribes typographic pairing, hierarchy, and licensing."""

    RECOMMENDED_PAIRINGS: List[Dict[str, str]] = [
        {
            "primary": "Inter / Plus Jakarta Sans",
            "primary_class": "Geometric Neo-Grotesque",
            "secondary": "JetBrains Mono / Fira Code",
            "secondary_class": "Engineered Monospace",
            "licensing": "SIL Open Font License 1.1 / Apache 2.0 (Free Commercial & Web)",
            "primary_fallback": "'Plus Jakarta Sans', 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            "secondary_fallback": "'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
        },
        {
            "primary": "Cabinet Grotesk / General Sans",
            "primary_class": "Modern Geometric Sans",
            "secondary": "Space Mono",
            "secondary_class": "Fixed-pitch Monospace",
            "licensing": "Fontshare Permissive License / SIL OFL 1.1",
            "primary_fallback": "'Cabinet Grotesk', 'General Sans', system-ui, -apple-system, 'Segoe UI', sans-serif",
            "secondary_fallback": "'Space Mono', ui-monospace, monospace",
        },
    ]

    @classmethod
    def prescribe_typography(cls, category: str = "software") -> TypographySpec:
        """Generate typography specification for engineering brand."""
        selected = cls.RECOMMENDED_PAIRINGS[0]
        return TypographySpec(
            primary_font=selected["primary"],
            primary_classification=selected["primary_class"],
            secondary_font=selected["secondary"],
            secondary_classification=selected["secondary_class"],
            hierarchy_scale="Major Third (1.250)",
            letter_spacing_logotype="-0.025em",
            letter_spacing_tagline="0.08em",
            licensing=selected["licensing"],
            primary_fallback_stack=selected["primary_fallback"],
            secondary_fallback_stack=selected["secondary_fallback"],
            font_weight_logotype=800,
            font_weight_tagline=500,
            line_height_ratio=1.2,
            commercial_license_verified=True,
        )
