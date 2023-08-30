from __future__ import annotations

from typing import Union

from loguru import logger as log

# from settings.config import app_settings, logging_settings
from config import settings

# from red_utils.fastapi_utils import default_api_str, tags_metadata

# ENV: str = app_settings.APP_ENV
ENV: str = settings.ENV
CONTAINER_ENV: bool = settings.CONTAINER_ENV

if CONTAINER_ENV:
    env_string: str = f"[env:{ENV.upper()} (container)]"
else:
    env_string: str = f"[env:{ENV.upper()}]"

valid_strains: list[str] = ["indica", "hybrid", "sativa", "unknown"]
valid_forms: list[str] = [
    "vaporizer",
    "disposable vaporizer",
    "cartridge",
    "disposable cartridge",
    "flower",
    "shake",
    "dab",
    "live resin",
    "rosin",
    "budder",
    "hash",
    "badder",
    "edible" "tincture",
    "topical",
]
