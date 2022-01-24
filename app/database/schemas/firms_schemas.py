from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel


class FirmBase(BaseModel):
    name: str


class FirmPart(FirmBase):
    id: int
    user_id: int
    company_id: int

    class Config:
        orm_mode = True


class FirmFinance(BaseModel):
    paid_for: Optional[Decimal] = Decimal(0)
    debt: Optional[Decimal] = Decimal(0)
    date: Optional[datetime] = None

    class Config:
        orm_mode = True


class Firm(FirmPart, FirmFinance):
    pass


class FirmCreate(FirmBase, FirmFinance):
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
    date = datetime


class Invoice(InvoiceBase):
    id: int
    firm_id: int
    user_id: int
    company_id: int

    class Config:
        orm_mode = True


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(InvoiceBase):
    pass
