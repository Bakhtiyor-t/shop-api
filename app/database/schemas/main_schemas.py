from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class MainBase(BaseModel):
    pass


class Period(MainBase):
    from_date: Optional[datetime] = datetime.now() - timedelta(days=7)
    to_date: Optional[datetime] = datetime.now() + timedelta(days=7)


class Report(BaseModel):
    profit: Decimal
    income: Decimal
    expense: Decimal
    debt: Decimal
