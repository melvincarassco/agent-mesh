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
  service_account_id = "gcp-foundation-dev-sa"
  github_repo        = var.github_repo
}

module "artifact_registry" {
  source        = "../../modules/artifact_registry"
  repository_id = "gcp-foundation-dev"
  location      = var.region
  description   = "Development Docker image repository"
}

module "secret_manager" {
  source                = "../../modules/secret_manager"
  secret_ids            = ["gcp-foundation-dev-secret-key", "gcp-foundation-dev-db-url"]
  service_account_email = module.iam.service_account_email
}

module "cloud_run" {
  source                = "../../modules/cloud_run"
  service_name          = "gcp-foundation-dev"
  location              = var.region
  image_uri             = "${module.artifact_registry.repository_url}/image:latest"
  min_instances         = 0
  max_instances         = 5
  cpu                   = "1000m"
  memory                = "512Mi"
  allow_unauthenticated = true
  service_account_email = module.iam.service_account_email

  env_vars = {
    ENVIRONMENT    = "development"
    DEBUG          = "true"
    LOG_LEVEL      = "DEBUG"
    GCP_PROJECT_ID = var.project_id
    GCP_REGION     = var.region
  }
}
