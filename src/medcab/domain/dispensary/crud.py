from __future__ import annotations

import uuid

from .models import DispensaryModel
from .schemas import Dispensary, DispensaryCreate

from core.utils.crud_utils import convert_sqla_rows_to_dicts
from loguru import logger as log
from red_utils.ext.pydantic_utils.parsers import parse_pydantic_schema
from sqlalchemy import func, select
from sqlalchemy.engine import Row
from sqlalchemy.orm import Query, Session

def validate_db(db: Session = None) -> Session:
    if not db:
        raise ValueError("Missing DB Session object")

    if not isinstance(db, Session):
        raise TypeError(
            f"Invalid type for db: ({type(db)}). Must be of type sqlalchemy.orm.Session"
        )

    return db


def validate_dispensary_create(dispensary) -> DispensaryCreate:
    if not dispensary:
        raise ValueError("Missing Dispensary to add to database")

    if not isinstance(dispensary, DispensaryCreate):
        raise TypeError(
            f"Invalid type for Dispensary: ({type(dispensary)}). Must be of type DispensaryCreate"
        )

    return dispensary


def count_dispensary(db: Session = None) -> int:
    try:
        with db as sess:
            dispensary_count = sess.query(func.count(DispensaryModel.id)).scalar()

            return dispensary_count
    except Exception as exc:
        log.error(
            f"Unhandled exception getting count of Dispensaries in database. Details: {exc}"
        )
        return None


def create_dispensary(dispensary: DispensaryCreate = None, db: Session = None) -> DispensaryModel:
    validate_db(db)

    log.debug(f"Dispensary ({type(dispensary)}): {dispensary}")

    with db as sess:
        db_dispensary: DispensaryModel | None = None

        log.debug(f"Building SELECT statement on .name, .city, and .state")
        try:
            db_dispensary_sel = select(DispensaryModel).where(
                DispensaryModel.name == dispensary.name
            )
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception building SELECT Dispensary [{dispensary.name}] statement. Details: {exc}"
            )
            log.error(msg)

        log.debug(f"Executing SELECT DispensaryModel statement")

        try:
            db_dispensaries: list[Row] = sess.execute(db_dispensary_sel).all()

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception executing SELECT statement for Dispensaries [{dispensary.name}]. Details: {exc}"
            )
            log.error(msg)

            raise msg

        if db_dispensaries is not None:
            log.debug(
                f"Results: ({type(db_dispensaries)}) [items:{len(db_dispensaries)}]: {db_dispensaries}"
            )

        if db_dispensaries is None:
            log.debug(f"No matching Dispensaries found for '{dispensary.name}'. Creating.")

            try:
                dump_schema = parse_pydantic_schema(schema=dispensary)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception dumping Pydantic schema. Details: {exc}"
                )
                log.error(msg)

            log.debug(f"Dump schema ({type(dump_schema)}): {dump_schema}")

            try:
                new_dispensary: DispensaryModel = DispensaryModel(**dump_schema)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception convering Dispensary schema to model. Schema ({type(dump_schema)}): {dump_schema}. Details: {exc}"
                )

            try:
                sess.add(new_dispensary)
                sess.commit()

                return new_dispensary

            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception committing Dispensary to database. Details: {exc}"
                )

        else:
            log.debug(
                f"Found [{len(db_dispensaries)}] Dispensary/ies matching name '{dispensary.name}' in the database."
            )
            db_dispensary_dicts: list[dict] = convert_sqla_rows_to_dicts(rows=db_dispensaries)

            log.debug(f"Converted [{len(db_dispensary_dicts)}] Dispensary Row(s) to dict(s)")

            for _dispensary in db_dispensary_dicts:
                d: DispensaryModel = _dispensary["DispensaryModel"]
                log.debug(f"_dispensary ({type(d)}): {d}")
                # log.debug(f"Product:\n\tStrain: {p.strain}\n\tFamily: {p.family}\n\tForm: {p.form}")

                if not d.city == dispensary.city:
                    pass
                else:
                    if not d.state == dispensary.state:
                        pass
                    else:
                        log.debug(
                            f"Dispensary [{dispensary.name}] in city {dispensary.city}, {dispensary.state} already exists"
                        )

                        db_dispensary: DispensaryModel = d

            if db_dispensary is None:
                log.debug(
                    f"Dispensary [{dispensary.name}] in city {dispensary.city}, {dispensary.state} not found in database. Creating."
                )

                try:
                    dump_schema = parse_pydantic_schema(schema=dispensary)
                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception dumping Dispensary schema to dict. Product ({type(dispensary)}): {dispensary}. Details: {exc}"
                    )
                    log.error(msg)

                try:
                    new_dispensary: DispensaryModel = DispensaryModel(**dump_schema)
                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception converting Dispensary schema to model. Schema ({type(dump_schema)}): {dump_schema}. Details: {exc}"
                    )

                try:
                    sess.add(new_dispensary)
                    sess.commit()

                    return new_dispensary

                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception inserting new Dispensary. Product ({type(new_dispensary)}): {new_dispensary}. Details: {exc}"
                    )

            else:
                return db_dispensary


