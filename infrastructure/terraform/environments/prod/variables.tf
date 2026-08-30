variable "project_id" {
  type        = string
  description = "GCP Production Project ID."
  default     = "carassco-prod"
}

variable "region" {
  type        = string
  description = "GCP Production Region."
  default     = "us-central1"
}

variable "github_repo" {
  type        = string
  description = "GitHub Repository for Workload Identity Federation."
  default     = "carassco-labs/gcp-foundation"
}
