import json
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app.database.schemas.cash_box_schemas import CashBox, CashBoxCreate, CashBoxUpdate
from app.database.schemas.main_schemas import Period
from app.services.auth_service import get_current_user
from app.services.cash_box_service import CashBoxService
from app.sockets.ws_service import manager
from app.utils.Constants import Tags

router = APIRouter(
    prefix="/cash_box",
    tags=["Касса"]
)


@router.get("/", response_model=List[CashBox])
async def get_info(
        period: Period = Depends(),
        user_id: int = Depends(get_current_user),
        service: CashBoxService = Depends(),
):
    return service.get_info(user_id, period)


@router.post("/", response_model=CashBox)
async def create_recod(
        item: CashBoxCreate,
        user_id: int = Depends(get_current_user),
        service: CashBoxService = Depends()
):
    data = CashBox.from_orm(service.create_record(user_id, item))
    await manager.broadcast(
        message=data.json(),
        tag=Tags.CASH_BOX.value,
        company_id=data.company_id
    )
    return data


@router.put("/{item_id}", response_model=CashBox)
async def update_record(
        item: CashBoxUpdate,
        item_id: int,
        user_id: int = Depends(get_current_user),
        service: CashBoxService = Depends()
):
    data = CashBox.from_orm(service.update_record(
        user_id=user_id,
        item_id=item_id,
        item_data=item
    ))
    await manager.broadcast(
        message=data.json(),
        tag=Tags.CASH_BOX.value,
        company_id=data.company_id
    )
    return data


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(
        item_id: int,
        user_id: int = Depends(get_current_user),
        service: CashBoxService = Depends()
):
    user = service.delete_record(user_id, item_id)
    message = {"item_id": item_id, "message": "Element deleted"}
    await manager.broadcast(
        message=json.dumps(message),
        tag=Tags.CASH_BOX.value,
        company_id=user.company_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
