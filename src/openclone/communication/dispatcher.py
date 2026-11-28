"""Unified Multi-Channel Notification Dispatcher & Delivery Ledger.

Orchestrates multi-channel routing, idempotency enforcement, preference filtering,
provider failover, and hash-chained audit logging.
"""
from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Set

from src.openclone.communication.models import (
    ChannelType,
    DeliveryAttempt,
    DeliveryStatus,
    NotificationCategory,
    NotificationPayload,
    NotificationPriority,
    ProviderResult,
    UserPreference,
)
from src.openclone.communication.preferences import PreferenceEngine
from src.openclone.communication.providers import (
    BaseEmailProvider,
    BasePushProvider,
    BaseSmsProvider,
    MockEmailProvider,
    MockPushProvider,
    MockSmsProvider,
    ProviderFailoverManager,
)
from src.openclone.communication.realtime import WebSocketSessionManager


class DeliveryLedger:
    """Tamper-evident, hash-chained delivery audit ledger."""

    def __init__(self):
        self.attempts: List[DeliveryAttempt] = []
        self._last_hash = "0" * 64

    def record_attempt(
        self,
        attempt_id: str,
        notification_id: str,
        channel: ChannelType,
        provider_name: str,
        status: DeliveryStatus,
        attempt_number: int,
        error_message: Optional[str] = None,
    ) -> DeliveryAttempt:
        now = time.time()
        payload = f"{self._last_hash}|{attempt_id}|{notification_id}|{channel.value}|{provider_name}|{status.value}|{now:.3f}"
        current_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        self._last_hash = current_hash

        entry = DeliveryAttempt(
            attempt_id=attempt_id,
            notification_id=notification_id,
            channel=channel,
            provider_name=provider_name,
            status=status,
            attempt_number=attempt_number,
            timestamp_epoch=now,
            error_message=error_message,
            sha256_hash=current_hash,
        )
        self.attempts.append(entry)
        return entry

    def get_attempts(self, notification_id: str) -> List[DeliveryAttempt]:
        return [a for a in self.attempts if a.notification_id == notification_id]

    def verify_integrity(self) -> bool:
        """Verify the cryptographic chain of all audit entries."""
        last = "0" * 64
        for a in self.attempts:
            payload = f"{last}|{a.attempt_id}|{a.notification_id}|{a.channel.value}|{a.provider_name}|{a.status.value}|{a.timestamp_epoch:.3f}"
            expected = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            if a.sha256_hash != expected:
                return False
            last = a.sha256_hash
        return True


