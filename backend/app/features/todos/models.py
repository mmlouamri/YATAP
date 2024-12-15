from app.core.users.models import UserDB
from app.lib.base_models import BaseTortoiseModel
from tortoise import fields


class TodoDB(BaseTortoiseModel):
    title = fields.CharField(min_length=1, max_length=255)
    description = fields.TextField()
    is_done = fields.BooleanField(default=False)
    owner: fields.ForeignKeyRelation["UserDB"] = fields.ForeignKeyField("models.UserDB", "todos", on_delete=fields.CASCADE)
