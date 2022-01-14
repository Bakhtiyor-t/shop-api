from typing import List

from fastapi import APIRouter, status, Depends
from fastapi.responses import Response

from app.database.schemas.firms_schemas import Firm, Invoice, FirmCreate, InvoiceCreate, InvoiceUpdate
from app.database.schemas.main_schemas import Period
from app.database.schemas.users_schemas import User
from app.services.auth_service import get_current_user
from app.services.frims_service import FirmsService

router = APIRouter(
    prefix="/firms",
    tags=["Фирмы"]
)


@router.get("/", response_model=List[Firm])
async def get_fimrs(
        period: Period = Depends(),
        user_id: int = Depends(get_current_user),
        service: FirmsService = Depends()
):
    return service.get_firms(user_id, period)


@router.post("/", response_model=Firm)
async def create_firm(
        firm: FirmCreate,
        user_id: int = Depends(get_current_user),
        service: FirmsService = Depends()
):
    return service.create_firm(user_id, firm)


@router.put("/{firm_id}", response_model=Firm)
async def update_firm(
        firm_id: int,
        firm_name: str,
        user_id: int = Depends(get_current_user),
        service: FirmsService = Depends()
):
    return service.update_firm(user_id, firm_id, firm_name)


@router.delete("/{firm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_firm(
        firm_id: int,
        user_id: int = Depends(get_current_user),
        service: FirmsService = Depends()
):
    service.delete_firm(user_id, firm_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{firm_id}/invoices", response_model=List[Invoice])
async def get_firm_invoices(
        firm_id: int,
        period: Period = Depends(),
        user_id: int = Depends(get_current_user),
        service: FirmsService = Depends()
):
    return service.get_invoices(user_id, firm_id, period)


@router.post("/{firm_id}/invoice", response_model=Invoice)
async def create_invoice(
        firm_id: int,
        invoice: InvoiceCreate,
        user_id: int = Depends(get_current_user),
        service: FirmsService = Depends()
):
    return service.create_invoice(user_id, firm_id, invoice)


@router.put("/invoice/{invoice_id}", response_model=Invoice)
async def update_invoice(
        invoice_id: int,
        invoice: InvoiceUpdate,
        user_id: int = Depends(get_current_user),
        service: FirmsService = Depends()
):
    return service.update_invoice(user_id, invoice_id, invoice)


@router.delete(
    "/invoice/{invoice_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_invoice(
        invoice_id: int,
        user_id: int = Depends(get_current_user),
        service: FirmsService = Depends()
):
    service.delete_invoice(user_id, invoice_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
