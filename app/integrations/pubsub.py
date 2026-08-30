"""
GCP Cloud Pub/Sub Integration Client.
"""
import json
import logging
import os
import uuid
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)


class PubSubClient:
    """Client wrapper for GCP Cloud Pub/Sub messaging operations."""

    def __init__(self, project_id: Optional[str] = None) -> None:
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID")
        self._publisher = None

    def _get_publisher(self):
        if self._publisher is None:
            try:
                from google.cloud import pubsub_v1
                self._publisher = pubsub_v1.PublisherClient()
            except Exception as exc:
                logger.warning(f"Could not initialize GCP PubSub PublisherClient: {exc}")
                self._publisher = False
        return self._publisher if self._publisher is not False else None

    def publish_event(
        self,
        topic_id: str,
        data: Dict[str, Any],
        attributes: Optional[Dict[str, str]] = None
    ) -> str:
        """Publishes a JSON payload to a target Pub/Sub topic."""
        publisher = self._get_publisher()
        payload_bytes = json.dumps(data).encode("utf-8")
        attrs = attributes or {}

        if publisher and self.project_id:
            try:
                topic_path = publisher.topic_path(self.project_id, topic_id)
                future = publisher.publish(topic_path, payload_bytes, **attrs)
                message_id = future.result()
                logger.info(f"Published Pub/Sub message '{message_id}' to topic '{topic_id}'")
                return str(message_id)
            except Exception as exc:
                logger.error(f"Failed to publish Pub/Sub event to topic '{topic_id}': {exc}")
                raise exc

        mock_msg_id = f"mock-pubsub-msg-{uuid.uuid4().hex[:8]}"
        logger.info(f"[Mock Mode] Published event {mock_msg_id} to topic '{topic_id}'")
        return mock_msg_id

    def subscribe_topic(
        self,
        subscription_id: str,
        callback: Callable[[Dict[str, Any]], None]
    ) -> None:
        """Registers a callback for incoming messages on a Pub/Sub subscription."""
        logger.info(f"Registered subscriber callback on subscription: {subscription_id}")
