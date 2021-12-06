from datetime import datetime
from decimal import Decimal
from typing import List

from fastapi import Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.expenses_schemas import ExpenseCreate, ExpenseUpdate
from app.database.schemas.firms_schemas import FirmFinance
from app.database.schemas.main_schemas import Period
from app.utils import validator


class ExpenseService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_expenses(self, user_id: int, period: Period) -> List[tables.Expense]:
        expenses = (
            self.session
                .query(tables.Expense)
                .filter_by(user_id=user_id)
                .where(tables.Expense.date >= period.from_date)
                .where(tables.Expense.date < period.to_date)
                .order_by(desc(tables.Expense.date))
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
        if expense_data.firm_id:
            expense.firm_flag = True
        self.session.add(expense)
        self.session.commit()
        self.session.refresh(expense)
        self.create_finance(expense)
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
        prev_expense = expense.price
        for field, value in expense_data:
            setattr(expense, field, value)
        self.session.commit()
        self.session.refresh(expense)
        if expense.firm_flag:
            self.update_finance(expense, prev_expense)
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
        exp = expense
        self.session.delete(expense)
        self.session.commit()
        self.delete_finance(exp)

    # Finance operations

    def get_finance(self, firm_id: int) -> tables.FinanceHistory:
        return (
            self.session
                .query(tables.FinanceHistory)
                .filter_by(firm_id=firm_id)
                .order_by(desc(tables.FinanceHistory.date))
                .first()
        )

    def create_finance(self, expense: tables.Expense) -> None:
        finance = self.get_finance(expense.firm_id)
        paid_for = finance.paid_for + expense.price
        debt = finance.debt - expense.price
        self.set_finance(paid_for, debt, expense.firm_id)

    def update_finance(
            self,
            expense: tables.Expense,
            prev_expense: Decimal
    ) -> None:
        finance = self.get_finance(expense.firm_id)
        paid_for = finance.paid_for + (expense.price - prev_expense)
        debt = finance.debt + (expense.price - prev_expense)
        self.set_finance(paid_for, debt, expense.firm_id)

    def set_finance(
            self,
            paid_for: Decimal,
            debt: Decimal,
            firm_id: int,
    ) -> None:
        data = FirmFinance(paid_for=paid_for, debt=debt, date=datetime.now())
        new_finance = tables.FinanceHistory(
            **data.dict(),
            firm_id=firm_id
        )
        self.session.add(new_finance)
        self.session.commit()
        self.session.refresh(new_finance)

    def delete_finance(self, expense: tables.Expense) -> None:
        finance = self.get_finance(expense.firm_id)
        paid_for = finance.paid_for - expense.price
        debt = finance.debt + expense.price
        self.set_finance(paid_for, debt, expense.firm_id)
