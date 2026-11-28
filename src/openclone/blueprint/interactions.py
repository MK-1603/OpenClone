"""OpenClone Component & Interaction Specification Engine.

Defines exact behavioral contracts for buttons, forms, modals, tables, inputs,
specifying click behavior, states, triggers, and error conditions.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from src.openclone.blueprint.models import InteractiveComponentSpec, PageDefinition


class ComponentInteractionEngine:
    """Generates complete interaction specifications for all UI components."""

    @classmethod
    def generate_component_specs(cls, pages: List[PageDefinition]) -> List[InteractiveComponentSpec]:
        specs: List[InteractiveComponentSpec] = []

        # 1. Primary Action Button
        specs.append(InteractiveComponentSpec(
            component_id="comp-btn-primary",
            name="Primary CTA Button",
            component_type="button",
            page_ids=[p.page_id for p in pages],
            default_state="solid background, bold font, rounded corners",
            hover_state="subtle brightness increase, shadow elevation",
            active_state="inset scaling (0.98x scale), pressed visual feedback",
            disabled_state="40% opacity, cursor not-allowed, pointer-events none",
            loading_state="embedded spinner icon, label hidden, button disabled",
            on_click_action="Dispatches form submission or navigates to designated route",
            accessibility_label="Primary actionable button with explicit ARIA label",
        ))

        # 2. Authentication Login Form
        specs.append(InteractiveComponentSpec(
            component_id="comp-form-login",
            name="Authentication Login Form",
            component_type="form",
            page_ids=["page-auth-signin"],
            default_state="clean inputs with placeholder hints",
            on_click_action="Validates input format, emits POST /api/v1/auth/login",
            triggered_api_id="/api/v1/auth/login",
            validation_rules=["email: RFC 5322 regex", "password: min 8 chars with complexity check"],
            accessibility_label="Sign in form with explicit fieldset and labels",
        ))

        # 3. Dynamic Filter Search Toolbar
        specs.append(InteractiveComponentSpec(
            component_id="comp-toolbar-search",
            name="Workspace Filter Search Bar",
            component_type="input",
            page_ids=["page-workspace-dashboard"],
            default_state="magnifying glass icon, clear button when text entered",
            hover_state="subtle border highlight",
            on_click_action="Debounces keystrokes (300ms) and triggers query filter",
            triggered_api_id="/api/v1/dashboard/metrics",
            validation_rules=["sanitizes SQL / XSS characters"],
            accessibility_label="Search items input",
        ))

        # 4. Item Creation Modal
        specs.append(InteractiveComponentSpec(
            component_id="comp-modal-create",
            name="Resource Creation Modal",
            component_type="modal",
            page_ids=["page-workspace-dashboard"],
            default_state="hidden overlay",
            active_state="centered dialog with backdrop blur, focus trapped inside",
            on_click_action="Opens on click, closes on Escape key or outside click",
            validation_rules=["all required fields non-empty"],
            accessibility_label="Create resource dialog window",
        ))

        return specs
