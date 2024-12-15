import uuid

from pydantic import BaseModel
from app.lib.base_schemas import BasePydanticModel


class TodoSchema(BasePydanticModel):
    title: str
    description: str
    is_done: bool
    owner_id: uuid.UUID


class TodosSchema(BaseModel):
    data: list[TodoSchema]
    count: int


class TodoCreateSchema(BaseModel):
    title: str
    description: str


class TodoUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None
