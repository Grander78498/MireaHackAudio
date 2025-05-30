import asyncio
from bson import ObjectId
from pathlib import Path

from models import Audio
from dependencies import get_s3_session, get_mongo_client

# from ml.restavration import process


async def save_file(id, file_path, bucket, file_name):
    async with get_s3_session().client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
    ) as s3_client:
        await s3_client.upload_file(file_path, bucket, file_name)
    
    # processed_file_name, words, tags = process(file_path, separate_vocals=True)
    # processed_file_path = Path().absolute().joinpath(processed_file_name)

    # async with get_s3_session().client(
    #     service_name='s3',
    #     endpoint_url='https://storage.yandexcloud.net',
    # ) as s3_client:
    #     await s3_client.upload_file(processed_file_path, bucket, processed_file_name)

    # async for mongo_client in get_mongo_client():
    #     db = mongo_client['db-audio']
    #     audio_table = db.audio

    #     result = await audio_table.find_one({"_id": ObjectId(id)})
    #     audio = Audio(**result)
    #     audio.tags = tags
    #     audio.word_timestamps = words
    #     audio.cleaned_file_name = processed_file_name
    #     await audio_table.update_one({"_id": ObjectId(id)}, {"$set": audio.model_dump()})
    # print('Файл сохранён')


# @celery.task
# def task_save_file(id, file_path, bucket, file_name):
#     asyncio.run(save_file(id, file_path, bucket, file_name))