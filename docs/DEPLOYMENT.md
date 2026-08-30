# Deployment Strategy & CI/CD Pipeline Architecture

> **Comprehensive deployment lifecycle, environment promotion matrix, zero-downtime traffic migration, rollback strategy, and GitHub Actions CI/CD workflows.**

---

## 1. Overview

`agent-mesh` implements a modern GitOps-aligned Continuous Integration and Continuous Delivery (CI/CD) pipeline. 

Deployments to **GCP Cloud Run** are entirely automated, zero-downtime, keyless (via Workload Identity Federation), and revision-controlled.

---

## 2. Environment Lifecycle Matrix

| Environment | Trigger | Target GCP Project | Deploy Target | Traffic Migration |
| :--- | :--- | :--- | :--- | :--- |
| **Development** | Commit to `feature/*` branch | `carassco-dev` | Ephemeral Local / Dev Run | 100% Immediate |
| **Testing / QA** | Pull Request to `main` | `carassco-qa` | CI Runner / QA Cloud Run | Automated PR Check |
| **Staging** | Merge to `main` branch | `carassco-staging` | Staging Cloud Run Service | 100% Immediate |
| **Production** | Git Tag (`vX.Y.Z`) created | `carassco-prod` | Production Cloud Run Service | Canary (10%) ➔ 100% |

---

## 3. Deployment Flow & Pipeline Stages

```text
  [ Developer Push ]
          │
          ▼
┌──────────────────────────┐
│   GitHub Actions (CI)    │
│  - Ruff Linting          │
│  - Pytest Suite          │
│  - Security Vulnerability│
└─────────┬────────────────┘
          │ (Passes)
          ▼
┌──────────────────────────┐
│  Build & Push (Docker)   │
│  - Build Multi-stage Img │
│  - Tag git SHA / Version │
│  - Push to GCP Artifact  │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│ GCP Cloud Run Deployment │
│  - Deploy New Revision   │
│  - Startup Health Probe  │
└─────────┬────────────────┘
          │ (Healthy)
          ▼
┌──────────────────────────┐
│ Traffic Migration (100%) │
│  - Zero Downtime Shift   │
│  - Decommission Old Rev  │
└────────────────────────┘
```

### Stage 1: Quality Gate & Testing (CI)
On every pull request, GitHub Actions executes:
- **Linting & Code Formatting**: `ruff check .` and `ruff format --check .`
- **Type Checking**: `mypy app`
- **Automated Testing**: `pytest --cov=app tests/`
- **Container Vulnerability Scan**: Trivy scan of the Docker build image.

### Stage 2: Keyless OIDC Authentication
The runner authenticates with GCP via Workload Identity Federation (WIF):
- Obtains short-lived OAuth tokens tied to the GitHub repository identity.
- No long-lived GCP service account JSON keys stored in GitHub Secrets.

### Stage 3: Container Publishing
- Multi-stage Docker image built using Docker buildx layer caching.
- Tagged with both immutable Git Commit SHA (`sha-a1b2c3d`) and semantic release tag (`v1.2.0`).
- Published to GCP Artifact Registry (`us-docker.pkg.dev/carassco-prod/backend/agent-mesh:v1.2.0`).

### Stage 4: Cloud Run Revision Deployment
- Deploys container image as a new Cloud Run Revision.
- Configures environment variables, CPU/Memory limits, and min/max instance scaling bounds.
- Executes container HTTP `/health` startup probe.

---

## 4. Rollback Strategy

Because Cloud Run revisions are immutable snapshots of container configurations, rollbacks are **instantaneous** (<2 seconds) and require zero re-building.

### Automated Rollback (Startup Failure)
If a new revision fails its HTTP health check or crashes on container startup:
1. Cloud Run aborts the revision deployment automatically.
2. 100% of live user traffic remains routed to the previous healthy revision.
3. GitHub Actions marks the pipeline run as **Failed** and alerts the engineering team.

### Manual Emergency Rollback (Post-Deployment Bug)
If a critical application bug escapes to production, engineers can execute an immediate traffic rollback via gcloud CLI or GitHub Actions manual dispatch workflow:

```bash
# List recent Cloud Run service revisions
gcloud run revisions list --service=agent-mesh --region=us-central1

# Instantly revert 100% of traffic to previous known healthy revision
gcloud run services update-traffic agent-mesh \
  --region=us-central1 \
  --to-revisions=agent-mesh-00042-xyz=100
```

---

## 5. CI/CD Workflow Definitions

Workflows are located under `.github/workflows/`:

- `.github/workflows/ci.yml`: Code quality checks, linting, unit/integration testing on all branches and PRs.
- `.github/workflows/cd.yml`: Automated container build, push to GCP Artifact Registry, and deployment to GCP Cloud Run upon push to `main` or release tag.
- `.github/workflows/code_quality.yml`: Dependency vulnerability scans and security static analysis.
