from pydantic import BaseModel, Field, validator, ValidationError
from typing import Union
from decimal import Decimal

from .validators import valid_families, valid_forms


class ProductBase(BaseModel):
    strain: str | None = Field(default=None)
    family: str | None = Field(default=None)
    form: str | None = Field(default=None)
    total_thc: Decimal = Field(default=0.0, max_digits=5, decimal_places=3)
    total_cbd: Decimal = Field(default=0.0, max_digits=5, decimal_places=3)
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


class Product(ProductBase):
    pass
