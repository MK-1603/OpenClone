"""OpenClone Database & Storage Security Protection Engine.

Enforces parameterized queries, multi-tenant isolation, safe ORM patterns,
least-privilege connection settings, and object storage boundary protection.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Set


class DatabaseSecurityError(Exception):
    """Raised when database query or configuration violates security policy."""
    pass


# Unsafe dynamic SQL concatenation indicators
UNSAFE_SQL_CONCAT_PATTERNS = [
    re.compile(r"WHERE\s+[a-zA-Z0-9_.]+\s*=\s*'[^']*'\s*(?:OR|AND)", re.I),
    re.compile(r"WHERE\s+[a-zA-Z0-9_.]+\s*=\s*\"\s*\+", re.I),
    re.compile(r"f[\"'].*SELECT.*\{.*\}", re.I),
    re.compile(r"(?i)\bUNION\s+SELECT\b"),
]

# Sensitive tenant-isolated table names that require tenant/workspace scoping
MULTI_TENANT_TABLES: Set[str] = {
    "projects",
    "tasks",
    "users",
    "audit_ledgers",
    "credentials",
    "artifacts",
}


class DatabaseSecurityGuard:
    """Security validator for SQL queries, database connections, and storage keys."""

    @staticmethod
    def validate_query(sql: str, params: Optional[Any] = None) -> bool:
        """Verify that SQL query uses parameterization and does not contain raw string injection."""
        clean_sql = sql.strip()

        # Check for unparameterized raw string injections
        for pattern in UNSAFE_SQL_CONCAT_PATTERNS:
            if pattern.search(clean_sql):
                raise DatabaseSecurityError(
                    "SQL injection risk detected: Query appears to use raw string concatenation instead of parameterized placeholders (?, %s, :val)."
                )

        # Destructive DDL operations require explicit parameterized flags
        if re.search(r"(?i)\bDROP\s+(?:DATABASE|TABLE|SCHEMA)\b", clean_sql):
            raise DatabaseSecurityError(
                "Destructive DDL blocked: DROP statements are prohibited through standard database interfaces."
            )

        return True

    @staticmethod
    def validate_tenant_isolation(
        sql: str,
        table_name: str,
        isolation_column: str = "workspace_id",
    ) -> bool:
        """Ensure queries targeting multi-tenant tables include workspace/tenant scoping clauses."""
        clean_sql = sql.strip()
        table_clean = table_name.strip().lower()

        if table_clean in MULTI_TENANT_TABLES:
            # Query must contain the isolation column in WHERE clause
            pattern = re.compile(rf"\bWHERE\b.*\b{isolation_column}\b", re.I | re.DOTALL)
            if not pattern.search(clean_sql):
                raise DatabaseSecurityError(
                    f"Tenant isolation violation: Query on multi-tenant table '{table_name}' "
                    f"lacks mandatory scoping filter '{isolation_column} = ?'"
                )
        return True

    @staticmethod
    def validate_connection_parameters(config: Dict[str, Any], environment: str = "production") -> bool:
        """Validate database connection security parameters against production standards."""
        env_clean = environment.strip().lower()

        # Check for empty or placeholder passwords
        password = str(config.get("password", "")).strip()
        if not password or password in ("password", "root", "admin", "123456"):
            raise DatabaseSecurityError("Database security violation: Empty or weak default database password.")

        if env_clean == "production":
            # In production, TLS/SSL connection is strictly required
            ssl_mode = str(config.get("sslmode", config.get("tls", ""))).lower()
            if ssl_mode not in ("require", "verify-full", "verify-ca", "true", "enabled"):
                raise DatabaseSecurityError(
                    "Production database security violation: Database connection must enforce TLS/SSL (sslmode=require)."
                )

            # Public binding check
            host = str(config.get("host", "")).lower()
            if host in ("0.0.0.0", ""):
                raise DatabaseSecurityError(
                    "Database security violation: Production database host cannot be bound to public '0.0.0.0'."
                )

        return True

    @staticmethod
    def validate_storage_key(storage_key: str) -> bool:
        """Validate object storage key to prevent directory traversal or root bucket escapes."""
        key_clean = storage_key.replace("\\", "/")
        if ".." in key_clean or key_clean.startswith("/") or key_clean.startswith("~"):
            raise DatabaseSecurityError(
                f"Storage boundary violation: Prohibited path traversal or absolute key detected: '{storage_key}'"
            )
        return True
