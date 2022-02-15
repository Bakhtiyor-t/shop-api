from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ExpenseBase(BaseModel):
    name: str
    price: Decimal
    date: datetime = datetime.now()


class ExpensePart(BaseModel):
    firm_id: Optional[int] = None
    firm_flag: Optional[bool] = False


class Expense(ExpenseBase, ExpensePart):
    id: int
    user_id: int
    company_id: int

    class Config:
        orm_mode = True


class ExpenseCreate(ExpenseBase, ExpensePart):
    pass


class ExpenseUpdate(ExpenseBase):
    pass
