from loguru import logger as log
from sqlalchemy.engine import Row


def convert_sqla_rows_to_dicts(rows: list[Row] = None) -> list[dict]:
    """Convert a list of SQLAlchemy Row results into a list of dict objects."""
    if rows is None:
        raise ValueError("Missing list of SQLAlchemy Row objects")

    try:
        db_product_dicts: list[dict] = [dict(row._asdict()) for row in rows]
        
        return db_product_dicts
    
    except Exception as exc:
        msg = Exception(f"Unhandled exception converting Row objects to dicts. Details: {exc}")
        log.error(msg)
        
        raise msg