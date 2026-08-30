# Schemas Layer (`app/schemas/`)

Contains Pydantic v2 data models for API requests, API responses, event payloads, and internal data structures.

## Standards

- Inherit all models from `pydantic.BaseModel`.
- Configure `model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)`.
- Use Field descriptions and examples for auto-generated OpenAPI documentation.
