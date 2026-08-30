"""
GCP Cloud Storage (GCS) Integration Client.
"""
import datetime
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


class CloudStorageClient:
    """Client wrapper for GCP Cloud Storage operations."""

    def __init__(self, project_id: Optional[str] = None) -> None:
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID")
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from google.cloud import storage
                self._client = storage.Client(project=self.project_id)
            except Exception as exc:
                logger.warning(f"Could not initialize GCP Storage Client: {exc}")
                self._client = False
        return self._client if self._client is not False else None

    def upload_file(
        self,
        bucket_name: str,
        destination_blob_name: str,
        file_bytes: bytes,
        content_type: str = "application/octet-stream"
    ) -> str:
        """Uploads byte data to a GCS bucket blob and returns GCS URI."""
        client = self._get_client()
        if client:
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_string(file_bytes, content_type=content_type)
            gcs_uri = f"gs://{bucket_name}/{destination_blob_name}"
            logger.info(f"Successfully uploaded file to {gcs_uri}")
            return gcs_uri
        
        logger.info(f"[Mock Mode] Simulating upload to gs://{bucket_name}/{destination_blob_name}")
        return f"gs://{bucket_name}/{destination_blob_name}"

    def download_file(self, bucket_name: str, source_blob_name: str) -> bytes:
        """Downloads byte payload from a GCS blob."""
        client = self._get_client()
        if client:
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(source_blob_name)
            data = blob.download_as_bytes()
            logger.info(f"Successfully downloaded file from gs://{bucket_name}/{source_blob_name}")
            return data
            
        logger.info(f"[Mock Mode] Simulating download from gs://{bucket_name}/{source_blob_name}")
        return b"mock-gcs-file-content"

    def generate_signed_url(
        self,
        bucket_name: str,
        blob_name: str,
        expiration_minutes: int = 15
    ) -> str:
        """Generates a temporary signed HTTP URL for a GCS blob."""
        client = self._get_client()
        if client:
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            url = blob.generate_signed_url(
                version="v4",
                expiration=datetime.timedelta(minutes=expiration_minutes),
                method="GET",
            )
            return url

        return f"https://storage.googleapis.com/{bucket_name}/{blob_name}?mock_signature=123"
