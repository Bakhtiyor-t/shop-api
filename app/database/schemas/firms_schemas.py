from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class Firm(BaseModel):
    id: int
    name: str
    paid_for: Decimal
    debt: Decimal

    class Config:
        orm_mode = True


class Invoice(BaseModel):
    id: int
    firm_id: int
    image_id: int
    image_uri: str
    paid_for: Decimal
    payment: Decimal
    previous_debt: Decimal
    debt: Decimal
    date = date

    class Config:
        orm_mode = True

