from datetime import datetime
from decimal import Decimal

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database.database import Base
from app.database.models import tables
from app.database.schemas.firms_schemas import FirmFinance, Finance
from app.services.dublicated_operations import check_user


class FinanceService:

    def __init__(self, session: Session):
        self.session = session

    def get_finance(
            self,
            user_id: int,
            firm_id: int
    ) -> tables.FirmFinance:
        user = check_user(self.session, user_id)
        return (
            self.session
                .query(tables.FirmFinance)
                .filter_by(firm_id=firm_id, company_id=user.company_id)
                .order_by(desc(tables.FirmFinance.date))
                .first()
        )

    def set_finance(
            self,
            paid: Decimal,
            debt: Decimal,
            firm_id: int,
            company_id: int
    ):
        data = FirmFinance(paid=paid, debt=debt, date=datetime.now())
        new_finance = tables.FirmFinance(
            **data.dict(),
            firm_id=firm_id,
            company_id=company_id
        )
        self.session.add(new_finance)
        self.session.commit()
        self.session.refresh(new_finance)

    def create_finance(
            self,
            data: Finance,
            expense: bool = False
    ) -> None:
        finance = self.get_finance(data.user_id, data.firm_id)
        paid = finance.paid + data.paid
        if expense:
            debt = finance.debt - data.debt
        else:
            debt = finance.debt + data.debt

        self.set_finance(
            paid=paid,
            debt=debt,
            firm_id=data.firm_id,
            company_id=data.company_id
        )

    def update_finance(
            self,
            data: Finance,
            prev_data: Base,
            expense: bool = False
    ) -> None:
        finance = self.get_finance(data.user_id, data.firm_id)
        paid = finance.paid + (data.paid - prev_data.paid)
        if expense:
            debt = finance.debt + (prev_data.debt - data.debt)
        else:
            debt = finance.debt + (data.debt - prev_data.debt)
        self.set_finance(
            paid=paid,
            debt=debt,
            firm_id=data.firm_id,
            company_id=data.company_id
        )

    def delete_finance(
            self,
            data: Finance,
            expense: bool = False
    ) -> None:
        finance = self.get_finance(data.user_id, data.firm_id)
        paid = finance.paid - data.paid
        if expense:
            debt = finance.debt + data.debt
        else:
            debt = finance.debt - data.debt

        self.set_finance(
            paid=paid,
            debt=debt,
            firm_id=data.firm_id,
            company_id=data.company_id
        )
