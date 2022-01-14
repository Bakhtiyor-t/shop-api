from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app.database.schemas.shopping_list_schemas import ShoppingList, ShoppingListCreate, ShoppingListUpdate
from app.services.auth_service import get_current_user
from app.services.shopping_list_service import ShoppingListService

router = APIRouter(
    prefix="/shopping-list",
    tags=["Список покупок"]
)


@router.get("/", response_model=List[ShoppingList])
async def get_list(
        user_id: int = Depends(get_current_user),
        service: ShoppingListService = Depends()
):
    return service.get_list(user_id=user_id)


@router.post("/", response_model=ShoppingList)
async def create_item(
        list_item: ShoppingListCreate,
        user_id: int = Depends(get_current_user),
        service: ShoppingListService = Depends()
):
    return service.create_item(user_id=user_id, list_item=list_item)


@router.put("/{item_id}", response_model=ShoppingList)
async def update_item(
        item_id: int,
        list_item: ShoppingListUpdate,
        user_id: int = Depends(get_current_user),
        service: ShoppingListService = Depends()
):
    return service.update_item(
        user_id=user_id,
        item_id=item_id,
        list_item=list_item
    )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
        item_id: int,
        user_id: int = Depends(get_current_user),
        service: ShoppingListService = Depends()
):
    service.delete_item(user_id=user_id, item_id=item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
