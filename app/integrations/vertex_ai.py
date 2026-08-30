"""
GCP Vertex AI (Gemini & Embeddings) Integration Client.
"""
import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)


class VertexAIClient:
    """Client wrapper for GCP Vertex AI Gemini models and Vector Embeddings."""

    def __init__(self, project_id: Optional[str] = None, location: Optional[str] = None) -> None:
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID")
        self.location = location or os.getenv("GCP_REGION", "us-central1")
        self._initialized = False

    def _ensure_init(self) -> bool:
        if not self._initialized:
            try:
                import vertexai
                if self.project_id:
                    vertexai.init(project=self.project_id, location=self.location)
                    self._initialized = True
            except Exception as exc:
                logger.warning(f"Could not initialize GCP Vertex AI: {exc}")
                self._initialized = False
        return self._initialized

    def generate_content(
        self,
        prompt: str,
        model_name: str = "gemini-1.5-flash",
        temperature: float = 0.7
    ) -> str:
        """Generates text output using Vertex AI Gemini model."""
        if self._ensure_init():
            try:
                from vertexai.generative_models import GenerativeModel
                model = GenerativeModel(model_name)
                response = model.generate_content(
                    prompt,
                    generation_config={"temperature": temperature}
                )
                logger.info(f"Vertex AI generation complete with model '{model_name}'")
                return response.text
            except Exception as exc:
                logger.warning(f"Vertex AI Generation API unavailable: {exc}. Falling back to mock mode.")

        logger.info(f"[Mock Mode] Vertex AI generating response for prompt: {prompt[:30]}...")
        return f"Mock Vertex AI response for prompt: '{prompt}'"

    def generate_embeddings(
        self,
        text_list: List[str],
        model_name: str = "text-embedding-004"
    ) -> List[List[float]]:
        """Generates vector embeddings for a list of input strings."""
        if self._ensure_init():
            try:
                from vertexai.language_models import TextEmbeddingModel
                model = TextEmbeddingModel.from_pretrained(model_name)
                embeddings = model.get_embeddings(text_list)
                logger.info(f"Generated embeddings for {len(text_list)} items via model '{model_name}'")
                return [embedding.values for embedding in embeddings]
            except Exception as exc:
                logger.warning(f"Vertex AI Embeddings API unavailable: {exc}. Falling back to mock mode.")

        logger.info(f"[Mock Mode] Generating mock embeddings for {len(text_list)} inputs")
        return [[0.01 * (i + 1) for _ in range(768)] for i in range(len(text_list))]
