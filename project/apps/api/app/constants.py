from __future__ import annotations

from typing import Union

from loguru import logger as log

from config import settings


valid_strains: list[str] = ["indica", "hybrid", "sativa", "unknown"]
valid_forms: list[str] = [
    "vape",
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

###############
# Environment #
###############
ENV: str = settings.ENV
CONTAINER_ENV: bool = settings.CONTAINER_ENV

if CONTAINER_ENV:
    env_string: str = f"[env:{ENV.upper()} (container)]"

    app_title = settings.FASTAPI_TITLE
    app_description = settings.FASTAPI_DESCRIPTION
    app_version = settings.FASTAPI_VERSION

    db_type = settings.DB_TYPE
    db_host = settings.DB_HOST
    db_username = settings.DB_USERNAME
    db_password = settings.DB_PASSWORD
    db_port = settings.DB_PORT
    db_database = settings.DB_DATABASE

else:
    env_string: str = f"[env:{ENV.upper()}]"

    app_title = settings.fastapi["title"]
    app_description = settings.fastapi["description"]
    app_version = str(settings.app["version"])

    db_type = settings.db.db_type
    db_host = settings.db.db_host
    db_username = settings.db.db_username
    db_password = settings.db.db_password
    db_db_port = settings.db.db_db_port
    db_database = settings.db.db_database