class NotificationDispatcher:
    """Central notification orchestration and delivery engine."""

    def __init__(
        self,
        failover_manager: Optional[ProviderFailoverManager] = None,
        socket_manager: Optional[WebSocketSessionManager] = None,
    ):
        self.failover_manager = failover_manager or ProviderFailoverManager()
        if not self.failover_manager.email_providers:
            self.failover_manager.register_email_provider(MockEmailProvider())
        if not self.failover_manager.sms_providers:
            self.failover_manager.register_sms_provider(MockSmsProvider())
        if not self.failover_manager.push_providers:
            self.failover_manager.register_push_provider(MockPushProvider())

        self.socket_manager = socket_manager or WebSocketSessionManager()
        self.ledger = DeliveryLedger()

        # Idempotency cache: idempotency_key -> notification_id
        self._processed_idempotency_keys: Dict[str, Dict[str, Any]] = {}
        # In-app message inbox: user_id -> List[NotificationPayload]
        self._in_app_inbox: Dict[str, List[NotificationPayload]] = {}
        # Dead-Letter Queue: List of failed dispatch records
        self.dead_letter_queue: List[Dict[str, Any]] = []

    def dispatch(
        self,
        payload: NotificationPayload,
        preference: Optional[UserPreference] = None,
        max_retries: int = 2,
    ) -> Dict[str, Any]:
        """Dispatch notification across authorized channels with retry and audit."""
        # 1. Idempotency Check
        if payload.idempotency_key:
            if payload.idempotency_key in self._processed_idempotency_keys:
                cached = self._processed_idempotency_keys[payload.idempotency_key]
                return {
                    "notification_id": payload.notification_id,
                    "status": "duplicate_suppressed",
                    "idempotency_key": payload.idempotency_key,
                    "original_dispatch": cached,
                }

        # 2. Preference and Quiet-Hour Screening
        eval_result = PreferenceEngine.evaluate(payload, preference)
        approved_channels = eval_result.approved_channels
        suppressed_details = eval_result.suppressed_channels

        results: Dict[str, Any] = {
            "notification_id": payload.notification_id,
            "category": payload.category.value,
            "priority": payload.priority.value,
            "channel_results": {},
            "suppressed_channels": [
                {"channel": ch.value, "reason": reason} for ch, reason in suppressed_details
            ],
        }

        # Record suppressions in ledger
        for ch, reason in suppressed_details:
            self.ledger.record_attempt(
                attempt_id=f"att_sup_{payload.notification_id}_{ch.value}",
                notification_id=payload.notification_id,
                channel=ch,
                provider_name="preference_filter",
                status=DeliveryStatus.SUPPRESSED,
                attempt_number=1,
                error_message=reason,
            )

        # 3. Channel Dispatch
        for ch in approved_channels:
            ch_res = self._dispatch_single_channel(payload, ch, max_retries)
            results["channel_results"][ch.value] = ch_res

            if not ch_res.get("success", False):
                # Send to Dead-Letter Queue
                self.dead_letter_queue.append({
                    "notification_id": payload.notification_id,
                    "channel": ch.value,
                    "payload": payload,
                    "error": ch_res.get("error_message"),
                    "timestamp": time.time(),
                })

        # Cache idempotency key
        if payload.idempotency_key:
            self._processed_idempotency_keys[payload.idempotency_key] = results

        return results

    def _dispatch_single_channel(
        self,
        payload: NotificationPayload,
        channel: ChannelType,
        max_retries: int,
    ) -> Dict[str, Any]:
        """Deliver to a specific channel with bounded retry."""
        attempt_num = 0
        last_error = None
        provider_name = "unknown"

        while attempt_num <= max_retries:
            attempt_num += 1
            att_id = f"att_{payload.notification_id}_{channel.value}_{attempt_num}"

            if channel == ChannelType.EMAIL:
                if not payload.recipient_email:
                    return {"success": False, "error_message": "Missing recipient_email"}
                res = self.failover_manager.dispatch_email_with_failover(
                    to_email=payload.recipient_email,
                    subject=payload.subject,
                    body_text=payload.body_text,
                    body_html=payload.body_html,
                )
            elif channel == ChannelType.SMS:
                if not payload.recipient_phone:
                    return {"success": False, "error_message": "Missing recipient_phone"}
                res = self.failover_manager.dispatch_sms_with_failover(
                    to_phone=payload.recipient_phone,
                    body_text=payload.body_text,
                )
            elif channel == ChannelType.MOBILE_PUSH or channel == ChannelType.WEB_PUSH:
                push_prov = self.failover_manager.push_providers[0] if self.failover_manager.push_providers else None
                if not push_prov:
                    res = ProviderResult(success=False, channel=channel, provider_name="none", status=DeliveryStatus.FAILED, error_message="No push provider")
                else:
                    res = push_prov.send_push(
                        device_tokens=payload.device_tokens,
                        title=payload.subject,
                        body=payload.body_text,
                        data=payload.metadata,
                    )
            elif channel == ChannelType.IN_APP:
                if payload.recipient_id not in self._in_app_inbox:
                    self._in_app_inbox[payload.recipient_id] = []
                self._in_app_inbox[payload.recipient_id].append(payload)
                res = ProviderResult(
                    success=True,
                    channel=ChannelType.IN_APP,
                    provider_name="internal_inbox",
                    status=DeliveryStatus.DELIVERED,
                )
            elif channel == ChannelType.WEBSOCKET:
                recipients = self.socket_manager.broadcast_to_room(
                    room=f"user:{payload.recipient_id}",
                    event_name="notification",
                    data={"subject": payload.subject, "body": payload.body_text},
                )
                res = ProviderResult(
                    success=True,
                    channel=ChannelType.WEBSOCKET,
                    provider_name="websocket_broadcaster",
                    status=DeliveryStatus.DELIVERED if recipients > 0 else DeliveryStatus.SUBMITTED,
                )
            else:
                res = ProviderResult(
                    success=False,
                    channel=channel,
                    provider_name="unsupported",
                    status=DeliveryStatus.FAILED,
                    error_message=f"Unsupported channel type {channel.value}",
                )

            provider_name = res.provider_name
            self.ledger.record_attempt(
                attempt_id=att_id,
                notification_id=payload.notification_id,
                channel=channel,
                provider_name=provider_name,
                status=res.status,
                attempt_number=attempt_num,
                error_message=res.error_message,
            )

            if res.success:
                return {
                    "success": True,
                    "channel": channel.value,
                    "provider": provider_name,
                    "attempts": attempt_num,
                    "provider_message_id": res.provider_message_id,
                }

            last_error = res.error_message
            if not res.is_retryable:
                break

        return {
            "success": False,
            "channel": channel.value,
            "provider": provider_name,
            "attempts": attempt_num,
            "error_message": last_error or "Dispatch failed after retries",
        }

    def get_in_app_inbox(self, user_id: str) -> List[NotificationPayload]:
        return self._in_app_inbox.get(user_id, [])
