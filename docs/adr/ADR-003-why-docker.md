# ADR-003: Why Docker Containerization Standard

- **Status**: Accepted
- **Date**: 2026-08-04
- **Authors**: Staff Engineering Architecture Team
- **Deciders**: Carassco Labs Architecture Review Board

## Context & Problem Statement

To prevent environment divergence ("works on my machine"), ensure deterministic deployments, and support cloud-native deployment across GCP Cloud Run, Carassco Labs applications must package application code, OS dependencies, and Python runtime libraries into immutable deployable units.

## Decision Drivers

- **Environment Consistency**: Identical execution environment across local dev, CI runners, and Cloud Run production.
- **Security & Immutability**: Container isolation, non-root execution users, and minimal base image attack surfaces.
- **Portability**: Standard Open Container Initiative (OCI) format supported by Artifact Registry and local orchestrators.
- **Build Efficiency**: Layer caching and multi-stage container builds to keep image sizes small (<150MB).

## Considered Options

1. **Docker (OCI Multi-Stage Containers)**: Containerization using standard Dockerfiles and OCI runtime specifications.
2. **Buildpacks (Cloud Native Buildpacks)**: Automatic container generation without explicit Dockerfiles.
3. **Bare Virtual Machines / Virtualenvs**: Direct Python environment execution on VM instances.

## Decision Outcome

Chosen Option: **Docker (OCI Multi-Stage Containers)**, because explicit multi-stage Dockerfiles grant fine-grained control over security baseline hardening, layer caching, non-root runtime users, and exact dependency isolation.

### Positive Consequences

- Reproducible builds with pinned base images (`python:3.11-slim`).
- Reduced image attack surface via multi-stage builds (excluding compilers/build tools from runtime image).
- Local developer parity using Docker Compose.

### Negative Consequences & Tradeoffs

- Developers must maintain Dockerfile definitions and monitor layer ordering for build efficiency.

## Pros & Cons of the Options

### Option 1: Docker (OCI Multi-Stage Containers)
- Good, because multi-stage builds isolate build tools (gcc, git) from the final minimal production image.
- Good, because full transparency into container configuration and security scanning.
- Bad, because requires explicit Dockerfile maintenance across services.

### Option 2: Buildpacks
- Good, because zero Dockerfile maintenance for developers.
- Bad, because less control over system-level OS packages required for specialized C-extension Python libraries.

### Option 3: Bare Virtual Environments / VMs
- Good, because simple initial deployment setup on single servers.
- Bad, because environment drift, OS patch inconsistency, and lack of cloud-native autoscaling primitives.

## Validation Plan

Container security scanning in CI via Trivy/GCP Container Analysis, and automated image size monitoring (<200MB target).
