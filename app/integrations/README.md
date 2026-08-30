# GCP & External Integrations (`app/integrations/`)

Houses SDK client wrappers for Google Cloud Platform services and external microservices.

## Managed Integration Connectors

- **`gcp_secret_manager.py`**: GCP Secret Manager API fetcher & TTL cache.
- **`gcp_storage.py`**: GCP Cloud Storage (GCS) upload/download bucket manager.
- **`vertex_ai.py`**: GCP Vertex AI Gemini model invocation & vector search client wrapper.
- **`pubsub.py`**: GCP Cloud Pub/Sub publisher and subscriber client wrapper.
