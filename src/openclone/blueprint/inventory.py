"""OpenClone Product Information Architecture & Page Inventory Engine.

Generates the complete sitemap, navigation hierarchy, and page inventory ensuring
100% of approved features have explicit visual interfaces and navigation pathways.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional
from src.openclone.blueprint.models import PageCategory, PageDefinition, LayoutType


class PageInventoryEngine:
    """Generates complete sitemaps and page inventories from approved features."""

    @classmethod
    def generate_inventory(
        cls,
        project_name: str,
        features: List[Dict[str, Any]],
        category: str = "SaaS Application",
    ) -> List[PageDefinition]:
        pages: List[PageDefinition] = []

        # 1. Public Landing / Marketing Pages
        pages.append(PageDefinition(
            page_id="page-public-home",
            title=f"{project_name} — Home",
            slug="/",
            category=PageCategory.PUBLIC,
            purpose="Product landing page explaining value proposition, core features, and call-to-action.",
            layout=LayoutType.LANDING,
            user_roles=["guest", "user"],
            required_components=["hero-banner", "feature-grid", "pricing-table", "cta-button", "footer"],
            related_features=["FEAT-001"],
            navigation_parents=[],
        ))

        # 2. Authentication Pages
        pages.append(PageDefinition(
            page_id="page-auth-signin",
            title="Sign In",
            slug="/auth/signin",
            category=PageCategory.AUTHENTICATION,
            purpose="User authentication via email/password and OAuth2 providers.",
            layout=LayoutType.AUTH_CARD,
            user_roles=["guest"],
            required_components=["signin-form", "oauth-buttons", "forgot-password-link"],
            api_dependencies=["/api/v1/auth/login"],
            related_features=["FEAT-AUTH"],
            navigation_parents=["page-public-home"],
        ))

        pages.append(PageDefinition(
            page_id="page-auth-signup",
            title="Create Account",
            slug="/auth/signup",
            category=PageCategory.AUTHENTICATION,
            purpose="Registration flow for new user onboarding.",
            layout=LayoutType.AUTH_CARD,
            user_roles=["guest"],
            required_components=["signup-form", "terms-checkbox", "oauth-buttons"],
            api_dependencies=["/api/v1/auth/register"],
            related_features=["FEAT-AUTH"],
            navigation_parents=["page-public-home"],
        ))

        # 3. Main Workspace Dashboard
        pages.append(PageDefinition(
            page_id="page-workspace-dashboard",
            title="Dashboard Overview",
            slug="/dashboard",
            category=PageCategory.WORKSPACE,
            purpose="Central command center displaying key operational metrics, activity feeds, and quick actions.",
            layout=LayoutType.SIDEBAR_WORKSPACE,
            user_roles=["user", "admin"],
            required_components=["stats-overview", "activity-stream", "quick-action-bar", "data-chart"],
            api_dependencies=["/api/v1/dashboard/metrics", "/api/v1/activity"],
            data_entities=["DashboardMetrics", "UserSession"],
            related_features=["FEAT-DASHBOARD"],
            navigation_parents=["page-public-home"],
        ))

        # 4. Map Each Feature to Dedicated Application Pages
        for idx, feat in enumerate(features, 1):
            f_id = feat.get("feature_id", f"FEAT-{idx:03d}")
            f_title = feat.get("title", f"Feature {idx}")
            slug_part = re.sub(r"[^A-Za-z0-9]", "-", f_title.lower()).strip("-")

            pages.append(PageDefinition(
                page_id=f"page-feat-{f_id.lower()}",
                title=f_title,
                slug=f"/app/{slug_part}",
                category=PageCategory.WORKSPACE,
                purpose=f"Dedicated interface for managing and executing {f_title}.",
                layout=LayoutType.SIDEBAR_WORKSPACE,
                user_roles=["user", "admin"],
                required_components=["data-table", "search-filter-bar", "create-modal", "action-dropdown"],
                api_dependencies=[f"/api/v1/{slug_part}"],
                data_entities=[f_title.replace(" ", "")],
                related_features=[f_id],
                navigation_parents=["page-workspace-dashboard"],
            ))

        # 5. Settings & Account Management
        pages.append(PageDefinition(
            page_id="page-account-settings",
            title="Settings & Preferences",
            slug="/settings",
            category=PageCategory.ACCOUNT,
            purpose="Manage user profile, API credentials, notifications, and security.",
            layout=LayoutType.SETTINGS_SPLIT,
            user_roles=["user", "admin"],
            required_components=["profile-form", "api-key-manager", "notification-toggles", "mfa-toggle"],
            api_dependencies=["/api/v1/user/profile", "/api/v1/user/keys"],
            data_entities=["UserProfile", "ApiCredential"],
            related_features=["FEAT-SETTINGS"],
            navigation_parents=["page-workspace-dashboard"],
        ))

        # 6. Admin Management
        pages.append(PageDefinition(
            page_id="page-admin-governance",
            title="Administration & Audit Logs",
            slug="/admin",
            category=PageCategory.ADMINISTRATIVE,
            purpose="Audit ledger logs, tenant governance, and system-level parameters.",
            layout=LayoutType.SIDEBAR_WORKSPACE,
            user_roles=["admin"],
            required_components=["audit-log-table", "tenant-selector", "permission-matrix"],
            api_dependencies=["/api/v1/admin/audit-ledger"],
            data_entities=["AuditLogEntry"],
            related_features=["FEAT-GOVERNANCE"],
            navigation_parents=["page-workspace-dashboard"],
        ))

        return pages
