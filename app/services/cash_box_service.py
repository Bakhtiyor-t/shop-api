from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_session


class CashBoxService:

    def __init__(self, sesiion: Session = Depends(get_session)):
        self.session = sesiion

    def get_info(self, user_id: int):
        pass

    def create_record(self, ):
        pass
