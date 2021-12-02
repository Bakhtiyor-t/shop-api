from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.firms_schemas import FirmCreate, Firm, Invoice, InvoiceCreate, InvoiceUpdate
from app.utils import validator


class FirmsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_firms(self, user_id: int) -> List[Firm]:
        firms = (
            self.session.query(tables.Firm)
                .filter_by(user_id=user_id).all()
        )
        # validator.is_none_check(firms)
        return firms

    def create_firm(
            self,
            user_id: int,
            firm_data: FirmCreate
    ) -> tables.Firm:
        firm = tables.Firm(**firm_data.dict(), user_id=user_id)
        self.session.add(firm)
        validator.check(session=self.session, obj=firm)
        return firm

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
    ) -> List[Invoice]:
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
        validator.check(self.session, invoice)
        return invoice

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
        for field, value in invoice_data:
            setattr(invoice, field, value)
        self.session.commit()
        self.session.refresh(invoice)
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
        self.session.delete(invoice)
        self.session.commit()
