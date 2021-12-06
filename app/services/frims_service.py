from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.firms_schemas import FirmCreate, Firm, InvoiceCreate, InvoiceUpdate, FirmPart, \
    FirmFinance, Invoice
from app.database.schemas.main_schemas import Period
from app.utils import validator


class FirmsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @classmethod
    def get_firm(
            cls,
            firm: tables.Firm,
            firm_finance: tables.FinanceHistory
    ) -> Optional[Firm]:
        if firm is None:
            return None
        firm_data = FirmPart.from_orm(firm)
        if firm_finance is None:
            return Firm(**firm_data.dict())
        finance_data = FirmFinance.from_orm(firm_finance)
        return Firm(**firm_data.dict(), **finance_data.dict())

    def get_firms(
            self,
            user_id: int,
            period: Period = Period()
    ) -> List[Firm]:
        firms = (
            self.session.query(tables.Firm)
                .filter_by(user_id=user_id).all()
        )
        if firms is None:
            return []
        result = []
        for firm in firms:
            finance = (
                self.session
                    .query(tables.FinanceHistory)
                    .filter_by(firm_id=firm.id)
                    .where(tables.FinanceHistory.date >= period.from_date)
                    .where(tables.FinanceHistory.date < period.to_date)
                    .order_by(desc(tables.FinanceHistory.date))
                    .first()
            )
            result.append(self.get_firm(firm, finance))
        return result

    def create_firm(
            self,
            user_id: int,
            firm_data: FirmCreate,
    ) -> Firm:
        firm = tables.Firm(name=firm_data.name, user_id=user_id)
        self.session.add(firm)
        validator.check(session=self.session, obj=firm)
        firm_finance = tables.FinanceHistory(**firm_data.dict(exclude={"name"}), firm_id=firm.id)
        self.session.add(firm_finance)
        self.session.commit()
        self.session.refresh(firm_finance)
        return self.get_firm(firm, firm_finance)

    def update_firm(
            self,
            user_id: int,
            firm_id: int,
            firm_name: str
    ) -> tables.Firm:
        firm = (
            self.session.query(tables.Firm)
                .filter_by(id=firm_id, user_id=user_id)
                .first()
        )
        validator.is_none_check(firm)
        firm.name = firm_name
        self.session.commit()
        self.session.refresh(firm)
        return firm

    def delete_firm(
            self,
            user_id: int,
            firm_id: int,
    ) -> None:
        firm = (
            self.session.query(tables.Firm)
                .filter_by(id=firm_id, user_id=user_id)
                .first()
        )
        validator.is_none_check(firm)
        self.session.delete(firm)
        self.session.commit()

    def get_invoices(
            self,
            user_id: int,
            firm_id: int,
    ) -> List[tables.Invoice]:
        invoices = (
            self.session.query(tables.Invoice)
                .filter_by(user_id=user_id, firm_id=firm_id)
                .all()
        )
        # validator.is_none_check(invoices)
        return invoices

    def create_invoice(
            self,
            user_id: int,
            firm_id: int,
            invoice_data: InvoiceCreate
    ) -> tables.Invoice:
        invoice = tables.Invoice(
            **invoice_data.dict(),
            firm_id=firm_id,
            user_id=user_id
        )
        self.get_debt(invoice_data, invoice)
        validator.check(self.session, invoice)
        self.create_finance(invoice)
        return invoice

    @classmethod
    def get_debt(cls, data: InvoiceCreate, invoice: tables.Invoice) -> None:
        if data.debt == 0 and data.previous_debt != 0:
            invoice.debt = (data.payment +
                            data.previous_debt -
                            data.paid_for)

    def update_invoice(
            self,
            user_id: int,
            firm_id: int,
            invoice_id: int,
            invoice_data: InvoiceUpdate
    ) -> tables.Invoice:
        invoice = (
            self.session.query(tables.Invoice)
                .filter_by(id=invoice_id, user_id=user_id, firm_id=firm_id)
                .first()
        )
        validator.is_none_check(invoice)
        prev_inv = Invoice.from_orm(invoice)
        for field, value in invoice_data:
            setattr(invoice, field, value)
        self.get_debt(invoice_data, invoice)
        self.session.commit()
        self.session.refresh(invoice)
        self.update_finance(invoice, prev_inv)
        return invoice

    def delete_invoice(
            self,
            user_id: int,
            firm_id: int,
            invoice_id: int
    ) -> None:
        invoice = (
            self.session.query(tables.Invoice)
                .filter_by(id=invoice_id, user_id=user_id, firm_id=firm_id)
                .first()
        )
        validator.is_none_check(invoice)
        inv = invoice
        self.session.delete(invoice)
        self.session.commit()
        self.delete_finance(inv)

    # Finance operations

    def get_finance(self, firm_id: int) -> tables.FinanceHistory:
        return (
            self.session
                .query(tables.FinanceHistory)
                .filter_by(firm_id=firm_id)
                .order_by(desc(tables.FinanceHistory.date))
                .first()
        )

    def create_finance(self, invoice: tables.Invoice) -> None:
        finances = self.get_finance(invoice.firm_id)
        paid_for = invoice.paid_for + finances.paid_for
        debt = finances.debt + invoice.debt
        self.set_finance(paid_for, debt, invoice.firm_id)

    def update_finance(
            self,
            invoice: tables.Invoice,
            prev_inv: tables.Invoice
    ) -> None:
        finance = self.get_finance(invoice.firm_id)
        paid_for = finance.paid_for + (invoice.paid_for - prev_inv.paid_for)
        debt = finance.debt + (invoice.debt - prev_inv.debt)
        print(paid_for, " : ", debt)
        # invoices = self.get_invoices(invoice.user_id, invoice.firm_id)
        # paid_for = Decimal(0)
        # debt = Decimal(0)
        # for item in invoices:
        #     paid_for += item.paid_for
        #     debt += item.debt
        self.set_finance(paid_for, debt, invoice.firm_id)

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

    def delete_finance(self, invoice: tables.Invoice) -> None:
        finance = self.get_finance(invoice.firm_id)
        paid_for = finance.paid_for - invoice.paid_for
        debt = finance.debt - invoice.debt
        self.set_finance(paid_for, debt, invoice.firm_id)
