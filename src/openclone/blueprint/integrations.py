"""OpenClone Technical Integration & Connection Mapping Engine.

Maps UI components and pages to frontend services, backend handlers,
API contracts (OpenAPI), database entities, foreign keys, and event streams.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from src.openclone.blueprint.models import ApiConnectionMapping, DatabaseEntityMapping, PageDefinition


class IntegrationMappingEngine:
    """Constructs explicit bidirectional contracts between UI, APIs, and Data Models."""

    @classmethod
    def generate_api_mappings(cls, pages: List[PageDefinition]) -> List[ApiConnectionMapping]:
        apis: List[ApiConnectionMapping] = []

        # 1. Auth Endpoint
        apis.append(ApiConnectionMapping(
            endpoint_id="api-auth-login",
            path="/api/v1/auth/login",
            method="POST",
            description="Authenticates user credentials and returns signed JWT access & refresh tokens.",
            request_schema={
                "type": "object",
                "required": ["email", "password"],
                "properties": {
                    "email": {"type": "string", "format": "email"},
                    "password": {"type": "string"},
                },
            },
            response_schema={
                "type": "object",
                "properties": {
                    "access_token": {"type": "string"},
                    "token_type": {"type": "string", "enum": ["Bearer"]},
                    "expires_in": {"type": "integer"},
                },
            },
            auth_required=False,
            related_components=["comp-form-login"],
            related_data_entities=["UserSession", "UserAccount"],
        ))

        # 2. Dashboard Metrics Endpoint
        apis.append(ApiConnectionMapping(
            endpoint_id="api-dashboard-metrics",
            path="/api/v1/dashboard/metrics",
            method="GET",
            description="Fetches aggregated operational metrics and activity summary for current workspace.",
            request_schema={},
            response_schema={
                "type": "object",
                "properties": {
                    "total_projects": {"type": "integer"},
                    "active_tasks": {"type": "integer"},
                    "system_health": {"type": "string"},
                },
            },
            auth_required=True,
            related_components=["comp-toolbar-search"],
            related_data_entities=["DashboardMetrics"],
        ))

        # 3. Dynamic Feature APIs from Page Definitions
        for p in pages:
            for api_dep in p.api_dependencies:
                if api_dep not in [a.path for a in apis]:
                    apis.append(ApiConnectionMapping(
                        endpoint_id=f"api-{api_dep.replace('/', '-').strip('-')}",
                        path=api_dep,
                        method="GET",
                        description=f"REST service supporting {p.title}",
                        request_schema={},
                        response_schema={"type": "object"},
                        auth_required=True,
                        related_components=[f"comp-{p.page_id}"],
                        related_data_entities=p.data_entities,
                    ))

        return apis

    @classmethod
    def generate_database_mappings(cls, pages: List[PageDefinition]) -> List[DatabaseEntityMapping]:
        entities: List[DatabaseEntityMapping] = []

        # 1. User Account Table
        entities.append(DatabaseEntityMapping(
            entity_name="UserAccount",
            table_name="users",
            primary_key="id UUID",
            attributes={
                "id": "UUID PRIMARY KEY",
                "email": "VARCHAR(255) UNIQUE NOT NULL",
                "password_hash": "VARCHAR(255) NOT NULL",
                "role": "VARCHAR(50) NOT NULL DEFAULT 'user'",
                "created_at": "TIMESTAMPTZ DEFAULT NOW()",
            },
            foreign_keys={},
            relationships=["1:N with user_sessions", "1:N with audit_logs"],
            access_patterns=["SELECT BY email", "SELECT BY id"],
        ))

        # 2. Audit Log Table
        entities.append(DatabaseEntityMapping(
            entity_name="AuditLogEntry",
            table_name="audit_logs",
            primary_key="id UUID",
            attributes={
                "id": "UUID PRIMARY KEY",
                "user_id": "UUID REFERENCES users(id)",
                "action": "VARCHAR(100) NOT NULL",
                "sha256_digest": "VARCHAR(64) NOT NULL",
                "timestamp": "TIMESTAMPTZ DEFAULT NOW()",
            },
            foreign_keys={"user_id": "users.id"},
            relationships=["N:1 with users"],
            access_patterns=["SELECT BY user_id", "SELECT ORDER BY timestamp DESC"],
        ))

        # 3. Dynamic entities from pages
        for p in pages:
            for ent in p.data_entities:
                if ent not in [e.entity_name for e in entities]:
                    entities.append(DatabaseEntityMapping(
                        entity_name=ent,
                        table_name=ent.lower() + "s",
                        primary_key="id UUID",
                        attributes={
                            "id": "UUID PRIMARY KEY",
                            "name": "VARCHAR(255) NOT NULL",
                            "status": "VARCHAR(50) NOT NULL",
                            "created_at": "TIMESTAMPTZ DEFAULT NOW()",
                        },
                        foreign_keys={},
                        relationships=[],
                        access_patterns=["SELECT ALL", "SELECT BY id"],
                    ))

        return entities
