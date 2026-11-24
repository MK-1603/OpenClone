"""Communication and Notification Data Models.

Defines unified entity schemas, priority definitions, and delivery lifecycle states.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ChannelType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    MOBILE_PUSH = "mobile_push"
    WEB_PUSH = "web_push"
    IN_APP = "in_app"
    WEBSOCKET = "websocket"
    SSE = "sse"
    WEBHOOK = "webhook"


class NotificationCategory(str, Enum):
    SECURITY = "security"          # Mandatory; bypasses quiet hours and opt-outs
    TRANSACTIONAL = "transactional" # High priority; e.g. receipts, order updates
    SYSTEM = "system"              # Maintenance, operational updates
    REMINDER = "reminder"          # Appointments, tasks
    MARKETING = "marketing"        # Requires explicit opt-in, strict quiet hours
    PROMOTIONAL = "promotional"    # Promotional campaigns


class NotificationPriority(int, Enum):
    CRITICAL_SECURITY = 0  # Highest, dedicated queue, zero throttling
    TRANSACTIONAL = 1      # Core business events
    NORMAL = 2             # Daily reminders, standard in-app
    BULK_MARKETING = 3     # Low priority, background throttling


class DeliveryStatus(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    SUBMITTED = "submitted"
    DELIVERED = "delivered"
    BOUNCED = "bounced"
    FAILED = "failed"
    SUPPRESSED = "suppressed"
    SUPPRESSED_QUIET_HOURS = "suppressed_quiet_hours"


@dataclass
class UserPreference:
    """User delivery preferences across channels and quiet hours."""
    user_id: str
    allowed_channels: List[ChannelType] = field(default_factory=lambda: [ChannelType.EMAIL, ChannelType.IN_APP])
    opted_out_categories: List[NotificationCategory] = field(default_factory=list)
    quiet_hours_enabled: bool = False
    quiet_hours_start_hour: int = 22  # 10 PM
    quiet_hours_end_hour: int = 8     # 8 AM
    user_timezone_offset_hours: float = 0.0  # UTC offset in hours


@dataclass
class NotificationPayload:
    """Complete multi-channel notification dispatch payload."""
    notification_id: str
    recipient_id: str
    category: NotificationCategory
    priority: NotificationPriority
    channels: List[ChannelType]
    subject: str
    body_text: str
    body_html: Optional[str] = None
    recipient_email: Optional[str] = None
    recipient_phone: Optional[str] = None
    device_tokens: List[str] = field(default_factory=list)
    idempotency_key: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at_epoch: float = field(default_factory=time.time)


@dataclass
class ProviderResult:
    """Result from external channel provider delivery."""
    success: bool
    channel: ChannelType
    provider_name: str
    provider_message_id: Optional[str] = None
    status: DeliveryStatus = DeliveryStatus.SUBMITTED
    error_message: Optional[str] = None
    is_retryable: bool = False
    cost_usd: float = 0.0


@dataclass
class DeliveryAttempt:
    """Audit record for a single delivery attempt."""
    attempt_id: str
    notification_id: str
    channel: ChannelType
    provider_name: str
    status: DeliveryStatus
    attempt_number: int
    timestamp_epoch: float
    error_message: Optional[str] = None
    sha256_hash: str = ""
