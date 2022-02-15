from fastapi import APIRouter, Depends

from app.database.schemas.main_schemas import Period, Report
from app.services.auth_service import get_current_user
from app.services.main_service import MainService

router = APIRouter(
    prefix="/main",
    tags=["Сервис для вычислении"]
)


@router.get("/", response_model=Report)
async def get_info(
        period: Period = Depends(),
        user_id: int = Depends(get_current_user),
        service: MainService = Depends()
):
    return service.get_info(user_id, period)
