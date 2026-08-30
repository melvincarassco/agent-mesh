# Configuration & Secret Management Architecture

> **Comprehensive guide to environment configuration, GCP Secret Manager integration, hierarchy resolution, and multi-environment setup for `agent-mesh`.**

---

## 1. Overview & Core Philosophy

In accordance with [12-Factor App methodology](https://12factor.net/config) and [Carassco Labs Security Standards](file:///Users/dalehendriques/Downloads/MELVIN_WORK/carassco-labs/handbook/docs/13-security-standards.md), application configuration is strictly decoupled from code.

- **Zero Hardcoded Secrets**: Secrets, credentials, and API tokens are NEVER committed to version control or baked into Docker container layers.
- **Strong Type Safety**: All settings are parsed, validated, and type-checked at container startup using Pydantic `BaseSettings`.
- **IAM-Driven Secret Resolution**: In production, secrets are dynamically resolved from GCP Secret Manager via IAM Service Account credentials.

---

## 2. Configuration Hierarchy

Configuration settings are resolved at container initialization following a strict, predictable precedence order (higher numbers override lower numbers):

```text
▲ 5. GCP Secret Manager (IAM Authorized Runtime API Fetch)
│ 4. OS Environment Variables (Cloud Run Service / Shell)
│ 3. Local `.env` File (.env / .env.production)
│ 2. JSON/YAML Profile Config (config/env.{ENVIRONMENT}.json)
└ 1. Code Default Fallbacks (app/core/config.py)
```

If a setting is present in multiple layers (e.g. `DATABASE_URL` is defined in both `.env` and GCP Secret Manager), the higher priority layer (**GCP Secret Manager**) takes precedence.

---

## 3. Environment Variables Specification

All environment variable names use upper-case snake case (`SNAKE_CASE`) with standard prefixes where appropriate.

### Standard Core Environment Variables

| Variable Name | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `ENVIRONMENT` | `str` | `development` | Runtime environment (`development`, `testing`, `staging`, `production`) |
| `DEBUG` | `bool` | `false` | Enable verbose debugging & detailed tracebacks (Dev only!) |
| `APP_NAME` | `str` | `agent-mesh` | Service identifier used in log correlation and metrics |
| `APP_VERSION` | `str` | `1.0.0` | Semantic version string |
| `PORT` | `int` | `8080` | Container bind port (Cloud Run sets this automatically) |
| `LOG_LEVEL` | `str` | `INFO` | Logging threshold (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) |
| `GCP_PROJECT_ID` | `str` | *Required in Prod* | Google Cloud Platform Project ID |
| `GCP_REGION` | `str` | `us-central1` | Default GCP region for service API calls |

### Secret Variable Mapping

Secrets managed via GCP Secret Manager follow explicit naming conventions:

| Config Field | Local `.env` Variable | GCP Secret Manager ID |
| :--- | :--- | :--- |
| `secret_key` | `SECRET_KEY` | `agent-mesh-secret-key` |
| `database_url` | `DATABASE_URL` | `agent-mesh-db-url` |
| `api_key_gemini` | `GEMINI_API_KEY` | `carassco-gemini-api-key` |
| `redis_password` | `REDIS_PASSWORD` | `agent-mesh-redis-password` |

---

## 4. GCP Secret Manager Integration

### Local Development vs Cloud Execution

In `development` mode, settings are loaded from the local `.env` file or environment.
In `production` mode, the application initializes the `google-cloud-secret-manager` Python SDK to retrieve encrypted payloads directly from GCP.

### In-Memory Caching & Performance

To prevent high-frequency API latency and excessive API billing on every incoming HTTP request:
- Secret Manager lookups are cached in-memory with a configurable Time-To-Live (TTL) of **15 minutes** (`SECRET_CACHE_TTL_SECONDS=900`).
- Cache invalidation occurs automatically upon expiration or container recycling.

### IAM Permissions Required

The Cloud Run Service Account executing the container requires the following minimal IAM role:
- `roles/secretmanager.secretAccessor` granted on target secret resources.

---

## 5. Environment Profiles Breakdown

### A. Local Development Configuration (`development`)
- Activated via `ENVIRONMENT=development` in `.env`.
- `DEBUG=true` enables auto-reload and verbose logging.
- GCP Secret Manager is bypassed; local `.env` values or local docker containers (e.g. local PostgreSQL / Redis) are used.

### B. Testing Configuration (`testing`)
- Activated automatically during `pytest` test suite execution.
- Overrides `DATABASE_URL` to an in-memory SQLite database or ephemeral test container.
- Mocks all external GCP SDK calls (Vertex AI, Cloud Storage).

### C. Staging Configuration (`staging`)
- Connects to dedicated GCP Staging project resources.
- `DEBUG=false`.
- Secret Manager actively resolves staging secrets (`projects/carassco-staging/secrets/...`).

### D. Production Configuration (`production`)
- Fully hardened mode (`DEBUG=false`, strict CORS origin whitelist).
- All sensitive credentials dynamically injected from GCP Secret Manager (`projects/carassco-prod/secrets/...`).
- Logs formatted strictly as single-line GCP Structured JSON.

---

## 6. Local Development Workflow

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Modify local values in `.env` as required.
3. Start the local container environment using Docker Compose:
   ```bash
   docker-compose up --build
   ```
4. Verify configuration status at `http://localhost:8080/health`.
