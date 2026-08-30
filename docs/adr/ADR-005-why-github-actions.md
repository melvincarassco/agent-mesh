# ADR-005: Why GitHub Actions for CI/CD Automation

- **Status**: Accepted
- **Date**: 2026-08-04
- **Authors**: Staff Engineering Architecture Team
- **Deciders**: Carassco Labs Architecture Review Board

## Context & Problem Statement

Carassco Labs requires a unified, secure, and developer-friendly Continuous Integration and Continuous Delivery (CI/CD) platform to automate code quality checks, pytest execution, container builds, and GCP deployments across all repositories.

## Decision Drivers

- **Developer Proximity**: Native integration with GitHub repositories, Pull Requests, and code review checks.
- **Keyless Cloud Authentication**: Support for OpenID Connect (OIDC) & Workload Identity Federation (WIF) with GCP (eliminating long-lived GCP service account keys in secrets).
- **Extensibility & Ecosystem**: Rich marketplace of reusable actions (docker/build-push-action, google-github-actions).
- **Standardization**: Ability to define reusable workflow templates across all Carassco Labs applications.

## Considered Options

1. **GitHub Actions**: Integrated workflow automation platform natively built into GitHub.
2. **GCP Cloud Build**: Cloud-native build service hosted inside Google Cloud.
3. **GitLab CI / Jenkins**: Third-party CI tools requiring separate hosting or platform migration.

## Decision Outcome

Chosen Option: **GitHub Actions**, because it provides seamless developer experience directly inside GitHub PRs, eliminates key management security risks via OIDC Workload Identity Federation, and simplifies template inheritance across Carassco Labs.

### Positive Consequences

- Direct feedback on PRs with inline linter, typecheck, and test output.
- Enhanced security profile through OIDC keyless authentication with GCP Secret Manager and Artifact Registry.
- Centralized workflow templates maintained in repository configuration.

### Negative Consequences & Tradeoffs

- GitHub Actions runner minute usage must be budgeted across organization teams.

## Pros & Cons of the Options

### Option 1: GitHub Actions
- Good, because zero-key GCP authentication via `google-github-actions/auth` OIDC federation.
- Good, because code reviews, status checks, and merge blocking are unified in one UI.
- Bad, because build caching requires explicit setup (`actions/cache` or Docker buildx cache).

### Option 2: GCP Cloud Build
- Good, because native GCP IAM context and high build concurrency.
- Bad, because developer status check visibility requires custom webhook integrations back to GitHub.

### Option 3: Jenkins / GitLab CI
- Good, because customizable self-hosted infrastructure.
- Bad, because heavy server maintenance overhead and context switching away from GitHub.

## Validation Plan

Validation via PR workflow completion time metrics (<3 mins target for CI), successful keyless GCP deployment verification, and zero long-lived credentials present in GitHub secrets.
