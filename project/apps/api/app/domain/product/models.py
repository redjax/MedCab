from typing import Any, Optional, List

import uuid

from datetime import datetime, date, timedelta

from red_utils.sqlalchemy_utils import Base
from red_utils.sqlalchemy_utils.custom_types import CompatibleUUID
import sqlalchemy as sa
from sqlalchemy.sql import func

from sqlalchemy.orm import Session, Mapped, mapped_column
from red_utils.sqlalchemy_utils.custom_types import CompatibleUUID

from loguru import logger as log


class ProductModel(Base):
    __tablename__ = "product"

    type_annotation_map = {uuid.UUID: CompatibleUUID}

    # id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, insert_default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(sa.String, index=True)
    strain: Mapped[str] = mapped_column(sa.String, index=True)
    favorite: Mapped[bool] = mapped_column(sa.Boolean, index=True)
    weight: Mapped[float] = mapped_column(sa.Float)
    purchaseDate: Mapped[date] = mapped_column(sa.Date, nullable=True)
    dispensary: Mapped[str] = mapped_column(sa.String)
    brand: Mapped[str] = mapped_column(sa.String, index=True)
    manufacturer: Mapped[str] = mapped_column(sa.String)
    harvestDate: Mapped[date] = mapped_column(sa.Date)
    expirationDate: Mapped[date] = mapped_column(sa.Date)
    testedDate: Mapped[date] = mapped_column(sa.Date)
    packageDate: Mapped[date] = mapped_column(sa.Date)
    batchNumber: Mapped[str] = mapped_column(sa.String)
    form: Mapped[str] = mapped_column(sa.String, index=True)
