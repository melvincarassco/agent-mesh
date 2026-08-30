variable "project_id" {
  type        = string
  description = "The GCP Project ID."
}

variable "service_account_id" {
  type        = string
  description = "The account ID for the Cloud Run execution Service Account."
  default     = "gcp-foundation-sa"
}

variable "github_repo" {
  type        = string
  description = "GitHub repository string for Workload Identity binding (e.g. 'carassco-labs/gcp-foundation')."
  default     = ""
}
