from typing import Union
from decimal import Decimal

from domain.product import Product
from domain.dispensary import Dispensary

from typing import Union
import uuid

import pendulum
from core.validators.product import VALID_FAMILIES, VALID_FORMS
from loguru import logger as log
from pydantic import BaseModel, Field, ValidationError, field_validator, computed_field, ConfigDict

class PurchaseBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    date: Union[str, pendulum.Date] = Field(default=None)
    dispensary: Dispensary | None = Field(default=None)
    product: Product = Field(default=None)
    price: Decimal = Field(default=0.0, max_digits=5, decimal_places=3)
    
    @field_validator("date")
    def validate_date(cls, v) -> pendulum.Date:
        if isinstance(v, pendulum.Date):
            return v
        else:
            try:
                v: pendulum.Date = pendulum.from_format(v, "YYYY-MM-DD")
                return v
            except Exception as exc:
                raise ValidationError

class PurchaseCreate(PurchaseBase):
    id: uuid.UUID

    # class Config:
    #     from_attributes = True


class PurchaseUpdate(PurchaseBase):
    id: uuid.UUID | None = None
    date: Union[str, pendulum.Date] | None = None
    dispensary: Dispensary | None = None
    product: Product | None = None
    price: Decimal | None = None

    # weight: float | None = None
    # favorite: bool | None = None
    # purchaseDate: date | None = None
    # dispensary: str | None = None
    # brand: str | None = None
    # manufacturer: str | None = None
    # harvestDate: date | None = None
    # expirationDate: date | None = None
    # testedDate: date | None = None
    # packageDate: date | None = None
    # batchNumber: str | None = None

    # cannabinoids: CannabinoidList | None = None
    # terpenes: list[Terpene] | None = None
    # notes: list[ProductNote] | None = None
    # images: list[ProductImage] | None = None

    # class Config:
    #     from_attributes = True

class Purchase(PurchaseBase):
    pass

