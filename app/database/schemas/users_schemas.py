from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
