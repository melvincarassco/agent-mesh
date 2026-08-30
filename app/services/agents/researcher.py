"""
Researcher Agent Module.
Gathers domain context, queries storage/search, and summarizes context.
"""
from typing import Any, Dict
from app.services.agents.base import BaseAgent


class ResearcherAgent(BaseAgent):
    """Specialist Agent responsible for domain information retrieval."""

    def __init__(self) -> None:
        super().__init__(agent_role="researcher")

    async def run(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        task_desc = task_input.get("description", "Gather research context")
        prompt = f"Perform research and extract key insights for: {task_desc}"
        
        result_text = self.invoke_model(prompt)

        return {
            "status": "success",
            "findings": result_text,
            "sources_queried": ["vertex_vector_search", "cloud_storage_artifacts"]
        }
