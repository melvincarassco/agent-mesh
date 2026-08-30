output "service_url" {
  value       = google_cloud_run_v2_service.main.uri
  description = "The URL of the deployed Cloud Run service."
}

output "service_name" {
  value       = google_cloud_run_v2_service.main.name
  description = "The name of the Cloud Run service."
}

output "location" {
  value       = google_cloud_run_v2_service.main.location
  description = "The region of the Cloud Run service."
}
