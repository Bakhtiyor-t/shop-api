from fastapi import APIRouter

from app.database.schemas.main_schemas import Period

router = APIRouter(
    prefix="/main",
    tags=["Сервис для вычислении"]
)


@router.get("/")
async def get_info():
    pass


@router.get("/period")
async def get_from_period(period: Period):
    pass
