"""OpenClone Project Identity & Asset Registry.

Provides central storage, versioning, retrieval, and integrity tracking for all
project branding assets, logos, palettes, icons, and package files.
"""
from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional
from src.openclone.identity.models import AssetDescriptor, AssetCategory, IdentityLifecycleState


class AssetRegistry:
    """Central registry and lifecycle manager for all generated project assets."""

    _instance: Optional["AssetRegistry"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._assets: Dict[str, AssetDescriptor] = {}
        self._project_index: Dict[str, List[str]] = {}
        self._history: Dict[str, List[AssetDescriptor]] = {}
        self._initialized = True

    def register_asset(self, asset: AssetDescriptor) -> None:
        """Register or update an asset with version tracking."""
        asset_id = asset.asset_id
        if asset_id in self._assets:
            # Preserve previous in history
            prev = copy.deepcopy(self._assets[asset_id])
            self._history.setdefault(asset_id, []).append(prev)
            asset.version = prev.version + 1

        self._assets[asset_id] = asset
        self._project_index.setdefault(asset.project_id, [])
        if asset_id not in self._project_index[asset.project_id]:
            self._project_index[asset.project_id].append(asset_id)

    def get_asset(self, asset_id: str) -> Optional[AssetDescriptor]:
        return self._assets.get(asset_id)

    def list_assets(self, project_id: Optional[str] = None, category: Optional[AssetCategory] = None) -> List[AssetDescriptor]:
        assets = list(self._assets.values())
        if project_id:
            assets = [a for a in assets if a.project_id == project_id]
        if category:
            assets = [a for a in assets if a.category == category]
        return assets

    def approve_asset(self, asset_id: str) -> bool:
        asset = self.get_asset(asset_id)
        if asset:
            asset.is_approved = True
            return True
        return False

    def get_asset_history(self, asset_id: str) -> List[AssetDescriptor]:
        return self._history.get(asset_id, [])
