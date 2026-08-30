"""
Reference Pattern: Async Domain Service
"""
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class SampleDomainService:
    """Reference implementation of a domain service layer."""

    async def execute_task(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Executing sample domain task", extra={"payload_keys": list(payload.keys())})
        return {"status": "completed", "input_count": len(payload)}
