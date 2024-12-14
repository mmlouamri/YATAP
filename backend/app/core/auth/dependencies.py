from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.config import config
from app.core.users.models import UserDB

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{config.API_PREFIX}/{config.API_VERSION}/auth/token"
)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = await UserDB.get_or_none(email=email)
    if user is None:
        raise credentials_exception
    return user

UserDep = Annotated[UserDB, Depends(get_current_user)]
