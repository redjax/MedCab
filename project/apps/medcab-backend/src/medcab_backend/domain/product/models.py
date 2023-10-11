from red_utils.ext.sqlalchemy_utils import Base

from typing import Any, Optional, List

import uuid

import pendulum
from pendulum.datetime import DateTime, Date, Time
from pendulum.time import timedelta

from red_utils.ext.sqlalchemy_utils.custom_types import CompatibleUUID

import sqlalchemy as sa
from sqlalchemy.sql import func

from sqlalchemy.orm import Session, Mapped, mapped_column, relationship

from decimal import Decimal

from loguru import logger as log


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
