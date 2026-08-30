"""
Unit tests for GCP SDK Connectors (Secret Manager, Cloud Storage, Vertex AI, Pub/Sub).
"""
import time
from unittest.mock import MagicMock
from app.integrations.gcp_secret_manager import SecretManagerClient
from app.integrations.gcp_storage import CloudStorageClient
from app.integrations.vertex_ai import VertexAIClient
from app.integrations.pubsub import PubSubClient


def test_secret_manager_client_ttl_cache(monkeypatch):
    """Verify SecretManagerClient TTL caching and fallback logic."""
    sm_client = SecretManagerClient(default_project_id="test-project", ttl_seconds=2)
    
    # Mock GCP Secret Manager API response
    mock_gcp_client = MagicMock()
    mock_payload = MagicMock()
    mock_payload.data.decode.return_value = "super-secret-api-key"
    mock_gcp_client.access_secret_version.return_value.payload = mock_payload
    sm_client._client = mock_gcp_client

    # First call: API fetch
    secret_val1 = sm_client.get_secret("api-key")
    assert secret_val1 == "super-secret-api-key"
    assert mock_gcp_client.access_secret_version.call_count == 1

    # Second call within TTL: Cache hit
    secret_val2 = sm_client.get_secret("api-key")
    assert secret_val2 == "super-secret-api-key"
    assert mock_gcp_client.access_secret_version.call_count == 1

    # Clear cache manually
    sm_client.clear_cache()
    secret_val3 = sm_client.get_secret("api-key")
    assert secret_val3 == "super-secret-api-key"
    assert mock_gcp_client.access_secret_version.call_count == 2


def test_secret_manager_env_fallback(monkeypatch):
    """Verify local environment fallback when GCP Secret Manager API is unavailable."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
    sm_client = SecretManagerClient(default_project_id="test-project")
    sm_client._client = False  # Disable GCP API client

    secret_val = sm_client.get_secret("database-url")
    assert secret_val == "postgresql://user:pass@localhost:5432/db"


def test_cloud_storage_client_mock():
    """Verify CloudStorageClient upload, download, and signed URL generation."""
    storage_client = CloudStorageClient(project_id="test-project")
    storage_client._client = False

    # Upload
    uri = storage_client.upload_file("my-bucket", "folder/data.json", b'{"key": "val"}')
    assert uri == "gs://my-bucket/folder/data.json"

    # Download
    data = storage_client.download_file("my-bucket", "folder/data.json")
    assert isinstance(data, bytes)

    # Signed URL
    url = storage_client.generate_signed_url("my-bucket", "folder/data.json")
    assert "https://storage.googleapis.com" in url


def test_vertex_ai_client_mock():
    """Verify VertexAIClient model generation and vector embeddings."""
    vertex_client = VertexAIClient(project_id="test-project")
    
    # Prompt Generation
    response_text = vertex_client.generate_content("Explain quantum computing")
    assert "Quantum" in response_text or "Mock" in response_text

    # Vector Embeddings
    embeddings = vertex_client.generate_embeddings(["text sample 1", "text sample 2"])
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 768


def test_pubsub_client_mock():
    """Verify PubSubClient event publishing."""
    pubsub_client = PubSubClient(project_id="test-project")
    pubsub_client._publisher = False

    msg_id = pubsub_client.publish_event(
        topic_id="user-events",
        data={"event_type": "user_signup", "user_id": "12345"},
        attributes={"source": "api"}
    )
    assert msg_id.startswith("mock-pubsub-msg-")
