"""
End-to-End Tests for /health, /ready, and Middleware Execution.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """Verify /health liveness probe response."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app_name"] == "agent-mesh"
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_readiness_check(async_client: AsyncClient):
    """Verify /ready readiness probe response."""
    response = await async_client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["checks"]["configuration"] == "ok"


@pytest.mark.asyncio
async def test_v1_health_check(async_client: AsyncClient):
    """Verify /v1/health router inclusion."""
    response = await async_client.get("/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_correlation_id_propagation(async_client: AsyncClient):
    """Verify X-Correlation-ID header propagation through middleware."""
    custom_cid = "custom-trace-id-12345"
    response = await async_client.get("/health", headers={"X-Correlation-ID": custom_cid})
    assert response.status_code == 200
    assert response.headers.get("X-Correlation-ID") == custom_cid


@pytest.mark.asyncio
async def test_auto_correlation_id_generation(async_client: AsyncClient):
    """Verify automatic X-Correlation-ID UUID generation when missing."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert "X-Correlation-ID" in response.headers
    assert len(response.headers["X-Correlation-ID"]) > 10
