from loguru import logger as log

from config import settings
from red_utils.sqlalchemy_utils import (
    get_engine,
    get_session,
    saSQLiteConnection,
    saPGConnection,
    Base,
    create_base_metadata,
)

from constants import db_type, db_host, db_username, db_password, db_port, db_database


log.debug(f"Matching DB Type to: {db_type}")
match db_type:
    case "sqlite":
        log.debug(f"Detected SQLite DB")
        db_config = saSQLiteConnection(database=db_database)
    case "postgres":
        log.debug(f"Detected Postgres DB")
        db_config = saPGConnection(
            host=db_host,
            username=db_username,
            password=db_password,
            database=db_database,
        )
    case _:
        raise Exception(f"Unknown DB_TYPE: {db_type}")

engine = get_engine(connection=db_config, db_type=db_type, echo=True)
SessionLocal = get_session(engine=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    except Exception as exc:
        raise Exception(f"Unhandled exception getting database session. Details: {exc}")

    finally:
        db.close()
