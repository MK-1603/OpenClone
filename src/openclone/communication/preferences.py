"""Notification Preference & Quiet-Hours Filter Engine.

Enforces user opt-outs, channel selections, time-zone aware quiet-hour suppression,
and ensures mandatory security alerts are never suppressed.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List, Tuple

from src.openclone.communication.models import (
    ChannelType,
    DeliveryStatus,
    NotificationCategory,
    NotificationPayload,
    UserPreference,
)


@dataclass
class PreferenceEvaluation:
    """Outcome of preference screening."""
    approved_channels: List[ChannelType]
    suppressed_channels: List[Tuple[ChannelType, str]]
    is_quiet_hours: bool


class PreferenceEngine:
    """Filters channels based on user preferences and legal/security mandates."""

    @staticmethod
    def is_in_quiet_hours(pref: UserPreference, current_utc_epoch: float) -> bool:
        """Calculate if current time falls within user's local quiet hours."""
        if not pref.quiet_hours_enabled:
            return False

        # Convert epoch to user local hour
        user_local_seconds = current_utc_epoch + (pref.user_timezone_offset_hours * 3600.0)
        local_hour = int((user_local_seconds % 86400) // 3600)

        start = pref.quiet_hours_start_hour
        end = pref.quiet_hours_end_hour

        if start > end:
            # Over midnight: e.g. 22:00 to 08:00
            return local_hour >= start or local_hour < end
        else:
            return start <= local_hour < end

    @classmethod
    def evaluate(
        cls,
        payload: NotificationPayload,
        pref: Optional[UserPreference] = None,
        current_epoch: Optional[float] = None,
    ) -> PreferenceEvaluation:
        """Screen requested channels against preferences."""
        epoch = current_epoch if current_epoch is not None else time.time()

        # If no user preferences provided, all requested channels are allowed
        if pref is None:
            return PreferenceEvaluation(
                approved_channels=list(payload.channels),
                suppressed_channels=[],
                is_quiet_hours=False,
            )

        # Rule 1: MANDATORY SECURITY OVERRIDE
        # Critical security notifications cannot be disabled by user preference or quiet hours.
        if payload.category == NotificationCategory.SECURITY:
            return PreferenceEvaluation(
                approved_channels=list(payload.channels),
                suppressed_channels=[],
                is_quiet_hours=False,
            )

        in_quiet_hours = cls.is_in_quiet_hours(pref, epoch)
        approved: List[ChannelType] = []
        suppressed: List[Tuple[ChannelType, str]] = []

        # Check Category Opt-Out
        if payload.category in pref.opted_out_categories:
            for ch in payload.channels:
                suppressed.append((ch, f"User opted out of category '{payload.category.value}'"))
            return PreferenceEvaluation(
                approved_channels=[],
                suppressed_channels=suppressed,
                is_quiet_hours=in_quiet_hours,
            )

        # Check per-channel permissions and quiet hours
        for ch in payload.channels:
            if ch not in pref.allowed_channels:
                suppressed.append((ch, f"Channel '{ch.value}' is not enabled in user preferences"))
                continue

            # Quiet hours apply to non-urgent channels (SMS, Push, Phone)
            # In-app and Email can be delivered asynchronously unless strictly marketing
            if in_quiet_hours and ch in (ChannelType.SMS, ChannelType.MOBILE_PUSH, ChannelType.WEB_PUSH):
                suppressed.append((ch, f"Quiet hours active ({pref.quiet_hours_start_hour}:00 - {pref.quiet_hours_end_hour}:00)"))
                continue

            approved.append(ch)

        return PreferenceEvaluation(
            approved_channels=approved,
            suppressed_channels=suppressed,
            is_quiet_hours=in_quiet_hours,
        )
