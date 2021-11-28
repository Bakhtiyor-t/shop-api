from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.database.database import get_session
from app.database.models import tables
from app.settings import settings

auth = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    @classmethod
    def verify_passwod(cls, plain_password: str, hased_password) -> bool:
        return bcrypt.verify(plain_password, hased_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> tables.User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        try:
            payload = jwt.decode(
                token=token,
                key=settings.jwt_secret,
                algorithms=settings.jwt_algorithm
            )
        except JWTError:
            raise exception

        user_data = payload.get("user")

        try:
            user = tables.User.parse_obj(user_data)
        except ValidationError:
            raise exception

        return user
