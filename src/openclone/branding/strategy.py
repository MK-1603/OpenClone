"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — Strategy Engine.

Translates verified brand briefs into positioning statements, archetypes,
differentiation pillars, and visual identity trajectories.
"""

from __future__ import annotations

from typing import List

from src.openclone.branding.models import BrandBrief, BrandStrategy, LogoCategory


class BrandStrategyEngine:
    """Translates brand brief into formal visual strategy."""

    @classmethod
    def formulate(cls, brief: BrandBrief, documented_assumptions: List[str]) -> BrandStrategy:
        """Formulate strategic brand positioning and visual trajectory."""
        # Determine brand archetype from personality and values
        traits_str = " ".join(brief.personality_traits).lower()
        if any(w in traits_str for w in ["authority", "governed", "discipline", "ruler", "standard"]):
            archetype = "The Ruler / The Architect (Order, Engineering Control, Reliability)"
        elif any(w in traits_str for w in ["precision", "expert", "sage", "intellect", "scientific"]):
            archetype = "The Sage (Rigorous Truth, Deep Verification, Accuracy)"
        else:
            archetype = "The Creator (Constructive Power, Innovation, Architecture)"

        positioning = (
            f"For {brief.target_audience} who demand uncompromising standards, "
            f"{brief.brand_name} is the {brief.category} that delivers {brief.positioning}."
        )

        differentiation = [
            f"Deterministic engineering rigor over decorative visual fluff.",
            f"Mathematical construction and verified contrast compliance.",
            f"Universal multi-environment adaptability across terminals, IDEs, and print.",
        ]

        # Recommended logo categories based on archetype & technical domain
        recommended_categories = [
            LogoCategory.COMBINATION_MARK,
            LogoCategory.GEOMETRIC_MARK,
            LogoCategory.EMBLEM,
        ]

        visual_direction = (
            f"High-contrast, geometric precision with architectural structure. "
            f"Crisp lines, deliberate optical weighting, and zero unanchored AI gradient blobs."
        )

        typography_direction = (
            f"Clean neo-grotesque or geometric sans-serif for high legibility at micro-scales, "
            f"paired with a disciplined monospace or humanist sans for secondary metadata."
        )

        color_strategy = (
            f"Authoritative deep primary tone paired with an energetic electric accent and "
            f"high-contrast neutral light and dark canvases (minimum 4.5:1 WCAG contrast)."
        )

        return BrandStrategy(
            positioning_statement=positioning,
            brand_archetype=archetype,
            core_attributes=brief.personality_traits[:4],
            differentiation_factors=differentiation,
            visual_direction=visual_direction,
            recommended_categories=recommended_categories,
            typography_direction=typography_direction,
            color_strategy=color_strategy,
            documented_assumptions=documented_assumptions,
        )
