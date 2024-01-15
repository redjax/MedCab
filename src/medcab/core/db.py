from __future__ import annotations

from typing import Union

from .dependencies import APP_SETTINGS, DB_SETTINGS

from core import DBSettings
from loguru import logger as log
from red_utils.ext import sqlalchemy_utils as sa_utils
from red_utils.ext.sqlalchemy_utils import validate_db_type
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

def get_db_connection_class(db_settings: DBSettings = DB_SETTINGS):
    assert db_settings is not None, ValueError("db_settings cannot be None")

    match db_settings.type:
        case "sqlite":
            DB_CONN: sa_utils.saSQLiteConnection = sa_utils.saSQLiteConnection(
                database=DB_SETTINGS.database
            )
        case _:
            raise NotImplementedError(
                f"Support for database type '{db_settings.type}' not implemented."
            )

    return DB_CONN


def get_db_engine(
    db_conn: Union[
        sa_utils.saSQLiteConnection,
        sa_utils.saPGConnection,
        sa_utils.saConnectionGeneric,
    ] = None
) -> sa.Engine:
    assert db_conn is not None, ValueError("db_conn cannot be None")
    assert (
        isinstance(db_conn, sa_utils.saSQLiteConnection)
        or isinstance(db_conn, sa_utils.saPGConnection)
        or isinstance(db_conn, sa_utils.saConnectionGeneric)
    ), TypeError(
        f"db_conn must be one of [saSQLiteConnection, saPGConnection, or saConnectionGeneric], not ({type(db_conn)})"
    )

    if isinstance(db_conn, sa_utils.saSQLiteConnection):
        db_type: str = "sqlite"
    else:
        raise NotImplementedError(f"This database type is not yet implemented.")

    try:
        engine: sa.Engine = sa_utils.get_engine(db_conn, db_type=db_type)
        log.success(f"SQLAlchemy engine inintialized")

        return engine
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting SQLAlchemy database engine. Details: {exc}"
        )
        log.error(msg)

        return msg


def get_db_session(
    engine: sa.Engine = None, autoflush: bool = False, expire_on_commit: bool = False
) -> sessionmaker[Session]:
    assert engine is not None, ValueError("engine cannot be None")
    assert isinstance(engine, sa.Engine), TypeError(
        f"engine must be of type sqlalchemy.Engine, not ({type(engine)})"
    )

    try:
        session: sessionmaker[Session] = sa_utils.get_session(
            engine=engine, autoflush=autoflush, expire_on_commit=expire_on_commit
        )

        return session
    except Exception as exc:
        msg = Exception(f"Unhandled exception getting database session. Details: {exc}")
        log.error(msg)

        raise msg


def init_base_metadata(
    engine: sa.Engine = None, sqla_base: DeclarativeBase = sa_utils.Base
):
    session = get_db_session(engine=engine)
    log.debug(f"Session ({type(session)}): {session}")

    log.info(f"Creating Base metadata")
    try:
        sa_utils.create_base_metadata(base_obj=sqla_base, engine=engine)
        log.success("Base metadata created successfully")
    except Exception as exc:
        msg = Exception(f"Unhandled exception creating Base metadata. Details: {exc}")
        log.error(msg)

        raise msg
