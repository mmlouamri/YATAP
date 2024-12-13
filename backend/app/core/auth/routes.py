from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.auth.schemas import RegisterRequest, TokenResponse
from app.core.users.schemas import UserSchema
from app.core.users.exceptions import (
    EmailAlreadyExistsException,
    InvalidPasswordException,
    UserDoesNotExistException,
)
from app.core.auth.services import login_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        token_response = await login_user(form_data.username, form_data.password)
        return token_response

    except UserDoesNotExistException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist."
        )
    except InvalidPasswordException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password.",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserSchema
)
async def register(register_request: RegisterRequest):
    try:
        user = await register_user(register_request)
        return user

    except EmailAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )
