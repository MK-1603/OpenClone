# Paperclip Remote HTTP Adapter

**Version:** 2.0.0  
**Classification:** Integration Guide  
**Status:** IMPLEMENTED  

---

## 1. Overview

The Paperclip Remote HTTP Adapter allows OpenClone to act as a secure, distributed workforce node controlled by external orchestrators (such as the Paperclip Multi-Agent Governance Framework). It exposes REST endpoints protected by cryptographic HMAC-SHA256 authentication and binds all operations to the deterministic OpenClone runtime.

Module implementation: `src/openclone/integrations/paperclip/server.py`

---

## 2. API Endpoints

| Method | Path | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Node health, active engine count, and uptime | No |
| `GET` | `/capabilities` | Advertised agent roles, engine versions, and tools | Yes |
| `GET` | `/tasks` | List recent task summaries from SQLite ledger | Yes |
| `POST` | `/tasks` | Ingest and dispatch a new engineering task | Yes |
| `GET` | `/tasks/{task_id}` | Retrieve real-time status and execution outputs of a task | Yes |

---

## 3. Server Configuration

The server configuration can be initialized programmatically or via environment variables:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `PAPERCLIP_SERVER_HOST` | `127.0.0.1` | Network interface to bind HTTP listener |
| `PAPERCLIP_SERVER_PORT` | `8443` | Listening port |
| `PAPERCLIP_API_SECRET` | *(Required in prod)* | Symmetric secret for HMAC signature generation |
| `PAPERCLIP_ALLOW_ANONYMOUS` | `false` | Development flag allowing unsigned requests (strictly disabled in prod) |

---

## 4. Usage Example

### Starting the Server

```python
from openclone.integrations.paperclip.server import PaperclipHTTPServer, PaperclipServerConfig

config = PaperclipServerConfig(
    host="127.0.0.1",
    port=8443,
    api_secret="prod-enterprise-paperclip-secret-32-bytes-min",
    allow_anonymous=False
)

server = PaperclipHTTPServer(config=config)
server.start()
```

### Dispatching a Governed Task via cURL

```bash
TIMESTAMP=$(date +%s)
NONCE=$(uuidgen)
SECRET="prod-enterprise-paperclip-secret-32-bytes-min"
BODY='{"task_id":"TASK-101","agent_id":"backend-agent","description":"Generate microservice boilerplate"}'

MESSAGE="${TIMESTAMP}:${NONCE}:${BODY}"
SIGNATURE=$(echo -n "$MESSAGE" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print $2}')

curl -X POST http://127.0.0.1:8443/tasks \
  -H "Content-Type: application/json" \
  -H "X-OpenClone-Timestamp: $TIMESTAMP" \
  -H "X-OpenClone-Nonce: $NONCE" \
  -H "X-OpenClone-Signature: $SIGNATURE" \
  -d "$BODY"
```
