"""
Health & Readiness Probes Router.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from app.core.config import Settings, get_settings

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Liveness Probe Response Schema."""
    status: str = Field(default="ok", json_schema_extra={"example": "ok"})
    app_name: str = Field(..., json_schema_extra={"example": "agent-mesh"})
    version: str = Field(..., json_schema_extra={"example": "1.0.0"})
    environment: str = Field(..., json_schema_extra={"example": "development"})
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ReadyResponse(BaseModel):
    """Readiness Probe Response Schema."""
    status: str = Field(default="ready", json_schema_extra={"example": "ready"})
    checks: dict = Field(default_factory=lambda: {"configuration": "ok"})
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness Probe",
    description="Returns HTTP 200 OK if container process is active."
)
async def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment
    )


@router.get(
    "/ready",
    response_model=ReadyResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness Probe",
    description="Returns HTTP 200 OK if service dependencies & configurations are ready."
)
async def readiness_check(settings: Settings = Depends(get_settings)) -> ReadyResponse:
    return ReadyResponse(
        status="ready",
        checks={"configuration": "ok" if settings.app_name else "error"}
    )
