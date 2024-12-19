import uuid

from pydantic import BaseModel
from app.lib.base_schemas import BaseSchema


class TodoSchema(BaseSchema):
    title: str
    description: str
    is_done: bool
    owner_id: uuid.UUID



class TodoCreateSchema(BaseModel):
    title: str
    description: str


class TodoUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None
