from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app.database.schemas.cash_box_schemas import CashBox, CashBoxCreate, CashBoxUpdate
from app.database.schemas.users_schemas import User
from app.services.auth_service import get_current_user
from app.services.cash_box_service import CashBoxService

router = APIRouter(
    prefix="/cash_box",
    tags=["Касса"]
)


@router.get("/", response_model=List[CashBox])
async def get_info(
        user: User = Depends(get_current_user),
        service: CashBoxService = Depends(),
):
    return service.get_info(user.id)


@router.post("/", response_model=CashBox)
async def create_recod(
        item: CashBoxCreate,
        user: User = Depends(get_current_user),
        service: CashBoxService = Depends()
):
    return service.create_record(user.id, item)


@router.put("/{item_id}", response_model=CashBox)
async def update_record(
        item: CashBoxUpdate,
        item_id: int,
        user: User = Depends(get_current_user),
        service: CashBoxService = Depends()
):
    return service.update_record(
        user_id=user.id,
        item_id=item_id,
        item_data=item
    )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(
        item_id: int,
        user: User = Depends(get_current_user),
        service: CashBoxService = Depends()
):
    service.delete_record(user.id, item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

