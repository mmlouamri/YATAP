from datetime import datetime
import uuid
from typing import Generic, TypeVar
from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

T = TypeVar('DynamicType', bound=BaseSchema)


class IndexSchema(BaseModel, Generic[T]):
    data: list[T]
    count: int