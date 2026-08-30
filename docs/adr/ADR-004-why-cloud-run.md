# ADR-004: Why GCP Cloud Run for Compute Hosting

- **Status**: Accepted
- **Date**: 2026-08-04
- **Authors**: Staff Engineering Architecture Team
- **Deciders**: Carassco Labs Architecture Review Board

## Context & Problem Statement

Carassco Labs requires a cloud compute platform that can host containerized FastAPI services, automatically scale up during traffic spikes, scale to zero during off-peak hours to minimize cost, support zero-downtime rolling deployments, and eliminate cluster management overhead.

## Decision Drivers

- **Zero Operations Overhead**: Fully managed serverless compute (no Kubernetes node management or VM patching).
- **Scale-to-Zero & Instant Autoscale**: Sub-second scaling based on request concurrency with cost optimization.
- **Protocol Support**: Native support for HTTP/1.1, HTTP/2, gRPC, and WebSockets (vital for AI streaming).
- **Security & IAM**: Native integration with Secret Manager, Cloud IAM service accounts, and Cloud Load Balancing.

## Considered Options

1. **GCP Cloud Run**: Serverless container execution platform.
2. **GCP Google Kubernetes Engine (GKE)**: Managed Kubernetes cluster.
3. **GCP Compute Engine (GCE VMs)**: Dedicated Virtual Machine instances behind a Load Balancer.

## Decision Outcome

Chosen Option: **GCP Cloud Run**, because it provides the flexibility of full containerization with zero cluster management overhead, automatic scale-to-zero cost savings, and built-in revision management for instant traffic splitting and rollbacks.

### Positive Consequences

- Significant cloud expenditure reduction for early-stage and non-prod services via scale-to-zero.
- Out-of-the-box HTTPS endpoint provisioning with SSL certificate automation.
- Declarative revision management allowing single-command canary testing and instantaneous rollbacks.

### Negative Consequences & Tradeoffs

- Cold start latencies (typically 1–2s for Python containers) must be mitigated using minimum instances (`min-instances = 1`) for latency-critical production routes.

## Pros & Cons of the Options

### Option 1: GCP Cloud Run
- Good, because scales automatically from 0 to 1000+ instances without manual intervention.
- Good, because pay-per-second billing strictly during request execution.
- Bad, because background tasks outlasting HTTP response cycles require Cloud Tasks / PubSub delegation.

### Option 2: GCP Google Kubernetes Engine (GKE)
- Good, because complete control over networking, sidecars, and cluster topology.
- Bad, because continuous cluster control-plane costs and significant DevOps maintenance overhead.

### Option 3: GCP Compute Engine (GCE VMs)
- Good, because simple fixed hardware deployment.
- Bad, because manual OS maintenance, complex autoscaling group setup, and idle cost waste.

## Validation Plan

Monitored via GCP Cloud Monitoring latency dashboards, cold-start telemetry, and autoscaling response curves under simulated load tests.
