# Backend & System Design Knowledge Catalogue
**580 Core Engineering Topics Across 23 Architectural Domains**  
*OpenClone Global Engineering Intelligence | Reference Standards for Scalable Systems*

---

## 1. Overview & Architectural Philosophy

The OpenClone Backend Catalogue organizes 580 topics across 23 domains. It functions as an architectural decision matrix, not a mandate to introduce premature complexity.
**Principle**: Start with the simplest architecture (Modular Monolith with clean boundaries) and scale out to distributed microservices, queues, and caches only when measurable concurrency, data volume, or team organizational boundaries demand it.

---

## 2. The 23 Backend & Distributed Systems Domains

| Domain ID | Category | Scope & Core Topics Covered |
|---|---|---|
| **01** | **Architecture Strategies** | Monoliths, Modular Monoliths, Microservices, Event-Driven, Hexagonal/Ports & Adapters, Clean Architecture, CQRS, Event Sourcing, Domain-Driven Design (DDD). |
| **02** | **Load Balancing & Traffic Routing** | Layer 4 vs Layer 7, Consistent Hashing, Round Robin, Least Connections, Anycast, DNS Routing, TLS Termination, Reverse Proxies (Nginx, Envoy, Traefik). |
| **03** | **Rate Limiting & Abuse Prevention** | Token Bucket, Leaky Bucket, Sliding Window Log, Sliding Window Counter, Distributed Redis Limiters, Tiered Client Throttling, DoS Defenses. |
| **04** | **Resilience & Fault Tolerance** | Circuit Breakers (Resilience4j/Polly), Exponential Backoff with Jitter, Bulkheads, Fallbacks, Timeouts, Graceful Degradation, Chaos Engineering. |
| **05** | **Queues & Asynchronous Messaging** | AMQP (RabbitMQ), Kafka Event Streams, Redis Streams, SQS, Dead-Letter Queues (DLQ), Backpressure, Consumer Groups, Compaction. |
| **06** | **Distributed Systems & Consistency** | CAP Theorem, PACELC, Two-Phase Commit (2PC), Sagas (Choreographed vs Orchestrated), Vector Clocks, Paxos, Raft Consensus, CRDTs. |
| **07** | **Database Architecture & Scaling** | Read Replicas, Primary-Replica Replication, Connection Pooling (PgBouncer), Sharding (Key, Range, Directory), Partitioning, Online Schema Migrations. |
| **08** | **Caching Topologies** | Cache-Aside, Write-Through, Write-Behind, Refresh-Ahead, Cache Invalidation, Stampede Prevention (XFetch), Redis Clustering, CDN Edge Caching. |
| **09** | **API Architecture & Protocols** | REST Level 3 (HATEOAS), GraphQL (Subgraphs/Federation), gRPC/Protobuf, WebSockets, WebTransport, Server-Sent Events (SSE), Webhooks, Idempotency Keys. |
| **10** | **Authentication & Identity** | OAuth 2.1, OpenID Connect (OIDC), JWT vs Session Cookies, PASETO, Passkeys / WebAuthn, Mutual TLS (mTLS), SAML 2.0, SCIM Provisioning. |
| **11** | **Authorization & Access Control** | Role-Based Access Control (RBAC), Attribute-Based (ABAC), Relationship-Based (ReBAC / Zanzibar), Row-Level Security (RLS), Policy-as-Code (OPA/Cedar). |
| **12** | **Security Engineering** | Parameterized Queries (SQLi prevention), Input Sanitization, Secret Management (Vault), Key Rotation, Data Encryption at Rest/Transit, Memory-Safe runtimes. |
| **13** | **Performance & Concurrency** | Non-blocking I/O (epoll/kqueue), Goroutines/Virtual Threads, CPU Profiling (pprof), Memory Leak Detection, Zero-Copy I/O, Garbage Collection tuning. |
| **14** | **Scalability & Capacity Planning** | Vertical vs Horizontal scaling, Little's Law, Amdahl's Law, Universal Scalability Law (USL), Dimensioning compute, Autoscale policies, Warm pools. |
| **15** | **Background Jobs & Workflows** | Durable Workflow Engines (Temporal), Cron schedulers, Distributed Locks (Redlock), Long-running batch pipelines, Job idempotency. |
| **16** | **Observability & Telemetry** | OpenTelemetry (OTel), Structured JSON Logging, Distributed Tracing (Trace/Span IDs), Prometheus Metrics, Golden Signals (Latency, Traffic, Errors, Saturation). |
| **17** | **Deployment & Infrastructure** | Blue-Green, Canary, Rolling Deployments, Immutable Infrastructure, Docker OCI packaging, Kubernetes primitives, GitOps (ArgoCD), Zero-Downtime rollouts. |
| **18** | **Event-Driven Architectures** | Event notification, Event-carried state transfer, Idempotent consumers, Outbox Pattern, Change Data Capture (Debezium), Schema Registries. |
| **19** | **Multi-Tenant SaaS Engineering** | Database-per-tenant vs Schema-per-tenant vs Shared-database with tenant_id, Cross-tenant leakage tests, Tenant-aware connection pools, Fair resource usage. |
| **20** | **Advanced Distributed Data** | Distributed transactions, Read-your-own-writes consistency, Session guarantees, Vector databases, Time-series databases, Graph databases. |
| **21** | **Reliability & Disaster Recovery** | RPO / RTO targets, Automated multi-region database failover, Backup integrity validation, Disaster recovery drills, Runbooks. |
| **22** | **Networking & Protocols** | TCP/IP flow control, HTTP/2 multiplexing, HTTP/3 (QUIC), BGP Anycast, Service Meshes (Istio/Linkerd), VPC Peering, PrivateLink. |
| **23** | **AI Backend Infrastructure** | Model serving engines (vLLM, TensorRT-LLM), Streaming token backpressure, Vector search indexing (HNSW/IVFFlat), Prompt cache routing, Embedding pipelines. |

---

## 3. Decision Framework for Architecture Adoption

Before adopting any advanced pattern (e.g., Kafka, Microservices, Kubernetes), verify:
1. Does the current workload exceed the limits of a well-tuned single-node relational database (>10k writes/sec, >10TB data)?
2. Does team organization require decoupled deployment pipelines?
3. If not, favor **Modular Monoliths** with strict internal package boundaries and database transactions.
