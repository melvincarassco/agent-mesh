output "repository_id" {
  value       = google_artifact_registry_repository.main.repository_id
  description = "The Artifact Registry repository ID."
}

output "repository_url" {
  value       = "${google_artifact_registry_repository.main.location}-docker.pkg.dev/${google_artifact_registry_repository.main.project}/${google_artifact_registry_repository.main.repository_id}"
  description = "The Artifact Registry Docker repository URL."
}
