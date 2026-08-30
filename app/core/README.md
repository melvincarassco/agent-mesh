# Core Module (`app/core/`)

The `core` module provides the underlying infrastructure kernel for the application.

## Components

- **`config.py`**: Pydantic `BaseSettings` settings manager with GCP Secret Manager runtime resolution.
- **`logging.py`**: Structured JSON logging formatter (`python-json-logger`) mapped to GCP Cloud Logging formats.
- **`security.py`**: Token validation, CORS management, and IAM authentication helpers.
- **`middleware.py`**: FastAPI ASGI middleware for correlation ID injection (`X-Correlation-ID`) and request execution timing.
