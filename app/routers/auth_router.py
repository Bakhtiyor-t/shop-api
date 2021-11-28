from fastapi import APIRouter

router = APIRouter(
    prefix="auth",
    tags=["Авторизация"]
)


@router.post("/sign-up")
async def sign_up():
    pass


@router.post("/sign-in")
async def sign_in():
    pass

