
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    category: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    stock: int = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)



class ProductListResponse(BaseModel):
    total: int
    page: int
    limit: int
    products: list[ProductResponse]
    
    

class ProductPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    category: str | None = Field(default=None, min_length=1, max_length=100)
    price: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2
    )
    stock: int | None = Field(default=None, ge=0)

