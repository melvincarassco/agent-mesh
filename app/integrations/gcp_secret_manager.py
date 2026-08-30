"""
GCP Secret Manager Integration Client with TTL Caching.
"""
import logging
import os
import time
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class SecretManagerClient:
    """Client for resolving secrets from GCP Secret Manager with in-memory TTL cache."""

    def __init__(self, default_project_id: Optional[str] = None, ttl_seconds: int = 900) -> None:
        self.default_project_id = default_project_id or os.getenv("GCP_PROJECT_ID")
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Tuple[str, float]] = {}
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from google.cloud import secretmanager
                self._client = secretmanager.SecretManagerServiceClient()
            except Exception as e:
                logger.warning(f"Could not initialize GCP SecretManagerServiceClient: {e}")
                self._client = False
        return self._client if self._client is not False else None

    def get_secret(
        self,
        secret_id: str,
        project_id: Optional[str] = None,
        version: str = "latest",
        fallback: Optional[str] = None
    ) -> Optional[str]:
        """Retrieves secret payload with TTL caching and local environment fallback."""
        target_project = project_id or self.default_project_id
        cache_key = f"{target_project}/{secret_id}/{version}"
        now = time.time()

        # 1. Check in-memory TTL cache
        if cache_key in self._cache:
            secret_value, expire_time = self._cache[cache_key]
            if now < expire_time:
                logger.debug(f"Secret Manager Cache Hit for key: {secret_id}")
                return secret_value

        # 2. Try fetching from GCP Secret Manager API
        client = self._get_client()
        if client and target_project:
            try:
                name = f"projects/{target_project}/secrets/{secret_id}/versions/{version}"
                response = client.access_secret_version(request={"name": name})
                secret_value = response.payload.data.decode("UTF-8")
                
                # Cache the retrieved secret
                self._cache[cache_key] = (secret_value, now + self.ttl_seconds)
                logger.info(f"Secret Manager API fetch success for: {secret_id}")
                return secret_value
            except Exception as exc:
                logger.warning(f"Failed to fetch secret '{secret_id}' from GCP Secret Manager: {exc}")

        # 3. Fallback to OS environment variable or provided fallback string
        env_val = os.getenv(secret_id.upper().replace("-", "_"))
        if env_val is not None:
            logger.info(f"Using local environment fallback for secret: {secret_id}")
            return env_val

        return fallback

    def clear_cache(self) -> None:
        """Clears all cached secrets."""
        self._cache.clear()
