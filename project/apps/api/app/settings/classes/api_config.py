"""Custom API configuration. The base class is simple, containing a BASE_URL and
optional API key & token.

For more customized APIs, requiring more properties, create custom classes that
inherit from APISettings.

"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, validator
from pydantic_settings import BaseSettings

# THIS_DIR = Path(__file__).parent


class APISettings(BaseSettings):
    BASE_URL: str = Field(default=None, env="BASE_URL")
    API_KEY: Optional[str] = Field(default=None, env="API_KEY")
    TOKEN: Optional[str] = Field(default=None, env="TOKEN")

    class Config:
        env_file = f"settings/env_files/api.env"

    @validator("API_KEY", "TOKEN")
    def validate_api_key(cls, v) -> str:
        """If no value set/detected in env, return None."""
        return v or None
