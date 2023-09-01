from typing import Union, Optional
from datetime import date
import uuid

from pydantic import BaseModel, Field, validator, ValidationError

from constants import valid_forms, valid_strains


from .schemas import Terpene


class ProductBase(BaseModel):
    name: str = Field(default=None)
    strain: str = Field(default=None)
    favorite: Optional[bool] = Field(default=False)
    weight: float = Field(default=0.0)
    purchaseDate: Optional[date] = Field(default=None)
    dispensary: Optional[str] = Field(default=None)
    brand: Optional[str] = Field(default=None)
    manufacturer: Optional[str] = Field(default=None)
    harvestDate: Optional[date] = Field(default=None)
    expirationDate: Optional[date] = Field(default=None)
    testedDate: Optional[date] = Field(default=None)
    packageDate: Optional[date] = Field(default=None)
    batchNumber: Optional[str] = Field(default=None)
    form: Optional[str] = Field(default=None)
    # cannabinoids: Optional[CannabinoidList] = Field(default=None)
    terpenes: Optional[list[Terpene]] = Field(default=None)
    # notes: Optional[list[ProductNote]] = None
    # images: Optional[list[ProductImage]] = None

    @validator("strain")
    def validate_strain(cls, v) -> str:
        if not v:
            return None

        if not v in valid_strains:
            raise ValidationError

        return v

    @validator("form")
    def validate_form(cls, v) -> str:
        if not v:
            return None

        if not v in valid_forms:
            raise ValidationError

        return v

    @validator("batchNumber")
    def validate_batch_number(cls, v) -> str:
        if v:
            if len(v) > 24:
                raise ValidationError

        return v

    # class Meta:
    #     orm_model = ProductModel


class ProductCreate(ProductBase):
    # id: int
    id: uuid.UUID

    class Config:
        from_attributes = True


class Product(ProductBase):
    pass


class ProductUpdate(ProductBase):
    # id: int | None = None
    id: uuid.UUID | None = None
    name: str | None = None
    strain: str | None = None
    favorite: bool | None = None
    weight: float | None = None
    purchaseDate: date | None = None
    dispensary: str | None = None
    brand: str | None = None
    manufacturer: str | None = None
    harvestDate: date | None = None
    expirationDate: date | None = None
    testedDate: date | None = None
    packageDate: date | None = None
    batchNumber: str | None = None
    form: str | None = None
    # cannabinoids: CannabinoidList | None = None
    # terpenes: list[Terpene] | None = None
    # notes: list[ProductNote] | None = None
    # images: list[ProductImage] | None = None

    class Config:
        from_attributes = True
