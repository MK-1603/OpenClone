---
id: sms-engineering
name: SMS Messaging & Verification Engineering
version: 1.0.0
description: SMS gateways, GSM-7 vs UCS-2 encoding calculation, OTP security, rate limiting, delivery receipts, and regional compliance (TRAI/DLT).
precedence: 33
category: backend
triggers:
  - "sms"
  - "sms otp"
  - "twilio"
  - "phone verification"
  - "text message"
  - "gsm-7"
negative_triggers:
  - "mobile app styling"
pre_build_gates:
  - "Enforce E.164 international phone number format validation."
  - "Configure OTP attempt rate limits (max 3 tries, 5-minute expiry, salt hashing)."
finish_gates:
  - "Verify GSM-7 (160 char) and UCS-2 (70 char) segment cost estimation."
  - "Implement carrier delivery callback signature verification."
maturity: L4_TESTED
---

# SMS Messaging & Verification Engineering

## 1. Overview
Governs SMS messaging, multi-part segmentation, OTP verification workflows, carrier delivery tracking, and regional messaging regulations.

## 2. Technical Standards
- **Encoding & Segmentation:** GSM-7 (160 chars/segment, 153 for multi-part) vs UCS-2 (70 chars/segment, 67 for multi-part).
- **OTP Security:** Expiration strictly ≤ 5 minutes; cryptographic hashing; brute-force protection (max 3 validation attempts).
- **Regional Compliance:** Strict adherence to India TRAI/DLT template IDs and registered Principal Entity headers where applicable.
- **Provider Integration:** Twilio, Vonage, Plivo, and AWS End User Messaging adapters.

## 3. Engine Reference
- `src/openclone/communication/providers.py` (`TwilioSmsProvider`, `BaseSmsProvider`)
