from datetime import datetime
import uuid
from typing import Generic, TypeVar
from pydantic import BaseModel


class BasePydanticModel(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime



# Define a generic type variable
DynamicType = TypeVar('DynamicType')

# Define a generic class using the dynamic type
class ClassNameWhatever(BaseModel, Generic[DynamicType]):
    data: list[DynamicType]
    count: int