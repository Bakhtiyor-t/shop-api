from typing import List

from fastapi import APIRouter, Depends

from app.database.schemas import debtors_schemas
from app.services.debtors_service import DebtorService

router = APIRouter(
    prefix="/debtors",
    tags=["Задолжники"]
)


@router.get("/", response_model=List[debtors_schemas.Debtor])
def get_debtors(
        service: DebtorService = Depends()
):
    return service.get_debtors()


@router.post("/", response_model=debtors_schemas.Debtor)
async def create_debtor(
        debtor: debtors_schemas.DebtorCreate,
        service: DebtorService = Depends()
):
    return service.create_debtor(debtor=debtor)


@router.put("/{debtor_id}", response_model=debtors_schemas.Debtor)
async def update_debtor(
        debtor_id: int,
        debtor: debtors_schemas.DebtorUpdate,
        service: DebtorService = Depends()
):
    return service.update_debtor(debtor_id=debtor_id, updated_data=debtor)


@router.delete("/{debtor_id}")
async def delete_debtor(
        debtor_id: int,
        service: DebtorService = Depends()
):
    return service.delete_debtor(debtor_id=debtor_id)
