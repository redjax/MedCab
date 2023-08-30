from typing import Optional, Any, Union
import arrow
from pathlib import Path
from datetime import date, datetime, time

from pydantic import BaseModel, Field, validator, ValidationError
from loguru import logger as log

from constants import valid_forms, valid_strains


class CannabinoidTerpeneBase(BaseModel):
    name: str = Field(default=None)
    content: float = Field(default=0.0)


class CannabinoidCreate(CannabinoidTerpeneBase):
    id: int

    class Config:
        from_attributes = True


class Cannabinoid(CannabinoidTerpeneBase):
    pass


class CannabinoidUpdate(CannabinoidTerpeneBase):
    id: int | None = None
    name: str | None = None
    content: float | None = None

    class Config:
        from_attributes = True


class CannabinoidOtherCreate(CannabinoidTerpeneBase):
    id: int

    class Config:
        from_attributes = True


class CannabinoidOther(CannabinoidTerpeneBase):
    note: str = Field(default=None)


class CannabinoidUpdate(CannabinoidTerpeneBase):
    id: int | None = None
    name: str | None = None
    content: float | None = None
    note: str | None = None

    class Config:
        from_attributes = True


class CannabinoidListBase(BaseModel):
    items: list[Cannabinoid] = []


class CannabinoidList(CannabinoidListBase):
    pass


class TerpeneBase(CannabinoidTerpeneBase):
    name: str = Field(default=None)
    content: float = Field(default=0.0)


class TerpeneCreate(CannabinoidTerpeneBase):
    id: int

    class Config:
        from_attributes = True


class Terpene(TerpeneBase):
    pass


class TerpeneUpdate(TerpeneBase):
    id: int | None = None
    name: str | None = None
    content: float | None = None


class ProductNoteBase(BaseModel):
    date: datetime = Field(default=datetime.now)
    message: str = Field(default=None)


class ProductNoteCreate(ProductNoteBase):
    id: int

    class Config:
        from_attributes = True


class ProductNote(ProductNoteBase):
    pass


class ProductNoteUpdate(ProductNoteBase):
    id: int | None = None
    date: datetime | None = None
    content: float | None = None

    class Config:
        from_attributes = True


class ProductImageBase(BaseModel):
    imageId: int = None


class ProductImageCreate(ProductImageBase):
    id: int

    class Config:
        from_attributes = True


class ProductImage(ProductImageBase):
    pass


class ProductImateUpdate(ProductImageBase):
    id: int | None = None
    imageId: int | None = None


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
    # terpenes: Optional[list[Terpene]] = Field(default=None)
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


class ProductCreate(ProductBase):
    id: int

    class Config:
        from_attributes = True


class Product(ProductBase):
    pass


class ProductUpdate(ProductBase):
    id: int | None = None
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
