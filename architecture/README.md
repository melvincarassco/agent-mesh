# System Architecture: Agent Mesh

This document defines the high-level architecture, component interaction, security boundaries, and GCP cloud-native flows for `agent-mesh`—the baseline backend template for Carassco Labs applications.

---

## 1. High-Level System Architecture

The foundation relies on a serverless, containerized web service model powered by **Google Cloud Run**, integrated with managed GCP enterprise infrastructure.

```mermaid
flowchart TD
    subgraph ClientLayer["Client & External API Layer"]
        Client["Web / Mobile / Third-Party Clients"]
        EdgeDNS["Cloud DNS / Cloud CDN"]
    end

    subgraph SecurityIngress["Security & Ingress"]
        HTTPSLB["Cloud Load Balancing (HTTPS)"]
        CloudArmor["Cloud Armor (WAF & DDoS Mitigation)"]
    end

    subgraph ComputeLayer["Compute Layer (GCP Cloud Run)"]
        direction TB
        CR_Service["Cloud Run Service (FastAPI Container)"]
        
        subgraph FastAPI_Internal["FastAPI Application Scaffolding"]
            Middleware["Core Middleware Stack\n(CORS, Correlation ID, Request Logging)"]
            Router["API Routers / Controllers"]
            Services["Business & AI Service Modules"]
            ConfigManager["Pydantic BaseSettings Manager"]
        end
    end

    subgraph InfrastructureLayer["Agent Mesh Infrastructure"]
        GSM["GCP Secret Manager\n(Dynamic Secrets & API Keys)"]
        GCS["GCP Cloud Storage\n(Object / Media Storage)"]
        CloudSQL["GCP Cloud SQL (PostgreSQL)\n/ Cloud Spanner"]
        VertexAI["GCP Vertex AI Services\n(LLMs, Embeddings, Pipelines)"]
        PubSub["GCP Cloud Pub/Sub\n(Event-Driven Messaging)"]
    end

    subgraph ObservabilityLayer["GCP Observability Suite"]
        CloudLogging["Cloud Logging (Stackdriver)"]
        CloudMonitoring["Cloud Monitoring & Alerting"]
        CloudTrace["Cloud Trace (OpenTelemetry)"]
    end

    Client --> EdgeDNS
    EdgeDNS --> HTTPSLB
    HTTPSLB --> CloudArmor
    CloudArmor --> CR_Service
    CR_Service --> Middleware
    Middleware --> Router
    Router --> Services
    
    Services --> ConfigManager
    ConfigManager --> GSM
    Services --> GCS
    Services --> CloudSQL
    Services --> VertexAI
    Services --> PubSub

    CR_Service -.->|JSON Logs| CloudLogging
    CR_Service -.->|Metrics| CloudMonitoring
    CR_Service -.->|Telemetry| CloudTrace
```

---

## 2. Request Lifecycle Architecture

Every HTTP/gRPC request flows through strict middleware validation, correlation ID injection, Pydantic type safety, and structured error handling.

```mermaid
sequenceDiagram
    autonumber
    participant Client as Client Application
    participant Ingress as Cloud Run Ingress
    participant Middleware as Middleware Pipeline
    participant Router as FastAPI Router
    participant Schema as Pydantic Schema Validator
    participant Service as Business Service / Domain Handler
    participant DataLayer as Data & GCP SDK Layer
    participant Logger as Structured Logger

    Client->>Ingress: HTTP Request (Headers + Body + Bearer Token)
    Ingress->>Middleware: Route Request to Container
    Middleware->>Middleware: 1. Inject X-Correlation-ID<br/>2. Apply CORS Rules<br/>3. Start Timing Stopwatch
    Middleware->>Router: Forward Context
    Router->>Schema: Validate Body & Parameters
    alt Schema Validation Fails (422)
        Schema-->>Router: Validation Exception
        Router-->>Client: 422 Unprocessable Entity (RFC 7807 JSON)
    else Schema Validation Succeeds
        Schema-->>Router: Sanitized Data Model
        Router->>Service: Call Domain Method
        Service->>DataLayer: Execute Query / API Call
        DataLayer-->>Service: Return Domain Result
        Service-->>Router: Return Response Model
        Router->>Middleware: Final Response Object
        Middleware->>Logger: Emit Structured JSON Log (Correlation ID, Latency, Status)
        Middleware-->>Client: HTTP 200 OK + Standardized JSON Body
    end
```

---

## 3. Configuration & Secrets Hierarchy

Configuration resolution follows a strict priority order, securing runtime values and preventing credential leakage.

```mermaid
flowchart LR
    subgraph ConfigSources["Configuration Sources (Ascending Priority)"]
        CodeDefaults["1. Code Defaults\n(app/core/config.py)"]
        ConfigFile["2. Environment Config File\n(config/env.{env}.json)"]
        LocalDotEnv["3. Local File\n(.env)"]
        OSEnvVars["4. OS Environment Variables\n(Cloud Run Config)"]
        GCPSecretManager["5. GCP Secret Manager\n(IAM Auth API Fetch)"]
    end

    subgraph ResolutionEngine["Runtime Configuration Engine"]
        PydanticSettings["Pydantic BaseSettings Provider"]
        CacheStore["In-Memory Vault Cache\n(TTL: 15 Mins)"]
    end

    subgraph AppState["Application Runtime State"]
        ImmutableConfig["Immutable Settings Singleton\n(get_settings())"]
    end

    CodeDefaults --> PydanticSettings
    ConfigFile --> PydanticSettings
    LocalDotEnv --> PydanticSettings
    OSEnvVars --> PydanticSettings
    GCPSecretManager --> CacheStore
    CacheStore --> PydanticSettings

    PydanticSettings --> ImmutableConfig
```

