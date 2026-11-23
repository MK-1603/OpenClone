"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — Typography Engine.

Evaluates typeface classification, typographic scale hierarchies,
character spacing, and open-source / commercial licensing considerations.
"""

from __future__ import annotations

from typing import Dict, List

from src.openclone.branding.models import TypographySpec


class TypographyEngine:
    """Evaluates and prescribes typographic pairing and licensing."""

    RECOMMENDED_PAIRINGS: List[Dict[str, str]] = [
        {
            "primary": "Inter / Plus Jakarta Sans",
            "primary_class": "Geometric Neo-Grotesque",
            "secondary": "JetBrains Mono / Fira Code",
            "secondary_class": "Engineered Monospace",
            "licensing": "SIL Open Font License 1.1 / Apache 2.0 (Free Commercial & Web)",
        },
        {
            "primary": "Cabinet Grotesk / General Sans",
            "primary_class": "Modern Geometric Sans",
            "secondary": "Space Mono",
            "secondary_class": "Fixed-pitch Monospace",
            "licensing": "Fontshare Permissive License / SIL OFL 1.1",
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
        )
