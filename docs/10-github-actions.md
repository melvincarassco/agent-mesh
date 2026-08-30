# 10. CI/CD Deployment with GitHub Actions

This guide explains how the GitHub Actions CI/CD workflow automatically tests and deploys the application to GCP Cloud Run.

## Workflow Overview

The `.github/workflows/deploy.yml` pipeline consists of two stages:

1. **Test Job**:
   - Triggers on both `push` and `pull_request` to `main`.
   - Sets up Python 3.11, installs dependencies, and runs `pytest tests/`.

2. **Deploy Job**:
   - Executes only after tests pass on pushes to `main`.
   - Authenticates with Google Cloud using Service Account credentials stored in GitHub Secrets.
   - Builds and tags the Docker image with the commit SHA.
   - Pushes the image to Google Container Registry.
   - Deploys the service to Cloud Run with zero downtime.

## Required GitHub Secrets

Configure the following secrets under **Repository Settings** > **Secrets and variables** > **Actions**:

- `GCP_PROJECT_ID`: Your GCP Project ID.
- `GCP_SA_KEY`: JSON service account key with `Cloud Run Admin` and `Storage Admin` roles.
