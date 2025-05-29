from typing import Annotated, Any
from bson import ObjectId
import logging

import aioboto3
import aiofiles
from fastapi import FastAPI, Depends, UploadFile, BackgroundTasks, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import AsyncMongoClient
from opensearchpy import AsyncOpenSearch

from dependencies import get_mongo_client, get_s3_client, get_opensearch_client, settings
from models import Audio, ListAudio, ListAuthor, ListPerformer

from tasks import save_file

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
)
logging.basicConfig(level=logging.INFO)


@app.post('/')
async def main(file: UploadFile, s3: Annotated[aioboto3.Session, Depends(get_s3_client)]):
    response = await s3.upload_fileobj(file.file, settings.bucket, file.filename)
    print(response)



@app.post('/save')
async def save_to_mongo(file: UploadFile,
                        mongo_client: Annotated[AsyncMongoClient, Depends(get_mongo_client)],
                        s3_client: Annotated[aioboto3.Session, Depends(get_s3_client)],
                        background_tasks: BackgroundTasks,
                        author: str = Form(), performer: str = Form(),
                        year: int | None = Form(default=None)) -> Any:

    db = mongo_client['db-audio']
    audio_table = db.audio
    audio = Audio(original_file_name=file.filename,
                  author=author,
                  performer=performer,
                  year=year)
    inserted_id = (await audio_table.insert_one(audio.model_dump())).inserted_id
    async with aiofiles.open(file.filename, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    background_tasks.add_task(save_file, file.filename, settings.bucket, file.filename)
    return JSONResponse({"id": str(inserted_id)})


@app.get(
        '/audio',
        response_model=ListAudio,
        response_model_by_alias=False
)
async def get_all_files(mongo_client: Annotated[AsyncMongoClient, Depends(get_mongo_client)]):
    db = mongo_client['db-audio']
    audio_table = db.audio

    return ListAudio(result=await audio_table.find().to_list(1000))

@app.get(
    '/audio/{audio_id}',
    response_model=Audio,
    response_model_by_alias=False,
)
async def get_all_files(audio_id: str, mongo_client: Annotated[AsyncMongoClient, Depends(get_mongo_client)]):
    db = mongo_client['db-audio']
    audio_table = db.audio

    result = await audio_table.find_one({"_id": ObjectId(audio_id)})
    return result

@app.get(
    '/author/',
    response_model=ListAuthor,
    response_model_by_alias=False,
)
async def get_authors(mongo_client: Annotated[AsyncMongoClient, Depends(get_mongo_client)]):
    db = mongo_client['db-audio']
    author_table = db.author

    return ListAuthor(authors=[author for author in await author_table.distinct('author')])


@app.get(
    '/performer/',
    response_model=ListPerformer,
    response_model_by_alias=False,
)
async def get_performers(mongo_client: Annotated[AsyncMongoClient, Depends(get_mongo_client)]):
    db = mongo_client['db-audio']
    performer_table = db.performer

    return ListPerformer(performers=[performer for performer in await performer_table.distinct('performer')])


@app.post('/performer')
async def create_performer(performer: str, mongo_client: Annotated[AsyncMongoClient, Depends(get_mongo_client)]):
    db = mongo_client['db-audio']
    performer_table = db.performer

    await performer_table.insert_one({'performer': performer})
    return JSONResponse({'msg': 'ok'})


@app.post('/author')
async def create_author(author: str, mongo_client: Annotated[AsyncMongoClient, Depends(get_mongo_client)]):
    db = mongo_client['db-audio']
    author_table = db.author

    await author_table.insert_one({'author': author})
    return JSONResponse({'msg': 'ok'})


@app.post('/search')
async def search_text(text: str, client: Annotated[AsyncOpenSearch, Depends(get_opensearch_client)]) -> Any:
    return await client.info()
