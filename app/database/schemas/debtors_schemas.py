from decimal import Decimal

from pydantic import BaseModel


class DebtorBase(BaseModel):
    name: str
    paid: Decimal
    debt: Decimal


class Debtor(DebtorBase):
    id: int
    user_id: int
    company_id: int

    class Config:
        orm_mode = True


class DebtorCreate(DebtorBase):
    pass


class DebtorUpdate(DebtorBase):
    pass
