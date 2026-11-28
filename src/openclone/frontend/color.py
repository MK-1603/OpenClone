"""Frontend Color Intelligence & Accessibility Verification Engine.

Provides exact mathematical WCAG 2.1 / 2.2 AA contrast calculations,
element-type context validation (normal text, large text, graphical controls, disabled states),
HSL conversions, and documented CMYK print approximations.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class ElementType(str, Enum):
    """UI element classification for accessibility contrast thresholds."""
    NORMAL_TEXT = "normal_text"      # < 18pt or < 14pt bold (Requires >= 4.5:1)
    LARGE_TEXT = "large_text"        # >= 18pt or >= 14pt bold (Requires >= 3.0:1)
    UI_COMPONENT = "ui_component"    # Graphical objects, buttons, input borders (Requires >= 3.0:1)
    DISABLED = "disabled"            # Inactive controls (WCAG 1.4.3 Incidental Exception)


@dataclass
class ContrastValidationResult:
    """Detailed mathematical contrast evaluation outcome."""
    foreground_hex: str
    background_hex: str
    element_type: ElementType
    contrast_ratio: float
    required_ratio: float
    passed: bool
    verdict: str  # PASS, FAIL, EXEMPT
    luminance_fg: float
    luminance_bg: float
    explanation: str
    recommendations: List[str] = field(default_factory=list)


class ColorIntelligenceEngine:
    """Mathematical color intelligence and WCAG 2.2 accessibility verification."""

    @staticmethod
    def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
        """Convert a 3 or 6 character hex code to RGB tuple."""
        clean = hex_code.lstrip("#").strip()
        if len(clean) == 3:
            clean = "".join([c * 2 for c in clean])
        if len(clean) != 6:
            raise ValueError(f"Invalid hex color code: '{hex_code}'")
        return int(clean[0:2], 16), int(clean[2:4], 16), int(clean[4:6], 16)

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Convert RGB integers (0-255) to 6-character hex code."""
        r = max(0, min(255, int(r)))
        g = max(0, min(255, int(g)))
        b = max(0, min(255, int(b)))
        return f"#{r:02X}{g:02X}{b:02X}"

    @classmethod
    def relative_luminance(cls, r: int, g: int, b: int) -> float:
        """Calculate exact WCAG relative luminance according to W3C formula."""
        def channel_lum(val: int) -> float:
            c = val / 255.0
            return c / 12.92 if c <= 0.03928 else math.pow((c + 0.055) / 1.055, 2.4)

        return 0.2126 * channel_lum(r) + 0.7152 * channel_lum(g) + 0.0722 * channel_lum(b)

    @classmethod
    def calculate_contrast_ratio(cls, hex1: str, hex2: str) -> float:
        """Calculate WCAG 2.1 contrast ratio between two hex colors."""
        rgb1 = cls.hex_to_rgb(hex1)
        rgb2 = cls.hex_to_rgb(hex2)
        l1 = cls.relative_luminance(*rgb1)
        l2 = cls.relative_luminance(*rgb2)
        lighter = max(l1, l2)
        darker = min(l1, l2)
        ratio = (lighter + 0.05) / (darker + 0.05)
        return round(ratio, 4)

    @classmethod
    def validate_contrast(
        cls,
        fg_hex: str,
        bg_hex: str,
        element_type: ElementType = ElementType.NORMAL_TEXT,
    ) -> ContrastValidationResult:
        """Evaluate a foreground/background pair against element-specific WCAG criteria."""
        rgb_fg = cls.hex_to_rgb(fg_hex)
        rgb_bg = cls.hex_to_rgb(bg_hex)
        l_fg = cls.relative_luminance(*rgb_fg)
        l_bg = cls.relative_luminance(*rgb_bg)

        ratio = cls.calculate_contrast_ratio(fg_hex, bg_hex)
        recommendations = []

        if element_type == ElementType.NORMAL_TEXT:
            required = 4.5
            passed = ratio >= required
            verdict = "PASS" if passed else "FAIL"
            explanation = f"Normal text requires >= 4.5:1. Calculated: {ratio:.2f}:1."
            if not passed:
                recommendations.append(
                    f"Contrast {ratio:.2f}:1 is insufficient for normal text on '{bg_hex}'. "
                    f"Increase foreground brightness for dark backgrounds or darken for light backgrounds."
                )

        elif element_type in (ElementType.LARGE_TEXT, ElementType.UI_COMPONENT):
            required = 3.0
            passed = ratio >= required
            verdict = "PASS" if passed else "FAIL"
            explanation = f"{element_type.value.replace('_', ' ').title()} requires >= 3.0:1 (WCAG 1.4.11 / 1.4.3). Calculated: {ratio:.2f}:1."
            if not passed:
                recommendations.append(
                    f"Contrast {ratio:.2f}:1 is insufficient for UI controls/large text. Target at least 3.0:1."
                )

        elif element_type == ElementType.DISABLED:
            required = 0.0  # Exempt under WCAG 1.4.3 (Incidental)
            passed = True
            verdict = "EXEMPT"
            explanation = f"Disabled controls are exempt from WCAG 1.4.3 minimums (Calculated: {ratio:.2f}:1)."
            if ratio < 1.5:
                recommendations.append("Disabled control contrast is very low (<1.5:1); consider slight contrast increase for readability.")

        else:
            required = 4.5
            passed = ratio >= required
            verdict = "PASS" if passed else "FAIL"
            explanation = f"Default contrast evaluation against 4.5:1. Calculated: {ratio:.2f}:1."

        return ContrastValidationResult(
            foreground_hex=fg_hex,
            background_hex=bg_hex,
            element_type=element_type,
            contrast_ratio=round(ratio, 2),
            required_ratio=required,
            passed=passed,
            verdict=verdict,
            luminance_fg=round(l_fg, 6),
            luminance_bg=round(l_bg, 6),
            explanation=explanation,
            recommendations=recommendations,
        )

    # --- Color Conversion Helpers ---

    @classmethod
    def rgb_to_hsl(cls, r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Convert sRGB (0-255) to HSL (H: 0-360, S: 0-100%, L: 0-100%)."""
        rf = r / 255.0
        gf = g / 255.0
        bf = b / 255.0
        cmax = max(rf, gf, bf)
        cmin = min(rf, gf, bf)
        delta = cmax - cmin

        # Luminance
        l = (cmax + cmin) / 2.0

        if delta == 0:
            h = 0.0
            s = 0.0
        else:
            s = delta / (1.0 - abs(2.0 * l - 1.0))
            if cmax == rf:
                h = ((gf - bf) / delta) % 6
            elif cmax == gf:
                h = ((bf - rf) / delta) + 2
            else:
                h = ((rf - gf) / delta) + 4
            h *= 60.0

        return round(h, 1), round(s * 100.0, 1), round(l * 100.0, 1)

    @classmethod
    def rgb_to_cmyk_documented(cls, r: int, g: int, b: int) -> Dict[str, Any]:
        """Convert sRGB to standard CMYK percentages with explicit documented assumptions.
        
        Notice: Standard mathematical conversion is an approximation. Production print
        engineering requires ICC profile-based color management (e.g. US Web Coated SWOP v2 or ISO Coated v2).
        """
        if r == 0 and g == 0 and b == 0:
            return {
                "cmyk_string": "C:0 M:0 Y:0 K:100",
                "c": 0, "m": 0, "y": 0, "k": 100,
                "assumption": "Standard theoretical K-channel extraction. Production print requires ICC color profile conversion.",
            }
        c = 1.0 - (r / 255.0)
        m = 1.0 - (g / 255.0)
        y = 1.0 - (b / 255.0)
        k = min(c, m, y)
        if k >= 1.0:
            return {
                "cmyk_string": "C:0 M:0 Y:0 K:100",
                "c": 0, "m": 0, "y": 0, "k": 100,
                "assumption": "Standard theoretical K-channel extraction.",
            }
        c_p = (c - k) / (1.0 - k)
        m_p = (m - k) / (1.0 - k)
        y_p = (y - k) / (1.0 - k)

        c_int = round(c_p * 100)
        m_int = round(m_p * 100)
        y_int = round(y_p * 100)
        k_int = round(k * 100)

        return {
            "cmyk_string": f"C:{c_int} M:{m_int} Y:{y_int} K:{k_int}",
            "c": c_int, "m": m_int, "y": y_int, "k": k_int,
            "assumption": "Theoretical sRGB-to-CMYK conversion; calibrate with target print shop ICC profile before printing.",
        }
