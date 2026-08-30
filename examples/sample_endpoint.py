"""
Reference Pattern: FastAPI API Router Endpoint
"""
from typing import Any, Dict
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/v1/examples", tags=["Examples"])


class ExampleRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Input query string")


class ExampleResponse(BaseModel):
    status: str = "success"
    result: Dict[str, Any]


@router.post("/", response_model=ExampleResponse, status_code=status.HTTP_200_OK)
async def process_example(payload: ExampleRequest) -> ExampleResponse:
    """Reference endpoint handler pattern."""
    return ExampleResponse(
        status="success",
        result={"echo": payload.query, "processed": True}
    )
