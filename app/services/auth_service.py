from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.users_schemas import UserUpdate, UserCreate, Token, User
from app.settings import settings
from app.utils import validator

auth = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")


def get_current_user(token: str = Depends(auth)):
    return AuthService.verify_token(token)


class AuthService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def sign_up(self, user_data: UserCreate) -> Token:
        password_hash = self.hash_password(user_data.password)
        user = tables.User(
            username=user_data.username,
            password_hash=password_hash
        )
        self.session.add(user)
        validator.check_unique(self.session)
        self.session.refresh(user)
        return self.create_token(user)

    def sign_in(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        user = (
            self.session
                .query(tables.User)
                .filter_by(username=username)
                .first()
        )

        if not user:
            raise exception
        if not self.verify_passwod(password, user.password_hash):
            raise exception

        return self.create_token(user)

    def get_user(self, user_id: int) -> tables.User:
        return (
            self.session
                .query(tables.User)
                .get(user_id)
        )

    def update_user(
            self,
            user_id: int,
            user_data: UserUpdate
    ) -> Token:
        user = self.get_user(user_id)
        user.username = user_data.username
        user.password_hash = self.hash_password(user_data.password)
        validator.check_unique(self.session)
        self.session.refresh(user)
        return self.create_token(user)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.session.delete(user)
        self.session.commit()

    @classmethod
    def verify_passwod(cls, plain_password: str, hased_password) -> bool:
        return bcrypt.verify(plain_password, hased_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> int:
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

        user_id = payload.get("sub", None)

        # try:
        #     user = users_schemas.User.parse_obj(user_data)
        # except ValidationError:
        #     raise exception
        return int(user_id)

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        user_data = User.from_orm(user)

        date = datetime.utcnow()
        payload = {
            "iat": date,
            "nbf": date,
            "exp": date + timedelta(minutes=settings.jwt_expire_minutes),
            "sub": str(user_data.id),
            "user": user_data.dict()
        }

        token = jwt.encode(
            payload,
            key=settings.jwt_secret,
            algorithm=settings.jwt_algorithm,

        )

        return Token(access_token=token)
