"""
ASGI Middlewares Module.
Provides Correlation ID propagation and HTTP request duration logging.
"""
import contextvars
import logging
import time
import uuid
from typing import Callable, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# Context variable to hold current correlation ID across async tasks
correlation_id_ctx: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "correlation_id", default=None
)


def get_correlation_id() -> Optional[str]:
    """Retrieves current task correlation ID."""
    return correlation_id_ctx.get()


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Injects or extracts X-Correlation-ID for trace propagation."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        token = correlation_id_ctx.set(correlation_id)

        try:
            response = await call_next(request)
            response.headers["X-Correlation-ID"] = correlation_id
            return response
        finally:
            correlation_id_ctx.reset(token)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs incoming HTTP requests with latency metrics."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()
        correlation_id = get_correlation_id()

        try:
            response = await call_next(request)
            process_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

            logger.info(
                f"{request.method} {request.url.path} - {response.status_code} - {process_time_ms}ms",
                extra={
                    "http_method": request.method,
                    "url_path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": process_time_ms,
                    "correlation_id": correlation_id,
                },
            )
            return response
        except Exception as exc:
            process_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(
                f"Unhandled Exception in {request.method} {request.url.path}: {str(exc)}",
                extra={
                    "http_method": request.method,
                    "url_path": request.url.path,
                    "duration_ms": process_time_ms,
                    "correlation_id": correlation_id,
                    "error": str(exc),
                },
                exc_info=True,
            )
            raise exc
