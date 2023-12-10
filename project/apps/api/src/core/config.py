from __future__ import annotations

from typing import Union

from dynaconf import settings
from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    env: str = Field(default=settings.ENV, env="ENV")
    container_env: bool = Field(default=settings.CONTAINER_ENV, env="CONTAINER_ENV")
    log_level: str = Field(default=settings.LOG_LEVEL, env="LOG_LEVEL")

    @field_validator("log_level")
    def validate_log_level(cls, v) -> str:
        if isinstance(v, str):
            return v.upper()
        else:
            try:
                return str(v)
            except ValueError:
                raise ValidationError
            except Exception as exc:
                raise Exception(
                    f"Unhandled exception converting log_level to str. Details: {exc}"
                )


class APISettings(BaseSettings):
    title: str = Field(default=settings.API_TITLE, env="APP_TITLE")
    description: str = Field(default=settings.API_DESCRIPTION, env="API_DESCRIPTION")
    version: str = Field(default=settings.API_VERSION, env="API_VERSIONN")
    debug: bool = Field(default=settings.API_DEBUG, env="API_DEBUG")


class DBSettings(BaseSettings):
    type: str = Field(default=settings.DB_TYPE, env="DB_TYPE")
    host: str | None = Field(default=settings.DB_HOST, env="DB_HOST")
    port: str | None = Field(default=settings.DB_PORT, env="DB_PORT")
    username: str | None = Field(default=settings.DB_USERNAME, env="DB_USERNAME")
    password: str | None = Field(
        default=settings.DB_PASSWORD, env="DB_DATABASE", repr=False
    )
    database: str = Field(default=settings.DB_DATABASE, env="DB_DATABASE")


app_settings: AppSettings = AppSettings()
api_settings: APISettings = APISettings()
db_settings: DBSettings = DBSettings()
