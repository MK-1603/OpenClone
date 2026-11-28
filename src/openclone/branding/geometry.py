"""OpenClone Logo Engineering & Brand Identity System (LEBIS) — Geometry Engine.

Calculates mathematical proportions (Golden Ratio, Root-2), baseline grid
alignments, clear-space buffer zones, coordinate bounding boxes, and
minimum legibility thresholds across all production variants.
"""

from __future__ import annotations

import math
from typing import Any, Dict

from src.openclone.branding.models import GeometryRules, VariantGeometry, VariantType


class GeometryEngine:
    """Enforces mathematical geometry, grid construction, coordinate layouts, and clearance rules."""

    GOLDEN_RATIO = 1.6180339887
    ROOT_TWO = 1.4142135623

    @classmethod
    def calculate_rules(
        cls,
        grid_unit_px: int = 8,
        min_digital_width_px: int = 24,
    ) -> GeometryRules:
        """Derive standard geometric construction rules with layout specs for all variants."""
        subgrid = max(2, grid_unit_px // 2)
        macrogrid = grid_unit_px * 8

        # Define exact coordinate geometry for each canonical variant
        geometries: Dict[str, VariantGeometry] = {
            VariantType.PRIMARY.value: VariantGeometry(
                variant_type=VariantType.PRIMARY,
                width=900,
                height=260,
                view_box="0 0 900 260",
                mark_origin_x=40.0,
                mark_origin_y=45.0,
                mark_scale=1.7,
                text_origin_x=250.0,
                text_origin_y=135.0,
                text_font_size=76.0,
                tagline_origin_x=254.0,
                tagline_origin_y=175.0,
                tagline_font_size=20.0,
                clear_space_box=cls.compute_clear_space_box(900.0, 260.0, 0.25),
            ),
            VariantType.HORIZONTAL.value: VariantGeometry(
                variant_type=VariantType.HORIZONTAL,
                width=500,
                height=120,
                view_box="0 0 500 120",
                mark_origin_x=20.0,
                mark_origin_y=15.0,
                mark_scale=0.9,
                text_origin_x=135.0,
                text_origin_y=74.0,
                text_font_size=48.0,
                clear_space_box=cls.compute_clear_space_box(500.0, 120.0, 0.25),
            ),
            VariantType.VERTICAL.value: VariantGeometry(
                variant_type=VariantType.VERTICAL,
                width=320,
                height=360,
                view_box="0 0 320 360",
                mark_origin_x=85.0,
                mark_origin_y=40.0,
                mark_scale=1.5,
                text_origin_x=160.0,
                text_origin_y=260.0,
                text_font_size=44.0,
                clear_space_box=cls.compute_clear_space_box(320.0, 360.0, 0.25),
            ),
            VariantType.SYMBOL_ONLY.value: VariantGeometry(
                variant_type=VariantType.SYMBOL_ONLY,
                width=200,
                height=200,
                view_box="0 0 200 200",
                mark_origin_x=25.0,
                mark_origin_y=25.0,
                mark_scale=1.5,
                text_origin_x=0.0,
                text_origin_y=0.0,
                text_font_size=0.0,
                clear_space_box=cls.compute_clear_space_box(200.0, 200.0, 0.25),
            ),
            VariantType.MONOCHROME_DARK.value: VariantGeometry(
                variant_type=VariantType.MONOCHROME_DARK,
                width=500,
                height=120,
                view_box="0 0 500 120",
                mark_origin_x=20.0,
                mark_origin_y=15.0,
                mark_scale=0.9,
                text_origin_x=135.0,
                text_origin_y=74.0,
                text_font_size=48.0,
                clear_space_box=cls.compute_clear_space_box(500.0, 120.0, 0.25),
            ),
            VariantType.MONOCHROME_LIGHT.value: VariantGeometry(
                variant_type=VariantType.MONOCHROME_LIGHT,
                width=500,
                height=120,
                view_box="0 0 500 120",
                mark_origin_x=20.0,
                mark_origin_y=15.0,
                mark_scale=0.9,
                text_origin_x=135.0,
                text_origin_y=74.0,
                text_font_size=48.0,
                clear_space_box=cls.compute_clear_space_box(500.0, 120.0, 0.25),
            ),
            VariantType.FAVICON.value: VariantGeometry(
                variant_type=VariantType.FAVICON,
                width=32,
                height=32,
                view_box="0 0 32 32",
                mark_origin_x=0.0,
                mark_origin_y=0.0,
                mark_scale=1.0,
                text_origin_x=0.0,
                text_origin_y=0.0,
                text_font_size=0.0,
                clear_space_box=cls.compute_clear_space_box(32.0, 32.0, 0.125),
            ),
            VariantType.SOCIAL_PREVIEW.value: VariantGeometry(
                variant_type=VariantType.SOCIAL_PREVIEW,
                width=1280,
                height=640,
                view_box="0 0 1280 640",
                mark_origin_x=100.0,
                mark_origin_y=180.0,
                mark_scale=2.8,
                text_origin_x=440.0,
                text_origin_y=310.0,
                text_font_size=108.0,
                tagline_origin_x=448.0,
                tagline_origin_y=375.0,
                tagline_font_size=32.0,
                clear_space_box=cls.compute_clear_space_box(1280.0, 640.0, 0.25),
            ),
        }

        return GeometryRules(
            grid_unit_px=grid_unit_px,
            proportion_ratio_name="Golden Ratio (1.618)",
            proportion_ratio_value=cls.GOLDEN_RATIO,
            clear_space_factor=0.25,
            min_digital_width_px=min_digital_width_px,
            min_print_width_mm=10.0,
            symmetry_notes="Bilateral symmetry along central vertical axis with optical compensation.",
            subgrid_unit_px=subgrid,
            macro_unit_px=macrogrid,
            variant_geometries=geometries,
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
