output "secret_ids_map" {
  value       = { for k, v in google_secret_manager_secret.secrets : k => v.id }
  description = "Map of secret keys to GCP Secret Manager IDs."
}
