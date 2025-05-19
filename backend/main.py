from typing import Annotated, Any
from bson import ObjectId

import aioboto3
from fastapi import FastAPI, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic.functional_validators import BeforeValidator
from pymongo import AsyncMongoClient

from dependencies import get_mongo_client, get_s3_client, settings


app = FastAPI()


@app.post('/')
async def main(file: UploadFile, s3: Annotated[aioboto3.Session, Depends(get_s3_client)]):
    response = await s3.upload_fileobj(file.file, settings.bucket, file.filename)
    print(response)


@app.post('/save')
async def save_to_mongo(author: str, text: str,
                        mongo_client: Annotated[AsyncMongoClient, Depends(get_mongo_client)]) -> Any:

    db = mongo_client['db-audio']
    tags = db.tags

    tag = {
        'author': author,
        'text': text,
    }
    inserted_id = (await tags.insert_one(tag)).inserted_id
    return inserted_id
