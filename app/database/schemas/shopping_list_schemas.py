from typing import Optional

from pydantic import BaseModel


class ShoppingListBase(BaseModel):
    name: str
    purchased: Optional[bool] = False


class ShoppingList(ShoppingListBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class ShoppingListCreate(ShoppingListBase):
    pass


class ShoppingListUpdate(ShoppingListBase):
    pass
