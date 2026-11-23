"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — Geometry Engine.

Calculates mathematical proportions (Golden Ratio, Root-2), baseline grid
alignments, clear-space buffer zones, and minimum legibility thresholds.
"""

from __future__ import annotations

import math
from typing import Dict, Tuple

from src.openclone.branding.models import GeometryRules


class GeometryEngine:
    """Enforces mathematical geometry, grid construction, and clearance rules."""

    GOLDEN_RATIO = 1.6180339887
    ROOT_TWO = 1.4142135623

    @classmethod
    def calculate_rules(
        cls,
        grid_unit_px: int = 8,
        min_digital_width_px: int = 24,
    ) -> GeometryRules:
        """Derive standard geometric construction rules."""
        return GeometryRules(
            grid_unit_px=grid_unit_px,
            proportion_ratio_name="Golden Ratio (1.618)",
            proportion_ratio_value=cls.GOLDEN_RATIO,
            clear_space_factor=0.25,
            min_digital_width_px=min_digital_width_px,
            min_print_width_mm=10.0,
            symmetry_notes="Bilateral symmetry along central vertical axis with optical compensation.",
        )

    @classmethod
    def compute_clear_space_box(
        cls,
        width: float,
        height: float,
        clear_space_factor: float = 0.25,
    ) -> Dict[str, float]:
        """Compute the exclusion / clear space bounding box around a mark."""
        x_buffer = width * clear_space_factor
        y_buffer = height * clear_space_factor
        return {
            "origin_x": -x_buffer,
            "origin_y": -y_buffer,
            "padded_width": width + (2 * x_buffer),
            "padded_height": height + (2 * y_buffer),
            "clear_buffer_px": round(min(x_buffer, y_buffer), 1),
        }
