from typing import Annotated, Any
from bson import ObjectId

import aioboto3
from fastapi import FastAPI, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pymongo import AsyncMongoClient
from opensearchpy import AsyncOpenSearch

from dependencies import get_mongo_client, get_s3_client, get_opensearch_client, settings

# from ml.restavration import process


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
)


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
    return str(inserted_id)


@app.post('/search')
async def search_text(text: str, client: Annotated[AsyncOpenSearch, Depends(get_opensearch_client)]) -> Any:
    return await client.info()
