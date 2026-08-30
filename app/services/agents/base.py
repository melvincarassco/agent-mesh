"""
Base Agent Interface.
Provides common prompt formatting, LLM invocation, and output parsing.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
from app.integrations.vertex_ai import VertexAIClient


class BaseAgent(ABC):
    """Abstract Base Class for specialist agents in Agent-Mesh."""

    def __init__(self, agent_role: str, model_name: str = "gemini-1.5-flash") -> None:
        self.agent_role = agent_role
        self.model_name = model_name
        self.ai_client = VertexAIClient()

    @abstractmethod
    async def run(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Executes agent-specific task logic."""
        pass

    def invoke_model(self, prompt: str, temperature: float = 0.7) -> str:
        """Invokes Vertex AI LLM with prompt context."""
        return self.ai_client.generate_content(
            prompt=prompt,
            model_name=self.model_name,
            temperature=temperature
        )
