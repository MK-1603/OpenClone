"""OpenClone Universal Communication & Notification Infrastructure Engine.

Provides multi-channel messaging (Email, SMS, Push, Real-Time WebSockets/SSE),
preference enforcement, quiet-hour calculation, provider failover, and delivery ledgers.
"""
from __future__ import annotations

from src.openclone.communication.dispatcher import (
    DeliveryLedger,
    NotificationDispatcher,
)
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
    FcmPushProvider,
    MockEmailProvider,
    MockPushProvider,
    MockSmsProvider,
    ProviderFailoverManager,
    ResendEmailProvider,
    TwilioSmsProvider,
)
from src.openclone.communication.realtime import (
    WebSocketConnection,
    WebSocketSessionManager,
)

__all__ = [
    "BaseEmailProvider",
    "BasePushProvider",
    "BaseSmsProvider",
    "ChannelType",
    "DeliveryAttempt",
    "DeliveryLedger",
    "DeliveryStatus",
    "FcmPushProvider",
    "MockEmailProvider",
    "MockPushProvider",
    "MockSmsProvider",
    "NotificationCategory",
    "NotificationDispatcher",
    "NotificationPayload",
    "NotificationPriority",
    "PreferenceEngine",
    "ProviderFailoverManager",
    "ProviderResult",
    "ResendEmailProvider",
    "TwilioSmsProvider",
    "UserPreference",
    "WebSocketConnection",
    "WebSocketSessionManager",
]