def get_all_dispensaries(db: Session = None) -> list[DispensaryModel]:
    validate_db(db)

    try:
        with db as sess:
            all_dispensaries = sess.query(DispensaryModel).all()

            return all_dispensaries

    except Exception as exc:
        raise Exception(f"Unhandled exception getting all Dispensaries. Details: {exc}")


def get_dispensary_by_id(id: uuid.UUID = None, db: Session = None) -> DispensaryModel:
    try:
        with db as sess:
            db_dispensary = sess.query(DispensaryModel).filter(DispensaryModel.id == id).first()

        return db_dispensary

    except Exception as exc:
        raise Exception(
            f"Unhandled exception retrieving Dispensary by ID: '{id}'. Details: {exc}"
        )


def get_dispensary_by_name(dispensary_name: str = None, db: Session = None) -> DispensaryModel:
    if not dispensary_name:
        raise ValueError("Missing a name to search")

    if not isinstance(dispensary_name, str):
        raise ValueError(
            f"Invalid type for name: {type(dispensary_name)}. Must be of type str"
        )

    try:
        with db as sess:
            db_dispensary = (
                sess.query(DispensaryModel)
                .where(DispensaryModel.name == dispensary_name)
                .first()
            )

            return db_dispensary

    except Exception as exc:
        raise Exception(
            f"Unhandled exception retrieving Dispensary by name '{dispensary_name}'. Details: {exc}"
        )


def get_dispensaries_by_city(
    city: str = None, db: Session = None
) -> list[DispensaryModel]:
    if not city:
        raise ValueError(f"Missing city")

    try:
        with db as sess:
            db_dispensaries: list[DispensaryModel] = (
                sess.query(DispensaryModel).where(DispensaryModel.city == city).all()
            )

            return db_dispensaries

    except Exception as exc:
        raise Exception(
            f"Unhandled exception getting Dispensaries by city. Details: {exc}"
        )


def get_dispensaries_by_state(state: str = None, db: Session = None) -> list[DispensaryModel]:
    if not state:
        raise ValueError(f"Missing state")

    try:
        with db as sess:
            db_dispensaries: list[DispensaryModel] = (
                sess.query(DispensaryModel).where(DispensaryModel.state == state).all()
            )

            return db_dispensaries

    except Exception as exc:
        raise Exception(f"Unhandled exception getting Dispensaries by form. Details: {exc}")


def update_dispensary_by_id(
    id: uuid.UUID = None, dispensary: Dispensary = None, db: Session = None
):
    try:
        with db as sess:
            db_dispensary: Query = (
                sess.query(DispensaryModel).filter(DispensaryModel.id == id).first()
            )

            if not db_dispensary:
                return None

            update_data = dispensary.model_dump(exclude_unset=True)

            sess.query(DispensaryModel).filter(DispensaryModel.id == id).update(
                update_data, synchronize_session=False
            )

            sess.commit()
            sess.refresh(db_dispensary)

        return db_dispensary

    except Exception as exc:
        raise Exception(f"Unhandled exception updating Dispensary by ID. Details: {exc}")


def delete_dispensary_by_id(id: uuid.UUID = None, db: Session = None):
    try:
        with db as sess:
            db_dispensary = sess.query(DispensaryModel).filter(DispensaryModel.id == id).first()

            if not db_dispensary:
                return None

            log.debug(f"Found Dispensary by ID: {id} - {db_dispensary}. Deleting")

            _del = sess.query(DispensaryModel).filter(DispensaryModel.id == id).delete()

            sess.commit()

            return {"success": f"Deleted Dispensary with ID: {id}"}

    except Exception as exc:
        raise Exception(
            f"Unhandled exception deleting Dispensary with ID: {id}. Details: {exc}"
        )


def delete_all_dispensaries(db: Session = None):
    try:
        with db as sess:
            db_dispensaries = sess.query(DispensaryModel).all()

            if not db_dispensaries:
                log.warning(f"No dispensaries in the database")

                return False

            for dispensary in db_dispensaries:
                sess.delete(dispensary)

            sess.commit()

            return db_dispensaries

    except Exception as exc:
        log.error(f"Unhandled exception deleting all Dispensaries. Details: {exc}")
        return False
