from enum import Enum
from bson import ObjectId
from typing import Annotated

from pydantic import BaseModel, Field, BeforeValidator, ConfigDict


PyObjectId = Annotated[str, BeforeValidator(str)]


class Role(str, Enum):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'


class User(BaseModel):
    id: ObjectId | None = Field(alias="_id", default=None)
    username: str
    password: str
    role: Role = Role.USER

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
