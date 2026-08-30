variable "repository_id" {
  type        = string
  description = "The ID of the Artifact Registry repository."
}

variable "location" {
  type        = string
  description = "The GCP region for the Artifact Registry."
  default     = "us-central1"
}

variable "description" {
  type        = string
  description = "Description for the Artifact Registry repository."
  default     = "Docker repository for Carassco Labs container images"
}
