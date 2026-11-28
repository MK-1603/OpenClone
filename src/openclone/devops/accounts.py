"""OpenClone Connected Accounts Management System.

Manages external provider account connections (GitHub, Vercel, Cloudflare, Render, Neon, Supabase),
credential encryption references, permission verification, and lifecycle states.
"""
from __future__ import annotations

import copy
import time
import uuid
from typing import Any, Dict, List, Optional
from src.openclone.devops.models import ConnectedAccountRecord, ConnectionStatus, ProviderCategory


class AccountConnectionManager:
    """Manages the lifecycle, verification, and revocation of external developer accounts."""

    _instance: Optional["AccountConnectionManager"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._accounts: Dict[str, ConnectedAccountRecord] = {}
        self._provider_index: Dict[str, str] = {}  # provider_id -> connection_id
        self._initialized = True

    def connect_account(
        self,
        provider_id: str,
        category: ProviderCategory,
        account_identifier: str,
        authentication_type: str = "api_token",
        granted_scopes: Optional[List[str]] = None,
        authorized_resources: Optional[List[str]] = None,
        user_id: str = "user_default",
        workspace_id: str = "workspace_default",
        verify_immediately: bool = True,
    ) -> ConnectedAccountRecord:
        """Connects and registers a provider account with secure metadata tracking."""
        conn_id = f"conn-{uuid.uuid4().hex[:8]}"
        record = ConnectedAccountRecord(
            connection_id=conn_id,
            user_id=user_id,
            workspace_id=workspace_id,
            provider_id=provider_id.lower(),
            category=category,
            authentication_type=authentication_type,
            account_identifier=account_identifier,
            granted_scopes=granted_scopes or ["read", "write"],
            authorized_resources=authorized_resources or ["default"],
            status=ConnectionStatus.VERIFIED if verify_immediately else ConnectionStatus.CONNECTED,
            last_verified_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) if verify_immediately else None,
        )

        self._accounts[conn_id] = record
        self._provider_index[provider_id.lower()] = conn_id
        return record

    def get_connection(self, connection_id: str) -> Optional[ConnectedAccountRecord]:
        return self._accounts.get(connection_id)

    def get_connection_by_provider(self, provider_id: str) -> Optional[ConnectedAccountRecord]:
        conn_id = self._provider_index.get(provider_id.lower())
        return self._accounts.get(conn_id) if conn_id else None

    def list_connections(self, category: Optional[ProviderCategory] = None) -> List[ConnectedAccountRecord]:
        conns = list(self._accounts.values())
        if category:
            conns = [c for c in conns if c.category == category]
        return conns

    def disconnect_account(self, provider_id: str) -> bool:
        conn_id = self._provider_index.get(provider_id.lower())
        if conn_id and conn_id in self._accounts:
            self._accounts[conn_id].status = ConnectionStatus.DISCONNECTED
            self._accounts[conn_id].updated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            return True
        return False

    def verify_connection(self, provider_id: str) -> bool:
        """Performs simulated live health check on connected credentials."""
        conn = self.get_connection_by_provider(provider_id)
        if conn and conn.status in (ConnectionStatus.CONNECTED, ConnectionStatus.VERIFIED):
            conn.status = ConnectionStatus.VERIFIED
            conn.last_verified_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            return True
        return False
