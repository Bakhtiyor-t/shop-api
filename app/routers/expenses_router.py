import json
from typing import List

from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import Response

from app.database.schemas.expenses_schemas import Expense, ExpenseCreate, ExpenseUpdate
from app.database.schemas.main_schemas import Period
from app.database.schemas.users_schemas import User
from app.services.auth_service import get_current_user
from app.services.expences_service import ExpenseService
from app.sockets.ws_service import manager
from app.utils.Constants import Tags

router = APIRouter(
    prefix="/expenses",
    tags=["Расходы"]
)


@router.get("/", response_model=List[Expense])
async def get_expenses(
        period: Period = Depends(),
        user_id: int = Depends(get_current_user),
        service: ExpenseService = Depends()
):
    return service.get_expenses(user_id, period)


@router.post("/", response_model=Expense)
async def create_expense(
        expense: ExpenseCreate,
        user_id: int = Depends(get_current_user),
        service: ExpenseService = Depends()
):
    data = Expense.from_orm(service.create_expense(user_id, expense))
    await manager.broadcast(
        message=data.json(),
        tag=Tags.EXPENSES.value,
        company_id=data.company_id
    )
    return data


@router.put("/{expense_id}", response_model=Expense)
async def update_expense(
        expense_id: int,
        expense: ExpenseUpdate,
        user_id: int = Depends(get_current_user),
        service: ExpenseService = Depends()
):
    data = Expense.from_orm(
        service.update_expense(
            user_id=user_id,
            expense_id=expense_id,
            expense_data=expense
        )
    )
    await manager.broadcast(
        message=data.json(),
        tag=Tags.EXPENSES.value,
        company_id=data.company_id
    )
    return data


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
        expense_id: int,
        user_id: int = Depends(get_current_user),
        service: ExpenseService = Depends()
):
    user = service.delete_expense(user_id, expense_id)
    message = {"item_id": expense_id, "message": "Element deleted"}
    await manager.broadcast(
        message=json.dumps(message),
        tag=Tags.EXPENSES.value,
        company_id=user.company_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
