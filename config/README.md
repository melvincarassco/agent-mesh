# Configuration Profiles (`config/`)

Contains multi-environment JSON configuration profiles and Pydantic `BaseSettings` setup examples.

## Files

- **`settings.py.example`**: Reference implementation for Pydantic v2 `BaseSettings` singleton with GCP Secret Manager hook.
- **`env.dev.json`**: Local development profile variables.
- **`env.prod.json`**: Production configuration profile variables.
