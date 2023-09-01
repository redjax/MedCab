from typing import Any, Optional, List

import uuid

from datetime import datetime, date, timedelta

from red_utils.sqlalchemy_utils import Base
from red_utils.sqlalchemy_utils.custom_types import CompatibleUUID
import sqlalchemy as sa
from sqlalchemy.sql import func

from sqlalchemy.orm import Session, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column
from red_utils.sqlalchemy_utils.custom_types import CompatibleUUID

from loguru import logger as log


## Association tables for relationship joins
#  https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many
product_terpene_table = Table(
    "product_terpene",
    Base.metadata,
    ## Bi-directional key many-to-many
    #  https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#setting-bi-directional-many-to-many
    Column("product_id", ForeignKey("product.id"), primary_key=True),
    Column("terpene_id", ForeignKey("terpene.id"), primary_key=True),
)


class ProductModel(Base):
    __tablename__ = "product"

    type_annotation_map = {uuid.UUID: CompatibleUUID}

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, insert_default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(sa.String, index=True)
    strain: Mapped[str] = mapped_column(sa.String, index=True)
    favorite: Mapped[bool] = mapped_column(sa.Boolean, index=True)
    weight: Mapped[float] = mapped_column(
        sa.Float(asdecimal=True, decimal_return_scale=4)
    )
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

    ## Relationships
    #  https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many
    terpenes: Mapped[Optional[List["TerpeneModel"]]] = relationship(
        secondary=product_terpene_table,
        back_populates="products",
        lazy="joined",
        cascade="all",
    )


class TerpeneModel(Base):
    __tablename__ = "terpene"

    type_annotation_map = {uuid.UUID: CompatibleUUID}

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, insert_default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(sa.String)
    content: Mapped[float] = mapped_column(
        sa.Float(precision=3, asdecimal=True, decimal_return_scale=4)
    )

    ## Relationships
    products: Mapped[List["ProductModel"]] = relationship(
        secondary=product_terpene_table, back_populates="terpenes"
    )
