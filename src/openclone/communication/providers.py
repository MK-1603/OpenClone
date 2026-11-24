"""Multi-Channel Provider Adapters and Failover Manager.

Implements decoupled providers for Email, SMS, and Push notifications with
automated failover and delivery result standardization.
"""
from __future__ import annotations

import abc
import re
from typing import Any, Dict, List, Optional

from src.openclone.communication.models import (
    ChannelType,
    DeliveryStatus,
    ProviderResult,
)


# ============================================================================
# BASE PROVIDER INTERFACES
# ============================================================================

class BaseEmailProvider(abc.ABC):
    """Abstract interface for transactional and bulk email providers."""

    @property
    @abc.abstractmethod
    def provider_name(self) -> str:
        pass

    @abc.abstractmethod
    def send_email(
        self,
        to_email: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> ProviderResult:
        pass


class BaseSmsProvider(abc.ABC):
    """Abstract interface for SMS messaging providers."""

    @property
    @abc.abstractmethod
    def provider_name(self) -> str:
        pass

    @abc.abstractmethod
    def send_sms(
        self,
        to_phone: str,
        body_text: str,
        sender_id: Optional[str] = None,
    ) -> ProviderResult:
        pass

    @staticmethod
    def calculate_segments(text: str) -> int:
        """Calculate SMS segments based on GSM-7 vs UCS-2 encoding."""
        # Simple detection: if any non-ASCII character exists, UCS-2 (70 chars per segment)
        # otherwise GSM-7 (160 chars per segment)
        try:
            text.encode("ascii")
            limit = 160
        except UnicodeEncodeError:
            limit = 70
        return max(1, (len(text) + limit - 1) // limit)


class BasePushProvider(abc.ABC):
    """Abstract interface for mobile and web push notification providers."""

    @property
    @abc.abstractmethod
    def provider_name(self) -> str:
        pass

    @abc.abstractmethod
    def send_push(
        self,
        device_tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> ProviderResult:
        pass


# ============================================================================
# CONCRETE ADAPTERS & MOCK PROVIDERS
# ============================================================================

class ResendEmailProvider(BaseEmailProvider):
    """Email provider adapter for Resend API."""

    def __init__(self, api_key: str = "mock_key"):
        self.api_key = api_key

    @property
    def provider_name(self) -> str:
        return "resend"

    def send_email(
        self,
        to_email: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> ProviderResult:
        # Validate recipient format
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", to_email):
            return ProviderResult(
                success=False,
                channel=ChannelType.EMAIL,
                provider_name=self.provider_name,
                status=DeliveryStatus.FAILED,
                error_message="Invalid email address format",
                is_retryable=False,
            )
        return ProviderResult(
            success=True,
            channel=ChannelType.EMAIL,
            provider_name=self.provider_name,
            provider_message_id=f"resend_{hash(to_email + subject) & 0xFFFFFFFF:08x}",
            status=DeliveryStatus.SUBMITTED,
            cost_usd=0.00028,
        )


class MockEmailProvider(BaseEmailProvider):
    """Configurable mock email provider for deterministic testing."""

    def __init__(self, provider_name: str = "mock_email", should_fail: bool = False, is_retryable: bool = False):
        self._name = provider_name
        self.should_fail = should_fail
        self.is_retryable = is_retryable
        self.sent_count = 0

    @property
    def provider_name(self) -> str:
        return self._name

    def send_email(
        self,
        to_email: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> ProviderResult:
        self.sent_count += 1
        if self.should_fail:
            return ProviderResult(
                success=False,
                channel=ChannelType.EMAIL,
                provider_name=self._name,
                status=DeliveryStatus.FAILED,
                error_message="Simulated provider connection error",
                is_retryable=self.is_retryable,
            )
        return ProviderResult(
            success=True,
            channel=ChannelType.EMAIL,
            provider_name=self._name,
            provider_message_id=f"mock_mail_{self.sent_count}",
            status=DeliveryStatus.SUBMITTED,
        )


class TwilioSmsProvider(BaseSmsProvider):
    """SMS provider adapter for Twilio."""

    def __init__(self, account_sid: str = "AC_mock", auth_token: str = "mock_token"):
        self.account_sid = account_sid
        self.auth_token = auth_token

    @property
    def provider_name(self) -> str:
        return "twilio"

    def send_sms(
        self,
        to_phone: str,
        body_text: str,
        sender_id: Optional[str] = None,
    ) -> ProviderResult:
        clean_phone = re.sub(r"[\s\-\(\)]", "", to_phone)
        if not re.match(r"^\+?[1-9]\d{7,14}$", clean_phone):
            return ProviderResult(
                success=False,
                channel=ChannelType.SMS,
                provider_name=self.provider_name,
                status=DeliveryStatus.FAILED,
                error_message="Invalid E.164 phone number format",
                is_retryable=False,
            )
        segments = self.calculate_segments(body_text)
        cost_per_segment = 0.0079
        return ProviderResult(
            success=True,
            channel=ChannelType.SMS,
            provider_name=self.provider_name,
            provider_message_id=f"SM_{hash(to_phone + body_text) & 0xFFFFFFFF:08x}",
            status=DeliveryStatus.SUBMITTED,
            cost_usd=round(cost_per_segment * segments, 4),
        )


class MockSmsProvider(BaseSmsProvider):
    """Configurable mock SMS provider for testing."""

    def __init__(self, provider_name: str = "mock_sms", should_fail: bool = False, is_retryable: bool = False):
        self._name = provider_name
        self.should_fail = should_fail
        self.is_retryable = is_retryable
        self.sent_count = 0

    @property
    def provider_name(self) -> str:
        return self._name

    def send_sms(
        self,
        to_phone: str,
        body_text: str,
        sender_id: Optional[str] = None,
    ) -> ProviderResult:
        self.sent_count += 1
        if self.should_fail:
            return ProviderResult(
                success=False,
                channel=ChannelType.SMS,
                provider_name=self._name,
                status=DeliveryStatus.FAILED,
                error_message="Simulated carrier rejection",
                is_retryable=self.is_retryable,
            )
        return ProviderResult(
            success=True,
            channel=ChannelType.SMS,
            provider_name=self._name,
            provider_message_id=f"mock_sms_{self.sent_count}",
            status=DeliveryStatus.SUBMITTED,
        )


class FcmPushProvider(BasePushProvider):
    """Push notification provider adapter for Firebase Cloud Messaging (FCM)."""

    def __init__(self, project_id: str = "mock-project"):
        self.project_id = project_id

    @property
    def provider_name(self) -> str:
        return "firebase_fcm"

    def send_push(
        self,
        device_tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> ProviderResult:
        if not device_tokens:
            return ProviderResult(
                success=False,
                channel=ChannelType.MOBILE_PUSH,
                provider_name=self.provider_name,
                status=DeliveryStatus.FAILED,
                error_message="No target device tokens provided",
                is_retryable=False,
            )
        return ProviderResult(
            success=True,
            channel=ChannelType.MOBILE_PUSH,
            provider_name=self.provider_name,
            provider_message_id=f"projects/{self.project_id}/messages/msg_{len(device_tokens)}",
            status=DeliveryStatus.SUBMITTED,
            cost_usd=0.0,
        )


class MockPushProvider(BasePushProvider):
    """Configurable mock push provider."""

    def __init__(self, provider_name: str = "mock_push", should_fail: bool = False, is_retryable: bool = False):
        self._name = provider_name
        self.should_fail = should_fail
        self.is_retryable = is_retryable
        self.sent_count = 0

    @property
    def provider_name(self) -> str:
        return self._name

    def send_push(
        self,
        device_tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> ProviderResult:
        self.sent_count += 1
        if self.should_fail:
            return ProviderResult(
                success=False,
                channel=ChannelType.MOBILE_PUSH,
                provider_name=self._name,
                status=DeliveryStatus.FAILED,
                error_message="Simulated FCM APNs gateway timeout",
                is_retryable=self.is_retryable,
            )
        return ProviderResult(
            success=True,
            channel=ChannelType.MOBILE_PUSH,
            provider_name=self._name,
            provider_message_id=f"mock_push_{self.sent_count}",
            status=DeliveryStatus.SUBMITTED,
        )


# ============================================================================
# PROVIDER FAILOVER MANAGER
# ============================================================================

class ProviderFailoverManager:
    """Manages primary and fallback providers for graceful channel degradation."""

    def __init__(self):
        self.email_providers: List[BaseEmailProvider] = []
        self.sms_providers: List[BaseSmsProvider] = []
        self.push_providers: List[BasePushProvider] = []

    def register_email_provider(self, provider: BaseEmailProvider):
        self.email_providers.append(provider)

    def register_sms_provider(self, provider: BaseSmsProvider):
        self.sms_providers.append(provider)

    def register_push_provider(self, provider: BasePushProvider):
        self.push_providers.append(provider)

    def dispatch_email_with_failover(
        self,
        to_email: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
    ) -> ProviderResult:
        if not self.email_providers:
            return ProviderResult(
                success=False,
                channel=ChannelType.EMAIL,
                provider_name="none",
                status=DeliveryStatus.FAILED,
                error_message="No email providers registered",
            )

        last_result: Optional[ProviderResult] = None
        for provider in self.email_providers:
            res = provider.send_email(to_email, subject, body_text, body_html)
            if res.success:
                return res
            last_result = res
            # Only failover to next provider if error is retryable/network outage
            if not res.is_retryable:
                break
        return last_result or ProviderResult(
            success=False,
            channel=ChannelType.EMAIL,
            provider_name="unknown",
            status=DeliveryStatus.FAILED,
            error_message="All email providers exhausted",
        )

    def dispatch_sms_with_failover(
        self,
        to_phone: str,
        body_text: str,
    ) -> ProviderResult:
        if not self.sms_providers:
            return ProviderResult(
                success=False,
                channel=ChannelType.SMS,
                provider_name="none",
                status=DeliveryStatus.FAILED,
                error_message="No SMS providers registered",
            )

        last_result: Optional[ProviderResult] = None
        for provider in self.sms_providers:
            res = provider.send_sms(to_phone, body_text)
            if res.success:
                return res
            last_result = res
            if not res.is_retryable:
                break
        return last_result or ProviderResult(
            success=False,
            channel=ChannelType.SMS,
            provider_name="unknown",
            status=DeliveryStatus.FAILED,
            error_message="All SMS providers exhausted",
        )
