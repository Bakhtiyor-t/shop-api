from fastapi import APIRouter, Depends

from app.sockets.ws_service import WsService
from app.utils.Constants import Tags

router = APIRouter()


@router.websocket("/get_firms")
async def get_firms(
        service: WsService = Depends(),
):
    await service.get_data(tag=Tags.FIRMS.value)


@router.websocket("/firm/{firm_id}/get_invoices")
async def get_invoices(
        firm_id: int,
        service: WsService = Depends(),
):
    await service.get_data(tag=Tags.INVOICES.value, firm_id=firm_id)


@router.websocket("/get_expenses")
async def get_expenses(
        service: WsService = Depends(),
):
    await service.get_data(tag=Tags.EXPENSES.value)


@router.websocket("/get_debtors")
async def get_debtors(
        service: WsService = Depends(),
):
    await service.get_data(tag=Tags.DEBTORS.value)


@router.websocket("/get_shopping_list")
async def get_shopping_list(
        service: WsService = Depends(),
):
    await service.get_data(tag=Tags.SHOPPING.value)


@router.websocket("/get_cash_box")
async def get_cash_box(
        service: WsService = Depends(),
):
    await service.get_data(tag=Tags.CASH_BOX.value)


@router.websocket("/get_reports")
async def get_reports(
        service: WsService = Depends(),
):
    await service.get_data(tag=Tags.REPORTS.value)
