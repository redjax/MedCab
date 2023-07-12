from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, ValidationError, validator
from pydantic_settings import BaseSettings

## Import custom classes
from settings.classes.api_config import APISettings

allowed_log_levels = ["DEBUG", "CRITICAL", "WARNING", "ERROR", "INFO"]
allowed_app_envs = ["prod", "dev", "", None]


class AppSettings(BaseSettings):
    APP_ENV: str = Field(default="prod", env="APP_ENV")
    APP_TITLE: str = Field(default="Default App Title", env="APP_TITLE")
    APP_DESCRIPTION: str = Field(
        default="Default app description", env="APP_DESCRIPTION"
    )
    APP_VERSION: str = Field(default="0.0.1", env="APP_VERSION")

    class Config:
        env_file = f"settings/env_files/.env"

    @validator("APP_ENV")
    def validate_app_env(cls, v) -> str:
        if v not in allowed_app_envs:
            raise ValidationError(
                f"Invalid App env: {v}. Must be one of {allowed_app_envs}"
            )

        return v or "prod"

    @validator("APP_TITLE")
    def validate_app_title(cls, v) -> str:
        """If no value set/detected in env, return None."""
        return v or "Default App Title"

    @validator("APP_DESCRIPTION")
    def validate_app_description(cls, v) -> str:
        """If no value set/detected in env, return None."""
        return v or "Default app description"

    @validator("APP_VERSION")
    def validate_app_ver(cls, v) -> str:
        """If no value set/detected in env, return None."""
        return v or "0.0.1"


class LoggingSetting(BaseSettings):
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")

    @validator("LOG_LEVEL")
    def valid_log_level(cls, v) -> str:
        if not v:
            v = "INFO"

        if v not in allowed_log_levels:
            raise ValidationError(
                f"Invalid log level [{v}]. Must be one of {allowed_log_levels}"
            )

        return v

    class Config:
        env_file = f"settings/env_files/logging.env"


app_settings = AppSettings()
logging_settings = LoggingSetting()
api_settings = APISettings()
