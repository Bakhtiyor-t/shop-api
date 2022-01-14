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
from app.services.dublicated_operations import check_user, get, set_finance
from app.utils import validator


class ExpenseService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_expenses(self, user_id: int, period: Period) -> List[tables.Expense]:
        return get(
            session=self.session,
            table=tables.Expense,
            user_id=user_id,
            period=period
        )

    def create_expense(
            self,
            user_id: int,
            expense_data: ExpenseCreate,
    ) -> tables.Expense:
        company_id = check_user(self.session, user_id)
        if expense_data.firm_id:
            data = expense_data.dict()
            expense_data.firm_flag = True
            validator.is_none_check(
                self.session.query(tables.Firm).get(expense_data.firm_id)
            )
        else:
            data = expense_data.dict(exclude={"firm_id"})

        expense = tables.Expense(
            **data,
            user_id=user_id,
            company_id=company_id,
        )

        self.session.add(expense)
        self.session.commit()
        self.session.refresh(expense)
        if expense_data.firm_id:
            self.create_finance(expense)
        return expense

    def update_expense(
            self,
            user_id: int,
            expense_id: int,
            expense_data: ExpenseUpdate,
    ) -> tables.Expense:
        company_id = check_user(self.session, user_id)
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
            user_id: int,
            expense_id: int,
    ) -> None:
        company_id = check_user(self.session, user_id)
        expense = (
            self.session
                .query(tables.Expense)
                .filter_by(id=expense_id)
                .first()
        )
        validator.is_none_check(expense)
        if expense.firm_id:
            self.delete_finance(expense)
        self.session.delete(expense)
        self.session.commit()

    # Finance operations

    def get_finance(self, user_id: int, firm_id: int) -> tables.FinanceHistory:
        company_id = check_user(self.session, user_id)
        return (
            self.session
                .query(tables.FinanceHistory)
                .filter_by(firm_id=firm_id, company_id=company_id)
                .order_by(desc(tables.FinanceHistory.date))
                .first()
        )

    def create_finance(self, expense: tables.Expense) -> None:
        company_id = check_user(self.session, expense.user_id)
        finance = self.get_finance(expense.user_id, expense.firm_id)
        paid_for = finance.paid_for + expense.price
        debt = finance.debt - expense.price
        self.set_finance(paid_for, debt, expense.user_id, expense.firm_id)

    def update_finance(
            self,
            expense: tables.Expense,
            prev_expense: Decimal
    ) -> None:
        finance = self.get_finance(expense.user_id, expense.firm_id)
        paid_for = finance.paid_for + (expense.price - prev_expense)
        debt = finance.debt + (expense.price - prev_expense)
        self.set_finance(paid_for, debt, expense.user_id, expense.firm_id)

    def set_finance(
            self,
            paid_for: Decimal,
            debt: Decimal,
            user_id: int,
            firm_id: int,
    ) -> None:
        set_finance(
            session=self.session,
            paid_for=paid_for,
            debt=debt,
            user_id=user_id,
            firm_id=firm_id
        )

    def delete_finance(self, expense: tables.Expense) -> None:
        finance = self.get_finance(expense.user_id, expense.firm_id)
        paid_for = finance.paid_for - expense.price
        debt = finance.debt + expense.price
        self.set_finance(paid_for, debt, expense.user_id, expense.firm_id)
