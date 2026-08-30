"""
Reference Pattern: GCP Pub/Sub Event Schema
"""
from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel, Field


class CloudEventMessage(BaseModel):
    event_id: str = Field(..., description="Unique event identifier (UUID)")
    event_type: str = Field(..., description="Domain event topic name")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = Field(default_factory=dict)
