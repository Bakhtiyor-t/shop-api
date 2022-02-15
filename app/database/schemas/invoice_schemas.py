from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from app.database.schemas.products_schemas import Product, ProductCreate, ProductUpdate


class InvoiceBase(BaseModel):
    to_pay: Decimal
    paid: Decimal
    previous_debt: Decimal
    debt: Decimal
    date: datetime = datetime.utcnow()


class BasicInvoice(InvoiceBase):
    id: int
    firm_id: int
    user_id: int
    company_id: int


class Invoice(BasicInvoice):
    products: List[Product]

    class Config:
        orm_mode = True


class InvoiceCreate(InvoiceBase):
    products: List[ProductCreate]


class InvoiceUpdate(InvoiceBase):
    products: List[ProductUpdate]


class InvoiceWithImage(BasicInvoice):
    image_id: str
    image_uri: str

    class Config:
        orm_mode = True


class InvoiceCreateWithImage(InvoiceBase):
    pass


class InvoiceUpdateWithImage(InvoiceBase):
    pass


class GeneralInvoice(BasicInvoice):
    products: Optional[List[Product]] = None
    image_id: Optional[str] = None
    image_uri: Optional[str] = None

    class Config:
        orm_mode = True
