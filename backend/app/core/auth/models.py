from datetime import datetime, timedelta, timezone
from tortoise import Model, fields
from tortoise.signals import pre_save

from app import config


class PasswordResetsDB(Model):
    email = fields.CharField(max_length=255, primary_key=True)
    token = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now=True)


@pre_save(PasswordResetsDB)
async def auto_delete_password_resets(sender, instance, **kwargs):
    expiration_time = datetime.now(timezone.utc) - timedelta(
        minutes=config.PASSWORD_RESET_EXPIRE_MINUTES
    )
    await PasswordResetsDB.filter(created_at__lt=expiration_time).delete()
