from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database.database import Base
from app.database.models import tables
from app.database.schemas.firms_schemas import FirmFinance
from app.database.schemas.main_schemas import Period
from app.utils import validator


def get_user(session, user_id: int) -> tables.User:
    return session.query(tables.User).get(user_id)


def check_user(session, user_id: int) -> int:
    print(session)
    user = get_user(session, user_id)
    if user.company_id is None:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Вы не состоите в компании!"
        )
    if not user.chief:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="У вас нет прав на это действие!"
        )

    return user.company_id


def get(
        session: Session,
        table: Base,
        user_id: int,
        period: Period
):
    company_id = check_user(session, user_id)
    data = (
        session
            .query(table)
            .filter_by(company_id=company_id)
            .where(table.date >= period.from_date)
            .where(table.date < period.to_date)
            .order_by(desc(table.date))
            .all()
    )
    return data


def update(
        session: Session,
        table: Base,
        user_id: int,
        item_id: int,
        item_data: BaseModel
):
    item = (
        session
            .query(table)
            .filter_by(id=item_id, user_id=user_id)
            .first()
    )
    validator.is_none_check(item)
    for field, value in item_data:
        setattr(item, field, value)
    session.commit()
    session.refresh(item)
    return item


def delete(
        session: Session,
        user_id: int,
        item_id: int,
        table: Base
) -> None:
    item = (
        session
            .query(table)
            .filter_by(id=item_id, user_id=user_id)
            .first()
    )
    validator.is_none_check(item)
    session.delete(item)
    session.commit()


def set_finance(
        session: Session,
        user_id: int,
        firm_id: int,
        paid_for: Decimal,
        debt: Decimal
):
    company_id = check_user(session, user_id)
    data = FirmFinance(paid_for=paid_for, debt=debt, date=datetime.now())
    new_finance = tables.FinanceHistory(
        **data.dict(),
        firm_id=firm_id,
        company_id=company_id
    )
    session.add(new_finance)
    session.commit()
    session.refresh(new_finance)
