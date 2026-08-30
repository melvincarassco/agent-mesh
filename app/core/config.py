"""
Core Application Configuration Module.
Provides immutable Pydantic Settings with environment and secret loading.
"""
import json
from functools import lru_cache
from typing import List, Optional, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application Settings Schema."""

    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")
    app_name: str = Field(default="agent-mesh", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    port: int = Field(default=8080, alias="PORT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    gcp_project_id: Optional[str] = Field(default=None, alias="GCP_PROJECT_ID")
    gcp_region: str = Field(default="us-central1", alias="GCP_REGION")

    secret_key: str = Field(
        default="dev-secret-key-change-in-production-32bytes",
        alias="SECRET_KEY"
    )

    allowed_origins: Union[List[str], str] = Field(
        default=["*"],
        alias="ALLOWED_ORIGINS"
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: object) -> List[str]:
        if isinstance(v, str):
            v_trimmed = v.strip()
            if v_trimmed.startswith("[") and v_trimmed.endswith("]"):
                try:
                    parsed = json.loads(v_trimmed)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed]
                except json.JSONDecodeError:
                    pass
            return [origin.strip() for origin in v_trimmed.split(",") if origin.strip()]
        if isinstance(v, list):
            return [str(item).strip() for item in v]
        return ["*"]

    @field_validator("log_level", mode="before")
    @classmethod
    def parse_log_level(cls, v: object) -> str:
        if isinstance(v, str):
            return v.upper()
        return "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """Returns cached immutable application settings singleton."""
    return Settings()
