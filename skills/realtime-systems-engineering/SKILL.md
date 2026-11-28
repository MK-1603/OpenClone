---
id: realtime-systems-engineering
name: Real-Time Systems & WebSocket Engineering
version: 1.0.0
description: WebSockets, Server-Sent Events (SSE), WebRTC, connection lifecycle, handshake authentication, presence tracking, heartbeats, and reconnection recovery.
precedence: 35
category: backend
triggers:
  - "websocket"
  - "real-time"
  - "sse"
  - "server-sent events"
  - "socket connection"
  - "presence tracking"
negative_triggers:
  - "static html"
pre_build_gates:
  - "Enforce authentication at initial handshake (JWT or signed ticket; never plain credentials in query string)."
  - "Implement ping/pong heartbeat keepalive with configurable connection reaping."
finish_gates:
  - "Verify reconnection exponential backoff and missed event replay capabilities."
  - "Ensure room broadcasting enforces subscriber authorization checks."
maturity: L4_TESTED
---

# Real-Time Systems & WebSocket Engineering

## 1. Overview
Governs bidirectional WebSocket communication, Server-Sent Events (SSE) streaming, room pub/sub broadcasting, heartbeat keepalives, and online presence tracking.

## 2. Technical Standards
- **Handshake Security:** Authenticate connections during the initial HTTP upgrade handshake; reject unauthenticated connections immediately.
- **Heartbeats & Reaping:** Periodic ping/pong frames; automatically terminate silent connections exceeding idle thresholds (default 60s).
- **Presence & Rooms:** Decouple socket connections from user IDs to support multi-device user presence; room-based broadcast isolation.

## 3. Engine Reference
- `src/openclone/communication/realtime.py` (`WebSocketSessionManager`, `WebSocketConnection`)
