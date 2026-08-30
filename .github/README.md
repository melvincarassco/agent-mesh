# GitHub Automation & Workflows (`.github/`)

Contains GitHub Actions CI/CD pipeline definitions, PR templates, and issue templates.

## Workflows

- `ci.yml`: Executes ruff linting, mypy type checks, and pytest test suite on PRs and commits.
- `cd.yml`: Authenticates with GCP via OIDC Workload Identity Federation, builds Docker image, pushes to Artifact Registry, and deploys to Cloud Run.
- `code_quality.yml`: Runs security dependency audits and Trivy container vulnerability scans.
