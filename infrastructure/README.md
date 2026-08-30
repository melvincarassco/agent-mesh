# Infrastructure as Code (`infrastructure/`)

Contains Terraform modules, Cloud Run definitions, Secret Manager provisioning, and IAM policy manifests for GCP infrastructure.

## Directory Layout

```text
infrastructure/
└── terraform/
    ├── modules/             # Reusable Terraform modules (Cloud Run, Artifact Registry, Secret Manager)
    └── environments/
        ├── dev/             # Development environment state & terraform.tfvars
        └── prod/            # Production environment state & terraform.tfvars
```

## Infrastructure Modules

1. **`cloud_run`**: Provisions GCP Cloud Run service with revision scaling bounds, container specs, and IAM permissions.
2. **`artifact_registry`**: Provisions Docker image repository in GCP Artifact Registry with vulnerability scanning.
3. **`secret_manager`**: Provisions secrets and assigns `roles/secretmanager.secretAccessor` permissions to Cloud Run Service Account.
4. **`iam`**: Provisions workload identity pools and service account bindings.
