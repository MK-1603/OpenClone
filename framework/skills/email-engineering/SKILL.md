---
id: email-engineering
name: Email Infrastructure & Deliverability Engineering
version: 1.0.0
description: SMTP/STARTTLS protocols, SPF/DKIM/DMARC authentication, transactional email templates, bounce/complaint handling, and deliverability reputation management.
precedence: 32
category: backend
triggers:
  - "email"
  - "email delivery"
  - "email deliverability"
  - "smtp"
  - "dkim"
  - "spf"
  - "dmarc"
  - "transactional email"
  - "email template"
  - "ses"
  - "resend"
negative_triggers:
  - "css animation"
pre_build_gates:
  - "Verify domain DNS records: SPF, DKIM, DMARC, and MX configuration."
  - "Implement header injection and template injection validation guards."
finish_gates:
  - "Configure automated bounce and complaint webhook ingestion into suppression list."
  - "Ensure responsive HTML emails contain strict plain-text MIME fallbacks."
maturity: L4_TESTED
---

# Email Infrastructure & Deliverability Engineering

## 1. Overview
Governs transactional and system email infrastructure, MIME composition, deliverability reputation, DNS authentication, and automated bounce handling.

## 2. Technical Standards
- **Authentication:** Mandatory SPF (`v=spf1 ...`), DKIM (2048-bit RSA), and DMARC (`p=reject` or `p=quarantine`).
- **Lifecycle Tracking:** Track status across Created, Queued, Submitted, Delivered, Bounced, Complained, and Suppressed.
- **Security:** Prevent CRLF header injection (`\r\n`), sanitize template inputs, and redact authentication links from logs.
- **Provider Adapters:** Decoupled support for Resend, Amazon SES, SendGrid, Mailgun, and Postmark.

## 3. Engine Reference
- `src/openclone/communication/providers.py` (`ResendEmailProvider`, `BaseEmailProvider`)
