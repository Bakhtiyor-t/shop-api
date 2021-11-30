from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.shopping_list_schemas import ShoppingList, ShoppingListCreate, ShoppingListUpdate
from app.utils import unique_check


class ShoppingListService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self, user_id: int) -> List[ShoppingList]:
        return (
            self.session
            .query(tables.ShoppingList)
            .filter_by(user_id=user_id)
            .all()
        )

    def create_item(
            self,
            user_id: int,
            list_item: ShoppingListCreate
    ) -> tables.ShoppingList:
        item = tables.ShoppingList(**list_item.dict(), user_id=user_id)
        self.session.add(item)
        unique_check.check(session=self.session, obj=item)
        return item

    def update_item(
            self,
            user_id: int,
            item_id: int,
            list_item: ShoppingListUpdate
    ) -> tables.ShoppingList:
        item = (
            self.session
                .query(tables.ShoppingList)
                .filter_by(id=item_id, user_id=user_id)
                .first()
        )

        unique_check.is_none_check(item)

        for field, value in list_item:
            setattr(item, field, value)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete_item(self, user_id: int, item_id: int) -> None:
        item = (
            self.session
            .query(tables.ShoppingList)
            .filter_by(id=item_id, user_id=user_id)
            .first()
        )

        unique_check.is_none_check(item)

        self.session.delete(item)
        self.session.commit()
