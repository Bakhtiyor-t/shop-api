from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.expenses_schemas import ExpenseCreate, ExpenseUpdate, Expense
from app.database.schemas.firms_schemas import Finance
from app.database.schemas.main_schemas import Period
from app.services.dublicated_operations import check_user, get
from app.services.finance_service import FinanceService
from app.utils import validator


class ExpenseService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.finance_service = FinanceService(session)

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
        user = check_user(self.session, user_id)
        # TODO если id сделать str то if, else не нужен
        if expense_data.firm_id:
            expense_data.firm_flag = True
            data = expense_data.dict()
            validator.is_none_check(
                self.session.query(tables.Firm).get(expense_data.firm_id)
            )
        else:
            data = expense_data.dict(exclude={"firm_id"})

        expense = tables.Expense(
            **data,
            user_id=user_id,
            company_id=user.company_id,
        )

        self.session.add(expense)
        self.session.commit()
        self.session.refresh(expense)
        if expense.firm_id:
            finance = self.get_finance(expense)
            self.finance_service.create_finance(data=finance, expense=True)
        return expense

    def update_expense(
            self,
            user_id: int,
            expense_id: int,
            expense_data: ExpenseUpdate,
    ) -> tables.Expense:
        check_user(self.session, user_id)
        expense = (
            self.session
                .query(tables.Expense)
                .filter_by(id=expense_id)
                .first()
        )
        validator.is_none_check(expense)
        prev_finance = None
        if expense.firm_id:
            prev_finance = self.get_finance(expense)

        for field, value in expense_data:
            setattr(expense, field, value)
        self.session.commit()
        self.session.refresh(expense)

        if expense.firm_id:
            finance = self.get_finance(expense)
            self.finance_service.update_finance(
                data=finance,
                prev_data=prev_finance,
                expense=True
            )
        return expense

    def delete_expense(
            self,
            user_id: int,
            expense_id: int,
    ) -> None:
        check_user(self.session, user_id)
        expense = (
            self.session
                .query(tables.Expense)
                .filter_by(id=expense_id)
                .first()
        )
        validator.is_none_check(expense)
        if expense.firm_id:
            finance = self.get_finance(expense)
            self.finance_service.delete_finance(data=finance, expense=True)
        self.session.delete(expense)
        self.session.commit()

    def get_finance(self, expense: Expense) -> Finance:
        print(expense.firm_id)
        return Finance(
            paid=expense.price,
            debt=expense.price,
            user_id=expense.user_id,
            firm_id=expense.firm_id,
            company_id=expense.company_id
        )

    # Finance operations

    # def get_finance(
    #         self,
    #         user_id: int,
    #         firm_id: int
    # ) -> tables.FirmFinance:
    #     user = check_user(self.session, user_id)
    #     return (
    #         self.session
    #             .query(tables.FirmFinance)
    #             .filter_by(firm_id=firm_id, company_id=user.company_id)
    #             .order_by(desc(tables.FirmFinance.date))
    #             .first()
    #     )
    #
    # def create_finance(self, expense: tables.Expense) -> None:
    #     finances = self.get_finance(expense.user_id, expense.firm_id)
    #     paid_for = finances.paid_for + expense.price
    #     debt = finances.debt - expense.price
    #     set_finance(
    #         session=self.session,
    #         paid_for=paid_for,
    #         debt=debt,
    #         firm_id=expense.firm_id,
    #         company_id=expense.company_id
    #     )
    #
    # def update_finance(
    #         self,
    #         expense: tables.Expense,
    #         prev_expense: Decimal
    # ) -> None:
    #     finance = self.get_finance(expense.user_id, expense.firm_id)
    #     paid_for = finance.paid_for + (expense.price - prev_expense)
    #     debt = finance.debt + (expense.price - prev_expense)
    #     set_finance(
    #         session=self.session,
    #         paid_for=paid_for,
    #         debt=debt,
    #         firm_id=expense.firm_id,
    #         company_id=expense.company_id
    #     )
    #
    # def delete_finance(self, expense: tables.Expense) -> None:
    #     finance = self.get_finance(expense.user_id, expense.firm_id)
    #     paid_for = finance.paid_for - expense.price
    #     debt = finance.debt + expense.price
    #     set_finance(
    #         session=self.session,
    #         paid_for=paid_for,
    #         debt=debt,
    #         firm_id=expense.firm_id,
    #         company_id=expense.company_id
    #     )
