from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.lib.base_schemas import BaseSchema


class UserSchema(BaseSchema):
    name: str
    email: EmailStr
    email_verified_at: datetime | None
    profile_photo_path: str | None
    last_login: datetime | None


class UserUpdateSchema(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    profile_photo_path: str | None = None
