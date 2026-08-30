output "prod_cloud_run_url" {
  value       = module.cloud_run.service_url
  description = "Production Cloud Run Service URL."
}

output "prod_artifact_registry_url" {
  value       = module.artifact_registry.repository_url
  description = "Production Artifact Registry Repository URL."
}

output "prod_service_account_email" {
  value       = module.iam.service_account_email
  description = "Production Cloud Run Service Account Email."
}
