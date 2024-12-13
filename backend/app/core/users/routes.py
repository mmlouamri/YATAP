from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.auth.dependencies import get_current_user
from app.core.users.models import UserDB
from app.core.users.schemas import UserSchema, UserUpdateSchema, UsersSchema


router = APIRouter(prefix="/users", tags=["user"])


@router.get("/", response_model=UsersSchema)
async def index(offset: int = 0, limit: int = 10):
    users = await UserDB.all().order_by("-created_at").offset(offset).limit(limit)
    return {"data": users, "count": len(users)}


@router.get("/{user_id}", response_model=UserSchema)
async def show(user_id: uuid.UUID):
    user = await UserDB.get_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserSchema)
async def update(
    user_id: uuid.UUID,
    update_data: UserUpdateSchema,
    cuser: Annotated[UserSchema, Depends(get_current_user)],
):
    user = await UserDB.get_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user_id != cuser.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can't update other users"
        )
    user = await user.update_from_dict(update_data.model_dump(exclude_unset=True))
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(
    user_id: uuid.UUID, cuser: Annotated[UserSchema, Depends(get_current_user)]
):
    user = await UserDB.get_or_none(id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user_id != cuser.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can't delete other users"
        )

    await user.delete()
    return Response(status_code=204)
