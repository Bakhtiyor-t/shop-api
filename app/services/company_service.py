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
                status_code=status.HTTP_412_PRECONDITION_FAILED,
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
                detail="Вы уже состоите в другой компании!"
            )
        check_permission(self.session, user_id)
        company.users.append(new_user)
        self.session.commit()
        self.session.refresh(company)

    def delete_user(
            self,
            deleted_user_id: int,
            user_id: int
    ) -> None:
        company: tables.Company = self.get_company(user_id)
        new_user = get_user(self.session, deleted_user_id)
        if new_user.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пользователь ноходится в другой компании!"
            )
        elif new_user.company_id == company.id:
            check_permission(self.session, user_id)
            new_user.company_id = None
            self.session.commit()
            self.session.refresh(new_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Непредвиданаая ошибка поробуйте позже!"
            )
