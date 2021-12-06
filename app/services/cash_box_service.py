from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.cash_box_schemas import CashBoxCreate, CashBoxUpdate
from app.database.schemas.main_schemas import Period
from app.utils import validator


class CashBoxService:

    def __init__(self, sesiion: Session = Depends(get_session)):
        self.session = sesiion

    def get_info(self, user_id: int,  period: Period) -> List[tables.CashBox]:
        items = (
            self.session
                .query(tables.CashBox)
                .filter_by(user_id=user_id)
                .all()
        )
        return items

    def create_record(
            self,
            user_id: int,
            item_data: CashBoxCreate
    ) -> tables.CashBox:
        item = tables.CashBox(**item_data.dict(), user_id=user_id)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def update_record(
            self,
            user_id: int,
            item_id: int,
            item_data: CashBoxUpdate
    ) -> tables.CashBox:
        item = (
            self.session
                .query(tables.CashBox)
                .filter_by(id=item_id, user_id=user_id)
                .first()
        )
        validator.is_none_check(item)
        for field, value in item_data:
            setattr(item, field, value)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete_record(
            self,
            user_id: int,
            item_id: int,
    ) -> None:
        item = (
            self.session
                .query(tables.CashBox)
                .filter_by(id=item_id, user_id=user_id)
                .first()
        )
        validator.is_none_check(item)
        self.session.delete(item)
        self.session.commit()

