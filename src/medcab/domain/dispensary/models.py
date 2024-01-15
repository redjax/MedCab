from datetime import date, datetime, timedelta
from typing import Union
import uuid

from loguru import logger as log
from red_utils.ext.sqlalchemy_utils import Base
from red_utils.ext.sqlalchemy_utils.custom_types import CompatibleUUID
import sqlalchemy as sa
from sqlalchemy import Column, ForeignKey,  Table
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy.sql import func

class DispensaryModel(Base):
    __tablename__ = "dispensary"
    
    type_annotation_map = {uuid.UUID: CompatibleUUID}
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, insert_default=uuid.uuid4)
    
    favorite: Mapped[bool] = mapped_column(sa.Boolean, index=True)
    name: Mapped[str] = mapped_column(sa.String)
    city: Mapped[str] = mapped_column(sa.String)
    state: Mapped[str] = mapped_column(sa.String)
