# Business Services Layer (`app/services/`)

This directory contains pure domain logic, workflow orchestration, and business rules.

## Design Patterns

- Services must be decoupled from HTTP transport objects (FastAPI `Request` or `Response`).
- Input parameters and return types must use Python type hints or Pydantic data models.
- External API calls to GCP services or third-party APIs must be invoked through `app/integrations/`.
