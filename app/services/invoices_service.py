from typing import List

from fastapi import Depends, UploadFile
from pydantic import UUID4
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.firms_schemas import Invoice, InvoiceUpdate, InvoiceCreate, Finance
from app.database.schemas.main_schemas import Period
from app.services.dublicated_operations import check_user
from app.services.finance_service import FinanceService
from app.utils import validator


class InvoicesService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.finance_service = FinanceService(session)

    def get_invoices(
            self,
            user_id: int,
            firm_id: int,
            period: Period
    ) -> List[tables.Invoice]:
        user = check_user(self.session, user_id)
        invoices = (
            self.session.query(tables.Invoice)
                .filter_by(company_id=user.company_id, firm_id=firm_id)
                .where(tables.Invoice.date >= period.from_date)
                .where(tables.Invoice.date < period.to_date)
                .order_by(desc(tables.Invoice.date))
                .all()
        )
        return invoices

    def create_invoice_with_image(
            self,
            user_id: int,
            firm_id: int,
            invoice_data: InvoiceCreate,
            file: UploadFile
    ) -> tables.Invoice:
        user = check_user(self.session, user_id)
        path = UUID4()
        print(path)
        invoice = tables.Invoice(
            **invoice_data.dict(),
            firm_id=firm_id,
            user_id=user_id,
            company_id=user.company_id
        )
        self.get_debt(invoice_data, invoice)
        self.session.add(invoice)
        validator.check_unique(self.session)
        self.session.refresh(invoice)
        finance = self.get_finance(invoice)
        self.finance_service.create_finance(finance)
        return invoice

    def get_debt(self, data: InvoiceCreate, invoice: tables.Invoice) -> None:
        if data.to_pay >= 0:
            invoice.debt = (data.to_pay +
                            data.previous_debt -
                            data.paid)

    def update_invoice(
            self,
            user_id: int,
            invoice_id: int,
            invoice_data: InvoiceUpdate
    ) -> tables.Invoice:
        user = check_user(self.session, user_id)
        invoice = (
            self.session.query(tables.Invoice)
                .filter_by(
                id=invoice_id,
                company_id=user.company_id
            )
                .first()
        )
        validator.is_none_check(invoice)
        prev_finance = self.get_finance(invoice)
        for field, value in invoice_data:
            setattr(invoice, field, value)
        self.get_debt(invoice_data, invoice)
        self.session.commit()
        self.session.refresh(invoice)
        finance = self.get_finance(invoice)
        self.finance_service.update_finance(finance, prev_finance)
        return invoice

    def delete_invoice(
            self,
            user_id: int,
            invoice_id: int
    ) -> None:
        check_user(self.session, user_id)
        invoice = (
            self.session.query(tables.Invoice)
                .filter_by(id=invoice_id)
                .first()
        )
        validator.is_none_check(invoice)
        finance = self.get_finance(invoice)
        self.finance_service.delete_finance(finance)
        self.session.delete(invoice)
        self.session.commit()

    def get_finance(self, invoice: Invoice) -> Finance:
        return Finance(
            paid=invoice.paid,
            debt=invoice.debt,
            user_id=invoice.user_id,
            firm_id=invoice.firm_id,
            company_id=invoice.company_id
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

    # def create_finance(self, invoice: tables.Invoice) -> None:
    #     finances = self.get_finance(invoice.user_id, invoice.firm_id)
    #     paid_for = invoice.paid_for + finances.paid_for
    #     debt = finances.debt + invoice.debt
    #     set_finance(
    #         session=self.session,
    #         paid_for=paid_for,
    #         debt=debt,
    #         firm_id=invoice.firm_id,
    #         company_id=invoice.company_id
    #     )

    # def update_finance(
    #         self,
    #         invoice: tables.Invoice,
    #         prev_inv: Invoice
    # ) -> None:
    #     finance = self.get_finance(invoice.user_id, invoice.firm_id)
    #     paid_for = finance.paid_for + (invoice.paid_for - prev_inv.paid_for)
    #     debt = finance.debt + (invoice.debt - prev_inv.debt)
    #     set_finance(
    #         session=self.session,
    #         paid_for=paid_for,
    #         debt=debt,
    #         firm_id=invoice.firm_id,
    #         company_id=invoice.company_id
    #     )

    # def delete_finance(self, invoice: tables.Invoice) -> None:
    #     finance = self.get_finance(invoice.user_id, invoice.firm_id)
    #     paid_for = finance.paid_for - invoice.paid_for
    #     debt = finance.debt - invoice.debt
    #     set_finance(
    #         session=self.session,
    #         paid_for=paid_for,
    #         debt=debt,
    #         firm_id=invoice.firm_id,
    #         company_id=invoice.company_id
    #     )
