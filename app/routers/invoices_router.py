from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.responses import Response

from app.database.schemas.invoice_schemas import Invoice, InvoiceCreateWithImage, InvoiceUpdate, InvoiceCreate, \
    GeneralInvoice, InvoiceWithImage, InvoiceUpdateWithImage
from app.database.schemas.main_schemas import Period
from app.services.auth_service import get_current_user
from app.services.invoices_service import InvoicesService

router = APIRouter(
    prefix="/firms",
    tags=["Накладные"]
)


@router.get("/{firm_id}/all_invoices", response_model=List[GeneralInvoice])
async def get_all_invoices(
        firm_id: int,
        period: Period = Depends(),
        user_id: int = Depends(get_current_user),
        service: InvoicesService = Depends()
):
    return service.get_all_invoices(user_id, firm_id, period)


@router.get("/{firm_id}/invoices", response_model=List[Invoice])
async def get_invoices_without_image(
        firm_id: int,
        period: Period = Depends(),
        user_id: int = Depends(get_current_user),
        service: InvoicesService = Depends()
):
    return service.get_invoices_without_image(user_id, firm_id, period)


@router.post("/{firm_id}/invoice", response_model=Invoice)
async def create_invoice_without_image(
        firm_id: int,
        invoice: InvoiceCreate,
        user_id: int = Depends(get_current_user),
        service: InvoicesService = Depends()
):
    return service.create_invoice_without_image(
        user_id=user_id,
        firm_id=firm_id,
        invoice_data=invoice,
    )


@router.put("/invoice/{invoice_id}", response_model=Invoice)
async def update_invoice_without_image(
        invoice_id: int,
        invoice: InvoiceUpdate,
        user_id: int = Depends(get_current_user),
        service: InvoicesService = Depends()
):
    return service.update_invoice_without_image(user_id, invoice_id, invoice)


@router.delete(
    "/invoice/{invoice_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_invoice(
        invoice_id: int,
        user_id: int = Depends(get_current_user),
        service: InvoicesService = Depends()
):
    service.delete_invoice(user_id, invoice_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{firm_id}/invoices_with_image", response_model=List[InvoiceWithImage])
async def get_invoices_with_image(
        firm_id: int,
        period: Period = Depends(),
        user_id: int = Depends(get_current_user),
        service: InvoicesService = Depends()
):
    return service.get_invoices_with_image(user_id, firm_id, period)


@router.post("/{firm_id}/invoice_with_image", response_model=InvoiceWithImage)
async def create_invoice_with_image(
        firm_id: int,
        invoice: InvoiceCreateWithImage = Depends(),
        file: UploadFile = File(...),
        user_id: int = Depends(get_current_user),
        service: InvoicesService = Depends()
):
    return service.create_invoice_with_image(
        user_id=user_id,
        firm_id=firm_id,
        invoice_data=invoice,
        file=file
    )


@router.put("/invoice_with_image/{invoice_id}", response_model=InvoiceWithImage)
async def update_invoice_with_image(
        invoice_id: int,
        invoice: InvoiceUpdateWithImage = Depends(),
        file: UploadFile = File(...),
        user_id: int = Depends(get_current_user),
        service: InvoicesService = Depends()
):
    return service.update_invoice_with_image(
        user_id=user_id,
        invoice_id=invoice_id,
        invoice_data=invoice,
        file=file
    )