---

## 4. CI/CD Deployment Flow

Deployments use GitHub Actions with Workload Identity Federation (Keyless IAM Authentication) for zero-trust container publishing and Cloud Run deployment.

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer
    participant GH as GitHub Repository
    participant GHA as GitHub Actions Runner
    participant WIF as GCP Workload Identity Federation
    participant AR as GCP Artifact Registry
    participant CR as GCP Cloud Run Service

    Dev->>GH: git push origin main / tag release
    GH->>GHA: Trigger `cd.yml` Workflow
    GHA->>GHA: Run Pytest, Ruff Linter, & Security Scans
    GHA->>WIF: Request Short-Lived OIDC Token
    WIF-->>GHA: Return GCP OAuth2 Access Token
    GHA->>GHA: Build Multi-Stage Docker Image
    GHA->>AR: Push Image (`us-docker.pkg.dev/.../image:sha-xyz`)
    GHA->>CR: Deploy New Revision (`--image us-docker.pkg.dev/...`)
    CR->>CR: Spin Up Canary Revision (0% Traffic)
    CR->>CR: Execute Startup Probe & Healthcheck (`/health`)
    alt Healthcheck Fails
        CR-->>GHA: Startup Error (Abort Deployment)
        GHA-->>Dev: Pipeline Failed (Previous Revision Maintained)
    else Healthcheck Passes
        CR->>CR: Shift 100% Traffic to New Revision
        CR-->>GHA: Deployment Successful
        GHA-->>Dev: Pipeline Success Notification
    end
```

---

## 5. Logging & Observability Architecture

Structured logging ensures zero log truncation, full trace propagation, and automated GCP Cloud Logging parsing.

```mermaid
flowchart LR
    subgraph FastAPI_App["FastAPI Container"]
        Logger["python-json-logger"]
        Formatter["GCP Log Formatter\n(severity, correlation_id, trace_id)"]
    end

    subgraph ContainerOutput["Standard IO"]
        Stdout["stdout / stderr stream"]
    end

    subgraph GCP_Observability["GCP Observability Infrastructure"]
        CloudLoggingAgent["GCP Cloud Logging Collector"]
        LogRouter["GCP Log Router (Sinks)"]
        BigQuerySink["BigQuery Audit Log Archive"]
        CloudMonitoring["Cloud Monitoring Alerting Policy"]
        CloudTrace["Cloud Trace Latency Map"]
    end

    Logger --> Formatter
    Formatter --> Stdout
    Stdout --> CloudLoggingAgent
    CloudLoggingAgent --> LogRouter
    LogRouter --> BigQuerySink
    LogRouter --> CloudMonitoring
    LogRouter --> CloudTrace
```

---

## 6. Secrets Management Flow

Secrets are never stored in code, Git, or static container environment variables. They are resolved via GCP IAM Service Accounts.

```mermaid
sequenceDiagram
    autonumber
    participant App as Cloud Run Container
    participant Auth as GCP IAM / Metadata Server
    participant GSM as GCP Secret Manager API
    participant Cache as Local In-Memory Secret Cache

    App->>Cache: Request Secret (e.g. `DATABASE_URL`)
    alt Secret Exists in Cache & Not Expired
        Cache-->>App: Return Decrypted Secret String
    else Secret Missing or Expired
        App->>Auth: Get Identity Token from Metadata Server (`http://169.254.169.254/...`)
        Auth-->>App: Access Token for Assigned Service Account
        App->>GSM: Request Secret Version (`v1/projects/.../secrets/db-url/versions/latest`)
        GSM->>GSM: Verify IAM Permission (`roles/secretmanager.secretAccessor`)
        GSM-->>App: Return Secret Payload
        App->>Cache: Store in Cache with TTL (15 min)
        Cache-->>App: Return Decrypted Secret String
    end
```

---

## 7. Future GCP Integration Roadmap

The foundation is designed to seamlessly integrate advanced GCP AI and data services in upcoming sprints:

```mermaid
mindmap
  root((Carassco Labs Agent Mesh))
    Core Architecture
      FastAPI Framework
      Cloud Run Serverless
      Workload Identity Federation
      Structured Logging & Tracing
    Storage & Database Layer
      Cloud SQL PostgreSQL (Relational)
      Cloud Spanner (Global Scalability)
      Cloud Storage (Unstructured / Artifacts)
      Redis MemoryStore (Caching & Rate Limiting)
    AI & Machine Learning (Vertex AI)
      Vertex AI Gemini APIs (LLM Operations)
      Vertex Vector Search (RAG Pipelines)
      Vertex AI Pipelines (Model Training & Eval)
    Event-Driven Architecture
      Cloud Pub/Sub (Asynchronous Messaging)
      Eventarc (Cloud Event Routing)
      Cloud Tasks (Distributed Queue Management)
    Enterprise Governance
      Cloud Armor WAF Rules
      VPC Service Controls
      Binary Authorization (Signed Images)
```
