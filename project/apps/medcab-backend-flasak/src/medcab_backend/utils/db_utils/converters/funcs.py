from sqlalchemy.engine.row import Row, RowMapping

row_to_dict = lambda row: {
    col.name: str(getattr(row, col.name)) for col in row.__table__.columns
}


def convert_row_to_dict(row: RowMapping = None) -> dict:
    """Convert a SQLAlchemy Row/RowMapping to a dict."""
    if not isinstance(row, RowMapping):
        raise TypeError(
            f"Invalid type for row: ({type(row)}). Must be of type sqlalchemy.engine.row.RowMapping"
        )

    try:
        row_dict: dict = row_to_dict(row=row)

        return row_dict

    except Exception as exc:
        raise Exception(
            f"Unhandled exception converting SQLAlchemy Row to dict. Details: {exc}"
        )
