from decimal import Decimal

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    count: float
    price: Decimal
    total_price: Decimal
    # для ед.езмерения пример (кг или шт)
    type: str
    # в дальнейшем можно сделать перечисление
    # type: # Enum


class Product(ProductBase):
    id: str
    company_id: str
    user_id: str

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass
