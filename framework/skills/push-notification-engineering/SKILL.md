---
id: push-notification-engineering
name: Push Notification & Device Token Engineering
version: 1.0.0
description: Mobile push (FCM, APNs), Web Push (VAPID, Service Workers), device token lifecycle, invalidation handling, and notification categorization.
precedence: 34
category: backend
triggers:
  - "push notification"
  - "fcm"
  - "apns"
  - "web push"
  - "vapid"
  - "device token"
negative_triggers:
  - "css layout"
pre_build_gates:
  - "Implement device token registration and automated invalidation upon 410 Gone / NotRegistered response."
  - "Configure notification channels (Android) and category action identifiers (iOS)."
finish_gates:
  - "Verify silent data payloads vs alert notifications across mobile and web."
  - "Ensure user opt-in permissions are tracked prior to dispatch."
maturity: L4_TESTED
---

# Push Notification & Device Token Engineering

## 1. Overview
Governs mobile and web push notifications, device token storage, VAPID key signing, token rotation, and provider response handling across Apple APNs and Google FCM.

## 2. Technical Standards
- **Token Lifecycle:** Prune inactive or invalidated tokens upon provider rejection (`Unregistered` / `BadDeviceToken`).
- **Web Push:** VAPID public/private key pairs with standard payload encryption (RFC 8291).
- **Collapse Keys & Badges:** Use collapse keys to prevent stale notification clutter; manage server-side badge counts.

## 3. Engine Reference
- `src/openclone/communication/providers.py` (`FcmPushProvider`, `BasePushProvider`)
