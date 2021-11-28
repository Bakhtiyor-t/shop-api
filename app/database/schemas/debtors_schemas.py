from decimal import Decimal

from pydantic import BaseModel


class DebtorBase(BaseModel):
    name: str
    paid_for: Decimal
    debt: Decimal


class Debtor(DebtorBase):
    id: int

    class Config:
        orm_mode = True


class DebtorCreate(DebtorBase):
    pass


class DebtorUpdate(DebtorBase):
    pass
