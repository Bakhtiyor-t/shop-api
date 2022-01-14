from fastapi import HTTPException, status
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION, FOREIGN_KEY_VIOLATION
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.models.tables import Base


def check_unique(session: Session) -> None:
    try:
        session.commit()
    except IntegrityError as err:
        # assert isinstance(err.orig, errors.lookup(UNIQUE_VIOLATION))
        if isinstance(err.orig, errors.lookup(UNIQUE_VIOLATION)):
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="Такое имя уже занято"
            )
        elif isinstance(err.orig, errors.lookup(FOREIGN_KEY_VIOLATION)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь с таким именем удалён из базы данных",
                headers={'WWW-Authenticate': 'Bearer'},
            )


def is_none_check(obj: Base):
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такой записи нет в базе данных"
        )
