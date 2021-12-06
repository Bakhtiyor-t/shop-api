from fastapi import Depends

from app.database.schemas.main_schemas import Period, Result
from app.services.cash_box_service import CashBoxService
from app.services.expences_service import ExpenseService
from app.services.frims_service import FirmsService


class MainService:

    def __init__(
            self,
            firm_service: FirmsService = Depends(),
            expenses_service: ExpenseService = Depends(),
            cash_box_service: CashBoxService = Depends()
    ):
        self.firm_service = firm_service
        self.expenses_service = expenses_service
        self.cash_box_service = cash_box_service

    def get_info(self, user_id: int, period: Period) -> Result:

        pass

