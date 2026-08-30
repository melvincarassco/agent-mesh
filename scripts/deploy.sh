#!/usr/bin/env bash
set -eo pipefail

# Configuration
PROJECT_ID=${GCP_PROJECT_ID:-"your-gcp-project-id"}
REGION=${GCP_REGION:-"us-central1"}
SERVICE_NAME=${SERVICE_NAME:-"agent-mesh-app"}
IMAGE_TAG="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"

echo "=== Deploying ${SERVICE_NAME} to GCP Cloud Run ==="

# 1. Build & submit container image to Google Container Registry / Artifact Registry
echo "[1/3] Building container image..."
gcloud builds submit --tag "${IMAGE_TAG}" .

# 2. Deploy container to Cloud Run
echo "[2/3] Deploying to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE_TAG}" \
  --platform managed \
  --region "${REGION}" \
  --allow-unauthenticated \
  --set-env-vars APP_ENV=production

# 3. Retrieve service URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --platform managed --region "${REGION}" --format 'value(status.url)')
echo "[3/3] Deployment complete! Service available at: ${SERVICE_URL}"
