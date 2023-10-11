from __future__ import annotations

from decimal import Decimal
from typing import Any, List, Optional
import uuid

from loguru import logger as log
import pendulum

from pendulum.datetime import Date, DateTime, Time
from pendulum.time import timedelta
from red_utils.ext.sqlalchemy_utils import Base
from red_utils.ext.sqlalchemy_utils.custom_types import CompatibleUUID
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy.sql import func

class ProductModel(Base):
    __tablename__ = "product"

    type_annotation_map = {uuid.UUID: CompatibleUUID}

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, insert_default=uuid.uuid4
    )

    favorite: Mapped[bool] = mapped_column(sa.Boolean, index=True, default=False)
    strain: Mapped[str] = mapped_column(sa.String, index=True)
    family: Mapped[str] = mapped_column(sa.String, index=True)
    form: Mapped[str] = mapped_column(sa.String, index=True)
    total_thc: Mapped[Decimal | None] = mapped_column(
        sa.Numeric(precision=3), default=0.0
    )
    total_cbd: Mapped[Decimal | None] = mapped_column(
        sa.Numeric(precision=3), default=0.0
    )
