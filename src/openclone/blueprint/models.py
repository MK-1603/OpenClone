"""OpenClone Universal Product Blueprint (UPB) — Core Data Models.

Defines the complete canonical data contracts for Information Architecture,
Page Inventory, User Journeys, Component Interactions, API/Data Mapping,
Application States, Responsive/A11y Specs, Traceability, and Final Blueprint Package.
"""
from __future__ import annotations

import enum
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


class PageCategory(str, enum.Enum):
    PUBLIC = "PUBLIC"
    AUTHENTICATION = "AUTHENTICATION"
    WORKSPACE = "WORKSPACE"
    ADMINISTRATIVE = "ADMINISTRATIVE"
    ACCOUNT = "ACCOUNT"
    SYSTEM = "SYSTEM"
    ERROR = "ERROR"
    UTILITY = "UTILITY"


class LayoutType(str, enum.Enum):
    LANDING = "LANDING"
    AUTH_CARD = "AUTH_CARD"
    SIDEBAR_WORKSPACE = "SIDEBAR_WORKSPACE"
    FULL_WIDTH_DASHBOARD = "FULL_WIDTH_DASHBOARD"
    SETTINGS_SPLIT = "SETTINGS_SPLIT"
    MODAL_DRAWER = "MODAL_DRAWER"


@dataclass
class PageDefinition:
    page_id: str
    title: str
    slug: str
    category: PageCategory
    purpose: str
    layout: LayoutType
    user_roles: List[str] = field(default_factory=lambda: ["user"])
    required_components: List[str] = field(default_factory=list)
    api_dependencies: List[str] = field(default_factory=list)
    data_entities: List[str] = field(default_factory=list)
    related_features: List[str] = field(default_factory=list)
    navigation_parents: List[str] = field(default_factory=list)


@dataclass
class UserJourneyStep:
    step_id: str
    order: int
    actor_role: str
    user_action: str
    system_response: str
    source_page_id: str
    target_page_id: str
    required_permission: Optional[str] = None
    failure_path: Optional[str] = None


@dataclass
class UserJourney:
    journey_id: str
    title: str
    actor_role: str
    goal: str
    preconditions: List[str] = field(default_factory=list)
    steps: List[UserJourneyStep] = field(default_factory=list)
    success_criteria: str = ""


@dataclass
class InteractiveComponentSpec:
    component_id: str
    name: str
    component_type: str  # button, form, modal, table, tab, card, input
    page_ids: List[str] = field(default_factory=list)
    default_state: str = "normal"
    hover_state: Optional[str] = None
    active_state: Optional[str] = None
    disabled_state: Optional[str] = None
    loading_state: Optional[str] = None
    on_click_action: str = ""
    triggered_api_id: Optional[str] = None
    validation_rules: List[str] = field(default_factory=list)
    accessibility_label: str = ""


@dataclass
class ApiConnectionMapping:
    endpoint_id: str
    path: str
    method: str  # GET, POST, PUT, DELETE, PATCH
    description: str
    request_schema: Dict[str, Any] = field(default_factory=dict)
    response_schema: Dict[str, Any] = field(default_factory=dict)
    auth_required: bool = True
    required_role: Optional[str] = None
    related_components: List[str] = field(default_factory=list)
    related_data_entities: List[str] = field(default_factory=list)


@dataclass
class DatabaseEntityMapping:
    entity_name: str
    table_name: str
    primary_key: str
    attributes: Dict[str, str] = field(default_factory=dict)
    foreign_keys: Dict[str, str] = field(default_factory=dict)
    relationships: List[str] = field(default_factory=list)
    access_patterns: List[str] = field(default_factory=list)


@dataclass
class ApplicationStateSpec:
    state_id: str
    page_id: str
    initial_state_desc: str
    loading_state_desc: str
    empty_state_desc: str
    success_state_desc: str
    error_state_desc: str
    unauthorized_state_desc: str
    state_scope: str = "local"  # local, shared, server, persistent


@dataclass
class ResponsiveBreakpointSpec:
    breakpoint_name: str  # mobile, tablet, desktop, ultra_wide
    min_width_px: int
    max_width_px: Optional[int]
    sidebar_behavior: str  # hidden, drawer, collapsed, expanded
    grid_columns: int
    navigation_type: str  # hamburger, tab_bar, full_header


@dataclass
class TraceabilityLink:
    source_type: str
    source_id: str
    relationship: str
    target_type: str
    target_id: str
    verified: bool = True


@dataclass
class ProductBlueprintPackage:
    blueprint_id: str
    project_id: str
    project_name: str
    version: str = "1.0.0"
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    pages: List[PageDefinition] = field(default_factory=list)
    journeys: List[UserJourney] = field(default_factory=list)
    components: List[InteractiveComponentSpec] = field(default_factory=list)
    apis: List[ApiConnectionMapping] = field(default_factory=list)
    database_entities: List[DatabaseEntityMapping] = field(default_factory=list)
    states: List[ApplicationStateSpec] = field(default_factory=list)
    traceability_links: List[TraceabilityLink] = field(default_factory=list)
    validation_status: str = "PENDING_VALIDATION"
    completeness_score: float = 0.0
