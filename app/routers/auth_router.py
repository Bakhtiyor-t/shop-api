from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.database.schemas import users_schemas
from app.database.schemas.users_schemas import UserUpdate, Token, User
from app.services.auth_service import AuthService, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"]
)


@router.post("/sign-up", response_model=Token)
async def sign_up(
        user: users_schemas.UserCreate,
        service: AuthService = Depends()
):
    return service.sign_up(user)


@router.post("/sign-in", response_model=Token)
async def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends()
):
    return service.sign_in(form_data.username, form_data.password)


# It's not correct work need fix
@router.get("/user", response_model=User)
def get_user(
        user_id: int = Depends(get_current_user),
        service: AuthService = Depends()
):
    return service.get_user(user_id)


@router.put("/", response_model=Token)
async def update_user(
        user_data: UserUpdate,
        user_id: int = Depends(get_current_user),
        service: AuthService = Depends()
):
    return service.update_user(user_id, user_data)


@router.delete("/")
async def delete_user(
        user_id: int = Depends(get_current_user),
        service: AuthService = Depends()
):
    return service.delete_user(user_id)
