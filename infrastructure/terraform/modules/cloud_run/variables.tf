variable "service_name" {
  type        = string
  description = "The name of the Cloud Run service."
}

variable "location" {
  type        = string
  description = "The GCP region for the Cloud Run service."
  default     = "us-central1"
}

variable "image_uri" {
  type        = string
  description = "The container image URI to deploy."
}

variable "min_instances" {
  type        = number
  description = "Minimum number of instances to scale down to."
  default     = 0
}

variable "max_instances" {
  type        = number
  description = "Maximum number of instances to scale up to."
  default     = 10
}

variable "cpu" {
  type        = string
  description = "CPU allocation for the container."
  default     = "1000m"
}

variable "memory" {
  type        = string
  description = "Memory allocation for the container."
  default     = "512Mi"
}

variable "env_vars" {
  type        = map(string)
  description = "Environment variables to set in the container."
  default     = {}
}

variable "allow_unauthenticated" {
  type        = bool
  description = "Whether to allow unauthenticated invocations."
  default     = true
}

variable "service_account_email" {
  type        = string
  description = "The service account email executing the container."
  default     = null
}
