from __future__ import annotations

from core.config import db_settings

from loguru import logger as log
from red_utils.ext.sqlalchemy_utils import (
    Base,
    create_base_metadata,
    get_engine,
    get_session,
    saPGConnection,
    saSQLiteConnection,
)

log.debug(f"Matching DB Type to: {db_settings.type}")
match db_settings.type:
    case "sqlite":
        log.debug(f"Detected SQLite DB")
        db_config = saSQLiteConnection(database=db_settings.database)
    case "postgres":
        log.debug(f"Detected Postgres DB")
        db_config = saPGConnection(
            host=db_settings.host,
            username=db_settings.username,
            password=db_settings.password,
            database=db_settings.database,
        )
    case _:
        raise Exception(f"Unknown DB_TYPE: {db_settings.type}")

engine = get_engine(connection=db_config, db_type=db_settings.type, echo=True)
SessionLocal = get_session(engine=engine, autoflush=True)


def get_db():
    db = SessionLocal()

    try:
        return db

    except Exception as exc:
        raise Exception(f"Unhandled exception getting database session. Details: {exc}")

    finally:
        db.close()
