from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.company_schemas import CreateCompany, UpdateCompany
from app.services.dublicated_operations import check_permission
from app.utils import validator


class CompanyService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_company(self, user_id: int) -> tables.Company:
        # TODO()
        # return (
        #     self.session
        #     .query(tables.Company)
        #     .get()
        # )
        pass

    def create_company(
            self,
            user_id: int,
            data: CreateCompany
    ) -> tables.Company:
        user: tables.User = self.session.query(tables.User).get(user_id)
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
