from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app.database.schemas import debtors_schemas, users_schemas
from app.services.auth_service import get_current_user
from app.services.debtors_service import DebtorService

router = APIRouter(
    prefix="/debtors",
    tags=["Задолжники"]
)


@router.get("/", response_model=List[debtors_schemas.Debtor])
def get_debtors(
        user: users_schemas.User = Depends(get_current_user),
        service: DebtorService = Depends()
):
    return service.get_debtors(user_id=user.id)


@router.post("/", response_model=debtors_schemas.Debtor)
async def create_debtor(
        debtor: debtors_schemas.DebtorCreate,
        user: users_schemas.User = Depends(get_current_user),
        service: DebtorService = Depends()
):
    return service.create_debtor(debtor=debtor, user_id=user.id)


@router.put("/{debtor_id}", response_model=debtors_schemas.Debtor)
async def update_debtor(
        debtor_id: int,
        debtor: debtors_schemas.DebtorUpdate,
        user: users_schemas.User = Depends(get_current_user),
        service: DebtorService = Depends()
):
    return service.update_debtor(
        debtor_id=debtor_id,
        updated_data=debtor,
        user_id=user.id
    )


@router.delete("/{debtor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_debtor(
        debtor_id: int,
        user: users_schemas.User = Depends(get_current_user),
        service: DebtorService = Depends()
):
    service.delete_debtor(debtor_id=debtor_id, user_id=user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
