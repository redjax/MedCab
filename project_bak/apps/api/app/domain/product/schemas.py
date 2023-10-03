from typing import Optional, Any, Union
import uuid
import arrow
from pathlib import Path
from datetime import date, datetime, time

from pydantic import BaseModel, Field, validator, ValidationError
from loguru import logger as log

from constants import valid_forms, valid_families

from decimal import Decimal

# from .models import ProductModel, TerpeneModel


class ProductBase(BaseModel):
    strain: str = Field(default=None)
    family: str = Field(default=None)
    form: Optional[str] = Field(default=None)
    total_thc: Decimal = Field(default=0.0, max_digits=5, decimal_places=3)
    total_cbd: Decimal = Field(default=0.0, max_digits=5, decimal_places=3)

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

    # @validator("batchNumber")
    # def validate_batch_number(cls, v) -> str:
    #     if v:
    #         if len(v) > 24:
    #             raise ValidationError

    #     return v

    # class Meta:
    #     orm_model = ProductModel


class ProductCreate(ProductBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ProductUpdate(ProductBase):
    id: uuid.UUID | None = None
    strain: str | None = None
    family: str | None = None
    form: str | None = None

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

    class Config:
        from_attributes = True


class Product(ProductBase):
    pass
