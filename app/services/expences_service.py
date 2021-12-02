from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.expenses_schemas import ExpenseCreate, ExpenseUpdate
from app.utils import validator


class ExpenseService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_expenses(self, user_id: int) -> List[tables.Expense]:
        expenses = (
            self.session
                .query(tables.Expense)
                .filter_by(user_id=user_id)
                .all()
        )
        return expenses

    def create_expense(
            self,
            user_id: int,
            expense_data: ExpenseCreate,
    ) -> tables.Expense:
        expense = tables.Expense(
            **expense_data.dict(),
            user_id=user_id,
        )
        self.session.add(expense)
        self.session.commit()
        self.session.refresh(expense)
        return expense

    def update_expense(
            self,
            expense_id: int,
            expense_data: ExpenseUpdate,
    ) -> tables.Expense:
        expense = (
            self.session
                .query(tables.Expense)
                .filter_by(id=expense_id)
                .first()
        )
        validator.is_none_check(expense)
        for field, value in expense_data:
            setattr(expense, field, value)
        self.session.commit()
        self.session.refresh(expense)
        return expense

    def delete_expense(
            self,
            expense_id: int,
    ) -> None:
        expense = (
            self.session
                .query(tables.Expense)
                .filter_by(id=expense_id)
                .first()
        )
        validator.is_none_check(expense)
        self.session.delete(expense)
        self.session.commit()
