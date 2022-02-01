from typing import List, Optional

from fastapi import Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.firms_schemas import FirmCreate, Firm, FirmFinance, FirmBasic
from app.database.schemas.main_schemas import Period
from app.services.dublicated_operations import delete, check_user
from app.utils import validator


class FirmsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_firm(
            self,
            firm: tables.Firm,
            firm_finance: tables.FirmFinance
    ) -> Optional[Firm]:
        if firm is None:
            return None
        firm_data = FirmBasic.from_orm(firm)
        if firm_finance is None:
            return Firm(**firm_data.dict())
        finance_data = FirmFinance.from_orm(firm_finance)
        return Firm(**firm_data.dict(), **finance_data.dict())

    def get_firms(
            self,
            user_id: int,
            period: Period
    ) -> List[Firm]:
        user = check_user(self.session, user_id)
        firms = (
            self.session
                .query(tables.Firm)
                .filter_by(company_id=user.company_id)
                .all()
        )

        if firms is None:
            return []

        result = []
        for firm in firms:
            finance = (
                self.session
                    .query(tables.FirmFinance)
                    .filter_by(firm_id=firm.id, company_id=user.company_id)
                    .where(tables.FirmFinance.date >= period.from_date)
                    .where(tables.FirmFinance.date < period.to_date)
                    .order_by(desc(tables.FirmFinance.date))
                    .first()
            )
            result.append(self.get_firm(firm, finance))
        return result

    def create_firm(
            self,
            user_id: int,
            firm_data: FirmCreate,
    ) -> Firm:
        user = check_user(self.session, user_id)
        firm = tables.Firm(
            name=firm_data.name,
            user_id=user_id,
            company_id=user.company_id
        )
        self.session.add(firm)
        validator.check_unique(session=self.session)
        self.session.refresh(firm)

        firm_finance = tables.FirmFinance(
            **firm_data.dict(exclude={"name"}),
            firm_id=firm.id,
            company_id=user.company_id
        )
        self.session.add(firm_finance)
        self.session.commit()
        self.session.refresh(firm_finance)

        return self.get_firm(firm, firm_finance)

    def update_firm(
            self,
            user_id: int,
            firm_id: int,
            firm_name: str
    ) -> tables.Firm:
        user = check_user(self.session, user_id)
        firm = (
            self.session.query(tables.Firm)
                .filter_by(id=firm_id, company_id=user.company_id)
                .first()
        )
        validator.is_none_check(firm)
        firm.name = firm_name
        firm.user_id = user_id
        self.session.commit()
        self.session.refresh(firm)
        return firm

    def delete_firm(
            self,
            user_id: int,
            firm_id: int,
    ) -> None:
        check_user(self.session, user_id)
        delete(
            session=self.session,
            item_id=firm_id,
            table=tables.Firm,
        )
