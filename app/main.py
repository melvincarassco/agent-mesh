"""
Main FastAPI Application Entrypoint.
Assembles application configuration, logging, middlewares, exception handlers, static dashboard UI, and routers.
"""
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.health import router as health_router
from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.middleware import (
    CorrelationIdMiddleware,
    RequestLoggingMiddleware,
    get_correlation_id,
)
from app.core.security import setup_cors

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


def create_app() -> FastAPI:
    """FastAPI Application Factory."""
    settings = get_settings()
    
    # Initialize structured JSON logging
    setup_logging(log_level=settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url="/redoc" if settings.environment != "production" else None,
    )

    # Setup Security & CORS
    setup_cors(app, settings)

    # Setup Middlewares
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(CorrelationIdMiddleware)

    # Global Exception Handlers (RFC 7807 Standard Format)
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "type": "about:blank",
                "title": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
                "status": exc.status_code,
                "detail": exc.detail,
                "correlation_id": get_correlation_id(),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "type": "https://tools.ietf.org/html/rfc7807",
                "title": "Unprocessable Entity",
                "status": 422,
                "detail": exc.errors(),
                "correlation_id": get_correlation_id(),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "type": "about:blank",
                "title": "Internal Server Error",
                "status": 500,
                "detail": "An unexpected error occurred." if not settings.debug else str(exc),
                "correlation_id": get_correlation_id(),
            },
        )

    # Mount Static Files & Root Web Telemetry Dashboard
    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

        @app.get("/", include_in_schema=False)
        async def serve_dashboard():
            return FileResponse(str(STATIC_DIR / "index.html"))

    # Mount Routers
    app.include_router(health_router)  # Top-level /health & /ready
    app.include_router(api_v1_router)   # /v1 API routes

    return app


app = create_app()
