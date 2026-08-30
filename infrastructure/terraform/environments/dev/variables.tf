variable "project_id" {
  type        = string
  description = "GCP Development Project ID."
  default     = "carassco-dev"
}

variable "region" {
  type        = string
  description = "GCP Development Region."
  default     = "us-central1"
}

variable "github_repo" {
  type        = string
  description = "GitHub Repository for Workload Identity Federation."
  default     = "carassco-labs/gcp-foundation"
}
