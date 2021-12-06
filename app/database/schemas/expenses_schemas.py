from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ExpenseBase(BaseModel):
    name: str
    price: Decimal
    date: datetime = datetime.now()
    firm_flag: bool = False


class Expense(ExpenseBase):
    id: int
    user_id: int
    firm_id: Optional[int] = None

    class Config:
        orm_mode = True


class ExpenseCreate(ExpenseBase):
    firm_id: Optional[int] = None


class ExpenseUpdate(ExpenseBase):
    pass
