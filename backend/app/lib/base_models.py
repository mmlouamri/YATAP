from datetime import datetime, timezone
import uuid
from pydantic import BaseModel
from tortoise import Model, fields


class BaseTortoiseModel(Model):
    id = fields.UUIDField(primary_key=True)
    created_at = fields.DatetimeField(null=True)
    updated_at = fields.DatetimeField(null=True)

    async def save(self, *args, **kwargs):
        if not self.created_at:
            now = datetime.now(timezone.utc)
            self.created_at = now
            self.updated_at = now
        else:
            self.updated_at = datetime.now(timezone.utc)
        await super().save(*args, **kwargs)


class BasePydanticModel(BaseModel):  # Refactor
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
