from __future__ import annotations

from pathlib import Path

from .config import AppSettings, DBSettings

from dynaconf import Dynaconf

DYNACONF_SETTINGS: Dynaconf = Dynaconf(
    environments=True,
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
)

APP_SETTINGS: AppSettings = AppSettings(
    env=DYNACONF_SETTINGS.ENV,
    container_env=DYNACONF_SETTINGS.CONTAINER_ENV,
    log_level=DYNACONF_SETTINGS.LOG_LEVEL,
    data_dir=DYNACONF_SETTINGS.APP_DATA_DIR,
    logs_dir=DYNACONF_SETTINGS.APP_LOGS_DIR,
    cache_dir=DYNACONF_SETTINGS.APP_CACHE_DIR,
    serial_dir=DYNACONF_SETTINGS.APP_SERIAL_DIR,
)

ENSURE_DIRS: list[Path] = [
    APP_SETTINGS.data_dir,
    APP_SETTINGS.cache_dir,
    APP_SETTINGS.serial_dir,
]

DB_SETTINGS: DBSettings = DBSettings(
    type=DYNACONF_SETTINGS.DB_TYPE,
    host=DYNACONF_SETTINGS.DB_HOST,
    port=DYNACONF_SETTINGS.DB_PORT,
    username=DYNACONF_SETTINGS.DB_USERNAME,
    password=DYNACONF_SETTINGS.DB_PASSWORD,
    database=DYNACONF_SETTINGS.DB_DATABASE,
)
