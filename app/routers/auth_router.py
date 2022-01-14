from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.database.schemas import users_schemas
from app.services.auth_service import AuthService, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"]
)


@router.post("/sign-up", response_model=users_schemas.Token)
async def sign_up(
        user: users_schemas.UserCreate,
        service: AuthService = Depends()
):
    return service.sign_up(user)


@router.post("/sign-in", response_model=users_schemas.Token)
async def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends()
):
    return service.sign_in(form_data.username, form_data.password)


# It's not correct work need fix
@router.get("/user", response_model=users_schemas.User)
def get_user(user: users_schemas.User = Depends(get_current_user)):
    return user
