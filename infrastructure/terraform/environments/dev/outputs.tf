output "dev_cloud_run_url" {
  value       = module.cloud_run.service_url
  description = "Development Cloud Run Service URL."
}

output "dev_artifact_registry_url" {
  value       = module.artifact_registry.repository_url
  description = "Development Artifact Registry Repository URL."
}

output "dev_service_account_email" {
  value       = module.iam.service_account_email
  description = "Development Cloud Run Service Account Email."
}
