from enum import Enum
from bson import ObjectId
from typing import Annotated

from pydantic import BaseModel, Field, BeforeValidator, ConfigDict


PyObjectId = Annotated[str, BeforeValidator(str)]


class MongoObject(BaseModel):
    id: ObjectId | None = Field(alias="_id", default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class Audio(MongoObject):
    original_file_name: str
    cleaned_file_name: str | None = Field(default=None)
    tags: list[str] = []
