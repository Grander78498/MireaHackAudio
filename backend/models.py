from enum import Enum
from bson import ObjectId
from typing import Annotated

from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from fastapi import Form


PyObjectId = Annotated[str, BeforeValidator(str)]


class MongoObject(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class WordTimestamp(BaseModel):
    word: str
    start: float
    end: float


class Audio(MongoObject):
    original_file_name: str
    cleaned_file_name: str | None = Field(default=None)
    tags: list[str] = []
    author: str
    performer: str
    year: int | None = None
    word_timestamps: list[WordTimestamp] = []
    is_processed: bool = False


class ListAudio(BaseModel):
    result: list[Audio]


class ListAuthor(BaseModel):
    authors: list[str]


class ListPerformer(BaseModel):
    performers: list[str]


class FilenameRequest(BaseModel):
    filename: str
