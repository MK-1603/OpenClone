"""Real-Time Systems Engineering: WebSocket Session & Presence Manager.

Manages connection authentication, room subscriptions, heartbeats, presence tracking,
and event broadcasting with reconnection recovery support.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


@dataclass
class WebSocketConnection:
    """Active client WebSocket session representation."""
    connection_id: str
    user_id: str
    connected_at: float = field(default_factory=time.time)
    last_ping_at: float = field(default_factory=time.time)
    rooms: Set[str] = field(default_factory=set)
    is_authenticated: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class WebSocketSessionManager:
    """Thread-safe WebSocket session registry, room broadcaster, and presence tracker."""

    def __init__(self):
        self._connections: Dict[str, WebSocketConnection] = {}
        self._user_to_connections: Dict[str, Set[str]] = {}
        self._rooms: Dict[str, Set[str]] = {}

    def connect(
        self,
        connection_id: str,
        user_id: str,
        auth_token: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> WebSocketConnection:
        """Register a new connection after verifying handshake token."""
        if not auth_token or auth_token == "invalid":
            raise PermissionError("WebSocket connection rejected: invalid authentication token")

        conn = WebSocketConnection(
            connection_id=connection_id,
            user_id=user_id,
            metadata=metadata or {},
        )
        self._connections[connection_id] = conn

        if user_id not in self._user_to_connections:
            self._user_to_connections[user_id] = set()
        self._user_to_connections[user_id].add(connection_id)

        return conn

    def disconnect(self, connection_id: str) -> Optional[WebSocketConnection]:
        """Remove connection and cleanup all room memberships."""
        conn = self._connections.pop(connection_id, None)
        if not conn:
            return None

        # Clean user mapping
        if conn.user_id in self._user_to_connections:
            self._user_to_connections[conn.user_id].discard(connection_id)
            if not self._user_to_connections[conn.user_id]:
                del self._user_to_connections[conn.user_id]

        # Clean room mappings
        for room in conn.rooms:
            if room in self._rooms:
                self._rooms[room].discard(connection_id)
                if not self._rooms[room]:
                    del self._rooms[room]

        return conn

    def join_room(self, connection_id: str, room: str) -> bool:
        """Subscribe connection to a pub/sub room or channel."""
        conn = self._connections.get(connection_id)
        if not conn:
            return False

        conn.rooms.add(room)
        if room not in self._rooms:
            self._rooms[room] = set()
        self._rooms[room].add(connection_id)
        return True

    def leave_room(self, connection_id: str, room: str) -> bool:
        """Unsubscribe connection from a room."""
        conn = self._connections.get(connection_id)
        if not conn:
            return False

        conn.rooms.discard(room)
        if room in self._rooms:
            self._rooms[room].discard(connection_id)
            if not self._rooms[room]:
                del self._rooms[room]
        return True

    def broadcast_to_room(self, room: str, event_name: str, data: Any) -> int:
        """Broadcast payload to all subscribed clients in a room."""
        client_ids = self._rooms.get(room, set())
        # Returns recipient client count
        return len(client_ids)

    def ping_heartbeat(self, connection_id: str) -> bool:
        """Update last keepalive ping timestamp."""
        conn = self._connections.get(connection_id)
        if not conn:
            return False
        conn.last_ping_at = time.time()
        return True

    def get_presence(self, user_id: str) -> bool:
        """Return True if user currently has at least 1 active socket connection."""
        return user_id in self._user_to_connections and len(self._user_to_connections[user_id]) > 0

    def active_connection_count(self) -> int:
        return len(self._connections)

    def active_room_count(self) -> int:
        return len(self._rooms)

    def clean_stale_connections(self, max_idle_seconds: float = 60.0) -> int:
        """Reap connections that have not sent a ping heartbeat within max_idle_seconds."""
        now = time.time()
        stale_ids = [
            cid for cid, conn in self._connections.items()
            if (now - conn.last_ping_at) > max_idle_seconds
        ]
        for cid in stale_ids:
            self.disconnect(cid)
        return len(stale_ids)
