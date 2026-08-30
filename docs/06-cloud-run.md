# 06. Deploying Application to GCP Cloud Run

This guide outlines how to deploy the FastAPI container application to GCP Cloud Run.

## Prerequisites

- GCP Project with Billing Enabled.
- Cloud Run API & Cloud Build API enabled:
  ```bash
  gcloud services enable run.googleapis.com cloudbuild.googleapis.com
  ```

## Manual Deployment

You can deploy the app directly using the deployment script:

```bash
chmod +x scripts/deploy.sh
export GCP_PROJECT_ID="your-project-id"
./scripts/deploy.sh
```

## Cloud Run Direct Command

Or execute the deployment manually via `gcloud`:

```bash
gcloud run deploy agent-mesh-app \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```
