from decimal import Decimal

from fastapi import Depends

from app.database.schemas.main_schemas import Period, Result
from app.services.cash_box_service import CashBoxService
from app.services.expences_service import ExpenseService
from app.services.frims_service import FirmsService


class MainService:

    def __init__(
            self,
            firm_service: FirmsService = Depends(),
            expenses_service: ExpenseService = Depends(),
            cash_box_service: CashBoxService = Depends()
    ):
        self.firm_service = firm_service
        self.expenses_service = expenses_service
        self.cash_box_service = cash_box_service

    def get_info(self, user_id: int, period: Period) -> Result:
        firms = self.firm_service.get_firms(user_id, period)
        expenses = self.expenses_service.get_expenses(user_id, period)
        cash_box = self.cash_box_service.get_info(user_id, period)

        total_paid = Decimal(0)
        total_debt = Decimal(0)
        total_expenses = Decimal(0)
        total_income = Decimal(0)

        for item in firms:
            total_paid += item.paid_for
            total_debt += item.debt

        for item in expenses:
            if not item.firm_flag:
                total_expenses += item.price

        for item in cash_box:
            item_income = item.cash + item.card
            total_income += item_income
            # total_debt -= item_income

        profit = total_income - total_paid - total_expenses
        income = total_income
        expense = total_paid + total_expenses
        debt = total_debt - total_paid

        return Result(
            profit=profit,
            income=income,
            expense=expense,
            debt=debt
        )

