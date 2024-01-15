from __future__ import annotations

from pathlib import Path

from core import DBSettings
from core.db import (
    get_db_connection_class,
    get_db_engine,
    get_db_session,
    init_base_metadata,
)
from core.dependencies import APP_SETTINGS, DB_SETTINGS, ENSURE_DIRS
from loguru import logger as log
from red_utils.ext import sqlalchemy_utils as sa_utils
from red_utils.ext.loguru_utils import LoguruSinkStdOut, init_logger
from red_utils.std.path_utils import ensure_dirs_exist
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase

if __name__ == "__main__":
    init_logger([LoguruSinkStdOut(level=APP_SETTINGS.log_level).as_dict()])


def entrypoint_app_startup(ensure_dirs: list[Path] = ENSURE_DIRS):
    log.info(f"Entrypoint: app_startup")

    log.info("Running app startup operations")
    try:
        ensure_dirs_exist(ensure_dirs)
        log.success("App startup complete")
    except Exception as exc:
        msg = Exception(f"Unhandled exception running app startup. Details: {exc}")
        log.error(msg)

        raise msg


def entrypoint_sqlalchemy_startup(
    db_settings: DBSettings = DB_SETTINGS, sqla_base: DeclarativeBase = sa_utils.Base
):
    conn_class = get_db_connection_class(db_settings)
    log.debug(f"Connection class: {conn_class}")

    engine = get_db_engine(db_conn=conn_class)

    init_base_metadata(engine=engine)
