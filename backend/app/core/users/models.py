from tortoise import fields
from app.lib.base_models import BaseTortoiseModel
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHashError, VerifyMismatchError


class UserDB(BaseTortoiseModel):
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True, db_index=True)
    email_verified_at = fields.DatetimeField(null=True)
    password_hash = fields.CharField(max_length=255)
    profile_photo_path = fields.CharField(max_length=2045, null=True)
    last_login = fields.DatetimeField(null=True)

    def verify_password(self, password: str) -> bool:
        try:
            return PasswordHasher().verify(self.password_hash, password)
        except (VerificationError, InvalidHashError, VerifyMismatchError):
            return False

    def set_password(self, password: str):
        self.password_hash = PasswordHasher().hash(password)
