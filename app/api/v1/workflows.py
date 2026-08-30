"""
Workflows & SSE Real-Time Event Streaming Router.
"""
import json
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.orchestrator import WorkflowOrchestrator, get_orchestrator

router = APIRouter(prefix="/workflows", tags=["Workflows"])


class WorkflowSubmitRequest(BaseModel):
    goal: str = Field(..., min_length=3, json_schema_extra={"example": "Research serverless architecture trends and draft a report"})


class WorkflowSubmitResponse(BaseModel):
    workflow_id: str = Field(..., json_schema_extra={"example": "wf-a1b2c3d4"})
    status: str = Field(default="INITIALIZED", json_schema_extra={"example": "INITIALIZED"})
    goal: str


@router.post(
    "/submit",
    response_model=WorkflowSubmitResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Multi-Agent Workflow Goal",
    description="Submits a high-level goal, runs Planner Agent, and initializes DAG dependency execution tree."
)
async def submit_workflow(
    payload: WorkflowSubmitRequest,
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator)
) -> WorkflowSubmitResponse:
    workflow_id = await orchestrator.initialize_workflow(goal=payload.goal)
    return WorkflowSubmitResponse(
        workflow_id=workflow_id,
        status="INITIALIZED",
        goal=payload.goal
    )


@router.get(
    "/{workflow_id}",
    summary="Get Workflow Execution Status",
    description="Returns current execution status and DAG task node graph."
)
async def get_workflow_status(
    workflow_id: str,
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator)
) -> Dict[str, Any]:
    wf = orchestrator.get_workflow(workflow_id)
    if not wf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found"
        )
    
    graph_dict = wf["graph"].model_dump()
    return {
        "workflow_id": wf["workflow_id"],
        "goal": wf["goal"],
        "status": wf["status"],
        "plan_summary": wf["plan_summary"],
        "graph": graph_dict
    }


@router.get(
    "/{workflow_id}/stream",
    summary="Stream Live Execution Events (SSE)",
    description="Server-Sent Events (SSE) stream broadcasting live agent thought steps, task transitions, and final output."
)
async def stream_workflow_execution(
    workflow_id: str,
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator)
) -> StreamingResponse:
    wf = orchestrator.get_workflow(workflow_id)
    if not wf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found"
        )

    async def sse_event_generator():
        async for event_data in orchestrator.run_workflow_stream(workflow_id):
            formatted_event = f"data: {json.dumps(event_data)}\n\n"
            yield formatted_event

    return StreamingResponse(
        sse_event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
