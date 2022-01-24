import json
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app.database.schemas import debtors_schemas
from app.database.schemas.debtors_schemas import Debtor, DebtorUpdate
from app.services.auth_service import get_current_user
from app.services.debtors_service import DebtorService
from app.sockets.ws_service import manager
from app.utils.Constants import Tags

router = APIRouter(
    prefix="/debtors",
    tags=["Задолжники"]
)


@router.get("/", response_model=List[Debtor])
def get_debtors(
        user_id: int = Depends(get_current_user),
        service: DebtorService = Depends()
):
    return service.get_debtors(user_id=user_id)


@router.post("/", response_model=Debtor)
async def create_debtor(
        debtor: debtors_schemas.DebtorCreate,
        user_id: int = Depends(get_current_user),
        service: DebtorService = Depends()
):
    data = Debtor.from_orm(
        service.create_debtor(debtor=debtor, user_id=user_id)
    )
    await manager.broadcast(
        message=data.json(),
        tag=Tags.DEBTORS.value,
        company_id=data.company_id
    )
    return data


@router.put("/{debtor_id}", response_model=Debtor)
async def update_debtor(
        debtor_id: int,
        debtor: DebtorUpdate,
        user_id: int = Depends(get_current_user),
        service: DebtorService = Depends()
):
    data = Debtor.from_orm(
        service.update_debtor(
            debtor_id=debtor_id,
            updated_data=debtor,
            user_id=user_id
        )
    )
    await manager.broadcast(
        message=data.json(),
        tag=Tags.DEBTORS.value,
        company_id=data.company_id
    )
    return data


@router.delete("/{debtor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_debtor(
        debtor_id: int,
        user_id: int = Depends(get_current_user),
        service: DebtorService = Depends()
):
    user = service.delete_debtor(debtor_id=debtor_id, user_id=user_id)
    message = {"item_id": debtor_id, "message": "Element deleted"}
    await manager.broadcast(
        message=json.dumps(message),
        tag=Tags.DEBTORS.value,
        company_id=user.company_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
