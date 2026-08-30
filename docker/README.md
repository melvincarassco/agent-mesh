# Container Environment Layout (`docker/`)

Defines Docker multi-stage build files, local development containers, and Docker Compose profiles.

## Container Files

- **`Dockerfile.dev`**: Development container spec featuring live code auto-reload (`uvicorn --reload`).
- **`Dockerfile.prod`**: Multi-stage production container spec with non-root runtime user (`appuser`), minimal layer footprint, and gunicorn/uvicorn worker execution.
- **`docker-compose.yml`**: Local service orchestration engine for local development.
- **`docker-compose.override.yml.example`**: Override template for local developer overrides.

## Container Specifications

- Base OS: `python:3.11-slim`
- Production Runtime User: `appuser` (`uid=10001`, `gid=10001`)
- Default Exposed Port: `8080`
