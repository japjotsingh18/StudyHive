from studyhive.core.config import Environment, Settings


def test_settings_use_safe_local_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.environment is Environment.DEVELOPMENT
    assert settings.database_url.startswith("postgresql+asyncpg://")
    assert settings.storage_path.is_absolute() is False
