from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.company_schemas import CreateCompany, UpdateCompany
from app.services.dublicated_operations import check_permission, check_user, get_user
from app.utils import validator


class CompanyService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_company(self, user_id: int) -> tables.Company:
        user = check_user(self.session, user_id)
        return (
            self.session
                .query(tables.Company)
                .get(user.company_id)
        )

    def create_company(
            self,
            user_id: int,
            data: CreateCompany
    ) -> tables.Company:
        user = get_user(self.session, user_id)
        if user.company_id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Вы уже состоите в компании!"
            )

        company = tables.Company(**data.dict())
        self.session.add(company)
        validator.check_unique(session=self.session)
        self.session.refresh(company)

        user.company_id = company.id
        user.chief = True
        self.session.commit()
        self.session.refresh(user)
        return company

    def update_company(
            self,
            user_id: int,
            data: UpdateCompany
    ) -> tables.Company:
        user = check_permission(self.session, user_id)
        company: tables.Company = (
            self.session
                .query(tables.Company)
                .get(user.company_id)
        )
        company.name = data.name
        validator.check_unique(self.session)
        self.session.refresh(company)
        return company

    def delete_company(self, user_id: int) -> None:
        user = check_permission(self.session, user_id)
        company: tables.Company = (
            self.session
                .query(tables.Company)
                .get(user.company_id)
        )
        validator.is_none_check(company)
        self.session.delete(company)
        self.session.commit()

        user.company_id = None
        user.chief = False
        self.session.commit()
        self.session.refresh(user)

    def add_user(
            self,
            added_user_id: int,
            user_id: int
    ) -> None:
        company: tables.Company = self.get_company(user_id)
        new_user = get_user(self.session, added_user_id)
        if new_user.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пользователь уже состоите в компании!"
            )
        check_permission(self.session, user_id)
        company.users.append(new_user)
        self.session.commit()
        self.session.refresh(company)

    def delete_user(
            self,
            deleted_user_id: int,
            admin_user_id: int
    ) -> None:
        check_permission(self.session, admin_user_id)
        company: tables.Company = self.get_company(admin_user_id)
        self._delete_user(
            admin_user_id=admin_user_id,
            company=company,
            deleted_user_id=deleted_user_id
        )

    def delete_users(
            self,
            users_ids: List[int],
            admin_user_id: int
    ) -> None:
        check_permission(self.session, admin_user_id)
        company: tables.Company = self.get_company(admin_user_id)
        for user_id in users_ids:
            self._delete_user(
                admin_user_id=admin_user_id,
                company=company,
                deleted_user_id=user_id
            )

    def check_delete_status(
            self,
            admin_user_id: int,
            company: tables.Company,
            deleted_user: tables.User
    ):
        if not deleted_user.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пользователь не ноходится в компании!"
            )
        elif deleted_user.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пользователь ноходится в другой компании!"
            )
        elif deleted_user.id == admin_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не сможете удалить самого себя из компании!"
            )
        elif deleted_user.company_id == company.id:
            return deleted_user
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Непредвиданаая ошибка поробуйте позже!"
            )

    def _delete_user(
            self,
            admin_user_id: int,
            company: tables.Company,
            deleted_user_id: int
    ):
        deleted_user = get_user(self.session, deleted_user_id)
        deleted_user = self.check_delete_status(
            admin_user_id=admin_user_id,
            company=company,
            deleted_user=deleted_user
        )
        deleted_user.company_id = None
        self.session.commit()
        self.session.refresh(deleted_user)
