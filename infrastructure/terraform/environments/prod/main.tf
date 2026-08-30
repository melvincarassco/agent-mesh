terraform {
  required_version = ">= 1.7.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "iam" {
  source             = "../../modules/iam"
  project_id         = var.project_id
  service_account_id = "gcp-foundation-prod-sa"
  github_repo        = var.github_repo
}

module "artifact_registry" {
  source        = "../../modules/artifact_registry"
  repository_id = "gcp-foundation-prod"
  location      = var.region
  description   = "Production Docker image repository"
}

module "secret_manager" {
  source                = "../../modules/secret_manager"
  secret_ids            = ["gcp-foundation-prod-secret-key", "gcp-foundation-prod-db-url"]
  service_account_email = module.iam.service_account_email
}

module "cloud_run" {
  source                = "../../modules/cloud_run"
  service_name          = "gcp-foundation"
  location              = var.region
  image_uri             = "${module.artifact_registry.repository_url}/image:latest"
  min_instances         = 1
  max_instances         = 20
  cpu                   = "2000m"
  memory                = "1Gi"
  allow_unauthenticated = true
  service_account_email = module.iam.service_account_email

  env_vars = {
    ENVIRONMENT    = "production"
    DEBUG          = "false"
    LOG_LEVEL      = "INFO"
    GCP_PROJECT_ID = var.project_id
    GCP_REGION     = var.region
  }
}
