from typing import List, Optional

from pydantic import BaseModel

from app.database.schemas.users_schemas import User


class BaseCompany(BaseModel):
    name: str


class Company(BaseCompany):
    id: int
    users: Optional[List[User]] = []

    class Config:
        orm_mode = True


class CreateCompany(BaseCompany):
    pass


class UpdateCompany(BaseCompany):
    pass
