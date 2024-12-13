from pydantic import EmailStr
from app.core.users.exceptions import InvalidPasswordException
from app.core.auth.schemas import RegisterRequest, TokenResponse
from app.core.auth.utils import create_access_token
from datetime import timedelta
from app.core.users.models import UserDB
from app.core.users.exceptions import (
    UserDoesNotExistException,
    EmailAlreadyExistsException,
)
from app.config import config
from argon2 import PasswordHasher


async def authenticate_user(email: str, password: str) -> UserDB:
    user = await UserDB.get_or_none(email=email)
    print("User", user)
    if not user:
        raise UserDoesNotExistException()

    if not user.verify_password(password):
        raise InvalidPasswordException()

    return user


async def register_user(register_request: RegisterRequest) -> UserDB:
    existing_user = await UserDB.get_or_none(email=register_request.email)
    if existing_user:
        raise EmailAlreadyExistsException()

    hashed_password = PasswordHasher().hash(register_request.password)
    user_data = register_request.model_dump()
    user_data["password_hash"] = hashed_password

    created_user = await UserDB.create(**user_data)
    return created_user


async def login_user(email: EmailStr, password: str) -> TokenResponse:
    user = await authenticate_user(email, password)

    access_token = create_access_token(
        {"sub": user.email}, timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return TokenResponse(access_token=access_token)
