# ADR-002: Why FastAPI as Standard Python Web Framework

- **Status**: Accepted
- **Date**: 2026-08-04
- **Authors**: Staff Engineering Architecture Team
- **Deciders**: Carassco Labs Architecture Review Board

## Context & Problem Statement

Carassco Labs backends serve high-concurrency API requests, orchestrate async AI workflows (e.g. LLM streaming responses, vector database lookups), and enforce strict data validation. We require a modern Python web framework with native `asyncio` support, auto-generated OpenAPI documentation, and robust type safety.

## Decision Drivers

- **Asynchronous IO**: Native `async/await` execution for non-blocking I/O during AI inference and database operations.
- **Type Safety & Data Validation**: Built-in integration with Pydantic v2 for compile-time/runtime data serialization.
- **Developer Velocity**: Auto-generated interactive API documentation (OpenAPI / Swagger / ReDoc).
- **Performance**: High throughput matching Node.js / Go speeds when paired with Starlette and Uvicorn.

## Considered Options

1. **FastAPI**: Async-first Python web framework built on Starlette and Pydantic.
2. **Flask**: Micro-framework with synchronous default execution.
3. **Django (Ninja / REST Framework)**: Full-stack synchronous web framework.

## Decision Outcome

Chosen Option: **FastAPI**, because it combines async performance with declarative Pydantic schemas, reducing boilerplate code by up to 40% while delivering production OpenAPI specs automatically.

### Positive Consequences

- Seamless schema sharing between frontend, backend, and external API consumers.
- Native support for Server-Sent Events (SSE) and WebSockets required for LLM streaming.
- Rapid developer onboarding due to clean class/model abstractions.

### Negative Consequences & Tradeoffs

- Requires discipline in managing async execution loops to prevent blocking code in async paths.

## Pros & Cons of the Options

### Option 1: FastAPI
- Good, because Pydantic v2 integration enforces strict schema validation and ultra-fast Rust-core parsing.
- Good, because native `async/await` prevents I/O thread starvation during remote AI API calls.
- Bad, because third-party synchronous Python libraries require execution in `run_in_executor` threads.

### Option 2: Flask
- Good, because lightweight and highly familiar across traditional Python codebases.
- Bad, because lack of native async/await limits high-concurrency streaming capabilities.
- Bad, because manual OpenAPI schema maintenance is required.

### Option 3: Django
- Good, because battery-included ORM and admin interface.
- Bad, because heavyweight ORM and synchronous legacy core add unnecessary overhead for microservices.

## Validation Plan

Monitored via automated unit/integration tests running under pytest-asyncio, alongside benchmark testing using Locust/k6 under high concurrency.
