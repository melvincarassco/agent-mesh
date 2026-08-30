# Application Core Directory (`app/`)

This directory contains the Python package layout for all FastAPI microservices and AI applications built on top of `agent-mesh`.

## Package Hierarchy & Boundaries

```text
app/
├── api/            # Controller layer: FastAPI APIRouter endpoints & HTTP contracts
├── core/           # Infrastructure kernel: Config, security, logging, & middleware
├── db/             # Persistence layer: ORM sessions, migrations, & connections
├── integrations/   # External SDK layer: GCP SDKs (Vertex AI, GCS, Secret Manager)
├── models/         # Database domain entities (SQLAlchemy / SQLModel)
├── schemas/        # Interface contracts: Pydantic v2 request/response models
├── services/       # Domain business logic & orchestration workflows
└── utils/          # Cross-cutting utility functions & formatters
```

## Architectural Guidelines

1. **Strict Dependency Order**:
   `api` ➔ `services` ➔ `models` / `schemas` ➔ `core` & `integrations`.
   Higher-level layers may depend on lower-level layers, but lower layers MUST NOT depend on higher layers.

2. **No Business Logic in API Controllers**:
   Routers in `app/api/` should only validate incoming requests (via Pydantic schemas), call the appropriate `app/services/` handler, and return HTTP responses.

3. **Asynchronous Execution**:
   All I/O operations (database queries, HTTP client requests, GCP SDK calls) MUST use non-blocking `async/await` syntax.
