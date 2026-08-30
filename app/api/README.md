# API Controller Layer (`app/api/`)

This directory houses FastAPI `APIRouter` instances grouped by domain or API version (e.g. `v1/`).

## Controller Conventions

- Route handlers MUST define explicit response models (`response_model=MyResponseSchema`).
- Route handlers MUST use dependency injection (`Depends()`) for service handlers and database sessions.
- Status codes MUST be explicitly declared (`status_code=status.HTTP_200_OK`).
