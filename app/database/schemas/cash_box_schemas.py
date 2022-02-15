from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CashBoxBase(BaseModel):

    cash: Decimal
    card: Decimal
    date: datetime = datetime.utcnow()


class CashBox(CashBoxBase):
    id: int
    user_id: int
    company_id: int

    class Config:
        orm_mode = True


class CashBoxCreate(CashBoxBase):
    pass


class CashBoxUpdate(CashBoxBase):
    pass
