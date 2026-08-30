# Project Overview: `agent-mesh`

> **Official Backend & Cloud Infrastructure Foundation for Carassco Labs**

---

## 1. Business Problem

As Carassco Labs expands its ecosystem of AI applications, microservices, and specialized data platforms, individual repositories risk architectural fragmentation, inconsistent security policies, duplicated setup overhead, and ad-hoc deployment patterns.

Without a standardized, production-grade cloud-native foundation:
- Developers spend up to 30% of sprint capacity reinventing boilerplate (FastAPI configurations, Docker setup, CI/CD pipelines, logging setups).
- Security risks escalate through hardcoded API keys, unencrypted environment variables, and overly permissive IAM permissions.
- Operational debugging becomes cumbersome due to divergent log formats, missing trace IDs, and lack of standard metrics.

`agent-mesh` resolves these pain points by serving as the mandatory, production-ready starter template for every Python & GCP service built across Carassco Labs.

---

## 2. Goals

- **100% Production Readiness Out-of-the-Box**: Provide a turnkey, enterprise-grade architecture with zero-effort setup for logging, configuration, health checks, and deployment.
- **Strict Adherence to Handbook Standards**: Embody all engineering principles defined in the [Carassco Labs Handbook](file:///Users/dalehendriques/Downloads/MELVIN_WORK/carassco-labs/handbook/README.md) (Python, FastAPI, GCP, Docker, Git, Security).
- **Template Inheritance**: Enable seamless cloning and project bootstrapping via automated template scripts (`scripts/bootstrap_project.py`).
- **Keyless Security Baseline**: Enforce GCP Workload Identity Federation, GCP Secret Manager integration, non-root Docker runtime users, and strict Pydantic validation.
- **Instant Observability**: Export structured JSON logs, latency telemetry, and correlation IDs to GCP Cloud Logging and Cloud Trace out-of-the-box.

---

## 3. Non-Goals

- **Monolithic Legacy Backend**: This repository is optimized for modern, containerized microservices and AI workloads—not monolithic legacy web apps.
- **Application Business Logic**: `agent-mesh` contains zero domain-specific application code. Application-specific models, services, and endpoints are implemented in downstream repositories cloned from this foundation.
- **Ad-Hoc Manual Deployments**: Direct manual pushes to production via personal CLI credentials bypass CI/CD and are explicitly prohibited.

---

## 4. Repository Structure

```text
agent-mesh/
├── .github/                  # CI/CD pipelines & GitHub templates
│   ├── workflows/            # Continuous Integration & Delivery workflows
│   └── PULL_REQUEST_TEMPLATE.md
├── app/                      # Application core module structure (downstream code goes here)
│   ├── api/                  # FastAPI controllers & endpoint routers
│   ├── core/                 # Core settings, security, logging, & middleware
│   ├── db/                   # Database sessions & migrations
│   ├── integrations/         # GCP & third-party SDK connectors (Vertex AI, GCS)
│   ├── models/               # ORM & database models
│   ├── schemas/              # Pydantic v2 validation models
│   ├── services/             # Domain business logic
│   └── utils/                # Utility helpers & formatters
├── architecture/             # System diagrams & architecture documentation
│   ├── README.md             # High-level architecture & sequence diagrams
│   └── decisions/            # Architectural Decision Records (ADRs)
├── assets/                   # Architectural diagrams & design assets
├── config/                   # Configuration schemas & environment profiles
├── docker/                   # Container definitions & compose profiles
├── docs/                     # In-depth operational documentation
│   ├── adr/                  # Official ADRs (ADR-001 through ADR-005)
│   ├── ARCHITECTURE.md       # High-level architecture reference
│   ├── CONFIGURATION.md      # Configuration & secret management guide
│   ├── DEPLOYMENT.md         # Deployment & rollback procedures
│   └── PROJECT_OVERVIEW.md   # Business goals, stack & roadmap (This document)
├── examples/                 # Reference patterns for endpoints, services, & events
├── infrastructure/           # Terraform IaC configurations & modules
├── scripts/                  # Scaffolding, validation, & management scripts
├── tests/                    # Unit, integration, & end-to-end test suites
├── .env.example              # Sample environment configuration template
├── .gitignore                # Standardized git ignore rules
├── Dockerfile                # Multi-stage production container definition
├── docker-compose.yml        # Local development orchestration manifest
├── LICENSE                   # Software license definition
└── README.md                 # Root engineering template reference
```

---

## 5. Technology Stack

| Layer | Technology | Specification / Version |
| :--- | :--- | :--- |
| **Language** | Python | `3.11+` |
| **Web Framework** | FastAPI | `^0.110.0` (Asynchronous ASGI) |
| **Data Validation** | Pydantic | `v2.x` (Rust-based core parsing) |
| **Containerization** | Docker | Multi-stage OCI standard build |
| **Local Orchestration** | Docker Compose | Development profiles with live reload |
| **Cloud Hosting** | GCP Cloud Run | Fully managed serverless containers |
| **Secret Management** | GCP Secret Manager | IAM-authenticated runtime secret resolution |
| **CI/CD** | GitHub Actions | Workload Identity Federation keyless deployments |
| **Infrastructure as Code** | Terraform | GCP provider `^5.0` |
| **Observability** | GCP Cloud Logging | `python-json-logger` structured JSON formatting |
| **Testing** | Pytest / HTTPX | `pytest-asyncio` for async controller testing |

---

## 6. Coding Standards Reference

This repository strictly implements the standards specified in the **Carassco Labs Handbook**:

- **Python Standards**: [03-python-standards.md](file:///Users/dalehendriques/Downloads/MELVIN_WORK/carassco-labs/handbook/docs/03-python-standards.md) (PEP 8, type hints, immutability).
- **FastAPI Standards**: [04-fastapi-standards.md](file:///Users/dalehendriques/Downloads/MELVIN_WORK/carassco-labs/handbook/docs/04-fastapi-standards.md) (router modularity, Pydantic v2 schemas).
- **GCP Standards**: [06-google-cloud-standards.md](file:///Users/dalehendriques/Downloads/MELVIN_WORK/carassco-labs/handbook/docs/06-google-cloud-standards.md) (Cloud Run, Secret Manager, Cloud Logging).
- **Docker Standards**: [07-docker-standards.md](file:///Users/dalehendriques/Downloads/MELVIN_WORK/carassco-labs/handbook/docs/07-docker-standards.md) (multi-stage builds, non-root `appuser`).
- **CI/CD Standards**: [08-cicd-standards.md](file:///Users/dalehendriques/Downloads/MELVIN_WORK/carassco-labs/handbook/docs/08-cicd-standards.md) (GitHub Actions workflows, automated status checks).

---

## 7. Deployment Strategy Overview

Deployments follow an automated, multi-stage pipeline:

```text
[Feature Branch] ──> [PR to Main] ──> [CI Pipeline: Lint/Test/Scan] ──> [Merge]
                                                                            │
                                                                            ▼
[Cloud Run Production] <── [Zero-Downtime Traffic Shift] <── [Container Push & Healthcheck]
```

Detailed deployment workflows and rollback mechanisms are documented in [docs/DEPLOYMENT.md](file:///Users/dalehendriques/Downloads/MELVIN_WORK/carassco-labs/agent-mesh/docs/DEPLOYMENT.md).

---

## 8. Future Roadmap

- **Phase 1 (Sprint 1 - Current)**: Architecture, ADRs, scaffolding, and documentation baseline.
- **Phase 2 (Sprint 2)**: FastAPI application kernel execution, health probes, Pydantic settings loading, and pytest suite.
- **Phase 3 (Sprint 3)**: Terraform IaC modules for Cloud Run, Artifact Registry, Secret Manager, and IAM Service Accounts.
- **Phase 4 (Sprint 4)**: AI Application SDK Integration (Vertex AI Gemini streaming, Vector Search RAG connectors, and Pub/Sub event router).
