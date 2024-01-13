from __future__ import annotations

from typing import Union
from pathlib import Path

from pydantic import Field, ValidationError, computed_field, field_validator
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    env: str = Field(default="prod", env="ENV")
    container_env: bool = Field(default=False, env="CONTAINER_ENV")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    data_dir: Union[str, Path] = Field(default=".data", env="APP_DATA_DIR")
    logs_dir: Union[str, Path] = Field(default="logs", env="APP_LOGS_DIR")
    cache_dir: Union[str, Path] = Field(default=".cache", env="APP_CACHE_DIR")
    serial_dir: Union[str, Path] = Field(default=".serial", env="APP_SERIAL_DIR")

    @field_validator("data_dir", "logs_dir", "cache_dir", "serial_dir")
    def validate_app_dir(cls, v) -> Path:
        assert v is not None, ValidationError
        if isinstance(v, str):
            v: Path = Path(v)
            return v
        elif isinstance(v, Path):
            return v
        else:
            raise ValidationError