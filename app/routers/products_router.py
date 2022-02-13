from typing import List

from fastapi import APIRouter, status, Response, Depends

from app.database.schemas.products_schemas import Product
from app.services.auth_service import get_current_user
from app.services.products_service import ProductsService

router = APIRouter(
    prefix="/products",
    tags=['Товары']
)


@router.get("/", response_model=List[Product])
async def get_products(
        user_id: int = Depends(get_current_user),
        service: ProductsService = Depends()
):
    return service.get_products(user_id)


@router.get("/search/{product_name}", response_model=List[Product])
async def search_product(
        product_name: str,
        user_id: int = Depends(get_current_user),
        service: ProductsService = Depends()
):
    return service.search_product(user_id, product_name)
