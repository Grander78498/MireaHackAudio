from pathlib import Path
from typing import Annotated

import aioboto3
from pymongo import AsyncMongoClient
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from project_settings import Settings
from models import User


settings = Settings()
session = aioboto3.Session()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def fake_decode_token(token: str) -> User:
    return User()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    user = fake_decode_token(token)
    return user



async def get_s3_client():
    async with session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        region_name='ru-central-1',
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key
    ) as s3:
        yield s3


async def get_mongo_client():
    if not settings.debug:
        CACERT = Path.home().joinpath('.mongodb/root.crt').as_posix()
        DB_RS = 'rs01'
        DB_NAME = 'db-audio'
        DB_HOST = settings.fqdn_host
        DB_USER = settings.mongo_user
        DB_PASSWORD = settings.mongo_password

        url = f'mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/?replicaSet={DB_RS}&authSource={DB_NAME}'
        
        async with AsyncMongoClient(
            url,
            tls=True,
            tlsCAFile=CACERT
        ) as client:
            yield client
    
    else:
        async with AsyncMongoClient('localhost', 27017) as client:
            yield client
            