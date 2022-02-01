from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.cash_box_schemas import CashBoxCreate, CashBoxUpdate
from app.database.schemas.main_schemas import Period
from app.services.dublicated_operations import update, delete, check_user, get


class CashBoxService:

    def __init__(self, sesiion: Session = Depends(get_session)):
        self.session = sesiion

    def get_info(
            self,
            user_id: int,
            period: Period
    ) -> List[tables.CashBox]:
        return get(
            session=self.session,
            table=tables.CashBox,
            user_id=user_id,
            period=period
        )

    def create_record(
            self,
            user_id: int,
            item_data: CashBoxCreate
    ) -> tables.CashBox:
        user = check_user(self.session, user_id)
        item = tables.CashBox(
            **item_data.dict(),
            user_id=user_id,
            company_id=user.company_id
        )
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
        check_user(self.session, user_id)
        return update(
            session=self.session,
            user_id=user_id,
            item_id=item_id,
            table=tables.CashBox,
            item_data=item_data
        )

    def delete_record(
            self,
            user_id: int,
            item_id: int,
    ) -> None:
        check_user(self.session, user_id)
        delete(
            session=self.session,
            item_id=item_id,
            table=tables.CashBox,
        )
