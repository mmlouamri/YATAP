from datetime import datetime
import uuid

from pydantic import BaseModel


class BasePydanticModel(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
