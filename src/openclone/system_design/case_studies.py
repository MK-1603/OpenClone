"""Real-World System Design Case Study Catalogue.

Provides pre-analyzed, production-ready architectures across 20 canonical
industry software systems per OpenClone Universal System Design Standard.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CaseStudyArchitecture:
    """Detailed architectural blueprint for a real-world system design case."""
    case_id: str
    name: str
    category: str
    summary: str
    key_challenges: List[str]
    primary_components: List[str]
    data_model_entities: List[str]
    concurrency_strategy: str
    failure_handling: str
    recommended_stack: Dict[str, str]


class SystemDesignCatalogue:
    """Repository of 20 canonical real-world system design case studies."""

    _CATALOGUE: Dict[str, CaseStudyArchitecture] = {}

    @classmethod
    def _initialize(cls):
        if cls._CATALOGUE:
            return

        cases = [
            CaseStudyArchitecture(
                case_id="CS-01",
                name="Authentication & Identity System",
                category="Security & Identity",
                summary="Unified authentication and session management with MFA, passkeys, and token rotation.",
                key_challenges=["Brute-force attacks", "Session invalidation race conditions", "Clock skew in JWTs"],
                primary_components=["Auth Gateway", "Argon2id Hasher", "Redis Token/Revocation Store", "PostgreSQL User Store"],
                data_model_entities=["User", "Credential", "Session", "MfaDevice", "AuditLog"],
                concurrency_strategy="Atomic token rotation via Redis Lua scripts; optimistic locking on user record.",
                failure_handling="Deny-by-default on redis failure; fail closed for auth; rate limiting at reverse proxy.",
                recommended_stack={"auth": "OAuth2.1 / OIDC", "db": "PostgreSQL", "cache": "Redis", "hasher": "Argon2id"},
            ),
            CaseStudyArchitecture(
                case_id="CS-02",
                name="URL Shortener",
                category="High-Throughput Web Services",
                summary="High-volume short-link generation and redirection with sub-50ms p99 latency.",
                key_challenges=["Hash collision prevention", "Write scalability vs read surge", "Cache stampede"],
                primary_components=["Reverse Proxy", "Base62 Encoder / Range Key Allocator", "Redis Cache", "PostgreSQL / DynamoDB"],
                data_model_entities=["ShortUrl", "UrlAnalytics", "UserAccount"],
                concurrency_strategy="Pre-allocated sequence ranges (ZooKeeper or Redis INCR by 10,000) for collision-free Base62 IDs.",
                failure_handling="Cache-aside with fallback to read replica; HTTP 301 vs 302 analytics trade-off handling.",
                recommended_stack={"app": "Go / FastAPI", "db": "PostgreSQL / ScyllaDB", "cache": "Redis Cluster", "proxy": "Cloudflare / NGINX"},
            ),
            CaseStudyArchitecture(
                case_id="CS-03",
                name="Real-Time Chat & Messaging System",
                category="Communication & Collaboration",
                summary="One-to-one and group messaging with presence, delivery receipts, and offline queuing.",
                key_challenges=["Connection state maintenance", "Message ordering across partitions", "Offline sync"],
                primary_components=["WebSocket Gateway", "Redis Pub/Sub & Presence", "Kafka / RabbitMQ", "Cassandra / ScyllaDB"],
                data_model_entities=["Message", "Conversation", "Participant", "Receipt", "DevicePresence"],
                concurrency_strategy="Snowflake ID generation for monotonic message sorting; partition per conversation ID.",
                failure_handling="WebSocket heartbeat with exponential reconnect; offline sync queue upon reconnect.",
                recommended_stack={"gateway": "Node.js / Go WebSockets", "broker": "Redis Streams / Kafka", "db": "ScyllaDB / PostgreSQL", "presence": "Redis"},
            ),
            CaseStudyArchitecture(
                case_id="CS-04",
                name="Social Media News Feed",
                category="Content Distribution",
                summary="Timeline aggregation with fan-out-on-write for standard users and fan-out-on-read for high-follower celebrities.",
                key_challenges=["Celebrity follower problem", "Storage explosion from duplicate feeds", "Stale cache"],
                primary_components=["Feed Service", "Fan-out Worker Pool", "Redis Feed Cache", "Object Store (Media)"],
                data_model_entities=["Post", "UserFollow", "UserTimeline", "MediaAsset"],
                concurrency_strategy="Hybrid fan-out: fan-out-on-write for users < 25k followers; dynamic merge for celebrities.",
                failure_handling="Asynchronous fan-out via worker queues; degraded feed serving from cached fallback.",
                recommended_stack={"feed": "Python / Rust", "cache": "Redis Cluster", "db": "PostgreSQL + Cassandra", "media": "S3 / Cloudflare R2"},
            ),
            CaseStudyArchitecture(
                case_id="CS-05",
                name="Distributed File & Object Storage",
                category="Storage Systems",
                summary="Scalable file uploads, multipart chunking, signed URLs, and content deduplication.",
                key_challenges=["Large file upload timeouts", "Bandwidth saturation", "Deduplication overhead"],
                primary_components=["API Gateway", "Presigned URL Generator", "S3/GCS Object Storage", "Metadata Database"],
                data_model_entities=["FileMetadata", "FileChunk", "AccessPolicy", "StorageBucket"],
                concurrency_strategy="Direct client-to-storage upload via presigned S3 URLs; SHA-256 chunk deduplication.",
                failure_handling="Resumable multipart uploads; retry failed chunk without restarting entire file.",
                recommended_stack={"api": "FastAPI", "storage": "AWS S3 / MinIO", "meta_db": "PostgreSQL", "cdn": "CloudFront"},
            ),
            CaseStudyArchitecture(
                case_id="CS-06",
                name="Video & Media Streaming System",
                category="Media & Streaming",
                summary="Video ingestion, asynchronous transcoding, adaptive bitrate streaming (HLS/DASH), and CDN caching.",
                key_challenges=["High compute transcoding cost", "Bandwidth consumption", "Buffering latency"],
                primary_components=["Upload Service", "Transcoding Worker Fleet (FFmpeg)", "Origin Storage", "CDN Edge Cache"],
                data_model_entities=["Video", "TranscodedVariant", "PlaylistManifest", "PlaybackSession"],
                concurrency_strategy="Queue-based asynchronous batch processing for transcoding; HLS segment caching at CDN.",
                failure_handling="Chunked transcoding jobs with checkpoint resumption; graceful quality degradation.",
                recommended_stack={"workers": "FFmpeg on Docker/K8s", "queue": "AWS SQS / RabbitMQ", "storage": "S3", "cdn": "Fastly / Cloudflare"},
            ),
            CaseStudyArchitecture(
                case_id="CS-07",
                name="Distributed Search Engine",
                category="Search & Indexing",
                summary="Full-text and faceted search with inverted index synchronization and typo-tolerant query parsing.",
                key_challenges=["Search index latency vs freshness", "Faceted aggregation performance", "Index rebuilds"],
                primary_components=["Search Ingestion Pipeline", "Elasticsearch / OpenSearch", "Primary DB", "Change Data Capture (Debezium)"],
                data_model_entities=["IndexedDocument", "SearchIndexSchema", "QueryAnalytics", "SynonymDictionary"],
                concurrency_strategy="Asynchronous Change Data Capture (CDC) via Kafka to update search indexes without blocking writes.",
                failure_handling="Circuit breaker on search cluster; fallback to primary database indexed lookup or cached results.",
                recommended_stack={"search": "OpenSearch / Elasticsearch", "cdc": "Debezium + Kafka", "primary_db": "PostgreSQL"},
            ),
            CaseStudyArchitecture(
                case_id="CS-08",
                name="E-Commerce Platform",
                category="Commerce & Transactions",
                summary="Catalogue browsing, cart management, inventory reservation, and order lifecycle management.",
                key_challenges=["Inventory overselling", "Flash sale concurrency spikes", "Checkout abandonment"],
                primary_components=["Product Catalogue", "Inventory Service", "Cart Service", "Order Checkout Coordinator"],
                data_model_entities=["Product", "InventoryItem", "Cart", "Order", "OrderItem"],
                concurrency_strategy="Optimistic locking on inventory records with temporary reservation holds (Redis TTL lock).",
                failure_handling="Automatic inventory hold release upon payment timeout; idempotency key on order placement.",
                recommended_stack={"framework": "Django / FastAPI", "db": "PostgreSQL", "cache": "Redis", "queue": "RabbitMQ"},
            ),
            CaseStudyArchitecture(
                case_id="CS-09",
                name="Payment Processing Platform",
                category="Financial & Ledger",
                summary="Double-entry ledger payment processing with idempotency keys and reconciliation.",
                key_challenges=["Double charging", "Webhook loss / replay", "Partial transaction failures"],
                primary_components=["Payment Gateway Integration", "Idempotency Filter", "Double-Entry Ledger", "Reconciliation Worker"],
                data_model_entities=["PaymentIntent", "LedgerAccount", "LedgerEntry", "WebhookEvent"],
                concurrency_strategy="Strict database unique constraint on Idempotency-Key; double-entry immutable accounting.",
                failure_handling="Provider webhook verification with HMAC signature; automated reconciliation cron for unconfirmed intents.",
                recommended_stack={"api": "Go / Python", "db": "PostgreSQL (ACID Serializable)", "vault": "HashiCorp Vault", "queue": "SQS"},
            ),
            CaseStudyArchitecture(
                case_id="CS-10",
                name="Booking & Reservation System",
                category="Reservations & Inventory",
                summary="Time-slotted inventory booking with temporary hold expiration and zero double-booking.",
                key_challenges=["Race conditions on simultaneous bookings", "Abandonment of holds", "Time-zone calculation bugs"],
                primary_components=["Booking Service", "Inventory Lock Manager", "Hold Expiration Sweeper", "Notification Service"],
                data_model_entities=["Slot", "Reservation", "Customer", "HoldLock"],
                concurrency_strategy="Row-level `SELECT ... FOR UPDATE` or Redis distributed lock with 10-minute TTL hold.",
                failure_handling="Background sweeper reclaims expired holds; idempotent confirmation endpoint.",
                recommended_stack={"app": "FastAPI", "db": "PostgreSQL", "lock": "Redis Redlock / DB lock", "scheduler": "Celery Beat"},
            ),
            CaseStudyArchitecture(
                case_id="CS-11",
                name="Ride-Hailing & Geospatial Matching",
                category="Geospatial & Real-time",
                summary="Real-time driver location tracking, H3/S2 spatial indexing, and trip dispatch.",
                key_challenges=["High write frequency for GPS coordinates", "Sub-second driver matching", "Location drift"],
                primary_components=["Location Ingestion Gateway", "Geospatial Index (H3/Redis GEO)", "Matching Engine", "Trip State Machine"],
                data_model_entities=["DriverLocation", "Trip", "Rider", "GeofenceZone"],
                concurrency_strategy="Spatial cell partitioning (Uber H3 hex bins); ephemeral driver location in Redis GEO.",
                failure_handling="Driver heartbeat expiration after 15s missing ping; idempotent trip state transitions.",
                recommended_stack={"gateway": "Go WebSocket Gateway", "geo_index": "Redis GEO / Uber H3", "db": "PostGIS", "broker": "Kafka"},
            ),
            CaseStudyArchitecture(
                case_id="CS-12",
                name="Event Ticket Booking System",
                category="High-Concurrency Booking",
                summary="High-concurrency seat selection, virtual waiting room, and ticket hold allocation.",
                key_challenges=["Massive traffic spike on ticket release", "Bot traffic", "Seat contention"],
                primary_components=["Virtual Waiting Room (Queue-it / Cloudflare)", "Seat Inventory Service", "Redis Seat State", "Payment Processor"],
                data_model_entities=["Event", "Seat", "TicketHold", "Order"],
                concurrency_strategy="Token-bucket queue gate into checkout; atomic seat reservation in Redis bitmap / Lua script.",
                failure_handling="Virtual queue throttles ingress to prevent database overload; auto-expire uncompleted checkouts.",
                recommended_stack={"waiting_room": "Cloudflare Workers", "db": "PostgreSQL", "cache": "Redis Lua", "queue": "RabbitMQ"},
            ),
            CaseStudyArchitecture(
                case_id="CS-13",
                name="Real-Time Analytics Ingestion System",
                category="Analytics & Big Data",
                summary="High-throughput telemetry ingestion, event deduplication, and OLAP columnar querying.",
                key_challenges=["Millions of events/sec write rate", "Out-of-order arrival", "Query aggregation latency"],
                primary_components=["Ingestion HTTP Gateway", "Kafka / Event Hub", "Stream Processor (Flink/Vector)", "ClickHouse / BigQuery"],
                data_model_entities=["RawEvent", "HourlyAggregatedMetric", "DimensionTable"],
                concurrency_strategy="Partitioning by tenant/device ID in Kafka; micro-batching writes to columnar OLAP engine.",
                failure_handling="Dead-letter queue for malformed telemetry; idempotent stream offset checkpointing.",
                recommended_stack={"gateway": "Go HTTP Gateway", "buffer": "Kafka", "olap": "ClickHouse", "visualization": "Grafana / Cube.js"},
            ),
            CaseStudyArchitecture(
                case_id="CS-14",
                name="Centralized Logging & Monitoring System",
                category="Observability Infrastructure",
                summary="Log shipping, structured parsing, retention policies, and alert rule evaluation.",
                key_challenges=["Log volume overwhelming storage", "High cardinality metric indexing", "Alert storming"],
                primary_components=["Log Forwarder (Vector / FluentBit)", "Kafka Buffer", "Loki / OpenSearch", "Prometheus / Thanos"],
                data_model_entities=["LogEntry", "MetricSeries", "AlertRule", "IncidentRecord"],
                concurrency_strategy="Log stream partitioning by service/environment; sampling and dynamic drop for DEBUG logs.",
                failure_handling="Backpressure signaling to log agents; rate-limiting alert notifications to prevent fatigue.",
                recommended_stack={"shipper": "Vector", "logs": "Grafana Loki", "metrics": "Prometheus", "alerts": "Alertmanager"},
            ),
            CaseStudyArchitecture(
                case_id="CS-15",
                name="Workflow Automation & Orchestration Engine",
                category="Workflow & State Machines",
                summary="Directed Acyclic Graph (DAG) workflow execution with retry policies and compensation.",
                key_challenges=["Worker crashes mid-step", "Long-running workflow state tracking", "Idempotency"],
                primary_components=["Workflow API", "State Machine Coordinator", "Step Worker Fleet", "Audit Log Ledger"],
                data_model_entities=["WorkflowDefinition", "WorkflowExecution", "StepExecution", "ExecutionHistory"],
                concurrency_strategy="Deterministic state machine with optimistic locking on execution state record.",
                failure_handling="Exponential backoff with jitter on transient failures; compensation tasks on fatal step abort.",
                recommended_stack={"engine": "Temporal / Celery Workflows", "db": "PostgreSQL", "broker": "Redis / RabbitMQ"},
            ),
            CaseStudyArchitecture(
                case_id="CS-16",
                name="Multi-Tenant B2B SaaS Platform",
                category="SaaS Architecture",
                summary="Organization onboarding, tenant data isolation (RLS), RBAC, usage metering, and audit logging.",
                key_challenges=["Cross-tenant data leakage", "Noisy neighbor resource starvation", "Tenant configuration drift"],
                primary_components=["Tenant Context Middleware", "Row-Level Security Filter", "Quota Rate Limiter", "Metering Engine"],
                data_model_entities=["Organization", "User", "RolePermission", "TenantSubscription", "UsageRecord"],
                concurrency_strategy="Per-tenant connection limits; database Row-Level Security (`current_setting('app.tenant_id')`).",
                failure_handling="Circuit breaker per tenant for external integrations; tenant quota enforcement at gateway.",
                recommended_stack={"backend": "FastAPI / NestJS", "db": "PostgreSQL with RLS", "cache": "Redis (Tenant Prefixed)", "billing": "Stripe"},
            ),
            CaseStudyArchitecture(
                case_id="CS-17",
                name="Feature Flag & Remote Configuration System",
                category="Configuration Management",
                summary="Dynamic evaluation of feature toggles, user percentage rollouts, and kill switches.",
                key_challenges=["Evaluation latency on critical path", "Flag synchronization drift", "Rule evaluation overhead"],
                primary_components=["Flag Admin Dashboard", "In-Memory Flag Evaluation Client", "SSE/WebSocket Sync Stream", "Audit Ledger"],
                data_model_entities=["FeatureFlag", "TargetingRule", "SegmentDefinition", "AuditTrail"],
                concurrency_strategy="Local in-memory evaluation within client SDK; streaming updates via SSE on change.",
                failure_handling="Default fallback flag values embedded in application code if evaluation service is unreachable.",
                recommended_stack={"service": "Go / Node.js", "db": "PostgreSQL", "streaming": "Server-Sent Events (SSE)", "sdk": "In-Memory"},
            ),
            CaseStudyArchitecture(
                case_id="CS-18",
                name="Developer API Platform & Gateway",
                category="API Platform",
                summary="API key provisioning, developer portal, tiered rate limiting, request validation, and analytics.",
                key_challenges=["API key validation latency", "Accurate quota tracking without bottlenecks", "DDoS mitigation"],
                primary_components=["API Gateway", "Token Bucket Rate Limiter", "Developer Portal", "Analytics Collector"],
                data_model_entities=["ApiKey", "DeveloperAccount", "ApiProduct", "QuotaTier", "UsageMetric"],
                concurrency_strategy="In-memory Redis Token Bucket with local caching of hashed API keys.",
                failure_handling="Graceful fallback to standard tier if Redis rate-limiter is unreachable; HTTP 429 response.",
                recommended_stack={"gateway": "Kong / Envoy / Traefik", "cache": "Redis", "db": "PostgreSQL", "docs": "OpenAPI / Redoc"},
            ),
            CaseStudyArchitecture(
                case_id="CS-19",
                name="Real-Time Collaborative Document Editor",
                category="Collaboration & Real-Time",
                summary="Concurrent document editing with Conflict-free Replicated Data Types (CRDTs) and presence.",
                key_challenges=["Network latency conflicts", "Offline edit reconciliation", "Undo/redo consistency"],
                primary_components=["WebSocket Gateway", "CRDT Document Sync Engine (Yjs / Automerge)", "Snapshot Storage", "Presence Service"],
                data_model_entities=["Document", "DocumentSnapshot", "OperationLog", "UserSession"],
                concurrency_strategy="Conflict-free Replicated Data Types (State-based CRDTs); peer-to-peer or server-mediated sync.",
                failure_handling="Periodic full document snapshots to object storage; local IndexedDB offline storage.",
                recommended_stack={"crdt": "Yjs", "gateway": "WebSocket Server (Node/Go)", "db": "PostgreSQL", "storage": "S3 (Snapshots)"},
            ),
            CaseStudyArchitecture(
                case_id="CS-20",
                name="Personalized Recommendation Engine",
                category="Machine Learning & AI",
                summary="User event collection, candidate generation, real-time feature retrieval, and inference ranking.",
                key_challenges=["Inference latency (<100ms)", "Feature store consistency", "Cold-start for new users"],
                primary_components=["Event Collector", "Real-Time Feature Store (Feast / Redis)", "Candidate Generator", "Ranking Model Server"],
                data_model_entities=["UserEmbedding", "ItemEmbedding", "InteractionLog", "ModelArtifact"],
                concurrency_strategy="Two-stage architecture: Approximate Nearest Neighbor (ANN) candidate retrieval + ranking model.",
                failure_handling="Fallback to popularity-based fallback rankings if ML ranking service exceeds 80ms timeout.",
                recommended_stack={"feature_store": "Redis / Feast", "ann": "Qdrant / Milvus", "model_server": "Triton / ONNX Runtime", "db": "PostgreSQL"},
            ),
        ]

        for c in cases:
            cls._CATALOGUE[c.case_id] = c

    @classmethod
    def get(cls, case_id: str) -> Optional[CaseStudyArchitecture]:
        cls._initialize()
        return cls._CATALOGUE.get(case_id)

    @classmethod
    def list_all(cls) -> List[CaseStudyArchitecture]:
        cls._initialize()
        return list(cls._CATALOGUE.values())
