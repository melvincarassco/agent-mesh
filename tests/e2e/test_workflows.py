"""
End-to-End Tests for Workflow Submission, Graph State, and SSE Live Streaming.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_workflow_submission_and_execution_stream(async_client: AsyncClient):
    """Verify workflow submission, DAG graph retrieval, and SSE event streaming."""
    # 1. Submit Workflow
    submit_resp = await async_client.post(
        "/v1/workflows/submit",
        json={"goal": "Research serverless AI trends and write an architecture document"}
    )
    assert submit_resp.status_code == 201
    submit_data = submit_resp.json()
    assert "workflow_id" in submit_data
    workflow_id = submit_data["workflow_id"]

    # 2. Get Workflow Status
    status_resp = await async_client.get(f"/v1/workflows/{workflow_id}")
    assert status_resp.status_code == 200
    status_data = status_resp.json()
    assert status_data["workflow_id"] == workflow_id
    assert "graph" in status_data
    assert len(status_data["graph"]["nodes"]) == 3

    # 3. Stream SSE Events
    stream_resp = await async_client.get(f"/v1/workflows/{workflow_id}/stream")
    assert stream_resp.status_code == 200
    assert "text/event-stream" in stream_resp.headers["content-type"]

    sse_content = stream_resp.text
    assert "workflow_started" in sse_content
    assert "task_completed" in sse_content
    assert "workflow_finished" in sse_content
