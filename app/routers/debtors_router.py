from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app.database.schemas.debtors_schemas import Debtor, DebtorCreate, DebtorUpdate
from app.services.auth_service import get_current_user
from app.services.debtors_service import DebtorService

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
        debtor: DebtorCreate,
        user_id: int = Depends(get_current_user),
        service: DebtorService = Depends()
):
    return service.create_debtor(debtor=debtor, user_id=user_id)


@router.put("/{debtor_id}", response_model=Debtor)
async def update_debtor(
        debtor_id: int,
        debtor: DebtorUpdate,
        user_id: int = Depends(get_current_user),
        service: DebtorService = Depends()
):
    return service.update_debtor(
        debtor_id=debtor_id,
        updated_data=debtor,
        user_id=user_id
    )


@router.delete("/{debtor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_debtor(
        debtor_id: int,
        user_id: int = Depends(get_current_user),
        service: DebtorService = Depends()
):
    service.delete_debtor(debtor_id=debtor_id, user_id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
