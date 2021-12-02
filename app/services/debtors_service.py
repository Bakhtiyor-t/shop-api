from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

from app.database.database import get_session
from app.database.schemas import debtors_schemas
from app.database.models import tables
from app.utils import validator


class DebtorService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_debtors(self, user_id: int) -> List[tables.Debtor]:
        debtors = self.session.query(tables.Debtor).filter_by(user_id=user_id).all()
        return debtors

    def create_debtor(
            self,
            user_id: int,
            debtor: debtors_schemas.DebtorCreate
    ) -> tables.Debtor:
        new_debtor = tables.Debtor(**debtor.dict(), user_id=user_id)
        validator.check(self.session, new_debtor)
        self.session.refresh(new_debtor)
        return new_debtor

    def update_debtor(
            self,
            user_id: int,
            debtor_id: int,
            updated_data: debtors_schemas.DebtorUpdate
    ) -> tables.Debtor:
        debtor = (
            self.session.query(tables.Debtor)
            .filter_by(user_id=user_id, id=debtor_id).first()
        )

        validator.is_none_check(debtor)

        for field, value in updated_data:
            setattr(debtor, field, value)
        self.session.commit()
        self.session.refresh(debtor)
        return debtor

    def delete_debtor(self, user_id: int, debtor_id: int) -> None:
        debtor = (self.session.query(tables.Debtor)
                  .filter_by(user_id=user_id, id=debtor_id).first())
        self.session.delete(debtor)
        self.session.commit()
