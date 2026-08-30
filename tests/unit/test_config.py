"""
Unit tests for App Core Configuration Settings.
"""
from app.core.config import Settings, get_settings


def test_default_settings():
    """Verify default values for core settings."""
    settings = Settings()
    assert settings.app_name == "agent-mesh"
    assert settings.environment == "development"
    assert settings.port == 8080
    assert settings.log_level == "INFO"
    assert settings.allowed_origins == ["*"]


def test_env_override(monkeypatch):
    """Verify environment variable overrides."""
    monkeypatch.setenv("APP_NAME", "custom-service")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("PORT", "9090")
    monkeypatch.setenv("LOG_LEVEL", "debug")
    monkeypatch.setenv("ALLOWED_ORIGINS", "https://app.carassco.com, https://admin.carassco.com")

    get_settings.cache_clear()
    settings = get_settings()

    assert settings.app_name == "custom-service"
    assert settings.environment == "production"
    assert settings.port == 9090
    assert settings.log_level == "DEBUG"
    assert settings.allowed_origins == [
        "https://app.carassco.com",
        "https://admin.carassco.com"
    ]
