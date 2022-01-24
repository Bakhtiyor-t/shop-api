from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.shopping_list_schemas import ShoppingList, ShoppingListCreate, ShoppingListUpdate
from app.services.dublicated_operations import update, delete, check_user
from app.utils import validator


class ShoppingListService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self, user_id: int) -> List[ShoppingList]:
        user = check_user(self.session, user_id)
        return (
            self.session
                .query(tables.ShoppingList)
                .filter_by(company_id=user.company_id)
                .all()
        )

    def create_item(
            self,
            user_id: int,
            list_item: ShoppingListCreate
    ) -> tables.ShoppingList:
        user = check_user(self.session, user_id)
        item = tables.ShoppingList(
            **list_item.dict(),
            user_id=user_id,
            company_id=user.company_id
        )
        self.session.add(item)
        validator.check_unique(session=self.session)
        self.session.refresh(item)
        return item

    def update_item(
            self,
            user_id: int,
            item_id: int,
            list_item: ShoppingListUpdate
    ) -> tables.ShoppingList:
        user = check_user(self.session, user_id)
        return update(
            session=self.session,
            table=tables.ShoppingList,
            user_id=user_id,
            item_id=item_id,
            item_data=list_item
        )

    def delete_item(
            self,
            user_id: int,
            item_id: int
    ) -> tables.User:
        user = check_user(self.session, user_id)
        delete(
            session=self.session,
            user_id=user_id,
            item_id=item_id,
            table=tables.ShoppingList,
        )
        return user
