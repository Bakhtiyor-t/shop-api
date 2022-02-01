from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class FirmBase(BaseModel):
    name: str


class FirmBasic(FirmBase):
    id: int
    user_id: int
    company_id: int

    class Config:
        orm_mode = True


class FirmFinance(BaseModel):
    paid: Optional[Decimal] = Decimal(0)
    debt: Optional[Decimal] = Decimal(0)
    date: Optional[datetime] = None

    class Config:
        orm_mode = True


class Firm(FirmBasic, FirmFinance):
    pass


class FirmCreate(FirmBase, FirmFinance):
    pass


class FirmUpdate(FirmBase):
    pass


class InvoiceBase(BaseModel):
    to_pay: Decimal
    paid: Decimal
    previous_debt: Decimal
    debt: Decimal
    date: datetime = datetime.utcnow()


class Invoice(InvoiceBase):
    id: int
    firm_id: int
    user_id: int
    company_id: int

    image_id: int
    image_uri: str

    class Config:
        orm_mode = True


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(InvoiceBase):
    pass


class Finance(FirmFinance):
    user_id: int
    firm_id: int
    company_id: int
