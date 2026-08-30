variable "secret_ids" {
  type        = list(string)
  description = "List of secret IDs to create in GCP Secret Manager."
}

variable "service_account_email" {
  type        = string
  description = "Service account email granted secretAccessor role."
  default     = null
}
