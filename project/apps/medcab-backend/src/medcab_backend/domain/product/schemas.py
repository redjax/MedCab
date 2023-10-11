from pydantic import BaseModel, Field, validator, ValidationError
from typing import Union
from decimal import Decimal

import uuid

from .validators import valid_families, valid_forms


class ProductBase(BaseModel):
    favorite: bool = Field(default=False)
    strain: str | None = Field(default=None)
    family: str | None = Field(default=None)
    form: str | None = Field(default=None)
    total_thc: Decimal = Field(default=0.000, max_digits=5, decimal_places=3)
    total_cbd: Decimal = Field(default=0.000, max_digits=5, decimal_places=3)
    # total_thc: Decimal | None = Field(default=0.0, max_digits=5, decimal_places=3)
    # total_cbd: Decimal | None = Field(default=0.0, max_digits=5, decimal_places=3)

    # weight: float = Field(default=0.0)
    # purchaseDate: Optional[date] = Field(default=None)
    # dispensary: Optional[str] = Field(default=None)
    # brand: Optional[str] = Field(default=None)
    # manufacturer: Optional[str] = Field(default=None)
    # harvestDate: Optional[date] = Field(default=None)
    # expirationDate: Optional[date] = Field(default=None)
    # testedDate: Optional[date] = Field(default=None)
    # packageDate: Optional[date] = Field(default=None)
    # batchNumber: Optional[str] = Field(default=None)

    # cannabinoids: Optional[CannabinoidList] = Field(default=None)
    # terpenes: Optional[list[Terpene]] = []
    # notes: Optional[list[ProductNote]] = None
    # images: Optional[list[ProductImage]] = None

    class Config:
        validate_assignment = True

    @validator("family")
    def validate_strain(cls, v) -> str:
        if not v:
            return None

        if not v in valid_families:
            raise ValidationError

        return v

    @validator("form")
    def validate_form(cls, v) -> str:
        if not v:
            return None

        if not v in valid_forms:
            raise ValidationError

        return v

    @validator("total_thc")
    def validate_total_thc(cls, v) -> Decimal:
        return v or Decimal(0.0)

    @validator("total_cbd")
    def validate_total_cbd(cls, v) -> Decimal:
        return v or Decimal(0.0)


class ProductCreate(ProductBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ProductResponse(ProductBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class Product(ProductBase):
    pass
