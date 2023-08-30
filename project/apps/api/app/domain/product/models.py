from typing import Any, Optional, List

import uuid

from datetime import datetime, timedelta

from red_utils.sqlalchemy_utils import Base
import sqlalchemy as sa
from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped, mapped_column
from red_utils.sqlalchemy_utils.custom_types import CompatibleUUID


class ProductModel(Base):
    __tablename__ = "product"

    # type_annotation_map = {uuid.UUID: CompatibleUUID}

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, index=True)
    strain: Mapped[str] = mapped_column(sa.String, index=True)
    favorite: Mapped[bool] = mapped_column(sa.Boolean, index=True)
    weight: Mapped[float] = mapped_column(sa.Float)
    purchaseDate: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )
    dispensary: Mapped[str] = mapped_column(sa.String)
    brand: Mapped[str] = mapped_column(sa.String, index=True)
    manufacturer: Mapped[str] = mapped_column(sa.String)
    harvestDate: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    expirationDate: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    testedDate: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    packageDate: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    batchNumber: Mapped[str] = mapped_column(sa.String)
    form: Mapped[str] = mapped_column(sa.String, index=True)
