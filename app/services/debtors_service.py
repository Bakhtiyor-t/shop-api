from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas import debtors_schemas
from app.services.dublicated_operations import update, delete, check_user
from app.utils import validator


class DebtorService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_debtors(self, user_id: int) -> List[tables.Debtor]:
        user = check_user(self.session, user_id)
        debtors = (
            self.session
                .query(tables.Debtor)
                .filter_by(company_id=user.company_id)
                .all()
        )
        return debtors

    def create_debtor(
            self,
            user_id: int,
            debtor: debtors_schemas.DebtorCreate
    ) -> tables.Debtor:
        user = check_user(self.session, user_id)
        new_debtor = tables.Debtor(
            **debtor.dict(),
            user_id=user_id,
            company_id=user.company_id
        )
        self.session.add(new_debtor)
        validator.check_unique(self.session)
        self.session.refresh(new_debtor)
        return new_debtor

    def update_debtor(
            self,
            user_id: int,
            debtor_id: int,
            updated_data: debtors_schemas.DebtorUpdate
    ) -> tables.Debtor:
        user = check_user(self.session, user_id)
        return update(
            session=self.session,
            user_id=user_id,
            item_id=debtor_id,
            table=tables.Debtor,
            item_data=updated_data
        )

    def delete_debtor(
            self,
            user_id: int,
            debtor_id: int
    ) -> tables.User:
        user = check_user(self.session, user_id)
        delete(
            session=self.session,
            user_id=user_id,
            item_id=debtor_id,
            table=tables.Debtor,
        )
        return user
