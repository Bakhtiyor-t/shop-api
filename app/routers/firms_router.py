from typing import List

from fastapi import APIRouter, status, Depends
from fastapi.responses import Response

from app.database.schemas.firms_schemas import Firm, FirmCreate, FirmUpdate
from app.database.schemas.main_schemas import Period
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
        firm_name: FirmUpdate,
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
