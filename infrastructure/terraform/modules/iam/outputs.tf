output "service_account_email" {
  value       = google_service_account.app_sa.email
  description = "The email address of the application Service Account."
}

output "workload_identity_provider" {
  value       = var.github_repo != "" ? google_iam_workload_identity_pool_provider.github_provider[0].name : ""
  description = "The full resource name of the GitHub Actions Workload Identity Provider."
}
