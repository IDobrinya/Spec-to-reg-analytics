from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class APISettings(EnvBaseSettings):
    URL: str = "http://localhost:8000"


class TimezoneSettings(EnvBaseSettings):
    TIMEZONE: str = "Europe/Moscow"


class Settings(APISettings, TimezoneSettings):
    pass


settings = Settings()
