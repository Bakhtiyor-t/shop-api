from typing import List

from fastapi import APIRouter, status, Depends
from fastapi.responses import Response

from app.database.schemas.company_schemas import Company, CreateCompany, UpdateCompany
from app.database.schemas.users_schemas import User
from app.services.auth_service import get_current_user
from app.services.company_service import CompanyService

router = APIRouter(
    prefix="/company",
    tags=["Компания"],
)


@router.get("/", response_model=Company)
async def get_company(
        user_id: int = Depends(get_current_user),
        service: CompanyService = Depends()
):
    return service.get_company(user_id)


@router.post("/", response_model=Company)
async def create_company(
        data: CreateCompany,
        user_id: int = Depends(get_current_user),
        service: CompanyService = Depends()
):
    return service.create_company(user_id, data)


@router.put("/", response_model=Company)
async def update_company(
        data: UpdateCompany,
        user_id: int = Depends(get_current_user),
        service: CompanyService = Depends()
):
    return service.update_company(user_id, data)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
        user_id: int = Depends(get_current_user),
        service: CompanyService = Depends()
):
    service.delete_company(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/add_user/{added_user_id}", status_code=status.HTTP_200_OK)
async def add_user(
        added_user_id: int,
        user_id: int = Depends(get_current_user),
        service: CompanyService = Depends()
):
    service.add_user(added_user_id, user_id)
    return {"message": "Пользователь успешно добавлен!"}


@router.delete("/delete_user/{deleted_user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        deleted_user_id: int,
        user_id: int = Depends(get_current_user),
        service: CompanyService = Depends()
):
    service.delete_user(deleted_user_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/delete_users/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users(
        users_ids: List[int],
        user_id: int = Depends(get_current_user),
        service: CompanyService = Depends()
):
    service.delete_users(users_ids, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
