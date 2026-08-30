# ADR-001: Why Google Cloud Platform (GCP) as Primary Cloud Infrastructure

- **Status**: Accepted
- **Date**: 2026-08-04
- **Authors**: Staff Engineering Architecture Team
- **Deciders**: Carassco Labs Architecture Review Board

## Context & Problem Statement

Carassco Labs requires a unified, enterprise-grade cloud provider to support scalable backend services, high-throughput microservices, and specialized AI/ML workflows (LLM serving, vector search, retrieval-augmented generation). We need a platform with robust serverless primitives, seamless identity federation, managed data infrastructure, and native AI integration without imposing high operational overhead.

## Decision Drivers

- **AI Native Services**: Direct access to state-of-the-art AI infrastructure (Vertex AI, Gemini models, TPU/GPU fleets).
- **Serverless Ecosystem**: Zero-idle-cost compute primitives with automatic scaling (GCP Cloud Run).
- **Security & IAM**: Granular service account IAM and keyless authentication via Workload Identity Federation.
- **Total Cost of Ownership (TCO)**: Pay-per-use scaling models and low operational maintenance overhead.

## Considered Options

1. **Google Cloud Platform (GCP)**: Primary public cloud provider focused on containerized serverless compute and Vertex AI.
2. **Amazon Web Services (AWS)**: Elastic compute and ECS/EKS infrastructure.
3. **Microsoft Azure**: Enterprise Azure App Services and Azure OpenAI service integration.

## Decision Outcome

Chosen Option: **Google Cloud Platform (GCP)**, because GCP offers unmatched AI ecosystem tooling via Vertex AI, superior developer velocity through Cloud Run container serverless compute, and native integration with keyless IAM identity federation.

### Positive Consequences

- Accelerated time-to-market for AI-driven applications using Vertex AI SDKs.
- Reduced infrastructure maintenance overhead via serverless Cloud Run.
- Standardized IAM, logging, monitoring, and secret management across all Carassco Labs projects.

### Negative Consequences & Tradeoffs

- Multi-cloud abstraction complexity if hybrid deployment is mandated in future.
- Regional quotas must be actively monitored as AI traffic expands.

## Pros & Cons of the Options

### Option 1: Google Cloud Platform (GCP)
- Good, because Cloud Run delivers instant scale-to-zero container hosting with HTTP/2 and gRPC support.
- Good, because Vertex AI provides native integration for Gemini LLMs and vector embeddings.
- Bad, because niche niche-cloud managed services require GCP-specific IAM configuration.

### Option 2: Amazon Web Services (AWS)
- Good, because vast ecosystem and broad third-party software compatibility.
- Bad, because ECS Fargate and Lambda container startup latencies are higher than Cloud Run for Python workloads.
- Bad, because fragmented AI/ML service layer compared to unified Vertex AI platform.

### Option 3: Microsoft Azure
- Good, because strong enterprise Active Directory integration.
- Bad, because Container Apps and App Services incur higher baseline overhead and complexity for small microservices.

## Validation Plan

Verification via load testing on Cloud Run latency, automated IAM policy checks in CI, and billing telemetry review during initial service rollouts.
