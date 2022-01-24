from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: int
    company_id: Optional[int] = None
    chief: Optional[bool] = False

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserToken(BaseModel):
    id: int
