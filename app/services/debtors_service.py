from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

from app.database.database import get_session
from app.database.schemas import debtors_schemas
from app.database.models import tables


class DebtorService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_debtors(self) -> List[debtors_schemas.Debtor]:
        debtors = self.session.query(tables.Debtor).all()
        return debtors

    def create_debtor(
            self,
            debtor: debtors_schemas.DebtorCreate
    ) -> tables.Debtor:
        new_debtor = tables.Debtor(**debtor.dict())
        self.session.add(new_debtor)
        try:
            self.session.commit()
        except IntegrityError as err:
            assert isinstance(err.orig, errors.lookup(UNIQUE_VIOLATION))
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="Такое имя уже занято"
            )
        self.session.refresh(new_debtor)
        return new_debtor

    def update_debtor(
            self,
            debtor_id: int,
            updated_data: debtors_schemas.DebtorUpdate
    ) -> debtors_schemas.Debtor:
        debtor = (self.session.query(tables.Debtor)
                  .filter_by(id=debtor_id).first())

        for field, value in updated_data:
            setattr(debtor, field, value)
        self.session.commit()
        return debtor

    def delete_debtor(self, debtor_id: int) -> None:
        debtor = (self.session.query(tables.Debtor)
                  .filter_by(id=debtor_id).first())
        self.session.delete(debtor)
        self.session.commit()
