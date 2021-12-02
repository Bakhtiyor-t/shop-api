from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class FirmBase(BaseModel):
    name: str
    paid_for: Decimal
    debt: Decimal


class Firm(FirmBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class FirmCreate(FirmBase):
    pass


# class FirmUpdate(BaseModel):
#     name: str


class InvoiceBase(BaseModel):
    image_id: int
    image_uri: str
    paid_for: Decimal
    payment: Decimal
    previous_debt: Decimal
    debt: Decimal
    date = date


class Invoice(InvoiceBase):
    id: int
    firm_id: int
    user_id: int

    class Config:
        orm_mode = True


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(InvoiceBase):
    pass
