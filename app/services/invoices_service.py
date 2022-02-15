import os
from typing import List, Any
from uuid import uuid4

from fastapi import Depends, UploadFile, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.firms_schemas import Finance
from app.database.schemas.invoice_schemas import Invoice, InvoiceUpdate, InvoiceCreateWithImage, InvoiceCreate
from app.database.schemas.main_schemas import Period
from app.services.dublicated_operations import check_user
from app.services.finance_service import FinanceService
from app.utils import validator


class InvoicesService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.finance_service = FinanceService(session)

    # General operations #
    def get_all_invoices(
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

    def get_invoices(
            self,
            user_id: int,
            firm_id: int,
            period: Period,
            item: Any
    ) -> List[tables.Invoice]:
        user = check_user(self.session, user_id)
        return (
            self.session.query(tables.Invoice)
                .filter_by(company_id=user.company_id, firm_id=firm_id)
                .where(tables.Invoice.date >= period.from_date)
                .where(tables.Invoice.date < period.to_date)
                .where(item != None)
                .order_by(desc(tables.Invoice.date))
                .all()
        )

    def get_finance(self, invoice: Invoice) -> Finance:
        return Finance(
            paid=invoice.paid,
            debt=invoice.debt,
            user_id=invoice.user_id,
            firm_id=invoice.firm_id,
            company_id=invoice.company_id
        )

    def get_debt(self, invoice: tables.Invoice) -> None:
        if invoice.to_pay >= 0:
            invoice.debt = (invoice.to_pay +
                            invoice.previous_debt -
                            invoice.paid)

    def save_invoice(
            self,
            invoice: tables.Invoice
    ):
        self.get_debt(invoice)
        self.session.add(invoice)
        validator.check_unique(self.session)
        self.session.refresh(invoice)
        finance = self.get_finance(invoice)
        self.finance_service.create_finance(finance)
        return invoice

    def get_updated_invoice(
            self,
            user_id: int,
            invoice_id: int
    ) -> tables.Invoice:
        user = check_user(self.session, user_id)
        invoice: tables.Invoice = (
            self.session
                .query(tables.Invoice)
                .filter_by(id=invoice_id, company_id=user.company_id)
                .first()
        )
        validator.is_none_check(invoice)
        return invoice

    def check_update(self, item: Any) -> None:
        if item:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Ошибка, вы пытаетесь изменить накладной в другом формате!"
            )

    def delete_invoice(
            self,
            user_id: int,
            invoice_id: int
    ) -> None:
        check_user(self.session, user_id)
        invoice: tables.Invoice = (
            self.session.query(tables.Invoice)
                .filter_by(id=invoice_id)
                .first()
        )
        validator.is_none_check(invoice)
        finance = self.get_finance(invoice)
        self.finance_service.delete_finance(finance)
        if invoice.image_id:
            os.remove(f".{invoice.image_uri}")
        self.session.delete(invoice)
        self.session.commit()

    # Invoice operations without image invoice #
    def get_invoices_without_image(
            self,
            user_id: int,
            firm_id: int,
            period: Period
    ) -> List[tables.Invoice]:
        return self.get_invoices(
            user_id,
            firm_id,
            period,
            tables.Invoice.products
        )

    def create_invoice_without_image(
            self,
            user_id: int,
            firm_id: int,
            invoice_data: InvoiceCreate,
    ) -> tables.Invoice:
        user = check_user(self.session, user_id)
        invoice = tables.Invoice(
            **invoice_data.dict(exclude={"products"}),
            company_id=user.company_id,
            user_id=user_id,
            firm_id=firm_id
        )
        result = self.save_invoice(invoice)
        self.create_products(
            user_id=invoice.user_id,
            company_id=invoice.company_id,
            invoice_id=invoice.id,
            product_data=invoice_data.products
        )
        self.session.refresh(invoice)
        return result

    def update_invoice_without_image(
            self,
            user_id: int,
            invoice_id: int,
            invoice_data: InvoiceUpdate
    ) -> tables.Invoice:

        invoice = self.get_updated_invoice(user_id, invoice_id)
        self.check_update(invoice.image_id)

        prev_finance = self.get_finance(invoice)
        inv_data = invoice_data.dict(exclude={"products"})
        for field, value in inv_data.items():
            setattr(invoice, field, value)
        self.get_debt(invoice)

        self.session.commit()
        self.session.refresh(invoice)
        # удаляю потому что может быть разное кол-во товаров
        self.delete_products(invoice.id)
        self.create_products(
            user_id=invoice.user_id,
            company_id=invoice.company_id,
            invoice_id=invoice.id,
            product_data=invoice_data.products
        )

        finance = self.get_finance(invoice)
        self.finance_service.update_finance(finance, prev_finance)
        return invoice

    def create_products(
            self,
            user_id,
            company_id,
            invoice_id,
            product_data,
    ):
        for item in product_data:
            product = tables.Product(
                **item.dict(),
                invoice_id=invoice_id,
                company_id=company_id,
                user_id=user_id
            )
            self.session.add(product)
            self.session.commit()
            self.session.refresh(product)

    def delete_products(self, invoice_id: int) -> None:
        products = (
            self.session
                .query(tables.Product)
                .filter_by(invoice_id=invoice_id)
                .all()
        )
        for product in products:
            self.session.delete(product)
            self.session.commit()

    # Invoice operations with image invoice
    def get_invoices_with_image(
            self,
            user_id: int,
            firm_id: int,
            period: Period
    ) -> List[tables.Invoice]:
        return self.get_invoices(
            user_id,
            firm_id,
            period,
            tables.Invoice.image_id
        )

    def create_invoice_with_image(
            self,
            user_id: int,
            firm_id: int,
            invoice_data: InvoiceCreateWithImage,
            file: UploadFile
    ) -> tables.Invoice:
        user = check_user(self.session, user_id)
        if file.content_type != "image/jpeg":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Файл должен быть изображением"
            )

        image_id = f'{uuid4()}.jpeg'
        image_url = "/static/invoices/" + image_id

        invoice = tables.Invoice(
            **invoice_data.dict(),
            firm_id=firm_id,
            user_id=user_id,
            company_id=user.company_id,
            image_id=image_id,
            image_uri=image_url
        )
        # Сначало сохраняем данные в бд, если они успешно сохранилось
        # только потом сохраняем изображение на сервере
        result = self.save_invoice(invoice)

        # я не понимаю как этот путь работает но оно работает)
        with open(f".{image_url}", "wb") as image:
            image.write(file.file.read())

        return result

    def update_invoice_with_image(
            self,
            user_id: int,
            invoice_id: int,
            invoice_data: InvoiceUpdate,
            file: UploadFile
    ) -> tables.Invoice:
        invoice = self.get_updated_invoice(user_id, invoice_id)
        self.check_update(invoice.products)

        prev_finance = self.get_finance(invoice)
        os.remove(f".{invoice.image_uri}")
        for field, value in invoice_data:
            setattr(invoice, field, value)

        self.get_debt(invoice)
        image_id = f'{uuid4()}.jpeg'
        image_url = "/static/invoices/" + image_id
        invoice.image_uri = image_url
        invoice.image_id = image_id

        self.session.commit()
        self.session.refresh(invoice)
        finance = self.get_finance(invoice)
        self.finance_service.update_finance(finance, prev_finance)

        with open(f".{image_url}", "wb") as image:
            image.write(file.file.read())

        return invoice
